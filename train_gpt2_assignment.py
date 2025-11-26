"""
S12 Assignment: Train GPT-2 on Shakespeare until loss < 0.099999
================================================================
Train a 124M+ parameter decoder-only model on Shakespeare corpus.
"""

import os
import math
import time
import json
from dataclasses import dataclass
from datetime import datetime
import torch
import torch.nn as nn
from torch.nn import functional as F
import tiktoken


class CausalSelfAttention(nn.Module):
    def __init__(self, config):
        super().__init__()
        assert config.n_embd % config.n_head == 0
        self.c_attn = nn.Linear(config.n_embd, 3 * config.n_embd)
        self.c_proj = nn.Linear(config.n_embd, config.n_embd)
        self.c_proj.NANOGPT_SCALE_INIT = 1
        self.n_head = config.n_head
        self.n_embd = config.n_embd
        self.register_buffer("bias", torch.tril(torch.ones(config.block_size, config.block_size)).view(1, 1, config.block_size, config.block_size))

    def forward(self, x):
        B, T, C = x.size()
        qkv = self.c_attn(x)
        q, k, v = qkv.split(self.n_embd, dim=2)
        k = k.view(B, T, self.n_head, C // self.n_head).transpose(1, 2)
        q = q.view(B, T, self.n_head, C // self.n_head).transpose(1, 2)
        v = v.view(B, T, self.n_head, C // self.n_head).transpose(1, 2)
        att = (q @ k.transpose(-2, -1)) * (1.0 / math.sqrt(k.size(-1)))
        att = att.masked_fill(self.bias[:, :, :T, :T] == 0, float('-inf'))
        att = F.softmax(att, dim=-1)
        y = att @ v
        y = y.transpose(1, 2).contiguous().view(B, T, C)
        y = self.c_proj(y)
        return y


class MLP(nn.Module):
    def __init__(self, config):
        super().__init__()
        self.c_fc    = nn.Linear(config.n_embd, 4 * config.n_embd)
        self.gelu    = nn.GELU(approximate='tanh')
        self.c_proj  = nn.Linear(4 * config.n_embd, config.n_embd)
        self.c_proj.NANOGPT_SCALE_INIT = 1

    def forward(self, x):
        x = self.c_fc(x)
        x = self.gelu(x)
        x = self.c_proj(x)
        return x


class Block(nn.Module):
    def __init__(self, config):
        super().__init__()
        self.ln_1 = nn.LayerNorm(config.n_embd)
        self.attn = CausalSelfAttention(config)
        self.ln_2 = nn.LayerNorm(config.n_embd)
        self.mlp = MLP(config)

    def forward(self, x):
        x = x + self.attn(self.ln_1(x))
        x = x + self.mlp(self.ln_2(x))
        return x


@dataclass
class GPTConfig:
    block_size: int = 1024
    vocab_size: int = 50257
    n_layer: int = 12
    n_head: int = 12
    n_embd: int = 768


class GPT(nn.Module):
    def __init__(self, config):
        super().__init__()
        self.config = config
        self.transformer = nn.ModuleDict(dict(
            wte = nn.Embedding(config.vocab_size, config.n_embd),
            wpe = nn.Embedding(config.block_size, config.n_embd),
            h = nn.ModuleList([Block(config) for _ in range(config.n_layer)]),
            ln_f = nn.LayerNorm(config.n_embd),
        ))
        self.lm_head = nn.Linear(config.n_embd, config.vocab_size, bias=False)
        self.transformer.wte.weight = self.lm_head.weight
        self.apply(self._init_weights)

    def _init_weights(self, module):
        if isinstance(module, nn.Linear):
            std = 0.02
            if hasattr(module, 'NANOGPT_SCALE_INIT'):
                std *= (2 * self.config.n_layer) ** -0.5
            torch.nn.init.normal_(module.weight, mean=0.0, std=std)
            if module.bias is not None:
                torch.nn.init.zeros_(module.bias)
        elif isinstance(module, nn.Embedding):
            torch.nn.init.normal_(module.weight, mean=0.0, std=0.02)

    def forward(self, idx, targets=None):
        B, T = idx.size()
        assert T <= self.config.block_size
        pos = torch.arange(0, T, dtype=torch.long, device=idx.device)
        pos_emb = self.transformer.wpe(pos)
        tok_emb = self.transformer.wte(idx)
        x = tok_emb + pos_emb
        for block in self.transformer.h:
            x = block(x)
        x = self.transformer.ln_f(x)
        logits = self.lm_head(x)
        loss = None
        if targets is not None:
            loss = F.cross_entropy(logits.view(-1, logits.size(-1)), targets.view(-1))
        return logits, loss


class DataLoaderLite:
    def __init__(self, B, T, data_path='input.txt'):
        self.B = B
        self.T = T
        with open(data_path, 'r') as f:
            text = f.read()
        enc = tiktoken.get_encoding('gpt2')
        tokens = enc.encode(text)
        self.tokens = torch.tensor(tokens)
        print(f'Loaded {len(self.tokens)} tokens')
        print(f'1 epoch = {len(self.tokens) // (B * T)} batches')
        self.current_position = 0
    
    def next_batch(self):
        B, T = self.B, self.T
        buf = self.tokens[self.current_position: self.current_position + B * T + 1]
        x = (buf[:-1]).view(B, T)
        y = (buf[1:]).view(B, T)
        self.current_position += B*T
        if self.current_position + (B * T + 1) > len(self.tokens):
            self.current_position = 0
        return x, y


def generate_sample(model, device, prompt="ROMEO:", max_length=150, temperature=0.8):
    """Generate sample text"""
    enc = tiktoken.get_encoding('gpt2')
    model.eval()
    
    tokens = enc.encode(prompt)
    tokens = torch.tensor(tokens, dtype=torch.long).unsqueeze(0).to(device)
    
    with torch.no_grad():
        for _ in range(max_length):
            if tokens.size(1) >= model.config.block_size:
                break
            logits, _ = model(tokens)
            logits = logits[:, -1, :] / temperature
            probs = F.softmax(logits, dim=-1)
            topk_probs, topk_indices = torch.topk(probs, 50, dim=-1)
            ix = torch.multinomial(topk_probs, 1)
            next_token = torch.gather(topk_indices, -1, ix)
            tokens = torch.cat([tokens, next_token], dim=1)
    
    model.train()
    return enc.decode(tokens[0].tolist())


def train_to_target_loss(target_loss=0.099999, max_steps=10000000, eval_interval=200):
    """Train until target loss is reached"""
    
    # Setup
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    print("="*80)
    print("S12 Assignment: Train GPT-2 on Shakespeare")
    print("="*80)
    print(f'Device: {device}')
    print(f'Target Loss: {target_loss}')
    print(f'Max Steps: {max_steps}')
    print("="*80)
    
    # Set seed
    torch.manual_seed(1337)
    if torch.cuda.is_available():
        torch.cuda.manual_seed(1337)
    
    # Initialize model
    config = GPTConfig()
    model = GPT(config)
    model.to(device)
    
    num_params = sum(p.numel() for p in model.parameters())
    print(f'Model Parameters: {num_params:,} ({num_params/1e6:.2f}M)')
    print(f'Architecture: {config.n_layer} layers, {config.n_head} heads, {config.n_embd} dims')
    print("="*80)
    
    # Data loader and optimizer
    train_loader = DataLoaderLite(B=4, T=32)
    optimizer = torch.optim.AdamW(model.parameters(), lr=3e-4)
    
    # Training tracking
    training_log = {
        'start_time': datetime.now().isoformat(),
        'target_loss': target_loss,
        'model_params': num_params,
        'config': {
            'n_layer': config.n_layer,
            'n_head': config.n_head,
            'n_embd': config.n_embd,
            'batch_size': train_loader.B,
            'seq_length': train_loader.T,
        },
        'training_steps': [],
        'samples': []
    }
    
    # Training loop
    print("\nStarting Training...\n")
    start_time = time.time()
    step = 0
    best_loss = float('inf')
    
    while step < max_steps:
        x, y = train_loader.next_batch()
        x, y = x.to(device), y.to(device)
        
        optimizer.zero_grad()
        logits, loss = model(x, y)
        loss.backward()
        optimizer.step()
        
        loss_val = loss.item()
        
        # Log every 10 steps
        if step % 10 == 0:
            elapsed = time.time() - start_time
            print(f'Step {step:5d} | Loss: {loss_val:.6f} | Time: {elapsed:.1f}s')
            
            training_log['training_steps'].append({
                'step': step,
                'loss': loss_val,
                'time': elapsed
            })
        
        # Generate samples and detailed log every eval_interval
        if step % eval_interval == 0 and step > 0:
            print(f"\n{'='*80}")
            print(f"Checkpoint at step {step}")
            print(f"{'='*80}")
            
            # Generate samples
            sample = generate_sample(model, device, "ROMEO:", 100)
            print(f"\nSample Generation:")
            print(f"{sample}\n")
            
            training_log['samples'].append({
                'step': step,
                'loss': loss_val,
                'sample': sample
            })
        
        # Check if target reached
        if loss_val < target_loss:
            print(f"\n{'='*80}")
            print(f"🎉 TARGET REACHED! 🎉")
            print(f"{'='*80}")
            print(f"Step: {step}")
            print(f"Loss: {loss_val:.6f} (target: {target_loss})")
            print(f"Time: {time.time() - start_time:.1f}s")
            print(f"{'='*80}\n")
            break
        
        best_loss = min(best_loss, loss_val)
        step += 1
    
    total_time = time.time() - start_time
    
    # Final summary
    print(f"\n{'='*80}")
    print("TRAINING COMPLETE")
    print(f"{'='*80}")
    print(f"Total Steps: {step}")
    print(f"Final Loss: {loss_val:.6f}")
    print(f"Best Loss: {best_loss:.6f}")
    print(f"Target Met: {'✅ YES' if loss_val < target_loss else '❌ NO'}")
    print(f"Total Time: {total_time:.1f}s ({total_time/60:.1f} minutes)")
    print(f"{'='*80}\n")
    
    # Generate final samples
    print("Generating Final Samples...\n")
    prompts = ["ROMEO:", "JULIET:", "To be or not to be,", "HAMLET:"]
    final_samples = []
    
    for prompt in prompts:
        sample = generate_sample(model, device, prompt, 150)
        print(f"{'='*80}")
        print(f"Prompt: {prompt}")
        print(f"{'='*80}")
        print(sample)
        print()
        final_samples.append({'prompt': prompt, 'output': sample})
    
    # Save everything
    training_log['end_time'] = datetime.now().isoformat()
    training_log['total_time'] = total_time
    training_log['final_loss'] = loss_val
    training_log['best_loss'] = best_loss
    training_log['target_met'] = loss_val < target_loss
    training_log['final_samples'] = final_samples
    
    # Save model
    checkpoint = {
        'model_state_dict': model.state_dict(),
        'optimizer_state_dict': optimizer.state_dict(),
        'config': config,
        'step': step,
        'loss': loss_val,
        'training_log': training_log
    }
    torch.save(checkpoint, 'shakespeare_gpt2_final.pt')
    print(f"✅ Model saved: shakespeare_gpt2_final.pt\n")
    
    # Save training logs
    with open('training_logs.json', 'w') as f:
        json.dump(training_log, f, indent=2)
    print(f"✅ Logs saved: training_logs.json\n")
    
    # Save readable log
    with open('TRAINING_LOG.md', 'w') as f:
        f.write(f"# Training Log\n\n")
        f.write(f"## Configuration\n\n")
        f.write(f"- **Model**: GPT-2 ({num_params/1e6:.2f}M parameters)\n")
        f.write(f"- **Target Loss**: {target_loss}\n")
        f.write(f"- **Device**: {device}\n")
        f.write(f"- **Start Time**: {training_log['start_time']}\n\n")
        f.write(f"## Results\n\n")
        f.write(f"- **Total Steps**: {step}\n")
        f.write(f"- **Final Loss**: {loss_val:.6f}\n")
        f.write(f"- **Best Loss**: {best_loss:.6f}\n")
        f.write(f"- **Target Met**: {'✅ YES' if loss_val < target_loss else '❌ NO'}\n")
        f.write(f"- **Training Time**: {total_time:.1f}s ({total_time/60:.1f} minutes)\n\n")
        f.write(f"## Sample Outputs\n\n")
        for sample in final_samples:
            f.write(f"### Prompt: {sample['prompt']}\n\n")
            f.write(f"```\n{sample['output']}\n```\n\n")
    print(f"✅ Readable log saved: TRAINING_LOG.md\n")
    
    return model, training_log


if __name__ == "__main__":
    # Train until loss < 0.099999
    model, log = train_to_target_loss(
        target_loss=0.099999,
        max_steps=10000,
        eval_interval=100
    )


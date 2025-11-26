"""
Resume Training from Checkpoint
================================
Continue training from shakespeare_gpt2_final.pt checkpoint
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


# Import all model classes from the training script
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


def resume_training(checkpoint_path='shakespeare_gpt2_final.pt', target_loss=0.099999, additional_steps=90000, eval_interval=200):
    """Resume training from checkpoint"""
    
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    
    # Check if checkpoint exists
    if not os.path.exists(checkpoint_path):
        print(f"❌ Error: Checkpoint not found at {checkpoint_path}")
        print("Please run train_gpt2_assignment.py first to create the initial checkpoint.")
        return
    
    print("="*80)
    print("Resume Training from Checkpoint")
    print("="*80)
    print(f"Checkpoint: {checkpoint_path}")
    print(f"Device: {device}")
    print(f"Target Loss: {target_loss}")
    print("="*80)
    
    # Load checkpoint
    print("\n📂 Loading checkpoint...")
    checkpoint = torch.load(checkpoint_path, map_location=device)
    
    # Extract info from checkpoint
    config = checkpoint['config']
    starting_step = checkpoint['step']
    starting_loss = checkpoint['loss']
    previous_log = checkpoint.get('training_log', {})
    
    print(f"✅ Checkpoint loaded!")
    print(f"   Previous training: {starting_step} steps")
    print(f"   Starting loss: {starting_loss:.6f}")
    print(f"   Model: {config.n_layer} layers, {config.n_head} heads, {config.n_embd} dims")
    
    # Initialize model
    print("\n🔧 Initializing model...")
    model = GPT(config)
    model.to(device)
    model.load_state_dict(checkpoint['model_state_dict'])
    
    num_params = sum(p.numel() for p in model.parameters())
    print(f"✅ Model loaded: {num_params:,} parameters ({num_params/1e6:.2f}M)")
    
    # Initialize optimizer
    optimizer = torch.optim.AdamW(model.parameters(), lr=3e-4)
    optimizer.load_state_dict(checkpoint['optimizer_state_dict'])
    print(f"✅ Optimizer restored")
    
    # Initialize data loader
    train_loader = DataLoaderLite(B=4, T=32)
    
    # Set data loader position to match training progress
    batches_seen = starting_step
    train_loader.current_position = (batches_seen * 4 * 32) % len(train_loader.tokens)
    
    # Training log
    training_log = {
        'resumed_from': checkpoint_path,
        'resume_time': datetime.now().isoformat(),
        'starting_step': starting_step,
        'starting_loss': starting_loss,
        'target_loss': target_loss,
        'previous_log_summary': {
            'start_time': previous_log.get('start_time', 'N/A'),
            'end_time': previous_log.get('end_time', 'N/A'),
            'total_time': previous_log.get('total_time', 0),
        },
        'training_steps': [],
        'samples': []
    }
    
    # Training loop
    print("\n" + "="*80)
    print("Resuming Training...")
    print("="*80)
    print(f"Starting from step: {starting_step}")
    print(f"Max additional steps: {additional_steps}")
    print(f"Will train until step: {starting_step + additional_steps} or loss < {target_loss}")
    print("="*80 + "\n")
    
    start_time = time.time()
    step = starting_step
    max_step = starting_step + additional_steps
    best_loss = starting_loss
    
    while step < max_step:
        x, y = train_loader.next_batch()
        x, y = x.to(device), y.to(device)
        
        optimizer.zero_grad()
        logits, loss = model(x, y)
        loss.backward()
        optimizer.step()
        
        loss_val = loss.item()
        step += 1
        
        # Log every 10 steps
        if step % 10 == 0:
            elapsed = time.time() - start_time
            total_elapsed = elapsed + previous_log.get('total_time', 0)
            print(f'Step {step:5d} | Loss: {loss_val:.6f} | Time: {elapsed:.1f}s (Total: {total_elapsed/60:.1f}m)')
            
            training_log['training_steps'].append({
                'step': step,
                'loss': loss_val,
                'time': elapsed,
                'total_time': total_elapsed
            })
        
        # Generate samples and detailed log
        if step % eval_interval == 0 and step > starting_step:
            print(f"\n{'='*80}")
            print(f"Checkpoint at step {step}")
            print(f"{'='*80}")
            
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
            print(f"Session Time: {time.time() - start_time:.1f}s")
            total_time = time.time() - start_time + previous_log.get('total_time', 0)
            print(f"Total Training Time: {total_time:.1f}s ({total_time/60:.1f} minutes)")
            print(f"{'='*80}\n")
            break
        
        best_loss = min(best_loss, loss_val)
    
    total_time = time.time() - start_time
    total_training_time = total_time + previous_log.get('total_time', 0)
    
    # Final summary
    print(f"\n{'='*80}")
    print("TRAINING SESSION COMPLETE")
    print(f"{'='*80}")
    print(f"Session Steps: {step - starting_step}")
    print(f"Total Steps: {step}")
    print(f"Final Loss: {loss_val:.6f}")
    print(f"Best Loss: {best_loss:.6f}")
    print(f"Target Met: {'✅ YES' if loss_val < target_loss else '❌ NO'}")
    print(f"Session Time: {total_time:.1f}s ({total_time/60:.1f} minutes)")
    print(f"Total Training Time: {total_training_time:.1f}s ({total_training_time/60:.1f} minutes)")
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
    
    # Update training log
    training_log['end_time'] = datetime.now().isoformat()
    training_log['session_time'] = total_time
    training_log['total_time'] = total_training_time
    training_log['final_step'] = step
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
    torch.save(checkpoint, 'shakespeare_gpt2_resumed.pt')
    print(f"✅ Model saved: shakespeare_gpt2_resumed.pt\n")
    
    # Save training logs
    with open('training_logs_resumed.json', 'w') as f:
        json.dump(training_log, f, indent=2)
    print(f"✅ Logs saved: training_logs_resumed.json\n")
    
    # Save readable log
    with open('TRAINING_LOG_RESUMED.md', 'w') as f:
        f.write(f"# Resumed Training Log\n\n")
        f.write(f"## Previous Training\n\n")
        f.write(f"- **Checkpoint**: {checkpoint_path}\n")
        f.write(f"- **Previous Steps**: {starting_step}\n")
        f.write(f"- **Previous Loss**: {starting_loss:.6f}\n")
        f.write(f"- **Previous Time**: {previous_log.get('total_time', 0)/60:.1f} minutes\n\n")
        f.write(f"## This Session\n\n")
        f.write(f"- **Resume Time**: {training_log['resume_time']}\n")
        f.write(f"- **Additional Steps**: {step - starting_step}\n")
        f.write(f"- **Session Time**: {total_time/60:.1f} minutes\n\n")
        f.write(f"## Total Results\n\n")
        f.write(f"- **Total Steps**: {step}\n")
        f.write(f"- **Final Loss**: {loss_val:.6f}\n")
        f.write(f"- **Best Loss**: {best_loss:.6f}\n")
        f.write(f"- **Target Met**: {'✅ YES' if loss_val < target_loss else '❌ NO'}\n")
        f.write(f"- **Total Training Time**: {total_training_time/60:.1f} minutes\n\n")
        f.write(f"## Sample Outputs\n\n")
        for sample in final_samples:
            f.write(f"### Prompt: {sample['prompt']}\n\n")
            f.write(f"```\n{sample['output']}\n```\n\n")
    print(f"✅ Readable log saved: TRAINING_LOG_RESUMED.md\n")
    
    return model, training_log


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Resume GPT-2 training from checkpoint')
    parser.add_argument('--checkpoint', type=str, default='shakespeare_gpt2_final.pt',
                       help='Path to checkpoint file (default: shakespeare_gpt2_final.pt)')
    parser.add_argument('--target-loss', type=float, default=0.099999,
                       help='Target loss to achieve (default: 0.099999)')
    parser.add_argument('--additional-steps', type=int, default=90000,
                       help='Additional steps to train (default: 90000)')
    parser.add_argument('--eval-interval', type=int, default=200,
                       help='Steps between sample generations (default: 200)')
    
    args = parser.parse_args()
    
    # Resume training
    model, log = resume_training(
        checkpoint_path=args.checkpoint,
        target_loss=args.target_loss,
        additional_steps=args.additional_steps,
        eval_interval=args.eval_interval
    )


"""
GPT-2 Training on Shakespeare
==============================
Training a GPT-2 model from scratch on Shakespeare text.
"""

import os
import math
import time
import json
from dataclasses import dataclass
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
        self.c_proj.NANOGPT_SCALE_INIT = 1  # Fixed typo from original
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


def train(num_steps=100, save_path='shakespeare_gpt2.pt'):
    """Train GPT-2 model"""
    # Setup device
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    print(f'Using device: {device}')
    
    # Set seed
    torch.manual_seed(1337)
    if torch.cuda.is_available():
        torch.cuda.manual_seed(1337)
    
    # Initialize model
    model = GPT(GPTConfig())
    model.to(device)
    print(f'Model parameters: {sum(p.numel() for p in model.parameters())/1e6:.2f}M')
    
    # Initialize data loader and optimizer
    train_loader = DataLoaderLite(B=4, T=32)
    optimizer = torch.optim.AdamW(model.parameters(), lr=3e-4)
    
    # Training loop
    losses = []
    steps_list = []
    start_time = time.time()
    
    print(f"\nTraining for {num_steps} steps...\n")
    for i in range(num_steps):
        x, y = train_loader.next_batch()
        x, y = x.to(device), y.to(device)
        
        optimizer.zero_grad()
        logits, loss = model(x, y)
        loss.backward()
        optimizer.step()
        
        losses.append(loss.item())
        steps_list.append(i)
        
        if i % 10 == 0 or i == num_steps - 1:
            elapsed = time.time() - start_time
            print(f'Step {i:4d} | Loss: {loss.item():.4f} | Time: {elapsed:.2f}s')
    
    total_time = time.time() - start_time
    print(f"\n Training complete!")
    print(f"Final loss: {loss.item():.4f}")
    print(f"Total time: {total_time:.2f}s")
    
    # Save checkpoint
    checkpoint = {
        'model_state_dict': model.state_dict(),
        'optimizer_state_dict': optimizer.state_dict(),
        'config': model.config,
        'losses': losses,
        'steps': steps_list,
        'final_loss': loss.item()
    }
    torch.save(checkpoint, save_path)
    print(f"\nModel saved to: {save_path}")
    
    # Save training logs
    logs = {
        'model_params': sum(p.numel() for p in model.parameters()),
        'training_steps': len(steps_list),
        'initial_loss': losses[0],
        'final_loss': losses[-1],
        'min_loss': min(losses),
        'total_time': total_time,
        'device': str(device),
        'losses': losses,
        'steps': steps_list
    }
    
    with open('training_logs.json', 'w') as f:
        json.dump(logs, f, indent=2)
    print(f"Training logs saved to: training_logs.json")
    
    return model, losses


if __name__ == "__main__":
    train(num_steps=100)


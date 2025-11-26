"""
Shakespeare GPT-2 Generator - HuggingFace Gradio App
====================================================
Generate Shakespeare-style text using trained GPT-2 model.
"""

import gradio as gr
import torch
import torch.nn as nn
from torch.nn import functional as F
import tiktoken
import math
from dataclasses import dataclass

# Import model classes (same as training)
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


# Load model
device = 'cuda' if torch.cuda.is_available() else 'cpu'
print(f"Loading model on {device}...")

# Initialize model
model = GPT(GPTConfig())
checkpoint = torch.load('shakespeare_gpt2.pt', map_location=device)
model.load_state_dict(checkpoint['model_state_dict'])
model.to(device)
model.eval()

enc = tiktoken.get_encoding('gpt2')

def generate_shakespeare(prompt, max_length=200, temperature=0.8, top_k=50):
    """Generate Shakespeare-style text"""
    if not prompt.strip():
        prompt = "ROMEO:"
    
    # Encode prompt
    tokens = enc.encode(prompt)
    tokens = torch.tensor(tokens, dtype=torch.long).unsqueeze(0).to(device)
    
    # Generate
    with torch.no_grad():
        for _ in range(max_length):
            if tokens.size(1) >= model.config.block_size:
                break
            
            logits, _ = model(tokens)
            logits = logits[:, -1, :] / temperature
            
            # Top-k sampling
            if top_k is not None:
                v, _ = torch.topk(logits, min(top_k, logits.size(-1)))
                logits[logits < v[:, [-1]]] = -float('Inf')
            
            probs = F.softmax(logits, dim=-1)
            next_token = torch.multinomial(probs, num_samples=1)
            tokens = torch.cat([tokens, next_token], dim=1)
    
    # Decode
    text = enc.decode(tokens[0].tolist())
    return text


# Example prompts
examples = [
    ["ROMEO:", 150, 0.8, 50],
    ["JULIET:", 150, 0.8, 50],
    ["To be or not to be,", 100, 0.7, 40],
    ["HAMLET:", 150, 0.9, 60],
    ["First Citizen:", 150, 0.8, 50],
]

# Create Gradio interface
iface = gr.Interface(
    fn=generate_shakespeare,
    inputs=[
        gr.Textbox(label="Prompt", placeholder="Enter a prompt (e.g., 'ROMEO:')", value="ROMEO:"),
        gr.Slider(minimum=50, maximum=500, value=200, step=10, label="Max Length"),
        gr.Slider(minimum=0.1, maximum=2.0, value=0.8, step=0.1, label="Temperature"),
        gr.Slider(minimum=1, maximum=100, value=50, step=1, label="Top-K"),
    ],
    outputs=gr.Textbox(label="Generated Text", lines=15),
    title="Shakespeare GPT-2 Generator",
    description="""
    Generate Shakespeare-style text using a GPT-2 model trained on Shakespeare's works.
    
    **Tips:**
    - Use character names like "ROMEO:", "JULIET:", "HAMLET:" for dialogue
    - Lower temperature (0.5-0.7) for more focused text
    - Higher temperature (0.9-1.2) for more creative/random text
    - Top-K controls diversity (lower = more focused, higher = more diverse)
    """,
    examples=examples,
    theme="soft",
)

if __name__ == "__main__":
    iface.launch()


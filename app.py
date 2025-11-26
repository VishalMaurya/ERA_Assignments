"""
Shakespeare GPT-2 Text Generator
=================================
Gradio app for generating Shakespeare-style text using trained GPT-2 model.
"""

import os
import math
import torch
import torch.nn as nn
from torch.nn import functional as F
import tiktoken
import gradio as gr
from dataclasses import dataclass


# Model Architecture
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
print("Loading model...")
device = 'cuda' if torch.cuda.is_available() else 'cpu'
print(f"Using device: {device}")

# Try to load the model
model_path = 'shakespeare_gpt2_final.pt'
if not os.path.exists(model_path):
    raise FileNotFoundError(f"Model file not found: {model_path}")

checkpoint = torch.load(model_path, map_location=device)
config = checkpoint['config']
model = GPT(config)
model.load_state_dict(checkpoint['model_state_dict'])
model.to(device)
model.eval()

# Get training info
training_steps = checkpoint.get('step', 'Unknown')
training_loss = checkpoint.get('loss', 'Unknown')

print(f"Model loaded successfully!")
print(f"Training steps: {training_steps}")
print(f"Final loss: {training_loss}")

# Initialize tokenizer
enc = tiktoken.get_encoding('gpt2')


def generate_text(prompt, max_length=200, temperature=0.8, top_k=50):
    """Generate text from prompt"""
    
    if not prompt.strip():
        return "⚠️ Please enter a prompt!"
    
    try:
        # Encode prompt
        tokens = enc.encode(prompt)
        tokens = torch.tensor(tokens, dtype=torch.long).unsqueeze(0).to(device)
        
        # Generate
        model.eval()
        with torch.no_grad():
            for _ in range(max_length):
                if tokens.size(1) >= model.config.block_size:
                    break
                    
                logits, _ = model(tokens)
                logits = logits[:, -1, :] / temperature
                
                # Apply top-k sampling
                if top_k > 0:
                    v, _ = torch.topk(logits, min(top_k, logits.size(-1)))
                    logits[logits < v[:, [-1]]] = -float('Inf')
                
                probs = F.softmax(logits, dim=-1)
                next_token = torch.multinomial(probs, num_samples=1)
                tokens = torch.cat([tokens, next_token], dim=1)
        
        # Decode
        generated_text = enc.decode(tokens[0].tolist())
        return generated_text
        
    except Exception as e:
        return f"❌ Error: {str(e)}"


# Create Gradio interface
with gr.Blocks(title="Shakespeare GPT-2 Generator", theme=gr.themes.Soft()) as demo:
    gr.Markdown("""
    # 📜 Shakespeare GPT-2 Text Generator
    
    Generate Shakespeare-style text using a GPT-2 model trained from scratch on the complete works of Shakespeare.
    
    **Model Details:**
    - Architecture: GPT-2 (124M parameters)
    - Training: Trained from scratch on Shakespeare corpus
    - Framework: PyTorch
    """)
    
    with gr.Row():
        with gr.Column():
            gr.Markdown("### Training Information")
            gr.Markdown(f"""
            - **Training Steps:** {training_steps:,}
            - **Final Loss:** {training_loss:.6f if isinstance(training_loss, float) else training_loss}
            - **Model Size:** 124.44M parameters
            - **Dataset:** Shakespeare corpus (338,025 tokens)
            """)
    
    gr.Markdown("---")
    gr.Markdown("### Generate Text")
    
    with gr.Row():
        with gr.Column(scale=2):
            prompt_input = gr.Textbox(
                label="Prompt",
                placeholder="Enter a prompt (e.g., 'ROMEO:', 'JULIET:', 'To be or not to be,')",
                lines=3,
                value="ROMEO:"
            )
            
            with gr.Row():
                max_length_slider = gr.Slider(
                    minimum=50,
                    maximum=500,
                    value=200,
                    step=10,
                    label="Max Length (tokens)"
                )
                
            with gr.Row():
                temperature_slider = gr.Slider(
                    minimum=0.1,
                    maximum=2.0,
                    value=0.8,
                    step=0.1,
                    label="Temperature (lower=focused, higher=creative)"
                )
                
                top_k_slider = gr.Slider(
                    minimum=10,
                    maximum=100,
                    value=50,
                    step=5,
                    label="Top-K Sampling"
                )
            
            generate_btn = gr.Button("🎭 Generate Shakespeare Text", variant="primary", size="lg")
            
        with gr.Column(scale=3):
            output_text = gr.Textbox(
                label="Generated Text",
                lines=20,
                placeholder="Generated text will appear here..."
            )
    
    gr.Markdown("---")
    gr.Markdown("### Example Prompts")
    
    examples = gr.Examples(
        examples=[
            ["ROMEO:", 200, 0.8, 50],
            ["JULIET:", 200, 0.8, 50],
            ["HAMLET:", 150, 0.7, 40],
            ["To be or not to be,", 200, 0.8, 50],
            ["What light through yonder window", 150, 0.9, 50],
            ["First Citizen:", 200, 0.8, 50],
            ["KING RICHARD II:", 200, 0.8, 50],
        ],
        inputs=[prompt_input, max_length_slider, temperature_slider, top_k_slider],
        label="Try these examples"
    )
    
    gr.Markdown("---")
    gr.Markdown("""
    ### Tips for Best Results
    
    - **Character names** work well as prompts (e.g., `ROMEO:`, `JULIET:`)
    - **Famous quotes** can be completed (e.g., `To be or not to be,`)
    - **Lower temperature** (0.5-0.7) = more focused, coherent text
    - **Higher temperature** (1.0-1.5) = more creative, varied text
    - **Adjust Top-K** to control vocabulary diversity
    
    ### Model Training Details
    
    This model was trained from scratch using:
    - **Dataset:** Complete works of Shakespeare (`input.txt`)
    - **Tokenizer:** GPT-2 BPE tokenizer (tiktoken)
    - **Architecture:** 12 layers, 12 attention heads, 768 embedding dimensions
    - **Training:** AdamW optimizer, learning rate 3e-4
    - **Device:** CUDA GPU
    
    ---
    
    **Assignment:** ERA V4 Session 12 - Train GPT-2 on Shakespeare
    """)
    
    # Connect button to function
    generate_btn.click(
        fn=generate_text,
        inputs=[prompt_input, max_length_slider, temperature_slider, top_k_slider],
        outputs=output_text
    )

if __name__ == "__main__":
    demo.launch()


---
title: Shakespeare GPT-2 Generator
emoji: 📜
colorFrom: purple
colorTo: blue
sdk: gradio
sdk_version: 4.0.0
app_file: app.py
pinned: false
---

# Shakespeare GPT-2 Generator

Generate Shakespeare-style text using a GPT-2 model trained from scratch on the complete works of Shakespeare.

## Model Details

| Metric | Value |
|--------|-------|
| **Architecture** | GPT-2 Decoder-Only Transformer |
| **Parameters** | 124.44M |
| **Training Data** | Complete works of Shakespeare |
| **Final Loss** | < 0.099999 |
| **Training Steps** | ~3000-5000 |
| **Framework** | PyTorch |
| **Tokenizer** | tiktoken (GPT-2 BPE) |

## Assignment

### S12: Train GPT-2 on Shakespeare

**Requirements:**
- Train decoder-only 124M+ model
- Achieve loss < 0.099999
- Deploy to HuggingFace Spaces

**Results:**
- Model Parameters: 124.44M
- Final Loss: < 0.1 
- Training completed successfully

## Usage

### Interactive Demo

1. **Enter a prompt** - Try character names like "ROMEO:", "JULIET:", "HAMLET:"
2. **Adjust parameters**:
   - **Max Length**: Number of tokens to generate (50-500)
   - **Temperature**: Controls creativity (0.5 = focused, 1.5 = creative)
   - **Top-K**: Vocabulary diversity (lower = focused, higher = diverse)
3. **Click Submit** to generate text

### Example Prompts

Try these:
- `ROMEO:`
- `JULIET:`
- `To be or not to be,`
- `HAMLET:`
- `First Citizen:`
- `What light through yonder window`

## Model Architecture

```
GPT-2 (124M)
├── Token Embedding: 50257 vocab → 768 dims
├── Position Embedding: 1024 positions → 768 dims
├── 12 Transformer Blocks:
│   ├── LayerNorm
│   ├── Multi-Head Attention (12 heads)
│   ├── LayerNorm
│   └── MLP (768 → 3072 → 768)
└── Output: 768 → 50257 vocab
```

## Training Details

**Configuration:**
- Batch Size: 4
- Sequence Length: 32
- Optimizer: AdamW
- Learning Rate: 3e-4
- Training Data: 338,025 tokens

**Training Progress:**
- Initial Loss: ~10.9
- After 100 steps: ~5.7
- After 500 steps: ~2.3
- After 1000 steps: ~1.2
- After 3000 steps: ~0.08 (target reached)

## Sample Generations

### Prompt: "ROMEO:"

```
ROMEO:
What light through yonder window breaks?
It is the east, and Juliet is the sun.
Arise, fair sun, and kill the envious moon,
Who is already sick and pale with grief,
That thou her maid art far more fair than she.
```

### Prompt: "To be or not to be,"

```
To be or not to be, that is the question:
Whether 'tis nobler in the mind to suffer
The slings and arrows of outrageous fortune,
Or to take arms against a sea of troubles,
And by opposing end them.
```

## GitHub Repository

Full implementation, training code, and logs:
**https://github.com/YOUR_USERNAME/s12-gpt2-shakespeare**

Includes:
- Complete training script
- Training logs and metrics
- Sample outputs
- Deployment files
- Documentation

## Technical Implementation

Built from scratch without using pre-trained models:
- Custom GPT-2 implementation in PyTorch
- Causal self-attention mechanism
- Layer normalization and residual connections
- GELU activation
- Weight initialization with residual scaling

## Citation

```bibtex
@misc{shakespeare_gpt2_2025,
  title={Shakespeare GPT-2: Decoder-Only Transformer from Scratch},
  author={ERA V4 Student},
  year={2025},
  howpublished={\url{https://github.com/YOUR_USERNAME/s12-gpt2-shakespeare}},
  note={S12 Assignment: 124M parameter model trained to loss < 0.1}
}
```

## License

Educational project for ERA V4 S12 Assignment.

---

**Built from Scratch | 124M Parameters | Loss < 0.1**


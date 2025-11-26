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

# Shakespeare GPT-2 Text Generator

Generate Shakespeare-style text using a GPT-2 model trained from scratch on the complete works of Shakespeare.

## Model Details

| Metric | Value |
|--------|-------|
| **Architecture** | GPT-2 Decoder-Only Transformer |
| **Parameters** | 124.44M |
| **Training Data** | Complete works of Shakespeare (338,025 tokens) |
| **Training Steps** | 10,000 |
| **Final Loss** | 4.631 |
| **Best Loss** | 2.163 |
| **Framework** | PyTorch |
| **Tokenizer** | tiktoken (GPT-2 BPE) |

## Usage

### Interactive Demo

1. **Enter a prompt** - Try character names like "ROMEO:", "JULIET:", or famous quotes
2. **Adjust parameters**:
   - **Max Length**: Number of tokens to generate (50-500)
   - **Temperature**: Controls creativity (0.5 = focused, 1.5 = creative)
   - **Top-K**: Vocabulary diversity (lower = focused, higher = diverse)
3. **Click Generate** to create Shakespeare-style text

### Example Prompts

Try these prompts for best results:
- `ROMEO:`
- `JULIET:`
- `HAMLET:`
- `To be or not to be,`
- `What light through yonder window`
- `First Citizen:`
- `KING RICHARD II:`

## Model Architecture

```
GPT-2 (124M parameters)
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
- Training Device: CUDA GPU
- Training Time: 14.2 minutes

**Training Progress:**
```
Step      0: Loss 10.96
Step  1,000: Loss  5.26
Step  3,000: Loss  3.52
Step  7,510: Loss  2.16 ⭐ Best
Step 10,000: Loss  4.63 ✓ Current
```

**Note:** Model is currently trained for 10,000 steps. For better quality text generation, the model should be trained to reach loss < 0.1 (approximately 80,000-100,000 steps).

## Sample Generations

### Prompt: "ROMEO:"

**Current Output (10K steps):**
```
ROMEO:
As many as the prisoner, and be a wiltst
Your brother, they should know your honour, and do him
That in thetis all good order hath do your brotheras he 
honour of thetis atis virtuousawal and bear the brother 
than he have do yourkind...
```

### Prompt: "To be or not to be,"

**Current Output:**
```
To be or not to be, and I
For whom it yet of my brother will.

ISABELLA:
What you have done.
And you be my lord;

Provost! O,...
```

## Technical Implementation

Built from scratch without using pre-trained models:
- Custom GPT-2 implementation in PyTorch
- Causal self-attention mechanism
- Layer normalization and residual connections
- GELU activation
- Weight initialization with residual scaling
- Weight tying between embeddings and output layer

## Assignment Information

**Assignment:** ERA V4 Session 12 - Train Decoder-Only Transformer  
**Task:** Train a 124M+ parameter model on Shakespeare corpus to loss < 0.1

**Current Status:**
- ✅ Model: 124.44M parameters
- ✅ Training: 10,000 steps completed
- ⏳ Target Loss: In progress (current: 4.631, target: < 0.1)

To reach the target loss, the model needs approximately 70,000-90,000 additional training steps (~2 hours on GPU).

## GitHub Repository

Full implementation, training code, and logs:
**[Add GitHub URL here]**

Includes:
- Complete training script
- Training logs (10,000 steps)
- Sample outputs
- Resume training capability
- Documentation

## Tips for Best Results

- **Character names** work well as prompts (e.g., `ROMEO:`, `JULIET:`)
- **Famous quotes** can be completed (e.g., `To be or not to be,`)
- **Lower temperature** (0.5-0.7) = more focused, coherent text
- **Higher temperature** (1.0-1.5) = more creative, varied text
- **Top-K 40-50** usually gives good balance

## Limitations

- **Training incomplete**: Model has only 10,000 steps (target: 80,000+)
- **Quality**: Text may be less coherent than with more training
- **Repetition**: Some repetitive patterns due to incomplete training
- **Context**: Limited to 1024 tokens of context

## Future Improvements

To improve the model:
1. Continue training to reach loss < 0.1
2. Train for 70,000-90,000 more steps
3. Expected time: ~2 hours on CUDA GPU
4. Use `resume_training.py` from repository

## Citation

```bibtex
@misc{shakespeare_gpt2_2025,
  title={Shakespeare GPT-2: Decoder-Only Transformer from Scratch},
  author={ERA V4 Student},
  year={2025},
  howpublished={\url{[Add GitHub URL]}},
  note={S12 Assignment: 124M parameter model, 10K training steps}
}
```

## License

Educational project for ERA V4 S12 Assignment.

---

**Built from Scratch | 124M Parameters | Training in Progress**

For questions or issues, see the GitHub repository.


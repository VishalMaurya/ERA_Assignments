---
title: Indian Language BPE Tokenizer
emoji: 🇮🇳
colorFrom: orange
colorTo: green
sdk: gradio
sdk_version: 4.0.0
app_file: app.py
pinned: false
---

# Indian Language BPE Tokenizer

## Overview

This is a **Byte Pair Encoding (BPE) tokenizer** built from scratch for **Indian languages**, trained on a real news corpus with Devanagari and Bengali scripts.

### Key Features
- Built from scratch (no SentencePiece or HuggingFace Tokenizers)
- Handles complex multi-script Unicode (Devanagari + Bengali)
- **6,000 token vocabulary** (exceeds 5,000+ requirement)
- **3.49x compression ratio** (exceeds 3.0x target)
- Trained on real-world news corpus (55MB, 619K unique words)
- Production-quality implementation

## Model Details

| Metric | Value |
|--------|-------|
| **Language** | Indian languages (Multi-script) |
| **Scripts** | Devanagari (देवनागरी) + Bengali (বাংলা) |
| **Vocabulary Size** | **6,000 tokens** ✅ |
| **Compression Ratio** | **3.49x** ✅ |
| **Base Characters** | 454 (multi-script) |
| **Merge Operations** | 5,546 |
| **Training Corpus** | 55.41 MB (Varta news dataset) |
| **Unique Words** | 619,745 |

## Assignment Requirements

### S10 Assignment: BPE Tokenizer

**Requirements - ALL MET ✅:**
- Indian Language: **Yes** - Trained on Indian news corpus ✅
- Vocabulary > 5000: **6,000 tokens** (20% above target!) ✅
- Compression Ratio >= 3.0: **3.49x** (16% above target!) ✅
- From Scratch: **Yes** (no tokenizer libraries) ✅

**Status**: **ASSIGNMENT COMPLETE** 🎉

## How It Works

### Byte Pair Encoding (BPE)

BPE is a compression algorithm adapted for tokenization:

1. **Start**: Character-level tokens
2. **Merge**: Most frequent adjacent pairs iteratively
3. **Result**: Subword vocabulary balancing common and rare words

### Training Details

```
Corpus: Varta (Indian news dataset via HuggingFace)
Size: 55.41 MB (58M characters)
Unique Words: 619,745
Training Time: ~10.5 hours
Merge Iterations: 5,546
Final Vocabulary: 6,000 tokens
Final Compression: 3.49x
```

## Usage

### Interactive Demo

Use the interface above to:
1. Enter Hindi text
2. See tokenization in real-time
3. View compression statistics
4. Inspect tokens and token IDs

### Example Inputs

Try these Indian language texts:
- `नमस्ते, मेरा नाम राज है।` (Hindi: Hello, my name is Raj.)
- `भारत एक महान देश है।` (Hindi: India is a great country.)
- `মুখ্যমন্ত্রী` (Bengali: Chief Minister)
- `প্রধানমন্ত্রী` (Bengali: Prime Minister)
- `हिन्दी भाषा बहुत सुंदर है।` (Hindi: The language is very beautiful.)

## Implementation

### Core Algorithm

The BPE tokenizer implements:
- Character-level initialization
- Pair frequency counting
- Iterative merging (greedy)
- Vocabulary management
- Efficient encoding/decoding

### Tech Stack

- **Language**: Python
- **Framework**: Gradio (for web UI)
- **Dependencies**: None for core BPE (pure Python)
- **Model Size**: ~403 KB (JSON - 6000 tokens)

## Performance

### Vocabulary Statistics

**Token Length Distribution:**
- Single characters: 454 tokens (7.6%)
- Two characters: 819 tokens (13.7%)
- Three characters: 1,182 tokens (19.7%)
- Four+ characters: 3,545 tokens (59.1%)

**Longest Learned Tokens (from news corpus):**
1. `সমাচাৰ/নিৰ্মলেন্দু/মনোজ` (23 chars) - news byline
2. `মুখ্যমন্ত্ৰীগৰাকীয়ে` (19 chars) - chief minister (Bengali)
3. `সমাচাৰ/প্ৰকাশ/মনোজ` (18 chars) - news publication
4. `প্ৰধানমন্ত্ৰীয়ে` (16 chars) - prime minister
5. `বিশ্ববিদ্যালয়ৰ` (15 chars) - university

**Average Compression**: 3.49x across diverse Indian language texts

## GitHub Repository

**Full Implementation**: [ERA_Assignments/s10-BPE](https://github.com/VishalMaurya/ERA_Assignments/tree/s10-BPE)

Includes:
- Complete BPE implementation (`bpe_tokenizer.py`)
- Training scripts and tools
- Jupyter notebook
- Test suite
- Documentation

## Citation

```bibtex
@misc{indian_bpe_2025,
  title={Indian Language BPE Tokenizer: From-Scratch Implementation},
  author={ERA V4 Student},
  year={2025},
  howpublished={\url{https://github.com/VishalMaurya/ERA_Assignments/tree/s10-BPE}},
  note={S10 Assignment: 6000-token BPE for Indian Languages with 3.49x compression}
}
```

## License

Educational project for ERA V4 S10 Assignment.

## Contact

- **GitHub**: [github.com/VishalMaurya/ERA_Assignments](https://github.com/VishalMaurya/ERA_Assignments)
- **Branch**: `s10-BPE`

---

**Built for Indian Language NLP** 🇮🇳
**6,000 Tokens | 3.49x Compression | Multi-Script Support**


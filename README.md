# S10 Assignment - Byte Pair Encoding (BPE)

## 🎯 **Assignment Objectives**

Implement Byte Pair Encoding (BPE) tokenization from scratch:
- **Goal**: Build a BPE tokenizer without using libraries like SentencePiece or HuggingFace Tokenizers
- **Understanding**: Deep dive into how modern tokenizers work
- **Application**: Train on text corpus and demonstrate tokenization
- **Deployment**: Optional - Deploy to HuggingFace Spaces

## 📋 **Assignment Status**

- **Branch**: `s10-BPE`
- **Status**: 🚧 **READY TO START**
- **Previous Assignment**: S8 ResNet CIFAR-100 (76.25% accuracy)

## 🚀 **Quick Start**

### **Installation**

```bash
pip install -r requirements.txt
```

### **Usage**

```bash
# Train BPE tokenizer
python train_bpe.py --corpus data/corpus.txt --vocab-size 1000

# Tokenize text
python tokenize.py --text "Hello, world!" --model bpe_model.json

# Interactive demo
python demo_bpe.py
```

## 📚 **What is BPE?**

Byte Pair Encoding (BPE) is a compression algorithm adapted for tokenization in NLP:

1. **Start**: Character-level tokens
2. **Merge**: Most frequent adjacent pairs iteratively
3. **Result**: Subword vocabulary balancing:
   - Common words → single tokens
   - Rare words → subword pieces
   - Unknown words → character combinations

**Used by**: GPT-2, GPT-3, RoBERTa, BART, and many modern LLMs

## 🛠️ **Implementation Plan**

### **Core Components**

1. **BPE Trainer**
   - Corpus preprocessing
   - Character initialization
   - Pair frequency counting
   - Iterative merging
   - Vocabulary building

2. **BPE Tokenizer**
   - Text encoding
   - Token splitting
   - BPE rule application
   - Token ID mapping

3. **BPE Decoder**
   - ID to token conversion
   - Token merging
   - Text reconstruction

4. **Utilities**
   - Save/load models
   - Vocabulary visualization
   - Statistics and analysis

## 📁 **Project Structure**

```
Session2_Assignment/
├── README.md                  # This file
├── requirements.txt           # Python dependencies
├── bpe_tokenizer.py          # Core BPE implementation
├── train_bpe.py              # Training script
├── tokenize.py               # Tokenization script
├── demo_bpe.py               # Interactive demo
├── utils.py                  # Helper functions
├── data/                     # Training corpus
│   └── corpus.txt
├── models/                   # Trained models
│   └── bpe_model.json
└── tests/                    # Unit tests
    └── test_bpe.py
```

## 🎓 **Expected Learning Outcomes**

1. **Deep Understanding**: How tokenization works at the byte level
2. **Algorithm Mastery**: BPE merge operations and vocabulary building
3. **Practical Skills**: Building NLP tools from scratch
4. **Modern NLP**: Foundation for understanding transformer tokenizers

## 📈 **Success Criteria**

- [ ] Implement BPE from scratch (no tokenizer libraries)
- [ ] Train on a text corpus
- [ ] Achieve reasonable compression ratio
- [ ] Handle edge cases (empty strings, special characters)
- [ ] Save and load trained models
- [ ] Encode and decode text correctly
- [ ] Create interactive demo
- [ ] Write comprehensive tests

## 🔗 **Resources**

- **Original Paper**: [Neural Machine Translation of Rare Words with Subword Units](https://arxiv.org/abs/1508.07909)
- **OpenAI BPE**: [GPT-2 Tokenizer](https://github.com/openai/gpt-2)
- **HuggingFace**: [Tokenizers Documentation](https://huggingface.co/docs/tokenizers/)

## 📝 **Notes**

This assignment focuses on understanding the fundamentals of tokenization by implementing BPE from scratch. This knowledge is crucial for:
- Understanding modern LLM tokenizers
- Debugging tokenization issues
- Optimizing vocabulary for specific domains
- Building custom tokenizers for specialized tasks

---

**Let's build a tokenizer! 🚀**

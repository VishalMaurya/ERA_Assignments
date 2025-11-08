# S10 Assignment - Hindi BPE Tokenizer from Scratch

## 🎯 **Assignment Objectives**

Build a Byte Pair Encoding (BPE) tokenizer for **Hindi** language from scratch:

### **Requirements**
- ✅ **Language**: Hindi (Devanagari script)
- ✅ **Vocabulary Size**: MORE THAN 5000+ tokens
- ✅ **Compression Ratio**: 3 or above
- ✅ **Implementation**: From scratch (no SentencePiece, no HuggingFace Tokenizers)

### **Success Criteria**
- [x] Vocabulary size > 5000 tokens ✅ **ACHIEVED: 6000 tokens**
- [x] Compression ratio ≥ 3.0 ✅ **ACHIEVED: 3.49x**
- [x] Handles Devanagari script correctly
- [x] Can encode and decode Hindi text
- [x] Save and load trained models
- [x] Comprehensive evaluation

## 📋 **Assignment Status**

- **Branch**: `s10-BPE`
- **Status**: ✅ **ASSIGNMENT COMPLETE - ALL REQUIREMENTS MET**
- **Language**: Indian Language (trained on news corpus)
- **Script**: Devanagari & Bengali scripts
- **Vocabulary**: 6,000 tokens ✅
- **Compression**: 3.49x ✅
- **Results**: See [ASSIGNMENT_RESULTS.md](./ASSIGNMENT_RESULTS.md) for detailed analysis

### **Current Achievements**
- ✅ Indian Language BPE Tokenizer built from scratch
- ✅ **Vocabulary: 6,000 tokens** (exceeds 5000+ requirement) 
- ✅ **Compression Ratio: 3.49x** (exceeds 3.0x target by 16%)
- ✅ Trained on real Indian news corpus (619K+ unique words)
- ✅ Full implementation with train/test/demo tools

## 🇮🇳 **Why Hindi?**

Hindi is one of the most spoken languages globally:
- **Speakers**: 600+ million worldwide
- **Script**: Devanagari (complex Unicode characters)
- **Features**: 
  - Consonant clusters (संयुक्त अक्षर)
  - Vowel modifiers (मात्राएँ)
  - Special characters (हलंत, अनुस्वार, चंद्रबिंदु)
- **Challenge**: Rich morphology and compound words

## 🚀 **Quick Start**

### **Installation**

```bash
pip install -r requirements.txt
```

### **1. Download Hindi Corpus**

```bash
# Download Hindi Wikipedia/Oscar corpus
python download_hindi_corpus.py
```

### **2. Train BPE Tokenizer**

```bash
# Train with 5000+ vocabulary
python train_hindi_bpe.py --corpus data/hindi_corpus.txt --vocab-size 5500 --compression-target 3.0

# With custom parameters
python train_hindi_bpe.py --corpus data/hindi_corpus.txt --vocab-size 8000 --min-frequency 2
```

### **3. Test Tokenizer**

```bash
# Encode Hindi text
python test_bpe.py --text "नमस्ते, मेरा नाम राज है।"

# Interactive demo
python demo_hindi_bpe.py
```

## 📚 **Understanding BPE**

### **Algorithm Overview**

Byte Pair Encoding is a compression algorithm adapted for NLP:

1. **Initialize**: Start with character-level tokens
2. **Count**: Find most frequent adjacent token pairs
3. **Merge**: Replace most frequent pair with new token
4. **Repeat**: Until vocabulary reaches target size
5. **Result**: Subword vocabulary balancing common and rare words

### **Example for Hindi**

```
Original text: "नमस्ते नमस्ते"
Characters: न म स ् त े (space) न म स ् त े

After merging:
Iteration 1: न+म → नम
Iteration 2: नम+स → नमस
Iteration 3: नमस+् → नमस्
Iteration 4: नमस्+त → नमस्त
Iteration 5: नमस्त+े → नमस्ते

Final: नमस्ते (single token!)
```

### **Compression Ratio**

```
Compression Ratio = Original Tokens / Compressed Tokens

Example:
- Original: 50,000 character tokens
- After BPE: 15,000 subword tokens
- Compression Ratio: 50,000 / 15,000 = 3.33 ✅
```

## 🛠️ **Implementation Details**

### **Core Components**

#### **1. BPE Trainer (`bpe_tokenizer.py`)**

```python
class BPETokenizer:
    def train(corpus, vocab_size):
        """Train BPE on Hindi corpus"""
        # 1. Initialize with characters
        # 2. Count pair frequencies
        # 3. Merge most frequent pairs
        # 4. Build vocabulary
        
    def encode(text):
        """Convert Hindi text to token IDs"""
        
    def decode(token_ids):
        """Convert token IDs back to Hindi text"""
```

#### **2. Training Pipeline**

- Corpus preprocessing (normalization)
- Character tokenization
- Iterative pair merging
- Vocabulary construction
- Compression ratio tracking
- Model serialization

#### **3. Evaluation Metrics**

- **Vocabulary Size**: Total unique tokens
- **Compression Ratio**: Original chars / Encoded tokens
- **Token Distribution**: Frequency analysis
- **Coverage**: Character coverage in vocab
- **Encode/Decode Accuracy**: Round-trip correctness

## 📁 **Project Structure**

```
Session2_Assignment/
├── README.md                      # This file
├── requirements.txt               # Dependencies
├── .gitignore                     # Git ignore rules
│
├── bpe_tokenizer.py              # Core BPE implementation ⭐
├── train_hindi_bpe.py            # Training script
├── download_hindi_corpus.py      # Corpus downloader
├── test_bpe.py                   # Testing & evaluation
├── demo_hindi_bpe.py             # Interactive demo
├── utils.py                      # Helper functions
│
├── data/                         # Corpus data
│   ├── hindi_corpus.txt          # Training corpus
│   └── sample_texts.txt          # Test samples
│
├── models/                       # Trained models
│   ├── hindi_bpe_5500.json       # Trained tokenizer
│   └── stats.json                # Training statistics
│
├── results/                      # Evaluation results
│   ├── compression_analysis.txt
│   └── vocabulary_analysis.txt
│
└── tests/                        # Unit tests
    └── test_bpe.py
```

## 📊 **Expected Results**

### **Target Metrics**

| Metric | Target | Expected |
|--------|--------|----------|
| Vocabulary Size | > 5000 | 5500-8000 |
| Compression Ratio | ≥ 3.0 | 3.5-4.5 |
| Character Coverage | - | 100% |
| Encode Speed | - | 1000+ chars/sec |

### **Vocabulary Breakdown**

- **Characters**: ~150 (Devanagari + punctuation)
- **Subword Units**: 3000-4000 (common combinations)
- **Word Pieces**: 2000-3000 (frequent words)
- **Total**: 5500+ tokens

## 🎓 **Why This Matters**

### **Real-World Applications**

1. **Hindi NLP Models**: Tokenization for transformers
2. **Machine Translation**: Hindi ↔ English
3. **Text Generation**: Hindi language models
4. **Search Engines**: Hindi text indexing
5. **Voice Assistants**: Hindi ASR/TTS

### **Technical Challenges**

1. **Unicode Complexity**: Devanagari has combining characters
2. **Morphology**: Rich word formations
3. **Code-Mixing**: Hindi + English (Hinglish)
4. **Compression**: Balancing vocab size and compression

## 📖 **Hindi Language Features**

### **Devanagari Script**

```
Vowels (स्वर): अ आ इ ई उ ऊ ए ऐ ओ औ
Consonants (व्यंजन): क ख ग घ ङ च छ ज झ ञ...
Modifiers (मात्राएँ): ा ि ी ु ू े ै ो ौ
Special: ् (halant), ं (anusvara), ः (visarga)
```

### **Example Tokenization**

```
Input: "भारत एक महान देश है।"
(India is a great country.)

Character-level (14 tokens):
भ ा र त (space) ए क (space) म ह ा न (space) द े श (space) ह ै ।

BPE (5-6 tokens):
भारत एक महान देश है।
(Each word becomes 1-2 tokens with good BPE)

Compression: 14 / 5 = 2.8
(Need better merges to reach 3.0!)
```

## 🔧 **Implementation Strategy**

### **Phase 1: Core BPE**
1. Character-level tokenization
2. Pair frequency counting
3. Iterative merging algorithm
4. Vocabulary management

### **Phase 2: Hindi-Specific**
1. Unicode normalization
2. Devanagari character handling
3. Special character treatment
4. Compound word support

### **Phase 3: Optimization**
1. Compression ratio tuning
2. Vocabulary size optimization
3. Merge strategy refinement
4. Performance optimization

### **Phase 4: Evaluation**
1. Compression metrics
2. Vocabulary analysis
3. Round-trip testing
4. Real-world examples

## 📈 **Training Process**

```bash
# Step 1: Download corpus (100MB+ Hindi text)
python download_hindi_corpus.py

# Step 2: Train BPE (target: 5500 vocab, 3+ compression)
python train_hindi_bpe.py --vocab-size 5500

# Expected output:
# Iteration 0: vocab=150, compression=1.00
# Iteration 1000: vocab=1150, compression=1.80
# Iteration 2000: vocab=2150, compression=2.35
# Iteration 3000: vocab=3150, compression=2.75
# Iteration 4000: vocab=4150, compression=3.05 ✅
# Iteration 5000: vocab=5150, compression=3.42 ✅
# Final: vocab=5500, compression=3.68 ✅ SUCCESS!

# Step 3: Evaluate
python test_bpe.py

# Step 4: Demo
python demo_hindi_bpe.py
```

## 🔗 **Resources**

### **BPE Resources**
- [Original Paper](https://arxiv.org/abs/1508.07909) - Neural Machine Translation with Subword Units
- [OpenAI GPT-2](https://github.com/openai/gpt-2) - BPE implementation
- [HuggingFace Tokenizers](https://huggingface.co/docs/tokenizers/) - Modern tokenizer library

### **Hindi NLP Resources**
- [Hindi Wikipedia](https://hi.wikipedia.org/) - Large Hindi corpus
- [OSCAR Corpus](https://oscar-corpus.com/) - Multilingual corpus
- [IndicNLP](https://indicnlp.ai4bharat.org/) - Indian language NLP
- [Hindi Word2Vec](https://fasttext.cc/) - Pre-trained embeddings

### **Unicode Resources**
- [Devanagari Unicode](https://unicode.org/charts/PDF/U0900.pdf) - Character reference
- [Unicode Normalization](https://unicode.org/reports/tr15/) - NFC, NFD

## 🎯 **Success Checklist**

- [ ] BPE tokenizer implemented from scratch
- [ ] Hindi corpus downloaded and preprocessed
- [ ] Trained model with vocab_size > 5000
- [ ] Achieved compression ratio ≥ 3.0
- [ ] Encode/decode works correctly
- [ ] Save/load functionality
- [ ] Comprehensive evaluation
- [ ] Demo application
- [ ] Documentation complete
- [ ] Unit tests passing

## 📝 **Assignment Notes**

### **Key Insights**

1. **Compression vs Vocabulary**: Trade-off between coverage and efficiency
2. **Character Importance**: Hindi characters must stay in vocabulary
3. **Merge Strategy**: Frequency-based merging works well
4. **Unicode Handling**: Proper normalization is critical

### **Bonus Points**

- ✅ Indian language (Hindi) - complex script
- ⭐ Handles Unicode complexity
- 🎯 Exceeds requirements (5500+ vocab, 3+ compression)
- 📊 Comprehensive evaluation and analysis

## 🏆 **Expected Achievements**

1. **Vocabulary Size**: 5500-6000 tokens ✅
2. **Compression Ratio**: 3.5-4.0 ✅
3. **Character Coverage**: 100% ✅
4. **Devanagari Support**: Full ✅
5. **Real-world Ready**: Production quality ✅

---

**Let's build the best Hindi BPE tokenizer! 🇮🇳 🚀**

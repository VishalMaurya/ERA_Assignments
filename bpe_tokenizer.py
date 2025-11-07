"""
Hindi BPE Tokenizer - Built from Scratch
========================================

A complete Byte Pair Encoding implementation for Hindi language.
Supports Devanagari script with full Unicode handling.

Author: ERA V4 S10 Assignment
"""

import json
import re
from collections import Counter, defaultdict
from typing import List, Dict, Tuple, Set

# Try to import tqdm, but don't fail if it's not available
try:
    from tqdm import tqdm
    HAS_TQDM = True
except ImportError:
    HAS_TQDM = False
    # Simple fallback for tqdm
    def tqdm(iterable, desc='', **kwargs):
        return iterable


class HindiBPETokenizer:
    """
    Byte Pair Encoding tokenizer for Hindi (Devanagari script).
    
    Features:
    - Train from scratch on Hindi corpus
    - Encode/decode Hindi text
    - Save/load trained models
    - Track compression ratio
    - Handle Unicode properly
    """
    
    def __init__(self):
        self.vocab = {}  # token -> id
        self.reverse_vocab = {}  # id -> token
        self.merges = []  # List of (pair, merged_token) tuples
        self.word_freqs = {}  # word -> frequency
        self.compression_stats = {}
        
    def _get_words_from_corpus(self, corpus_text: str) -> Dict[str, int]:
        """
        Extract words and their frequencies from corpus.
        
        Args:
            corpus_text: Raw Hindi text
            
        Returns:
            Dictionary of word -> frequency
        """
        # Split by whitespace and punctuation, but keep them
        # Use Unicode word boundaries for Hindi
        words = re.findall(r'\S+', corpus_text)
        
        # Count word frequencies
        word_freqs = Counter(words)
        
        print(f"📊 Found {len(word_freqs)} unique words")
        print(f"📊 Total words: {sum(word_freqs.values())}")
        
        return dict(word_freqs)
    
    def _get_characters(self, word_freqs: Dict[str, int]) -> Set[str]:
        """
        Extract all unique characters from the corpus.
        
        Args:
            word_freqs: Word frequency dictionary
            
        Returns:
            Set of unique characters
        """
        chars = set()
        for word in word_freqs.keys():
            chars.update(list(word))
        
        print(f"📊 Found {len(chars)} unique characters")
        return chars
    
    def _get_pair_frequencies(self, splits: Dict[str, List[str]], 
                              word_freqs: Dict[str, int]) -> Dict[Tuple[str, str], int]:
        """
        Count frequency of all adjacent token pairs.
        
        Args:
            splits: Current word splits {word: [tokens]}
            word_freqs: Word frequencies
            
        Returns:
            Dictionary of (token1, token2) -> frequency
        """
        pair_freqs = defaultdict(int)
        
        for word, freq in word_freqs.items():
            split = splits[word]
            if len(split) < 2:
                continue
                
            # Count all adjacent pairs
            for i in range(len(split) - 1):
                pair = (split[i], split[i + 1])
                pair_freqs[pair] += freq
        
        return dict(pair_freqs)
    
    def _merge_pair(self, pair: Tuple[str, str], splits: Dict[str, List[str]],
                   word_freqs: Dict[str, int]) -> Dict[str, List[str]]:
        """
        Merge a specific pair in all word splits.
        
        Args:
            pair: Pair to merge (token1, token2)
            splits: Current word splits
            word_freqs: Word frequencies
            
        Returns:
            Updated splits with merged pair
        """
        new_splits = {}
        merged_token = pair[0] + pair[1]
        
        for word in word_freqs.keys():
            split = splits[word]
            if len(split) < 2:
                new_splits[word] = split
                continue
            
            # Merge the pair
            new_split = []
            i = 0
            while i < len(split):
                if i < len(split) - 1 and split[i] == pair[0] and split[i + 1] == pair[1]:
                    new_split.append(merged_token)
                    i += 2
                else:
                    new_split.append(split[i])
                    i += 1
            
            new_splits[word] = new_split
        
        return new_splits
    
    def _calculate_compression_ratio(self, splits: Dict[str, List[str]],
                                     word_freqs: Dict[str, int]) -> float:
        """
        Calculate current compression ratio.
        
        Args:
            splits: Current word splits
            word_freqs: Word frequencies
            
        Returns:
            Compression ratio (original_tokens / current_tokens)
        """
        # Count original character-level tokens
        original_tokens = sum(len(word) * freq for word, freq in word_freqs.items())
        
        # Count current tokens after merging
        current_tokens = sum(len(splits[word]) * freq for word, freq in word_freqs.items())
        
        if current_tokens == 0:
            return 1.0
        
        return original_tokens / current_tokens
    
    def train(self, corpus_text: str, vocab_size: int = 5500, 
             min_frequency: int = 2, verbose: bool = True) -> Dict:
        """
        Train BPE tokenizer on Hindi corpus.
        
        Args:
            corpus_text: Hindi text corpus
            vocab_size: Target vocabulary size (must be > 5000)
            min_frequency: Minimum frequency for merging pairs
            verbose: Print progress
            
        Returns:
            Training statistics
        """
        if vocab_size <= 5000:
            print(f"⚠️  Warning: vocab_size should be > 5000 (got {vocab_size})")
        
        print(f"\n🚀 Starting BPE Training")
        print(f"🎯 Target vocabulary size: {vocab_size}")
        print(f"🎯 Minimum pair frequency: {min_frequency}")
        print(f"📝 Corpus size: {len(corpus_text)} characters")
        
        # Step 1: Extract words and frequencies
        print("\n📖 Step 1: Extracting words from corpus...")
        self.word_freqs = self._get_words_from_corpus(corpus_text)
        
        # Step 2: Initialize with character-level splits
        print("\n🔤 Step 2: Initializing character-level vocabulary...")
        chars = self._get_characters(self.word_freqs)
        
        # Initialize splits (each word split into characters)
        splits = {word: list(word) for word in self.word_freqs.keys()}
        
        # Initialize vocabulary with characters
        self.vocab = {char: idx for idx, char in enumerate(sorted(chars))}
        base_vocab_size = len(self.vocab)
        
        print(f"✅ Base vocabulary: {base_vocab_size} characters")
        
        # Calculate initial compression
        initial_compression = self._calculate_compression_ratio(splits, self.word_freqs)
        print(f"📊 Initial compression ratio: {initial_compression:.2f}")
        
        # Step 3: Iteratively merge most frequent pairs
        print(f"\n🔄 Step 3: Merging pairs (target: {vocab_size - base_vocab_size} merges)...")
        
        num_merges = vocab_size - base_vocab_size
        compression_history = []
        
        progress_bar = tqdm(range(num_merges), desc="Training BPE") if verbose else range(num_merges)
        
        for iteration in progress_bar:
            # Get pair frequencies
            pair_freqs = self._get_pair_frequencies(splits, self.word_freqs)
            
            if not pair_freqs:
                print(f"\n⚠️  No more pairs to merge at iteration {iteration}")
                break
            
            # Filter by minimum frequency
            pair_freqs = {pair: freq for pair, freq in pair_freqs.items() 
                         if freq >= min_frequency}
            
            if not pair_freqs:
                print(f"\n⚠️  No pairs above min_frequency at iteration {iteration}")
                break
            
            # Find most frequent pair
            best_pair = max(pair_freqs, key=pair_freqs.get)
            
            # Merge this pair
            splits = self._merge_pair(best_pair, splits, self.word_freqs)
            
            # Add merged token to vocabulary
            merged_token = best_pair[0] + best_pair[1]
            self.vocab[merged_token] = len(self.vocab)
            self.merges.append(best_pair)
            
            # Track compression
            if iteration % 500 == 0 or iteration == num_merges - 1:
                compression = self._calculate_compression_ratio(splits, self.word_freqs)
                compression_history.append({
                    'iteration': iteration,
                    'vocab_size': len(self.vocab),
                    'compression_ratio': compression,
                    'best_pair': best_pair,
                    'pair_freq': pair_freqs[best_pair]
                })
                
                if verbose:
                    progress_bar.set_postfix({
                        'vocab': len(self.vocab),
                        'compression': f"{compression:.2f}",
                        'pair_freq': pair_freqs[best_pair]
                    })
        
        # Build reverse vocabulary
        self.reverse_vocab = {idx: token for token, idx in self.vocab.items()}
        
        # Final statistics
        final_compression = self._calculate_compression_ratio(splits, self.word_freqs)
        
        self.compression_stats = {
            'initial_compression': initial_compression,
            'final_compression': final_compression,
            'compression_history': compression_history,
            'base_vocab_size': base_vocab_size,
            'final_vocab_size': len(self.vocab),
            'num_merges': len(self.merges),
            'total_words': len(self.word_freqs),
            'corpus_size': len(corpus_text)
        }
        
        # Print results
        print(f"\n{'='*60}")
        print(f"✅ Training Complete!")
        print(f"{'='*60}")
        print(f"📊 Final vocabulary size: {len(self.vocab)}")
        print(f"📊 Number of merges: {len(self.merges)}")
        print(f"📊 Initial compression: {initial_compression:.2f}x")
        print(f"📊 Final compression: {final_compression:.2f}x")
        print(f"{'='*60}")
        
        # Check requirements
        if len(self.vocab) > 5000:
            print(f"✅ Vocabulary size > 5000: PASSED ({len(self.vocab)})")
        else:
            print(f"❌ Vocabulary size > 5000: FAILED ({len(self.vocab)})")
        
        if final_compression >= 3.0:
            print(f"✅ Compression ratio ≥ 3.0: PASSED ({final_compression:.2f})")
        else:
            print(f"❌ Compression ratio ≥ 3.0: FAILED ({final_compression:.2f})")
        print(f"{'='*60}\n")
        
        return self.compression_stats
    
    def encode(self, text: str) -> List[int]:
        """
        Encode text to token IDs using trained BPE.
        
        Args:
            text: Hindi text to encode
            
        Returns:
            List of token IDs
        """
        if not self.vocab:
            raise ValueError("Tokenizer not trained! Call train() first.")
        
        # Split text into words
        words = re.findall(r'\S+', text)
        
        token_ids = []
        
        for word in words:
            # Start with character-level split
            split = list(word)
            
            # Apply merges in order
            for pair in self.merges:
                if len(split) < 2:
                    break
                
                new_split = []
                i = 0
                while i < len(split):
                    if i < len(split) - 1 and split[i] == pair[0] and split[i + 1] == pair[1]:
                        merged = pair[0] + pair[1]
                        new_split.append(merged)
                        i += 2
                    else:
                        new_split.append(split[i])
                        i += 1
                
                split = new_split
            
            # Convert tokens to IDs
            for token in split:
                if token in self.vocab:
                    token_ids.append(self.vocab[token])
                else:
                    # Unknown token - split into characters
                    for char in token:
                        if char in self.vocab:
                            token_ids.append(self.vocab[char])
                        else:
                            # Truly unknown character - use special token or skip
                            pass
        
        return token_ids
    
    def decode(self, token_ids: List[int]) -> str:
        """
        Decode token IDs back to text.
        
        Args:
            token_ids: List of token IDs
            
        Returns:
            Decoded Hindi text
        """
        if not self.reverse_vocab:
            raise ValueError("Tokenizer not trained! Call train() first.")
        
        tokens = [self.reverse_vocab.get(tid, '') for tid in token_ids]
        return ''.join(tokens)
    
    def save(self, filepath: str):
        """
        Save trained tokenizer to file.
        
        Args:
            filepath: Path to save JSON file
        """
        data = {
            'vocab': self.vocab,
            'merges': [(pair[0], pair[1]) for pair in self.merges],
            'compression_stats': self.compression_stats
        }
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        print(f"💾 Model saved to: {filepath}")
    
    def load(self, filepath: str):
        """
        Load trained tokenizer from file.
        
        Args:
            filepath: Path to JSON file
        """
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        self.vocab = data['vocab']
        self.merges = [(pair[0], pair[1]) for pair in data['merges']]
        self.compression_stats = data.get('compression_stats', {})
        self.reverse_vocab = {idx: token for token, idx in self.vocab.items()}
        
        print(f"📂 Model loaded from: {filepath}")
        print(f"📊 Vocabulary size: {len(self.vocab)}")
        print(f"📊 Number of merges: {len(self.merges)}")
        if self.compression_stats:
            print(f"📊 Compression ratio: {self.compression_stats.get('final_compression', 'N/A'):.2f}")
    
    def get_stats(self) -> Dict:
        """
        Get tokenizer statistics.
        
        Returns:
            Dictionary of statistics
        """
        return {
            'vocab_size': len(self.vocab),
            'num_merges': len(self.merges),
            'compression_ratio': self.compression_stats.get('final_compression', 0),
            'base_vocab_size': self.compression_stats.get('base_vocab_size', 0),
        }
    
    def tokenize_text(self, text: str) -> List[str]:
        """
        Tokenize text and return tokens (not IDs).
        
        Args:
            text: Hindi text to tokenize
            
        Returns:
            List of tokens
        """
        token_ids = self.encode(text)
        return [self.reverse_vocab[tid] for tid in token_ids if tid in self.reverse_vocab]


if __name__ == "__main__":
    # Quick test
    print("🧪 Testing Hindi BPE Tokenizer")
    print("="*60)
    
    # Sample Hindi corpus
    sample_corpus = """
    नमस्ते नमस्ते नमस्ते
    भारत एक महान देश है
    हिन्दी भारत की राजभाषा है
    दिल्ली भारत की राजधानी है
    मुंबई महाराष्ट्र की राजधानी है
    """ * 100  # Repeat for better training
    
    # Initialize and train
    tokenizer = HindiBPETokenizer()
    stats = tokenizer.train(sample_corpus, vocab_size=300, verbose=True)
    
    # Test encoding/decoding
    test_text = "नमस्ते भारत"
    print(f"\n🧪 Testing encoding/decoding:")
    print(f"Original: {test_text}")
    
    encoded = tokenizer.encode(test_text)
    print(f"Encoded: {encoded}")
    
    decoded = tokenizer.decode(encoded)
    print(f"Decoded: {decoded}")
    
    # Save model
    tokenizer.save("test_model.json")
    
    print("\n✅ Test complete!")


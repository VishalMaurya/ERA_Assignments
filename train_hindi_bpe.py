"""
Train Hindi BPE Tokenizer
=========================

Train a BPE tokenizer on Hindi corpus to meet assignment requirements:
- Vocabulary size > 5000
- Compression ratio ≥ 3.0
"""

import argparse
import json
from pathlib import Path
from datetime import datetime
from bpe_tokenizer import HindiBPETokenizer


def load_corpus(corpus_file: str) -> str:
    """Load Hindi corpus from file."""
    print(f"📂 Loading corpus from: {corpus_file}")
    
    with open(corpus_file, 'r', encoding='utf-8') as f:
        corpus = f.read()
    
    print(f"✅ Corpus loaded: {len(corpus)} characters")
    print(f"📊 Corpus size: {len(corpus) / 1024:.1f} KB")
    
    return corpus


def save_stats(stats: dict, output_dir: str):
    """Save training statistics."""
    output_path = Path(output_dir) / 'training_stats.json'
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(stats, f, indent=2, ensure_ascii=False)
    
    print(f"📊 Statistics saved to: {output_path}")


def print_compression_history(stats: dict):
    """Print compression ratio history."""
    print("\n" + "="*80)
    print("📈 Compression History")
    print("="*80)
    print(f"{'Iteration':<12} {'Vocab Size':<12} {'Compression':<15} {'Best Pair':<30} {'Frequency':<12}")
    print("-"*80)
    
    history = stats.get('compression_history', [])
    
    for entry in history:
        iteration = entry['iteration']
        vocab_size = entry['vocab_size']
        compression = entry['compression_ratio']
        best_pair = f"({entry['best_pair'][0][:10]}, {entry['best_pair'][1][:10]})"
        freq = entry['pair_freq']
        
        # Highlight when compression >= 3.0
        marker = "✅" if compression >= 3.0 else "  "
        
        print(f"{marker} {iteration:<10} {vocab_size:<12} {compression:<15.2f} {best_pair:<30} {freq:<12}")
    
    print("="*80)


def analyze_vocabulary(tokenizer: HindiBPETokenizer, output_dir: str):
    """Analyze and save vocabulary statistics."""
    vocab = tokenizer.vocab
    
    print("\n" + "="*60)
    print("📊 Vocabulary Analysis")
    print("="*60)
    
    # Categorize tokens
    single_chars = [t for t in vocab.keys() if len(t) == 1]
    two_chars = [t for t in vocab.keys() if len(t) == 2]
    three_chars = [t for t in vocab.keys() if len(t) == 3]
    four_plus = [t for t in vocab.keys() if len(t) >= 4]
    
    print(f"Single character tokens: {len(single_chars)}")
    print(f"Two character tokens: {len(two_chars)}")
    print(f"Three character tokens: {len(three_chars)}")
    print(f"Four+ character tokens: {len(four_plus)}")
    print(f"Total vocabulary: {len(vocab)}")
    
    # Show longest tokens
    longest_tokens = sorted(vocab.keys(), key=len, reverse=True)[:20]
    print(f"\n🏆 Top 20 Longest Tokens:")
    for i, token in enumerate(longest_tokens, 1):
        print(f"  {i:2d}. '{token}' (length: {len(token)})")
    
    # Save analysis
    analysis = {
        'vocab_size': len(vocab),
        'single_char': len(single_chars),
        'two_char': len(two_chars),
        'three_char': len(three_chars),
        'four_plus': len(four_plus),
        'longest_tokens': longest_tokens[:50],
        'sample_tokens': list(vocab.keys())[:100]
    }
    
    output_path = Path(output_dir) / 'vocabulary_analysis.json'
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(analysis, f, indent=2, ensure_ascii=False)
    
    print(f"\n💾 Analysis saved to: {output_path}")
    print("="*60)


def test_tokenizer(tokenizer: HindiBPETokenizer):
    """Test tokenizer with sample texts."""
    print("\n" + "="*60)
    print("🧪 Testing Tokenizer")
    print("="*60)
    
    test_cases = [
        "नमस्ते, मेरा नाम राज है।",
        "भारत एक महान देश है।",
        "हिन्दी भाषा बहुत सुंदर है।",
        "मुंबई भारत का सबसे बड़ा शहर है।",
        "क्रिकेट भारत का लोकप्रिय खेल है।"
    ]
    
    for i, text in enumerate(test_cases, 1):
        print(f"\nTest {i}: {text}")
        
        # Encode
        token_ids = tokenizer.encode(text)
        tokens = tokenizer.tokenize_text(text)
        
        # Calculate compression
        original_chars = len(text)
        num_tokens = len(token_ids)
        compression = original_chars / num_tokens if num_tokens > 0 else 0
        
        print(f"  Characters: {original_chars}")
        print(f"  Tokens: {num_tokens}")
        print(f"  Compression: {compression:.2f}x")
        print(f"  Token IDs: {token_ids[:10]}{'...' if len(token_ids) > 10 else ''}")
        print(f"  Tokens: {tokens[:5]}{'...' if len(tokens) > 5 else ''}")
        
        # Decode
        decoded = tokenizer.decode(token_ids)
        match = "✅" if decoded == text else "❌"
        print(f"  Decode match: {match}")
        if decoded != text:
            print(f"  Original: {text}")
            print(f"  Decoded:  {decoded}")
    
    print("="*60)


def main():
    parser = argparse.ArgumentParser(description='Train Hindi BPE Tokenizer')
    parser.add_argument('--corpus', type=str, default='data/hindi_corpus.txt',
                       help='Path to Hindi corpus file')
    parser.add_argument('--vocab-size', type=int, default=5500,
                       help='Target vocabulary size (must be > 5000)')
    parser.add_argument('--min-frequency', type=int, default=2,
                       help='Minimum frequency for merging pairs')
    parser.add_argument('--output-dir', type=str, default='models',
                       help='Output directory for trained model')
    parser.add_argument('--model-name', type=str, default='',
                       help='Model name (default: hindi_bpe_{vocab_size})')
    
    args = parser.parse_args()
    
    # Validate arguments
    if args.vocab_size <= 5000:
        print(f"⚠️  Warning: vocab_size should be > 5000 (got {args.vocab_size})")
        print(f"⚠️  Continuing anyway, but assignment requires > 5000")
    
    # Set model name
    if not args.model_name:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        args.model_name = f"hindi_bpe_{args.vocab_size}_{timestamp}"
    
    print("="*80)
    print("🚀 Hindi BPE Tokenizer Training")
    print("="*80)
    print(f"📝 Corpus: {args.corpus}")
    print(f"🎯 Target vocabulary size: {args.vocab_size}")
    print(f"🎯 Minimum pair frequency: {args.min_frequency}")
    print(f"📁 Output directory: {args.output_dir}")
    print(f"🏷️  Model name: {args.model_name}")
    print("="*80)
    
    # Load corpus
    try:
        corpus = load_corpus(args.corpus)
    except FileNotFoundError:
        print(f"\n❌ Corpus file not found: {args.corpus}")
        print(f"\n💡 Please run: python download_hindi_corpus.py")
        return
    
    # Initialize tokenizer
    print("\n🔧 Initializing tokenizer...")
    tokenizer = HindiBPETokenizer()
    
    # Train
    print("\n🏋️  Training tokenizer...")
    stats = tokenizer.train(
        corpus_text=corpus,
        vocab_size=args.vocab_size,
        min_frequency=args.min_frequency,
        verbose=True
    )
    
    # Save model
    model_path = Path(args.output_dir) / f"{args.model_name}.json"
    model_path.parent.mkdir(parents=True, exist_ok=True)
    tokenizer.save(str(model_path))
    
    # Save statistics
    save_stats(stats, args.output_dir)
    
    # Print compression history
    print_compression_history(stats)
    
    # Analyze vocabulary
    analyze_vocabulary(tokenizer, args.output_dir)
    
    # Test tokenizer
    test_tokenizer(tokenizer)
    
    # Final summary
    print("\n" + "="*80)
    print("🎉 Training Complete!")
    print("="*80)
    print(f"✅ Model saved to: {model_path}")
    print(f"✅ Vocabulary size: {len(tokenizer.vocab)}")
    print(f"✅ Compression ratio: {stats['final_compression']:.2f}x")
    print(f"✅ Number of merges: {len(tokenizer.merges)}")
    print("\n📊 Assignment Requirements:")
    print(f"  Vocabulary > 5000: {'✅ PASSED' if len(tokenizer.vocab) > 5000 else '❌ FAILED'} ({len(tokenizer.vocab)})")
    print(f"  Compression ≥ 3.0: {'✅ PASSED' if stats['final_compression'] >= 3.0 else '❌ FAILED'} ({stats['final_compression']:.2f}x)")
    print("\n🚀 Next steps:")
    print(f"  1. Test: python test_bpe.py --model {model_path}")
    print(f"  2. Demo: python demo_hindi_bpe.py --model {model_path}")
    print("="*80)


if __name__ == "__main__":
    main()


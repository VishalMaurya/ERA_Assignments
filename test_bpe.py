"""
Test Hindi BPE Tokenizer
========================

Comprehensive testing and evaluation of trained BPE tokenizer.
"""

import argparse
import json
from pathlib import Path
from bpe_tokenizer import HindiBPETokenizer


def load_model(model_path: str) -> HindiBPETokenizer:
    """Load trained tokenizer."""
    print(f"📂 Loading model from: {model_path}")
    
    tokenizer = HindiBPETokenizer()
    tokenizer.load(model_path)
    
    return tokenizer


def test_encode_decode(tokenizer: HindiBPETokenizer):
    """Test encoding and decoding."""
    print("\n" + "="*80)
    print("🧪 Test 1: Encode/Decode Round-Trip")
    print("="*80)
    
    test_texts = [
        "नमस्ते",
        "भारत एक महान देश है",
        "हिन्दी भाषा बहुत सुंदर है",
        "मुंबई भारत का सबसे बड़ा शहर है",
        "क्रिकेट भारत का लोकप्रिय खेल है",
        "ताजमहल आगरा में स्थित है",
        "गांधी जी भारत के राष्ट्रपिता हैं",
        "दिल्ली भारत की राजधानी है",
        "मैं हिन्दी सीख रहा हूं",
        "यह एक परीक्षा वाक्य है।"
    ]
    
    passed = 0
    failed = 0
    
    for i, text in enumerate(test_texts, 1):
        encoded = tokenizer.encode(text)
        decoded = tokenizer.decode(encoded)
        
        match = decoded == text
        status = "✅ PASS" if match else "❌ FAIL"
        
        print(f"\n{i}. {status}")
        print(f"   Original:  {text}")
        print(f"   Encoded:   {encoded[:10]}{'...' if len(encoded) > 10 else ''} ({len(encoded)} tokens)")
        print(f"   Decoded:   {decoded}")
        
        if match:
            passed += 1
        else:
            failed += 1
            print(f"   ⚠️  Mismatch detected!")
    
    print(f"\n📊 Results: {passed}/{len(test_texts)} passed, {failed}/{len(test_texts)} failed")
    print("="*80)


def test_compression(tokenizer: HindiBPETokenizer):
    """Test compression ratio."""
    print("\n" + "="*80)
    print("🧪 Test 2: Compression Ratio Analysis")
    print("="*80)
    
    test_texts = [
        "नमस्ते नमस्ते नमस्ते नमस्ते नमस्ते",
        "भारत भारत भारत भारत भारत",
        "हिन्दी भाषा बहुत सुंदर है और मुझे हिन्दी बहुत पसंद है",
        "मुंबई, दिल्ली, कोलकाता, चेन्नई भारत के बड़े शहर हैं",
        "क्रिकेट, हॉकी, फुटबॉल, बैडमिंटन लोकप्रिय खेल हैं"
    ]
    
    compressions = []
    
    for i, text in enumerate(test_texts, 1):
        char_count = len(text)
        tokens = tokenizer.encode(text)
        token_count = len(tokens)
        compression = char_count / token_count if token_count > 0 else 0
        
        compressions.append(compression)
        
        print(f"\n{i}. Text: {text[:50]}{'...' if len(text) > 50 else ''}")
        print(f"   Characters: {char_count}")
        print(f"   Tokens: {token_count}")
        print(f"   Compression: {compression:.2f}x")
        
        status = "✅" if compression >= 3.0 else "⚠️ "
        print(f"   Status: {status} ({'PASS' if compression >= 3.0 else 'Below target'})")
    
    avg_compression = sum(compressions) / len(compressions)
    print(f"\n📊 Average compression: {avg_compression:.2f}x")
    print(f"📊 Min compression: {min(compressions):.2f}x")
    print(f"📊 Max compression: {max(compressions):.2f}x")
    
    target_met = avg_compression >= 3.0
    print(f"\n🎯 Target (≥3.0x): {'✅ MET' if target_met else '❌ NOT MET'}")
    print("="*80)


def test_vocabulary_coverage(tokenizer: HindiBPETokenizer):
    """Test vocabulary coverage."""
    print("\n" + "="*80)
    print("🧪 Test 3: Vocabulary Coverage")
    print("="*80)
    
    vocab_size = len(tokenizer.vocab)
    print(f"📊 Vocabulary size: {vocab_size}")
    print(f"🎯 Target: > 5000")
    print(f"🎯 Status: {'✅ PASSED' if vocab_size > 5000 else '❌ FAILED'}")
    
    # Analyze vocabulary composition
    chars = [t for t in tokenizer.vocab.keys() if len(t) == 1]
    subwords = [t for t in tokenizer.vocab.keys() if 2 <= len(t) <= 3]
    words = [t for t in tokenizer.vocab.keys() if len(t) >= 4]
    
    print(f"\n📊 Vocabulary Breakdown:")
    print(f"   Single characters: {len(chars)} ({len(chars)/vocab_size*100:.1f}%)")
    print(f"   Subwords (2-3 chars): {len(subwords)} ({len(subwords)/vocab_size*100:.1f}%)")
    print(f"   Words (4+ chars): {len(words)} ({len(words)/vocab_size*100:.1f}%)")
    
    print(f"\n🔤 Sample characters (first 20):")
    print(f"   {' '.join(chars[:20])}")
    
    print(f"\n🔡 Sample subwords (first 10):")
    for token in subwords[:10]:
        print(f"   '{token}'")
    
    print(f"\n📝 Sample words (first 10):")
    for token in words[:10]:
        print(f"   '{token}'")
    
    print("="*80)


def test_special_cases(tokenizer: HindiBPETokenizer):
    """Test edge cases and special inputs."""
    print("\n" + "="*80)
    print("🧪 Test 4: Special Cases & Edge Cases")
    print("="*80)
    
    test_cases = [
        ("Empty string", ""),
        ("Single char", "अ"),
        ("Punctuation", "।"),
        ("Numbers", "१२३४५"),
        ("Mixed", "Hello नमस्ते 123"),
        ("Repeated", "ाााााा"),
        ("Special chars", "ं ः ् ँ"),
    ]
    
    for name, text in test_cases:
        try:
            if not text:
                print(f"\n{name}: [empty]")
                print(f"   Skipped (empty input)")
                continue
            
            encoded = tokenizer.encode(text)
            decoded = tokenizer.decode(encoded)
            
            match = decoded == text
            status = "✅" if match else "❌"
            
            print(f"\n{name}: {text}")
            print(f"   Tokens: {encoded}")
            print(f"   Decoded: {decoded}")
            print(f"   Status: {status}")
            
        except Exception as e:
            print(f"\n{name}: {text}")
            print(f"   ❌ Error: {e}")
    
    print("="*80)


def generate_report(tokenizer: HindiBPETokenizer, output_file: str):
    """Generate comprehensive evaluation report."""
    print("\n📄 Generating evaluation report...")
    
    stats = tokenizer.get_stats()
    
    report = {
        'model_info': {
            'vocab_size': stats['vocab_size'],
            'num_merges': stats['num_merges'],
            'compression_ratio': stats['compression_ratio'],
            'base_vocab_size': stats['base_vocab_size']
        },
        'requirements': {
            'vocab_size_requirement': '> 5000',
            'vocab_size_actual': stats['vocab_size'],
            'vocab_size_passed': stats['vocab_size'] > 5000,
            'compression_requirement': '>= 3.0',
            'compression_actual': stats['compression_ratio'],
            'compression_passed': stats['compression_ratio'] >= 3.0
        },
        'overall_status': (
            stats['vocab_size'] > 5000 and 
            stats['compression_ratio'] >= 3.0
        )
    }
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Report saved to: {output_file}")
    
    return report


def main():
    parser = argparse.ArgumentParser(description='Test Hindi BPE Tokenizer')
    parser.add_argument('--model', type=str, required=True,
                       help='Path to trained model JSON file')
    parser.add_argument('--text', type=str, default='',
                       help='Optional: Test specific text')
    parser.add_argument('--report', type=str, default='results/evaluation_report.json',
                       help='Path to save evaluation report')
    
    args = parser.parse_args()
    
    print("="*80)
    print("🧪 Hindi BPE Tokenizer Testing")
    print("="*80)
    
    # Load model
    tokenizer = load_model(args.model)
    
    # Run tests
    test_encode_decode(tokenizer)
    test_compression(tokenizer)
    test_vocabulary_coverage(tokenizer)
    test_special_cases(tokenizer)
    
    # Test custom text if provided
    if args.text:
        print("\n" + "="*80)
        print("🧪 Custom Text Test")
        print("="*80)
        print(f"Input: {args.text}")
        
        encoded = tokenizer.encode(args.text)
        decoded = tokenizer.decode(encoded)
        tokens = tokenizer.tokenize_text(args.text)
        
        print(f"Tokens: {tokens}")
        print(f"Token IDs: {encoded}")
        print(f"Decoded: {decoded}")
        print(f"Match: {'✅' if decoded == args.text else '❌'}")
        print(f"Compression: {len(args.text) / len(encoded):.2f}x")
        print("="*80)
    
    # Generate report
    report = generate_report(tokenizer, args.report)
    
    # Final summary
    print("\n" + "="*80)
    print("📊 Final Evaluation Summary")
    print("="*80)
    print(f"✅ Vocabulary size: {report['model_info']['vocab_size']}")
    print(f"   Requirement: > 5000")
    print(f"   Status: {'✅ PASSED' if report['requirements']['vocab_size_passed'] else '❌ FAILED'}")
    
    print(f"\n✅ Compression ratio: {report['model_info']['compression_ratio']:.2f}x")
    print(f"   Requirement: >= 3.0")
    print(f"   Status: {'✅ PASSED' if report['requirements']['compression_passed'] else '❌ FAILED'}")
    
    print(f"\n🎯 Overall Assignment Status: {'✅ PASSED' if report['overall_status'] else '❌ FAILED'}")
    print("="*80)


if __name__ == "__main__":
    main()


"""
Download Hindi MC4 Corpus
=========================

Downloads Hindi text from MC4 (Multilingual C4) dataset.
This provides diverse web-crawled Hindi text.
"""

from datasets import load_dataset
import os

def download_mc4_hindi(num_examples=50000, output_file="data/hindi_mc4.txt"):
    """Download Hindi MC4 text."""
    
    print("="*60)
    print("🌐 Downloading Hindi MC4 Corpus")
    print("="*60)
    print(f"📊 Target examples: {num_examples}")
    print(f"📁 Output: {output_file}")
    print("\n⏳ This may take several minutes...")
    print("="*60)
    
    try:
        # Load MC4 Hindi dataset in streaming mode
        print("\n📥 Loading MC4 Hindi dataset...")
        dataset = load_dataset("mc4", "hi", split="train", streaming=True)
        
        print("✅ Dataset loaded! Starting download...")
        
        # Collect texts
        texts = []
        for i, example in enumerate(dataset):
            if i >= num_examples:
                break
            
            text = example.get('text', '')
            if text.strip() and len(text) > 50:  # Filter out very short texts
                texts.append(text.strip())
            
            if (i + 1) % 1000 == 0:
                print(f"  📥 Downloaded: {i+1:,}/{num_examples:,} ({(i+1)/num_examples*100:.1f}%)")
        
        # Join all texts
        corpus = "\n\n".join(texts)
        
        # Save
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(corpus)
        
        # Count unique words
        words = corpus.split()
        unique_words = len(set(words))
        
        print(f"\n{'='*60}")
        print("✅ Download Complete!")
        print(f"{'='*60}")
        print(f"📊 Total examples: {len(texts):,}")
        print(f"📊 Total characters: {len(corpus):,}")
        print(f"📊 Total words: {len(words):,}")
        print(f"📊 Unique words: {unique_words:,}")
        print(f"📊 File size: {len(corpus)/1024/1024:.2f} MB")
        print(f"💾 Saved to: {output_file}")
        print(f"{'='*60}")
        
        return corpus
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        return None

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser()
    parser.add_argument('--num-examples', type=int, default=50000,
                       help='Number of examples to download')
    parser.add_argument('--output', type=str, default='data/hindi_mc4.txt',
                       help='Output file path')
    
    args = parser.parse_args()
    
    corpus = download_mc4_hindi(args.num_examples, args.output)
    
    if corpus:
        print("\n🚀 Next step: Train BPE")
        print(f"   python train_hindi_bpe.py --corpus {args.output} --vocab-size 6000 --min-frequency 2")
    else:
        print("\n❌ Failed to download corpus")


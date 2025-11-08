"""
Download Hindi Wikipedia Corpus
================================

Downloads Hindi text from Wikipedia using the datasets library.
This provides a much more diverse vocabulary for BPE training.
"""

from datasets import load_dataset
import os

def download_wikipedia_hindi(num_examples=50000, output_file="data/hindi_wikipedia.txt"):
    """Download Hindi Wikipedia text."""
    
    print("="*60)
    print("📚 Downloading Hindi Wikipedia Corpus")
    print("="*60)
    print(f"📊 Target examples: {num_examples}")
    print(f"📁 Output: {output_file}")
    print("\n⏳ This may take several minutes...")
    print("="*60)
    
    try:
        # Load Wikipedia Hindi dataset
        print("\n📥 Loading Wikipedia dataset...")
        dataset = load_dataset("wikipedia", "20220301.hi", split="train", trust_remote_code=True)
        
        print(f"✅ Dataset loaded! Total articles: {len(dataset)}")
        
        # Collect texts
        texts = []
        max_examples = min(num_examples, len(dataset))
        
        print(f"📥 Extracting {max_examples} articles...")
        
        for i in range(max_examples):
            text = dataset[i].get('text', '')
            if text.strip():
                texts.append(text.strip())
            
            if (i + 1) % 1000 == 0:
                print(f"  📥 Processed: {i+1:,}/{max_examples:,} ({(i+1)/max_examples*100:.1f}%)")
        
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
        print(f"📊 Total articles: {len(texts):,}")
        print(f"📊 Total characters: {len(corpus):,}")
        print(f"📊 Total words: {len(words):,}")
        print(f"📊 Unique words: {unique_words:,}")
        print(f"📊 File size: {len(corpus)/1024/1024:.2f} MB")
        print(f"💾 Saved to: {output_file}")
        print(f"{'='*60}")
        
        return corpus
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\n💡 Trying alternative method...")
        return None

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser()
    parser.add_argument('--num-examples', type=int, default=10000,
                       help='Number of articles to download')
    parser.add_argument('--output', type=str, default='data/hindi_wikipedia.txt',
                       help='Output file path')
    
    args = parser.parse_args()
    
    corpus = download_wikipedia_hindi(args.num_examples, args.output)
    
    if corpus:
        print("\n🚀 Next step: Train BPE")
        print(f"   python train_hindi_bpe.py --corpus {args.output} --vocab-size 6000")
    else:
        print("\n❌ Failed to download corpus")


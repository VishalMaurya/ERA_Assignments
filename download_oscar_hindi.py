"""
Download Real Hindi Corpus from OSCAR
====================================

Downloads actual Hindi text from OSCAR dataset which has
enough diversity to train a 5000+ vocabulary BPE tokenizer.
"""

from datasets import load_dataset
import os

def download_oscar_hindi(num_examples=100000, output_file="data/hindi_oscar.txt"):
    """Download Hindi text from OSCAR dataset."""
    
    print("="*60)
    print("🌐 Downloading Hindi OSCAR Corpus")
    print("="*60)
    print(f"📊 Target examples: {num_examples}")
    print(f"📁 Output: {output_file}")
    print("\n⏳ This may take several minutes...")
    print("="*60)
    
    try:
        # Load OSCAR Hindi dataset in streaming mode
        print("\n📥 Loading OSCAR dataset...")
        dataset = load_dataset("oscar-corpus/OSCAR-2301", "hi", split="train", streaming=True, trust_remote_code=True)
        
        print("✅ Dataset loaded! Starting download...")
        
        # Collect texts
        texts = []
        for i, example in enumerate(dataset):
            if i >= num_examples:
                break
            
            text = example.get('text', '')
            if text.strip():
                texts.append(text.strip())
            
            if (i + 1) % 1000 == 0:
                print(f"  📥 Downloaded: {i+1:,}/{num_examples:,} ({(i+1)/num_examples*100:.1f}%)")
        
        # Join all texts
        corpus = "\n\n".join(texts)
        
        # Save
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(corpus)
        
        print(f"\n{'='*60}")
        print("✅ Download Complete!")
        print(f"{'='*60}")
        print(f"📊 Total examples: {len(texts):,}")
        print(f"📊 Total characters: {len(corpus):,}")
        print(f"📊 File size: {len(corpus)/1024/1024:.2f} MB")
        print(f"💾 Saved to: {output_file}")
        print(f"{'='*60}")
        
        return corpus
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\n💡 Fallback: Using enhanced local corpus...")
        return None

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser()
    parser.add_argument('--num-examples', type=int, default=100000,
                       help='Number of examples to download')
    parser.add_argument('--output', type=str, default='data/hindi_oscar.txt',
                       help='Output file path')
    
    args = parser.parse_args()
    
    download_oscar_hindi(args.num_examples, args.output)
    
    print("\n🚀 Next step: Train BPE")
    print(f"   python train_hindi_bpe.py --corpus {args.output} --vocab-size 6000")


"""
Download Hindi Corpus from AI4Bharat
=====================================

Downloads Hindi text from AI4Bharat's datasets:
- ai4bharat/IndicParaphrase (Hindi paraphrase dataset)
- ai4bharat/sangraha (Large-scale Indian language corpus)

These datasets provide diverse vocabulary for BPE training.
"""

from datasets import load_dataset
import os

def download_indic_paraphrase(num_examples=50000, output_file="data/hindi_indic.txt"):
    """Download Hindi text from IndicParaphrase dataset."""
    
    print("="*60)
    print("🇮🇳 Downloading AI4Bharat Hindi Corpus")
    print("="*60)
    print(f"📊 Target examples: {num_examples}")
    print(f"📁 Output: {output_file}")
    print("\n⏳ This may take several minutes...")
    print("="*60)
    
    try:
        # Try IndicParaphrase first
        print("\n📥 Trying IndicParaphrase dataset...")
        dataset = load_dataset("ai4bharat/IndicParaphrase", "hi", split="train")
        
        print(f"✅ Dataset loaded! Total examples: {len(dataset)}")
        
        # Collect texts
        texts = []
        max_examples = min(num_examples, len(dataset))
        
        print(f"📥 Extracting {max_examples} examples...")
        
        for i in range(max_examples):
            # Get both source and target for more diversity
            source = dataset[i].get('source', '')
            target = dataset[i].get('target', '')
            
            if source.strip():
                texts.append(source.strip())
            if target.strip() and target != source:
                texts.append(target.strip())
            
            if (i + 1) % 5000 == 0:
                print(f"  📥 Processed: {i+1:,}/{max_examples:,} ({(i+1)/max_examples*100:.1f}%)")
        
        # Join all texts
        corpus = "\n".join(texts)
        
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
        print(f"📊 Total texts: {len(texts):,}")
        print(f"📊 Total characters: {len(corpus):,}")
        print(f"📊 Total words: {len(words):,}")
        print(f"📊 Unique words: {unique_words:,}")
        print(f"📊 File size: {len(corpus)/1024/1024:.2f} MB")
        print(f"💾 Saved to: {output_file}")
        print(f"{'='*60}")
        
        return corpus
        
    except Exception as e:
        print(f"\n❌ Error with IndicParaphrase: {e}")
        print("\n💡 Trying alternative datasets...")
        
    # Try other datasets
    alternative_datasets = [
        ("facebook/flores", "hin_Deva", "dev"),
        ("csebuetnlp/xlsum", "hindi", "train"),
    ]
    
    for dataset_name, config, split in alternative_datasets:
        try:
            print(f"\n📥 Trying {dataset_name}...")
            dataset = load_dataset(dataset_name, config, split=split)
            
            print(f"✅ Dataset loaded! Total examples: {len(dataset)}")
            
            texts = []
            max_examples = min(num_examples, len(dataset))
            
            for i in range(max_examples):
                text = dataset[i].get('text', '') or dataset[i].get('translation', {}).get('hin_Deva', '')
                if text.strip():
                    texts.append(text.strip())
                
                if (i + 1) % 1000 == 0:
                    print(f"  📥 Processed: {i+1:,}/{max_examples:,}")
            
            # Join and save
            corpus = "\n".join(texts)
            
            os.makedirs(os.path.dirname(output_file), exist_ok=True)
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(corpus)
            
            # Count unique words
            words = corpus.split()
            unique_words = len(set(words))
            
            print(f"\n{'='*60}")
            print("✅ Download Complete!")
            print(f"{'='*60}")
            print(f"📊 Dataset: {dataset_name}")
            print(f"📊 Total texts: {len(texts):,}")
            print(f"📊 Total words: {len(words):,}")
            print(f"📊 Unique words: {unique_words:,}")
            print(f"📊 File size: {len(corpus)/1024/1024:.2f} MB")
            print(f"💾 Saved to: {output_file}")
            print(f"{'='*60}")
            
            return corpus
            
        except Exception as e2:
            print(f"❌ Error with {dataset_name}: {e2}")
            continue
    
    print("\n❌ All download attempts failed")
    return None

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser()
    parser.add_argument('--num-examples', type=int, default=50000,
                       help='Number of examples to download')
    parser.add_argument('--output', type=str, default='data/hindi_indic.txt',
                       help='Output file path')
    
    args = parser.parse_args()
    
    corpus = download_indic_paraphrase(args.num_examples, args.output)
    
    if corpus:
        print("\n🚀 Next step: Train BPE")
        print(f"   python train_hindi_bpe.py --corpus {args.output} --vocab-size 6000 --min-frequency 2")
    else:
        print("\n❌ Failed to download corpus")
        print("💡 Consider manually downloading from:")
        print("   - https://huggingface.co/datasets/ai4bharat/IndicParaphrase")
        print("   - https://indicnlp.ai4bharat.org/corpora/")


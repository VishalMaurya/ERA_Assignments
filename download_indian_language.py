"""
Download Indian Language Corpus
================================

Tries to download diverse text from various Indian languages.
Uses datasets in Parquet format (not deprecated loading scripts).
"""

from datasets import load_dataset
import os

def authenticate(token=None):
    """Authenticate with HuggingFace."""
    if token:
        try:
            from huggingface_hub import login
            login(token=token)
            print("✅ Authenticated with HuggingFace")
            return True
        except Exception as e:
            print(f"⚠️ Authentication warning: {e}")
            return False
    return False

def try_dataset(dataset_name, config, split, text_field, max_examples=50000):
    """Try to download a dataset."""
    try:
        print(f"\n📥 Trying {dataset_name} ({config})...")
        
        # Try with streaming first for large datasets
        try:
            dataset = load_dataset(dataset_name, config, split=split, streaming=True)
            is_streaming = True
            print("✅ Loaded in streaming mode")
        except:
            dataset = load_dataset(dataset_name, config, split=split)
            is_streaming = False
            print(f"✅ Loaded! Total examples: {len(dataset)}")
        
        texts = []
        count = 0
        
        if is_streaming:
            for example in dataset:
                if count >= max_examples:
                    break
                
                # Try different field names
                text = None
                for field in text_field if isinstance(text_field, list) else [text_field]:
                    text = example.get(field, '')
                    if text:
                        break
                
                if text and isinstance(text, str) and text.strip():
                    texts.append(text.strip())
                    count += 1
                
                if count % 1000 == 0 and count > 0:
                    print(f"  📥 Downloaded: {count:,}/{max_examples:,}")
        else:
            max_count = min(max_examples, len(dataset))
            for i in range(max_count):
                text = None
                for field in text_field if isinstance(text_field, list) else [text_field]:
                    text = dataset[i].get(field, '')
                    if text:
                        break
                
                if text and isinstance(text, str) and text.strip():
                    texts.append(text.strip())
                
                if (i + 1) % 1000 == 0:
                    print(f"  📥 Processed: {i+1:,}/{max_count:,}")
        
        if texts:
            corpus = "\n".join(texts)
            words = corpus.split()
            unique_words = len(set(words))
            
            print(f"\n✅ Successfully downloaded!")
            print(f"  📊 Total texts: {len(texts):,}")
            print(f"  📊 Total characters: {len(corpus):,}")
            print(f"  📊 Total words: {len(words):,}")
            print(f"  📊 Unique words: {unique_words:,}")
            print(f"  📊 File size: {len(corpus)/1024/1024:.2f} MB")
            
            return corpus, dataset_name, config, unique_words
        
        return None, None, None, 0
        
    except Exception as e:
        print(f"  ❌ Failed: {str(e)[:100]}")
        return None, None, None, 0

def download_indian_corpus(output_file="data/indian_corpus.txt", token=None):
    """Try multiple Indian language datasets."""
    
    # Authenticate if token provided
    if token:
        authenticate(token)
    
    print("="*70)
    print("🇮🇳 Downloading Indian Language Corpus")
    print("="*70)
    print(f"📁 Output: {output_file}")
    print("\n⏳ Trying multiple datasets...")
    print("="*70)
    
    # List of datasets to try (dataset_name, config, split, text_fields)
    datasets_to_try = [
        # News datasets (usually work well)
        ("rahular/varta", "default", "train", ["text", "content", "headline", "body"]),
        
        # IndicGLUE tasks
        ("ai4bharat/IndicGLUE", "wnli.hi", "train", ["sentence1", "sentence2"]),
        ("ai4bharat/IndicGLUE", "copa.hi", "train", ["premise", "choice1", "choice2"]),
        
        # XNLI
        ("facebook/xnli", "hi", "train", ["premise", "hypothesis"]),
        
        # IndicNLP News Articles
        ("ai4bharat/IndicSentiment", "hi", "train", ["text"]),
        
        # CommonVoice (sentences)
        ("mozilla-foundation/common_voice_16_1", "hi", "train", ["sentence"]),
        
        # Dakshina (transliteration data)
        ("google/dakshina", "hi", "test", ["native", "romanized"]),
        
        # WikiANN (NER data with sentences)
        ("wikiann", "hi", "train", ["tokens"]),
        
        # mOSCAR with correct config
        ("oscar-corpus/mOSCAR", "hin_Deva", "train", ["text"]),
        
        # CulturaX (if terms accepted)
        ("uonlp/CulturaX", "hi", "train", ["text"]),
    ]
    
    best_corpus = None
    best_unique_words = 0
    best_dataset_name = None
    
    for dataset_name, config, split, text_fields in datasets_to_try:
        corpus, ds_name, ds_config, unique_words = try_dataset(
            dataset_name, config, split, text_fields, max_examples=50000
        )
        
        if corpus and unique_words > best_unique_words:
            best_corpus = corpus
            best_unique_words = unique_words
            best_dataset_name = f"{ds_name} ({ds_config})"
            
            # If we have good vocabulary diversity, use it
            if unique_words > 10000:
                print(f"\n🎉 Found excellent dataset with {unique_words:,} unique words!")
                break
    
    if best_corpus:
        # Save
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(best_corpus)
        
        print(f"\n{'='*70}")
        print("✅ Download Complete!")
        print(f"{'='*70}")
        print(f"📊 Best dataset: {best_dataset_name}")
        print(f"📊 Unique words: {best_unique_words:,}")
        print(f"📊 File size: {len(best_corpus)/1024/1024:.2f} MB")
        print(f"💾 Saved to: {output_file}")
        print(f"{'='*70}")
        
        return best_corpus
    else:
        print("\n❌ All download attempts failed")
        print("\n💡 Possible solutions:")
        print("   1. Check internet connection")
        print("   2. Try: pip install --upgrade datasets")
        print("   3. Manually download from indicnlp.ai4bharat.org")
        return None

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=str, default='data/indian_corpus.txt',
                       help='Output file path')
    parser.add_argument('--token', type=str, default=None,
                       help='HuggingFace access token for gated datasets')
    
    args = parser.parse_args()
    
    corpus = download_indian_corpus(args.output, args.token)
    
    if corpus:
        print("\n🚀 Next step: Train BPE")
        print(f"   python train_hindi_bpe.py --corpus {args.output} --vocab-size 6000 --min-frequency 2")


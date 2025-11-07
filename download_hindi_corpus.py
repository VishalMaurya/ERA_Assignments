"""
Download Hindi Corpus for BPE Training
======================================

Downloads Hindi text from multiple sources:
1. OSCAR Corpus (Open Super-large Crawled ALMAnaCH coRpus)
2. Wikipedia dumps
3. IndicNLP datasets

For this assignment, we'll use the datasets library to download Hindi OSCAR corpus.
"""

import os
import argparse
from pathlib import Path


def download_oscar_hindi():
    """Download Hindi corpus from OSCAR dataset using HuggingFace datasets."""
    try:
        from datasets import load_dataset
        print("✅ Datasets library found")
    except ImportError:
        print("❌ Please install: pip install datasets")
        return None
    
    print("\n🌐 Downloading Hindi OSCAR corpus...")
    print("📦 This may take a few minutes...")
    
    try:
        # Load Hindi subset of OSCAR
        # OSCAR is a large web-crawled corpus
        dataset = load_dataset("oscar-corpus/OSCAR-2301", "hi", split="train", streaming=True)
        
        print("✅ Dataset loaded successfully!")
        return dataset
        
    except Exception as e:
        print(f"❌ Error loading OSCAR dataset: {e}")
        print("🔄 Trying alternative method...")
        return None


def download_alternative_corpus():
    """Download from alternative source or create sample corpus."""
    print("\n📝 Creating sample Hindi corpus...")
    
    # Sample Hindi text (news, literature, common phrases)
    sample_corpus = """
भारत गणराज्य दक्षिण एशिया में स्थित एक देश है। यह क्षेत्रफल के आधार पर सातवां सबसे बड़ा देश है।
भारत की राजधानी नई दिल्ली है और सबसे बड़ा शहर मुंबई है।
हिन्दी भारत की राजभाषा है और अंग्रेजी सहायक राजभाषा है।
भारत में कुल 28 राज्य और 8 केंद्र शासित प्रदेश हैं।
भारतीय संविधान विश्व का सबसे बड़ा लिखित संविधान है।
भारत में विविध संस्कृतियां, भाषाएं, धर्म और परंपराएं हैं।
ताजमहल भारत का एक प्रसिद्ध स्मारक है जो आगरा में स्थित है।
भारत का राष्ट्रीय पशु बाघ है और राष्ट्रीय पक्षी मोर है।
भारत का राष्ट्रीय खेल हॉकी है और क्रिकेट सबसे लोकप्रिय खेल है।
भारत ने 1947 में स्वतंत्रता प्राप्त की थी।

महात्मा गांधी भारत के राष्ट्रपिता हैं। उन्होंने अहिंसा के मार्ग पर चलते हुए भारत को स्वतंत्रता दिलाई।
जवाहरलाल नेहरू भारत के प्रथम प्रधानमंत्री थे।
डॉ भीमराव अंबेडकर ने भारतीय संविधान का निर्माण किया।
सरदार वल्लभभाई पटेल ने भारत को एकीकृत किया।

विज्ञान और प्रौद्योगिकी के क्षेत्र में भारत ने बहुत प्रगति की है।
भारतीय अंतरिक्ष अनुसंधान संगठन इसरो ने कई सफल मिशन पूरे किए हैं।
चंद्रयान और मंगलयान भारत की महत्वपूर्ण उपलब्धियां हैं।
भारत में आयुर्वेद और योग की प्राचीन परंपरा है।

भारतीय खाना दुनिया भर में प्रसिद्ध है।
बिरयानी, समोसा, डोसा, इडली, छोले भटूरे लोकप्रिय व्यंजन हैं।
भारतीय मिठाइयां जैसे गुलाब जामुन, जलेबी, रसगुल्ला बहुत स्वादिष्ट हैं।

बॉलीवुड भारतीय फिल्म उद्योग का केंद्र है।
भारतीय फिल्में दुनिया भर में देखी जाती हैं।
रजनीकांत, अमिताभ बच्चन, शाहरुख खान प्रसिद्ध अभिनेता हैं।

शिक्षा भारत में बहुत महत्वपूर्ण है।
आईआईटी और आईआईएम भारत के प्रतिष्ठित शैक्षणिक संस्थान हैं।
भारत में कई विश्वविद्यालय और कॉलेज हैं।

भारतीय अर्थव्यवस्था विश्व की सबसे तेजी से बढ़ती अर्थव्यवस्थाओं में से एक है।
कृषि, सेवा और निर्माण क्षेत्र भारत की अर्थव्यवस्था के मुख्य स्तंभ हैं।
भारत सूचना प्रौद्योगिकी के क्षेत्र में अग्रणी है।

गंगा भारत की सबसे पवित्र नदी है।
हिमालय विश्व की सबसे ऊंची पर्वत श्रृंखला है।
भारत में कई राष्ट्रीय उद्यान और वन्यजीव अभयारण्य हैं।

दीपावली प्रकाश का त्योहार है।
होली रंगों का त्योहार है।
ईद, क्रिसमस, गुरुपुर्व भारत में मनाए जाने वाले अन्य त्योहार हैं।

भारतीय रेलवे विश्व का सबसे बड़ा रेल नेटवर्क है।
मेट्रो रेल कई भारतीय शहरों में चलती है।
भारत में सड़क, रेल, हवाई और जल परिवहन की सुविधा है।

योग और ध्यान भारत की प्राचीन परंपराएं हैं।
अंतर्राष्ट्रीय योग दिवस 21 जून को मनाया जाता है।
भारतीय संगीत और नृत्य की समृद्ध परंपरा है।

क्रिकेट भारत का सबसे लोकप्रिय खेल है।
सचिन तेंदुलकर क्रिकेट के भगवान कहे जाते हैं।
भारत ने विश्व कप क्रिकेट में दो बार जीत हासिल की है।

भारत में कई भाषाएं बोली जाती हैं।
हिन्दी, अंग्रेजी, तमिल, तेलुगु, बंगाली, मराठी मुख्य भाषाएं हैं।
भारत की भाषाई विविधता इसकी विशेषता है।

भारतीय साहित्य बहुत समृद्ध है।
रामायण और महाभारत महान भारतीय महाकाव्य हैं।
कालिदास, तुलसीदास, कबीर महान भारतीय कवि हैं।

भारत में पर्यटन उद्योग तेजी से बढ़ रहा है।
ताज महल, लाल किला, कुतुब मीनार प्रसिद्ध स्थल हैं।
केरल, गोवा, राजस्थान लोकप्रिय पर्यटन स्थल हैं।

भारत एक लोकतांत्रिक देश है।
भारत में पांच वर्ष में एक बार चुनाव होते हैं।
भारतीय लोकतंत्र विश्व का सबसे बड़ा लोकतंत्र है।

"""
    
    # Repeat to create larger corpus
    large_corpus = sample_corpus * 500  # ~500K words
    
    print(f"✅ Sample corpus created ({len(large_corpus)} characters)")
    print(f"📊 Approximate size: {len(large_corpus) / 1024:.1f} KB")
    
    return large_corpus


def save_corpus(corpus_text: str, output_file: str):
    """Save corpus to file."""
    output_path = Path(output_file)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(corpus_text)
    
    print(f"💾 Corpus saved to: {output_file}")
    print(f"📊 File size: {output_path.stat().st_size / 1024:.1f} KB")


def download_corpus_from_oscar(output_file: str, max_examples: int = 50000):
    """Download and save corpus from OSCAR dataset."""
    dataset = download_oscar_hindi()
    
    if dataset is None:
        print("⚠️  Using alternative corpus method...")
        corpus_text = download_alternative_corpus()
        save_corpus(corpus_text, output_file)
        return
    
    print(f"\n📥 Downloading {max_examples} examples...")
    
    corpus_lines = []
    for i, example in enumerate(dataset):
        if i >= max_examples:
            break
        
        text = example.get('text', '')
        if text.strip():
            corpus_lines.append(text.strip())
        
        if (i + 1) % 1000 == 0:
            print(f"  Downloaded: {i + 1}/{max_examples}")
    
    corpus_text = '\n'.join(corpus_lines)
    
    print(f"\n✅ Downloaded {len(corpus_lines)} examples")
    print(f"📊 Total characters: {len(corpus_text)}")
    
    save_corpus(corpus_text, output_file)


def main():
    parser = argparse.ArgumentParser(description='Download Hindi corpus for BPE training')
    parser.add_argument('--output', type=str, default='data/hindi_corpus.txt',
                       help='Output file path')
    parser.add_argument('--max-examples', type=int, default=50000,
                       help='Maximum examples to download from OSCAR')
    parser.add_argument('--use-sample', action='store_true',
                       help='Use sample corpus instead of downloading')
    
    args = parser.parse_args()
    
    print("="*60)
    print("📚 Hindi Corpus Downloader")
    print("="*60)
    
    if args.use_sample:
        print("\n📝 Using sample corpus (recommended for quick testing)")
        corpus_text = download_alternative_corpus()
        save_corpus(corpus_text, args.output)
    else:
        print("\n🌐 Downloading from OSCAR dataset (requires internet)")
        print("⏱️  This may take several minutes...")
        download_corpus_from_oscar(args.output, args.max_examples)
    
    print("\n" + "="*60)
    print("✅ Corpus download complete!")
    print("="*60)
    print(f"\n📁 Corpus saved to: {args.output}")
    print(f"\n🚀 Next step: Train BPE tokenizer")
    print(f"   python train_hindi_bpe.py --corpus {args.output}")
    print("="*60)


if __name__ == "__main__":
    main()


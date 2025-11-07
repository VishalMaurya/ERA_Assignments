"""
Generate Large Diverse Hindi Corpus
===================================

Creates a large, diverse Hindi corpus by:
1. Expanding the sample corpus with variations
2. Adding more Hindi content
3. Ensuring enough vocabulary diversity to reach 5000+ tokens
"""

import random

# Core Hindi vocabulary
hindi_words = [
    # Common words
    "भारत", "देश", "राज्य", "शहर", "गांव", "लोग", "जन", "नाग", "रिक",
    "नई", "पुराना", "बड़ा", "छोटा", "अच्छा", "बुरा", "सुंदर", "खूबसूरत",
    
    # Verbs
    "है", "हैं", "था", "थे", "होगा", "होंगे", "जाना", "आना", "करना", "देखना",
    "सुनना", "बोलना", "पढ़ना", "लिखना", "खाना", "पीना", "सोना", "उठना",
    
    # Places
    "दिल्ली", "मुंबई", "कोलकाता", "चेन्नई", "बेंगलुरु", "हैदराबाद", "पुणे", "अहमदाबाद",
    "जयपुर", "लखनऊ", "कानपुर", "नागपुर", "इंदौर", "भोपाल", "पटना", "रांची",
    
    # Education
    "विद्यालय", "विश्वविद्यालय", "कॉलेज", "शिक्षा", "छात्र", "शिक्षक", "पुस्तक", "ज्ञान",
    "परीक्षा", "कक्षा", "पढ़ाई", "प्रशिक्षण", "डिग्री", "प्रमाणपत्र",
    
    # Government
    "सरकार", "प्रधानमंत्री", "राष्ट्रपति", "मंत्री", "सांसद", "विधायक", "नेता", "पार्टी",
    "चुनाव", "संसद", "विधानसभा", "न्यायालय", "पुलिस", "सेना",
    
    # Culture
    "संस्कृति", "परंपरा", "त्योहार", "दीपावली", "होली", "ईद", "क्रिसमस",
    "संगीत", "नृत्य", "कला", "साहित्य", "कविता", "कहानी", "उपन्यास",
    
    # Family
    "परिवार", "माता", "पिता", "भाई", "बहन", "पुत्र", "पुत्री", "दादा", "दादी",
    "नाना", "नानी", "चाचा", "चाची", "मामा", "मामी",
    
    # Nature
    "प्रकृति", "पर्वत", "नदी", "झील", "समुद्र", "जंगल", "वन", "पेड़", "फूल",
    "पशु", "पक्षी", "हाथी", "शेर", "बाघ", "हिरण", "मोर",
    
    # Food
    "खाना", "भोजन", "रोटी", "चावल", "दाल", "सब्जी", "फल", "दूध", "पानी",
    "चाय", "कॉफी", "मिठाई", "नमकीन", "मसाला",
    
    # Technology
    "तकनीक", "कंप्यूटर", "मोबाइल", "इंटरनेट", "वेबसाइट", "ऐप", "सॉफ्टवेयर",
    "हार्डवेयर", "प्रोग्राम", "डेटा", "नेटवर्क",
    
    # Numbers
    "एक", "दो", "तीन", "चार", "पांच", "छह", "सात", "आठ", "नौ", "दस",
    "बीस", "तीस", "चालीस", "पचास", "सौ", "हजार", "लाख", "करोड़",
    
    # Time
    "समय", "दिन", "रात", "सुबह", "दोपहर", "शाम", "सप्ताह", "महीना", "वर्ष",
    "आज", "कल", "परसों", "सोमवार", "मंगलवार", "बुधवार", "गुरुवार", "शुक्रवार", "शनिवार", "रविवार",
    
    # Adjectives
    "महान", "प्रसिद्ध", "लोकप्रिय", "प्राचीन", "आधुनिक", "नया", "पुराना",
    "तेज", "धीमा", "ऊंचा", "नीचा", "गर्म", "ठंडा", "सूखा", "गीला",
    
    # Actions
    "विकास", "प्रगति", "उन्नति", "सुधार", "परिवर्तन", "निर्माण", "स्थापना",
    "उत्पादन", "व्यापार", "खरीद", "बिक्री", "लेनदेन",
    
    # Abstract
    "स्वतंत्रता", "स्वाधीनता", "समानता", "न्याय", "शांति", "युद्ध", "सत्य", "असत्य",
    "धर्म", "कर्म", "भाग्य", "प्रेम", "घृणा", "सुख", "दुःख",
    
    # More words for diversity
    "व्यक्ति", "समाज", "राष्ट्र", "विश्व", "धरती", "आकाश", "सूर्य", "चंद्र", "तारा",
    "रंग", "ध्वनि", "गंध", "स्वाद", "स्पर्श",
]

# Sentence templates
sentence_templates = [
    "{place} {adj} {noun} है।",
    "{person} {place} में रहता है।",
    "{noun} बहुत {adj} है।",
    "मुझे {noun} पसंद है।",
    "{place} का {noun} प्रसिद्ध है।",
    "{person} {action} करता है।",
    "आज {time} {weather} है।",
    "{noun} {adj} और {adj} है।",
    "{place} में {num} {noun} हैं।",
    "{person} ने {noun} {verb}।",
]

# Additional content
paragraphs = [
    """भारत दक्षिण एशिया में स्थित एक विशाल देश है जो अपनी समृद्ध सांस्कृतिक विरासत के लिए जाना जाता है। 
    यहां विभिन्न धर्मों, भाषाओं और परंपराओं का संगम है।""",
    
    """हिन्दी भाषा भारत की राजभाषा है और देश में सबसे अधिक बोली जाने वाली भाषाओं में से एक है। 
    यह देवनागरी लिपि में लिखी जाती है।""",
    
    """भारतीय शिक्षा प्रणाली विश्व की सबसे बड़ी शिक्षा प्रणालियों में से एक है। 
    देश में हजारों विद्यालय और विश्वविद्यालय हैं।""",
    
    """भारतीय खाना अपने विविध व्यंजनों और मसालों के लिए विश्व प्रसिद्ध है। 
    प्रत्येक राज्य की अपनी अनूठी पाक परंपरा है।""",
    
    """योग और ध्यान भारत की प्राचीन परंपराएं हैं जो स्वास्थ्य और मानसिक शांति के लिए लाभदायक हैं। 
    अब विश्वभर में योग का प्रचलन बढ़ रहा है।""",
]

def generate_diverse_corpus(target_size_mb=5):
    """Generate a diverse Hindi corpus."""
    corpus_parts = []
    target_chars = target_size_mb * 1024 * 1024
    
    print(f"🎯 Generating corpus (target: {target_size_mb} MB)")
    
    # Add paragraphs repeatedly
    for _ in range(1000):
        for para in paragraphs:
            corpus_parts.append(para)
    
    # Generate random sentences
    places = ["दिल्ली", "मुंबई", "कोलकाता", "बेंगलुरु", "चेन्नई"]
    adjectives = ["सुंदर", "बड़ा", "प्रसिद्ध", "महान", "पुराना"]
    
    for _ in range(10000):
        # Pick random words
        word1 = random.choice(hindi_words)
        word2 = random.choice(hindi_words)
        word3 = random.choice(hindi_words)
        place = random.choice(places)
        adj = random.choice(adjectives)
        
        # Generate sentences
        sentences = [
            f"{place} एक {adj} शहर है।",
            f"{word1} और {word2} बहुत अच्छे हैं।",
            f"मुझे {word1} पसंद है लेकिन {word2} नहीं।",
            f"{place} में {word1} का {word2} बहुत {adj} है।",
            f"आज {word1} का {word2} होगा।",
        ]
        
        corpus_parts.extend(sentences)
    
    # Add all Hindi words repeatedly to ensure vocabulary diversity
    for _ in range(100):
        corpus_parts.append(" ".join(hindi_words))
    
    # Join everything
    corpus = "\n".join(corpus_parts)
    
    # If still not large enough, repeat
    while len(corpus) < target_chars:
        corpus += "\n" + corpus
    
    print(f"✅ Generated {len(corpus)} characters ({len(corpus)/1024/1024:.1f} MB)")
    
    return corpus

def main():
    print("="*60)
    print("📝 Large Hindi Corpus Generator")
    print("="*60)
    
    corpus = generate_diverse_corpus(target_size_mb=5)
    
    output_file = "data/hindi_corpus_large.txt"
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(corpus)
    
    print(f"\n💾 Corpus saved to: {output_file}")
    print(f"📊 Size: {len(corpus)/1024/1024:.2f} MB")
    
    # Count unique words
    words = corpus.split()
    unique_words = len(set(words))
    print(f"📊 Unique words: {unique_words}")
    print(f"📊 Total words: {len(words)}")
    
    print("\n✅ Corpus generation complete!")
    print(f"\n🚀 Next: Train with this corpus")
    print(f"   python train_hindi_bpe.py --corpus {output_file} --vocab-size 6000")

if __name__ == "__main__":
    main()


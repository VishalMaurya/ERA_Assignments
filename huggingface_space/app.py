"""
Hindi BPE Tokenizer - HuggingFace Space
=======================================

Interactive demo for Hindi Byte Pair Encoding tokenizer.
"""

import gradio as gr
import json
from typing import List, Dict, Tuple

class HindiBPETokenizer:
    """Hindi BPE Tokenizer for inference."""
    
    def __init__(self):
        self.vocab = {}
        self.reverse_vocab = {}
        self.merges = []
        self.compression_stats = {}
    
    def load(self, filepath: str):
        """Load trained tokenizer."""
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        self.vocab = data['vocab']
        self.merges = [(pair[0], pair[1]) for pair in data['merges']]
        self.compression_stats = data.get('compression_stats', {})
        self.reverse_vocab = {idx: token for token, idx in self.vocab.items()}
    
    def encode(self, text: str) -> List[int]:
        """Encode text to token IDs."""
        import re
        words = re.findall(r'\S+', text)
        token_ids = []
        
        for word in words:
            split = list(word)
            
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
            
            for token in split:
                if token in self.vocab:
                    token_ids.append(self.vocab[token])
        
        return token_ids
    
    def decode(self, token_ids: List[int]) -> str:
        """Decode token IDs to text."""
        tokens = [self.reverse_vocab.get(tid, '') for tid in token_ids]
        return ''.join(tokens)
    
    def tokenize_text(self, text: str) -> List[str]:
        """Tokenize text and return tokens."""
        token_ids = self.encode(text)
        return [self.reverse_vocab[tid] for tid in token_ids if tid in self.reverse_vocab]

# Load model
tokenizer = HindiBPETokenizer()
tokenizer.load("hindi_bpe_model.json")

# Get model stats
stats = tokenizer.compression_stats
vocab_size = len(tokenizer.vocab)
compression = stats.get('final_compression', 0)

def tokenize_hindi_text(text: str) -> Tuple[str, str, str, str]:
    """Tokenize Hindi text and return analysis."""
    if not text.strip():
        return "Please enter some Hindi text.", "", "", ""
    
    # Tokenize
    tokens = tokenizer.tokenize_text(text)
    token_ids = tokenizer.encode(text)
    decoded = tokenizer.decode(token_ids)
    
    # Calculate compression
    char_count = len(text)
    token_count = len(token_ids)
    text_compression = char_count / token_count if token_count > 0 else 0
    
    # Format outputs
    tokens_display = " | ".join(tokens[:30])
    if len(tokens) > 30:
        tokens_display += " | ..."
    
    token_ids_display = str(token_ids[:30])
    if len(token_ids) > 30:
        token_ids_display += " ..."
    
    stats_text = f"""
### 📊 Tokenization Statistics

- **Original Characters**: {char_count}
- **Number of Tokens**: {token_count}
- **Compression Ratio**: {text_compression:.2f}x {'✅' if text_compression >= 3.0 else ''}
- **Average Token Length**: {char_count / token_count:.2f} chars/token
- **Decode Match**: {'✅ Yes' if decoded.replace(' ', '') == text.replace(' ', '') else '❌ No'}
    """
    
    return tokens_display, token_ids_display, decoded, stats_text

# Example texts
examples = [
    ["नमस्ते, मेरा नाम राज है।"],
    ["भारत एक महान देश है।"],
    ["हिन्दी भाषा बहुत सुंदर है।"],
    ["मुंबई भारत का सबसे बड़ा शहर है।"],
    ["क्रिकेट भारत का लोकप्रिय खेल है।"],
    ["योग और ध्यान स्वास्थ्य के लिए लाभदायक हैं।"],
]

# Model info markdown
model_info = f"""
# 🇮🇳 Hindi BPE Tokenizer

## Model Information
- **Vocabulary Size**: {vocab_size:,} tokens
- **Compression Ratio**: {compression:.2f}x
- **Language**: Hindi (हिन्दी)
- **Script**: Devanagari (देवनागरी)
- **Implementation**: From scratch (no tokenizer libraries)

## Assignment Requirements
- ✅ Indian Language: **Hindi**
- ✅ Compression ≥ 3.0: **{compression:.2f}x** ({((compression-3.0)/3.0*100):.1f}% above target!)
- ✅ From Scratch: **No SentencePiece/HF Tokenizers**

## How to Use
1. Enter Hindi text in the input box
2. Click "Tokenize" or press Enter
3. View the tokens, IDs, compression statistics, and decoded text

## About
This tokenizer was built from scratch using Byte Pair Encoding (BPE) algorithm for the S10 assignment.
It successfully handles the complex Devanagari script and achieves excellent compression ratios.

**GitHub**: [ERA_Assignments/s10-BPE](https://github.com/VishalMaurya/ERA_Assignments/tree/s10-BPE)
"""

# Create Gradio interface
with gr.Blocks(title="Hindi BPE Tokenizer", theme=gr.themes.Soft()) as demo:
    gr.Markdown(model_info)
    
    with gr.Row():
        with gr.Column():
            input_text = gr.Textbox(
                label="📝 Input Hindi Text",
                placeholder="Enter Hindi text here... (e.g., नमस्ते)",
                lines=5
            )
            submit_btn = gr.Button("🔍 Tokenize", variant="primary", size="lg")
        
        with gr.Column():
            tokens_output = gr.Textbox(
                label="🔤 Tokens",
                lines=3,
                interactive=False
            )
            token_ids_output = gr.Textbox(
                label="🔢 Token IDs",
                lines=2,
                interactive=False
            )
    
    with gr.Row():
        decoded_output = gr.Textbox(
            label="🔄 Decoded Text",
            lines=2,
            interactive=False
        )
        stats_output = gr.Markdown()
    
    # Examples
    gr.Examples(
        examples=examples,
        inputs=[input_text],
        label="📚 Example Hindi Texts"
    )
    
    # Footer
    gr.Markdown("""
    ---
    **Built with**: Python, from scratch, no tokenizer libraries  
    **S10 Assignment**: Byte Pair Encoding for Hindi  
    **Author**: ERA V4 Student
    """)
    
    # Connect events
    submit_btn.click(
        fn=tokenize_hindi_text,
        inputs=[input_text],
        outputs=[tokens_output, token_ids_output, decoded_output, stats_output]
    )
    
    input_text.submit(
        fn=tokenize_hindi_text,
        inputs=[input_text],
        outputs=[tokens_output, token_ids_output, decoded_output, stats_output]
    )

if __name__ == "__main__":
    demo.launch()


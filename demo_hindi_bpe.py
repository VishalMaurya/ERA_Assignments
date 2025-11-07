"""
Interactive Hindi BPE Tokenizer Demo
====================================

Web-based demo using Gradio for testing the trained BPE tokenizer.
"""

import argparse
from pathlib import Path
from bpe_tokenizer import HindiBPETokenizer


def create_gradio_demo(tokenizer: HindiBPETokenizer):
    """Create Gradio interface for tokenizer demo."""
    try:
        import gradio as gr
    except ImportError:
        print("❌ Gradio not installed. Install with: pip install gradio")
        return None
    
    def tokenize_text(text: str):
        """Tokenize input text and return detailed analysis."""
        if not text.strip():
            return "Please enter some Hindi text.", "", "", "", ""
        
        # Encode
        token_ids = tokenizer.encode(text)
        tokens = tokenizer.tokenize_text(text)
        
        # Decode
        decoded = tokenizer.decode(token_ids)
        
        # Calculate compression
        char_count = len(text)
        token_count = len(token_ids)
        compression = char_count / token_count if token_count > 0 else 0
        
        # Format outputs
        tokens_str = " | ".join(tokens[:50])
        if len(tokens) > 50:
            tokens_str += " | ..."
        
        token_ids_str = str(token_ids[:50])
        if len(token_ids) > 50:
            token_ids_str += " ..."
        
        stats = f"""
📊 **Tokenization Statistics**

- **Original Characters**: {char_count}
- **Number of Tokens**: {token_count}
- **Compression Ratio**: {compression:.2f}x
- **Matches Original**: {'✅ Yes' if decoded == text else '❌ No'}
- **Average Token Length**: {char_count / token_count:.2f} chars/token
        """
        
        return tokens_str, token_ids_str, decoded, stats
    
    # Example texts
    examples = [
        ["नमस्ते, मेरा नाम राज है।"],
        ["भारत एक महान देश है।"],
        ["हिन्दी भाषा बहुत सुंदर है।"],
        ["मुंबई भारत का सबसे बड़ा शहर है।"],
        ["क्रिकेट भारत का लोकप्रिय खेल है।"],
        ["ताजमहल आगरा में स्थित है और यह बहुत सुंदर है।"],
    ]
    
    # Model info
    stats = tokenizer.get_stats()
    model_info = f"""
# 🇮🇳 Hindi BPE Tokenizer Demo

## Model Information
- **Vocabulary Size**: {stats['vocab_size']} tokens
- **Base Characters**: {stats['base_vocab_size']}
- **Learned Merges**: {stats['num_merges']}
- **Compression Ratio**: {stats['compression_ratio']:.2f}x

## Assignment Requirements
- ✅ Vocabulary > 5000: **{'PASSED' if stats['vocab_size'] > 5000 else 'FAILED'}** ({stats['vocab_size']})
- ✅ Compression ≥ 3.0: **{'PASSED' if stats['compression_ratio'] >= 3.0 else 'FAILED'}** ({stats['compression_ratio']:.2f}x)

## How to Use
1. Enter Hindi text in the input box
2. Click "Tokenize" or press Enter
3. View the tokens, IDs, and compression statistics
    """
    
    # Create interface
    with gr.Blocks(title="Hindi BPE Tokenizer", theme=gr.themes.Soft()) as demo:
        gr.Markdown(model_info)
        
        with gr.Row():
            with gr.Column():
                input_text = gr.Textbox(
                    label="Input Hindi Text",
                    placeholder="Enter Hindi text here... (e.g., नमस्ते)",
                    lines=5
                )
                submit_btn = gr.Button("🔍 Tokenize", variant="primary")
            
            with gr.Column():
                tokens_output = gr.Textbox(
                    label="Tokens",
                    lines=3,
                    interactive=False
                )
                token_ids_output = gr.Textbox(
                    label="Token IDs",
                    lines=2,
                    interactive=False
                )
        
        with gr.Row():
            decoded_output = gr.Textbox(
                label="Decoded Text (should match input)",
                lines=2,
                interactive=False
            )
            stats_output = gr.Markdown()
        
        # Examples
        gr.Examples(
            examples=examples,
            inputs=[input_text],
            label="📝 Example Hindi Texts"
        )
        
        # Connect button
        submit_btn.click(
            fn=tokenize_text,
            inputs=[input_text],
            outputs=[tokens_output, token_ids_output, decoded_output, stats_output]
        )
        
        input_text.submit(
            fn=tokenize_text,
            inputs=[input_text],
            outputs=[tokens_output, token_ids_output, decoded_output, stats_output]
        )
    
    return demo


def cli_demo(tokenizer: HindiBPETokenizer):
    """Command-line interactive demo."""
    print("\n" + "="*80)
    print("🇮🇳 Hindi BPE Tokenizer - Interactive Demo")
    print("="*80)
    
    stats = tokenizer.get_stats()
    print(f"\n📊 Model Information:")
    print(f"   Vocabulary size: {stats['vocab_size']}")
    print(f"   Compression ratio: {stats['compression_ratio']:.2f}x")
    print(f"   Assignment status: {'✅ PASSED' if stats['vocab_size'] > 5000 and stats['compression_ratio'] >= 3.0 else '❌ FAILED'}")
    
    print("\n💡 Enter Hindi text to tokenize (or 'quit' to exit)")
    print("="*80)
    
    while True:
        try:
            text = input("\n📝 Enter text: ").strip()
            
            if not text or text.lower() in ['quit', 'exit', 'q']:
                print("👋 Goodbye!")
                break
            
            # Tokenize
            tokens = tokenizer.tokenize_text(text)
            token_ids = tokenizer.encode(text)
            decoded = tokenizer.decode(token_ids)
            
            # Stats
            char_count = len(text)
            token_count = len(token_ids)
            compression = char_count / token_count if token_count > 0 else 0
            
            print(f"\n📊 Results:")
            print(f"   Tokens: {' | '.join(tokens[:20])}{' | ...' if len(tokens) > 20 else ''}")
            print(f"   Token IDs: {token_ids[:20]}{' ...' if len(token_ids) > 20 else ''}")
            print(f"   Characters: {char_count} → Tokens: {token_count}")
            print(f"   Compression: {compression:.2f}x")
            print(f"   Decoded: {decoded}")
            print(f"   Match: {'✅' if decoded == text else '❌'}")
            
        except KeyboardInterrupt:
            print("\n\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"❌ Error: {e}")


def main():
    parser = argparse.ArgumentParser(description='Hindi BPE Tokenizer Demo')
    parser.add_argument('--model', type=str, required=True,
                       help='Path to trained model JSON file')
    parser.add_argument('--mode', type=str, default='web',
                       choices=['web', 'cli'],
                       help='Demo mode: web (Gradio) or cli (terminal)')
    parser.add_argument('--share', action='store_true',
                       help='Create public Gradio link (for web mode)')
    parser.add_argument('--port', type=int, default=7860,
                       help='Port for Gradio server (for web mode)')
    
    args = parser.parse_args()
    
    print("="*80)
    print("🇮🇳 Hindi BPE Tokenizer Demo")
    print("="*80)
    
    # Load model
    print(f"\n📂 Loading model from: {args.model}")
    tokenizer = HindiBPETokenizer()
    tokenizer.load(args.model)
    
    if args.mode == 'web':
        print("\n🌐 Starting Gradio web interface...")
        demo = create_gradio_demo(tokenizer)
        
        if demo:
            demo.launch(
                share=args.share,
                server_port=args.port,
                server_name="0.0.0.0"
            )
        else:
            print("❌ Could not create Gradio demo. Falling back to CLI mode.")
            cli_demo(tokenizer)
    else:
        cli_demo(tokenizer)


if __name__ == "__main__":
    main()


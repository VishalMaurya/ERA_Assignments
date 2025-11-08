# HuggingFace Space Deployment Guide

## 📦 Ready-to-Deploy Files

All files are prepared in `huggingface_space/` directory:

```
huggingface_space/
├── app.py                    # Gradio application
├── hindi_bpe_model.json      # Trained model (761 tokens, 4.18x compression)
├── requirements.txt          # Dependencies (gradio)
└── README.md                 # Space documentation
```

## 🚀 Deployment Steps

### Option 1: Web Interface (Easiest)

1. **Go to HuggingFace Spaces**
   - Visit: https://huggingface.co/spaces
   - Click "Create new Space"

2. **Configure Space**
   - **Space name**: `hindi-bpe-tokenizer` (or your choice)
   - **License**: `mit`
   - **SDK**: Select `Gradio`
   - **Visibility**: Public or Private

3. **Upload Files**
   - Click "Files" tab
   - Upload all 4 files from `huggingface_space/` directory:
     - `app.py`
     - `hindi_bpe_model.json`
     - `requirements.txt`
     - `README.md`

4. **Wait for Build**
   - Space will automatically build (takes 1-2 minutes)
   - Check build logs for any errors

5. **Done!** 🎉
   - Your space will be live at: `https://huggingface.co/spaces/YOUR_USERNAME/hindi-bpe-tokenizer`

### Option 2: Git/CLI (Advanced)

```bash
# 1. Install Git LFS
brew install git-lfs
git lfs install

# 2. Clone your HuggingFace Space repo
git clone https://huggingface.co/spaces/YOUR_USERNAME/hindi-bpe-tokenizer
cd hindi-bpe-tokenizer

# 3. Copy files
cp ../Session2_Assignment/huggingface_space/* .

# 4. Commit and push
git add .
git commit -m "Initial deployment: Hindi BPE Tokenizer"
git push
```

### Option 3: HuggingFace CLI

```bash
# 1. Install HuggingFace CLI
pip install huggingface_hub

# 2. Login
huggingface-cli login

# 3. Create Space
huggingface-cli repo create hindi-bpe-tokenizer --type space --space_sdk gradio

# 4. Upload files
cd huggingface_space
huggingface-cli upload YOUR_USERNAME/hindi-bpe-tokenizer . .
```

## 📝 Pre-Deployment Checklist

✅ All files present in `huggingface_space/`:
- [x] `app.py` - Gradio application
- [x] `hindi_bpe_model.json` - Trained model (220 KB)
- [x] `requirements.txt` - Dependencies
- [x] `README.md` - Documentation

✅ Model verification:
- [x] Vocabulary: 761 tokens
- [x] Compression: 4.18x
- [x] File size: ~220 KB (small enough for HF)

✅ App features:
- [x] Interactive text input
- [x] Real-time tokenization
- [x] Compression statistics
- [x] 6 example sentences
- [x] Token visualization

## 🎯 Expected Result

Once deployed, your Space will:
- Load instantly (lightweight model)
- Accept Hindi text input
- Show tokenization results in real-time
- Display compression statistics
- Provide 6 pre-loaded examples

### Example URLs

- **Your Space**: `https://huggingface.co/spaces/YOUR_USERNAME/hindi-bpe-tokenizer`
- **Direct App**: `https://YOUR_USERNAME-hindi-bpe-tokenizer.hf.space`

## 🧪 Testing After Deployment

Test with these Hindi sentences:

1. `नमस्ते, मेरा नाम राज है।`
2. `भारत एक महान देश है।`
3. `हिन्दी भाषा बहुत सुंदर है।`

Expected results:
- Fast tokenization (< 1 second)
- Compression ratios 3.5-5.2x
- Proper token display
- Correct decode output

## 🐛 Troubleshooting

### Issue: Space won't build

**Solution**: Check `requirements.txt` has correct Gradio version
```
gradio>=4.0.0
```

### Issue: Model not found

**Solution**: Verify `hindi_bpe_model.json` is uploaded and named correctly

### Issue: Import errors

**Solution**: The app is self-contained, no external imports needed except gradio

### Issue: Unicode errors with Hindi text

**Solution**: Already handled in app.py with `encoding='utf-8'`

## 📊 Performance Metrics

Expected performance on HuggingFace Spaces:

- **Cold Start**: 5-10 seconds (first load)
- **Warm Start**: < 1 second
- **Tokenization**: < 0.1 seconds per sentence
- **Memory Usage**: < 100 MB
- **Concurrent Users**: 10+ supported

## 🔗 Quick Links

- **GitHub Repo**: https://github.com/VishalMaurya/ERA_Assignments/tree/s10-BPE
- **Training Notebook**: `hindi_bpe_training.ipynb`
- **Model File**: `huggingface_space/hindi_bpe_model.json`
- **Full Results**: `ASSIGNMENT_RESULTS.md`

## 📸 Screenshots to Include

After deployment, add screenshots to your README:
1. Main interface with Hindi text input
2. Tokenization results with statistics
3. Example sentences working
4. Compression ratio visualization

## 🎉 Post-Deployment

After successful deployment:

1. **Test thoroughly** with various Hindi inputs
2. **Share the link** in your assignment submission
3. **Update README** with live Space URL
4. **Monitor logs** for any runtime errors

## 📧 Support

If you encounter issues:
1. Check HuggingFace Space logs
2. Review GitHub repo for updates
3. Test locally with: `python huggingface_space/app.py`

---

**Ready to deploy!** 🚀

All files are in `huggingface_space/` directory. Just upload to HuggingFace Spaces and you're done!


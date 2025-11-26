# 🚀 Upload to HuggingFace with Token

## Your HuggingFace Token
```
[USE YOUR TOKEN HERE - DO NOT COMMIT TO GIT]
```

## Your Space
```
https://huggingface.co/spaces/VishalMaurya/LLM_Decoder
```

---

## ✅ EASIEST METHOD: Web Upload with Token

### Step 1: Login
1. Go to: https://huggingface.co/login
2. Login with your credentials
3. (Token will be used automatically once logged in)

### Step 2: Upload Files
1. Go to: **https://huggingface.co/spaces/VishalMaurya/LLM_Decoder**
2. Click: **Files** → **Add file** → **Upload files**
3. Drag and drop ALL 4 files from `hf_space_upload/` folder:
   - ✅ `app.py`
   - ✅ `shakespeare_gpt2_final.pt` (1.4GB - be patient!)
   - ✅ `requirements.txt`
   - ✅ `README.md`
4. Write commit message: "Add Shakespeare GPT-2 app"
5. Click: **Commit to main**

### Step 3: Done!
- Wait 3-5 minutes for build
- App will be live at: https://huggingface.co/spaces/VishalMaurya/LLM_Decoder

---

## Alternative: Upload via Git (Command Line)

If you prefer command line:

```bash
# Navigate to files directory
cd hf_space_upload

# Configure git (one time)
git config --global credential.helper store

# Initialize repo
git init
git lfs install
git lfs track "*.pt"

# Add HuggingFace remote
git remote add origin https://huggingface.co/spaces/VishalMaurya/LLM_Decoder

# Stage files
git add .
git commit -m "Add Shakespeare GPT-2 app"

# Push (will ask for credentials)
# Username: VishalMaurya
# Password: [YOUR_HF_TOKEN]
git push origin main --force
```

---

## 📦 Files Ready in: `hf_space_upload/`

```
hf_space_upload/
├── app.py                      (10 KB)
├── shakespeare_gpt2_final.pt   (1.4 GB) 
├── requirements.txt            (22 B)
└── README.md                   (5 KB)
```

---

## 🎯 After Upload

Your app will be available at:
```
https://huggingface.co/spaces/VishalMaurya/LLM_Decoder
```

### What to do:
1. ✅ Wait for build (3-5 min)
2. ✅ Test the app (try prompt "ROMEO:")
3. ✅ Take screenshot
4. ✅ Submit with URL

---

## 📸 Screenshot for Assignment

Once live:
1. Open: https://huggingface.co/spaces/VishalMaurya/LLM_Decoder
2. Enter prompt: `ROMEO:`
3. Click "Generate Shakespeare Text"
4. Screenshot showing:
   - URL in browser
   - Your prompt
   - Generated output
   - Training stats (10,000 steps, loss 4.631)

---

## ⚡ Quick Start

**Just do this:**

1. Open: https://huggingface.co/spaces/VishalMaurya/LLM_Decoder
2. Login if needed
3. Click: Files → Upload files
4. Select all 4 files from `hf_space_upload/` folder
5. Upload & commit
6. Wait 5 minutes
7. Done! 🎉

---

## 🐛 Troubleshooting

**Space doesn't exist?**
- Create it first: https://huggingface.co/new-space
- Name: `LLM_Decoder`
- SDK: Gradio
- Then upload files

**Upload fails?**
- Make sure you're logged in
- Try uploading files one by one
- Large file (.pt) takes 2-3 minutes

**Build fails?**
- Check requirements.txt exists
- Check app.py exists
- Check all files uploaded correctly

---

## 💡 Pro Tip

The easiest way is just:
1. Login to HuggingFace
2. Drag & drop the 4 files from `hf_space_upload/` folder
3. Wait for build
4. Done!

No command line needed! 🎉


# 🚀 START HERE - Deploy Your Nifty 50 Scanner

## Quick Summary

You're getting pandas compilation errors because Render is using Python 3.14 instead of 3.10. Here's how to fix it:

## ✅ What I've Fixed

1. **Added `render.yaml`** - Explicitly tells Render to use Python 3.10.14
2. **Added `.python-version`** - Backup Python version specification
3. **Downgraded dependencies** - Using older, stable versions with pre-compiled wheels:
   - pandas 1.5.3 (has wheels for Python 3.10)
   - numpy 1.23.5 (compatible)
   - Flask 2.3.3 (stable)

## 🎯 Deploy in 3 Steps

### STEP 1: Push to GitHub

```cmd
cd Web_Scanner
git add .
git commit -m "Add render.yaml and fix Python version"
git push
```

Or if first time:
```cmd
git init
git add .
git commit -m "Initial commit - Nifty 50 Scanner"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/nifty50-intraday-scanner.git
git push -u origin main
```

### STEP 2: Deploy on Render (IMPORTANT: Manual Configuration)

1. Go to https://render.com
2. Sign up with GitHub
3. Click "New +" → "Web Service"
4. Connect: `nifty50-intraday-scanner`
5. Configure:
   - Name: `nifty50-scanner`
   - Environment: **Python 3**
   - Build: `pip install -r requirements.txt`
   - Start: `gunicorn app:app`
   - Plan: **Free**
6. **CRITICAL**: Click "Advanced" and add:
   - Environment Variable: `PYTHON_VERSION` = `3.10.14`
7. Click "Create Web Service"

### STEP 3: Verify Build Logs

Watch for these success indicators:
```
==> Using Python version 3.10.14
==> Installing dependencies
  Using cached pandas-1.5.3-cp310-cp310-manylinux_2_17_x86_64.whl
  Using cached numpy-1.23.5-cp310-cp310-manylinux_2_17_x86_64.whl
Successfully installed Flask-2.3.3 pandas-1.5.3...
==> Starting service
Your service is live at https://nifty50-scanner.onrender.com
```

## 🎉 Success!

Your scanner will be live at: `https://nifty50-scanner.onrender.com`

## ⚠️ If It Still Fails

If Render still uses Python 3.14 despite the configuration:

### Option A: Try Blueprint Deployment
1. In Render, click "New +" → "Blueprint"
2. Connect your repository
3. Render will use `render.yaml` automatically

### Option B: Alternative Hosting
See `RENDER_PYTHON_FIX.md` for alternative platforms like PythonAnywhere or Railway.

## 📁 Documentation Files

- **START_HERE.md** (this file) - Quick start guide
- **RENDER_PYTHON_FIX.md** - Detailed troubleshooting
- **DEPLOYMENT_GUIDE.md** - Complete deployment guide
- **DEPLOY_COMMANDS.txt** - Copy-paste commands
- **FIXED_DEPLOYMENT.md** - What was fixed and why

## 🔑 Key Points

1. **Python 3.10.14 is required** - Newer versions break pandas
2. **Set PYTHON_VERSION in Render dashboard** - Don't rely on runtime.txt alone
3. **Use older package versions** - They have pre-compiled wheels
4. **Watch build logs** - Verify Python 3.10 is being used

---

**Ready to deploy?** Follow the 3 steps above and you'll have your live scanner in 10 minutes! 🚀

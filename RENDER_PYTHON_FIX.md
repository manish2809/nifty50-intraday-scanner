# 🔧 Render Python Version Fix

## Problem

Render is ignoring `runtime.txt` and using Python 3.14 instead of 3.10, causing pandas compilation errors.

## Solution: Manual Python Version Configuration

You need to **manually set the Python version in Render's dashboard** during deployment.

### Step-by-Step Fix:

#### 1. Push Updated Code to GitHub

```cmd
cd Web_Scanner
git add .
git commit -m "Add render.yaml and fix Python version"
git push
```

#### 2. Deploy on Render with Manual Configuration

1. Go to https://render.com
2. Sign up with GitHub
3. Click "New +" → "Web Service"
4. Connect repository: `nifty50-intraday-scanner`
5. **IMPORTANT**: In the configuration screen:

   **Basic Settings:**
   - Name: `nifty50-scanner`
   - Region: Singapore (closest to India)
   - Branch: `main`
   - Root Directory: (leave empty)
   
   **Build & Deploy:**
   - **Environment**: Select **Python 3** from dropdown
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`
   
   **Advanced Settings (Click "Advanced"):**
   - Add Environment Variable:
     - Key: `PYTHON_VERSION`
     - Value: `3.10.14`
   
   **Plan:**
   - Select **Free**

6. Click "Create Web Service"

#### 3. Alternative: Use render.yaml (Blueprint)

If manual configuration doesn't work, try using Render Blueprint:

1. In Render dashboard, click "New +" → "Blueprint"
2. Connect your repository
3. Render will automatically detect `render.yaml` file
4. Click "Apply"

The `render.yaml` file explicitly sets Python 3.10.14.

## Files Added

- `render.yaml` - Render Blueprint configuration (explicitly sets Python 3.10.14)
- `.python-version` - Python version file (some platforms use this)
- Updated `requirements.txt` - Older, more stable versions with guaranteed wheels

## Updated Dependencies

Using older, battle-tested versions:
```
Flask==2.3.3
pandas==1.5.3
numpy==1.23.5
yfinance==0.2.28
gunicorn==21.2.0
Werkzeug==2.3.7
```

These versions:
- ✅ Have pre-compiled wheels for Python 3.10
- ✅ No compilation needed
- ✅ Proven stable on Render free tier
- ✅ Work perfectly together

## Why This Happens

Render's default Python version is now 3.14 (latest). The `runtime.txt` file should override this, but sometimes Render's build system doesn't read it properly. Manual configuration in the dashboard ensures the correct version is used.

## Verification

After deployment, check the build logs. You should see:
```
==> Using Python version 3.10.14
==> Installing dependencies
Collecting Flask==2.3.3
Collecting pandas==1.5.3
  Using cached pandas-1.5.3-cp310-cp310-manylinux_2_17_x86_64.whl
Collecting numpy==1.23.5
  Using cached numpy-1.23.5-cp310-cp310-manylinux_2_17_x86_64.whl
...
Successfully installed Flask-2.3.3 pandas-1.5.3 numpy-1.23.5...
==> Starting service
```

Key indicators of success:
- "Using Python version 3.10.14"
- "Using cached ... cp310 ... manylinux ... .whl" (pre-compiled wheels)
- No compilation errors

## If It Still Fails

### Option 1: Contact Render Support
Ask them why `runtime.txt` is being ignored and request Python 3.10.14.

### Option 2: Try Alternative Hosting

**PythonAnywhere** (Free tier available):
- Go to https://www.pythonanywhere.com
- Free tier includes Python 3.10
- Upload your code
- Configure web app

**Heroku** (Free tier discontinued, but has paid options):
- Similar to Render
- Better Python version control

**Railway** (Free trial):
- Go to https://railway.app
- Better Python version detection
- Similar to Render

## Success Checklist

- [ ] Created `render.yaml` file
- [ ] Created `.python-version` file
- [ ] Updated `requirements.txt` to older versions
- [ ] Pushed all changes to GitHub
- [ ] Manually set PYTHON_VERSION=3.10.14 in Render dashboard
- [ ] Selected Python 3 environment in Render
- [ ] Deployment successful
- [ ] Build logs show Python 3.10.14
- [ ] Build logs show "Using cached ... .whl" (not compiling)

---

**If this works**: Bookmark your live URL and enjoy your scanner!

**If this doesn't work**: The issue is with Render's Python version management. Consider alternative hosting platforms listed above.

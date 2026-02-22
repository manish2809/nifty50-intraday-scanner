# 🚀 Deployment Guide - Step by Step

## 📋 Prerequisites

- GitHub account (free)
- Render account (free)
- Git installed on your computer

---

## 🎯 Step-by-Step Deployment

### Step 1: Prepare Your Code (Already Done! ✓)

All files are ready in the `Web_Scanner` folder:
- ✅ `app.py` - Main application
- ✅ `templates/index.html` - Web interface
- ✅ `requirements.txt` - Dependencies
- ✅ `Procfile` - Render configuration
- ✅ `runtime.txt` - Python version
- ✅ `.gitignore` - Git ignore rules

---

### Step 2: Create GitHub Repository

#### 2.1 Create Repository on GitHub

1. Go to https://github.com
2. Click the **"+"** icon (top right) → **"New repository"**
3. Fill in:
   - **Repository name**: `nifty50-intraday-scanner`
   - **Description**: `Live intraday scanner for Nifty 50 stocks with entry/exit levels`
   - **Visibility**: Public
   - **DO NOT** initialize with README (we have our own)
4. Click **"Create repository"**

#### 2.2 Push Code to GitHub

Open Command Prompt in the `Web_Scanner` folder and run:

```bash
# Initialize git repository
git init

# Add all files
git add .

# Commit files
git commit -m "Initial commit - Nifty 50 Intraday Scanner"

# Rename branch to main
git branch -M main

# Add remote repository (replace YOUR_USERNAME with your GitHub username)
git remote add origin https://github.com/YOUR_USERNAME/nifty50-intraday-scanner.git

# Push to GitHub
git push -u origin main
```

**Example:**
```bash
git remote add origin https://github.com/manishkhemlani/nifty50-intraday-scanner.git
```

---

### Step 3: Deploy on Render

#### 3.1 Sign Up / Log In

1. Go to https://render.com
2. Click **"Get Started"**
3. Sign up with **GitHub** (easiest option)
4. Authorize Render to access your GitHub

#### 3.2 Create New Web Service

1. Click **"New +"** (top right)
2. Select **"Web Service"**
3. Click **"Connect a repository"**
4. Find and select: `nifty50-intraday-scanner`
5. Click **"Connect"**

#### 3.3 Configure Service

Fill in the following:

| Field | Value |
|-------|-------|
| **Name** | `nifty50-scanner` (or any name you like) |
| **Region** | Choose closest to India (Singapore recommended) |
| **Branch** | `main` |
| **Root Directory** | Leave empty |
| **Environment** | `Python 3` |
| **Build Command** | `pip install -r requirements.txt` |
| **Start Command** | `gunicorn app:app` |
| **Plan** | **Free** |

#### 3.4 Advanced Settings (Optional)

Click **"Advanced"** and add:

| Environment Variable | Value |
|---------------------|-------|
| `PYTHON_VERSION` | `3.11.7` |

#### 3.5 Deploy

1. Click **"Create Web Service"**
2. Wait for deployment (5-10 minutes)
3. Watch the logs for progress

---

### Step 4: Access Your Scanner

Once deployed, you'll see:

```
Your service is live at https://nifty50-scanner.onrender.com
```

**Bookmark this URL!** This is your live scanner.

---

## 🎉 Success! Your Scanner is Live!

### What You Can Do Now:

1. **Share the link** with friends
2. **Bookmark it** for daily use
3. **Open on mobile** - it's responsive!
4. **Access anytime** - no installation needed

---

## 🔧 Troubleshooting

### Issue 1: Deployment Failed

**Error: "Build failed"**

**Solution:**
1. Check Render logs for specific error
2. Verify all files are pushed to GitHub
3. Check `requirements.txt` is correct

**Error: "TA-Lib installation failed"**

**Solution:**
TA-Lib requires compilation. For Render free tier, we need to use a workaround.

Edit `requirements.txt` and remove `TA-Lib==0.4.28`, then update `app.py` to use pandas-based RSI:

```python
def calculate_rsi(data, period=14):
    delta = data.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    rs = gain / loss
    return 100 - (100 / (1 + rs))

# Replace ta.RSI with:
rsi = calculate_rsi(df['Close'], timeperiod=14).iloc[-1]
```

Then push changes:
```bash
git add .
git commit -m "Fix TA-Lib dependency"
git push
```

Render will auto-deploy the update.

---

### Issue 2: Service Spins Down

**Problem:** First load takes 30-60 seconds after inactivity

**Why:** Render free tier spins down after 15 minutes of no activity

**Solutions:**
1. **Accept it** - It's free! Just wait 30 seconds on first load
2. **Keep it alive** - Open the link daily
3. **Upgrade** - $7/month for always-on service

---

### Issue 3: Data Not Loading

**Check:**
1. Is market open? (9:15 AM - 3:30 PM IST, Mon-Fri)
2. Check browser console (F12) for errors
3. Click the Refresh button
4. Check Render logs for errors

---

## 📊 Monitoring Your App

### View Logs

1. Go to Render dashboard
2. Click on your service
3. Click **"Logs"** tab
4. See real-time logs

### Check Status

1. Dashboard shows service status
2. Green = Running
3. Yellow = Deploying
4. Red = Error

---

## 🔄 Updating Your Scanner

### Make Changes Locally

1. Edit files in `Web_Scanner` folder
2. Test locally: `python app.py`
3. Open `http://localhost:5000`

### Push Updates

```bash
git add .
git commit -m "Description of changes"
git push
```

Render will automatically detect changes and redeploy!

---

## 💡 Tips & Best Practices

### Performance

1. **Cache Duration**: 5 minutes is optimal (balance between freshness and API limits)
2. **Auto-Refresh**: 5 minutes in browser prevents excessive requests
3. **First Load**: Always slower on free tier, subsequent loads are fast

### Usage

1. **Best Time**: Open at 10 AM after market opens
2. **Refresh**: Click refresh button for latest data
3. **Mobile**: Works great on phones - add to home screen
4. **Sharing**: Safe to share the link - no sensitive data

### Cost

1. **Free Tier**: 750 hours/month (enough for daily use)
2. **Paid Tier**: $7/month for always-on, faster loading
3. **No Hidden Costs**: Free tier is truly free

---

## 🎯 Next Steps

### Enhancements You Can Add

1. **Historical Data**: Show past performance
2. **Alerts**: Email/SMS when strong signals appear
3. **Filters**: Filter by sector, price range, etc.
4. **Charts**: Add price charts for each stock
5. **Watchlist**: Save favorite stocks

### Custom Domain (Paid Plan)

1. Buy domain (e.g., `niftyscanner.com`)
2. Upgrade Render plan
3. Add custom domain in Render settings
4. Update DNS records

---

## ✅ Deployment Checklist

- [ ] Created GitHub repository
- [ ] Pushed code to GitHub
- [ ] Created Render account
- [ ] Connected GitHub to Render
- [ ] Configured web service
- [ ] Deployment successful
- [ ] Tested the live URL
- [ ] Bookmarked the URL
- [ ] Shared with friends (optional)

---

## 📞 Need Help?

### Resources

- **Render Docs**: https://render.com/docs
- **Flask Docs**: https://flask.palletsprojects.com/
- **GitHub Docs**: https://docs.github.com/

### Common Issues

1. **Forgot GitHub username**: Check https://github.com/settings/profile
2. **Git not installed**: Download from https://git-scm.com/
3. **Render deployment stuck**: Check logs, may need to restart

---

## 🎉 Congratulations!

Your Nifty 50 Intraday Scanner is now live and accessible from anywhere!

**Your Live URL**: `https://nifty50-scanner.onrender.com`

**Happy Trading! 📊📈**

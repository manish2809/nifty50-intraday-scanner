# 🌐 Nifty 50 Intraday Scanner - Web Application

Live web-based intraday scanner for Nifty 50 stocks. Access anytime from anywhere!

## 🚀 Features

- ✅ **Live Data**: Real-time analysis of all 50 Nifty stocks
- ✅ **Entry/Exit Levels**: Precise entry, stop loss, and target prices
- ✅ **Auto-Refresh**: Updates every 5 minutes automatically
- ✅ **Mobile Responsive**: Works on all devices
- ✅ **No Installation**: Just open the link in your browser
- ✅ **Free Hosting**: Deployed on Render (free tier)

## 📊 What You Get

- **Trading Signals**: STRONG BUY, BUY, NEUTRAL, SELL, STRONG SELL
- **Entry Price**: Suggested entry point for each trade
- **Stop Loss**: Maximum loss exit point
- **Target 1 & 2**: Two profit targets
- **Risk:Reward Ratio**: For each opportunity
- **Trading Strategy**: VWAP Breakout, Momentum Scalp, Gap Trade, etc.
- **Technical Indicators**: RSI, Volume Ratio, Trend direction

## 🌐 Deployment on Render

### Step 1: Create GitHub Repository

1. Go to [GitHub](https://github.com)
2. Click "New Repository"
3. Name: `nifty50-intraday-scanner`
4. Description: `Live intraday scanner for Nifty 50 stocks`
5. Public repository
6. Click "Create repository"

### Step 2: Push Code to GitHub

```bash
cd Web_Scanner
git init
git add .
git commit -m "Initial commit - Nifty 50 Intraday Scanner"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/nifty50-intraday-scanner.git
git push -u origin main
```

### Step 3: Deploy on Render

1. Go to [Render](https://render.com)
2. Sign up / Log in (use GitHub account)
3. Click "New +" → "Web Service"
4. Connect your GitHub repository: `nifty50-intraday-scanner`
5. Configure:
   - **Name**: `nifty50-scanner`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`
   - **Plan**: Free
6. Click "Create Web Service"
7. Wait 5-10 minutes for deployment

### Step 4: Access Your Scanner

Your scanner will be live at:
```
https://nifty50-scanner.onrender.com
```

(Replace with your actual Render URL)

## 🔧 Local Development

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Run Locally

```bash
python app.py
```

Open browser: `http://localhost:5000`

## 📱 How to Use

1. **Open the link** in your browser
2. **Wait for data to load** (takes 10-20 seconds first time)
3. **Review top opportunities** (sorted by score)
4. **Check entry/exit levels** for stocks you want to trade
5. **Click Refresh** button to get latest data
6. **Auto-refreshes** every 5 minutes

## 🎯 Trading Workflow

1. Open scanner link at 10 AM (after market opens)
2. Look for STRONG BUY or BUY signals
3. Enter at suggested Entry price
4. Set Stop Loss immediately
5. Book 50% profit at Target 1
6. Book remaining 50% at Target 2
7. Trail stop loss after Target 1

## ⚙️ Configuration

### Cache Duration

Data is cached for 5 minutes to reduce API calls. To change:

Edit `app.py`:
```python
CACHE_DURATION = 300  # Change to desired seconds
```

### Auto-Refresh Interval

To change auto-refresh interval in browser:

Edit `templates/index.html`:
```javascript
setInterval(loadData, 300000);  // Change to desired milliseconds
```

## 🔒 Important Notes

### Render Free Tier Limitations

- **Spins down after 15 minutes of inactivity**
- **First load after inactivity takes 30-60 seconds**
- **750 hours/month free** (enough for daily use)
- **No credit card required**

### Solution for Spin-Down

Add to favorites and open daily. Or upgrade to paid plan ($7/month) for always-on service.

## 📊 API Endpoints

### GET /
Main web interface

### GET /api/scanner
Returns JSON data:
```json
{
  "success": true,
  "timestamp": "22 February 2026, 10:30 AM IST",
  "stats": {
    "total": 50,
    "strong_buy": 5,
    "buy": 8,
    "avg_risk_reward": 1.65
  },
  "data": [...]
}
```

### GET /api/refresh
Force refresh data (clears cache)

## 🛠️ Troubleshooting

### Deployment Failed

**Error: "TA-Lib installation failed"**
- Render doesn't support TA-Lib by default
- Solution: Use alternative indicators or upgrade to paid plan with custom buildpack

**Workaround**: Remove TA-Lib dependency and use pandas for indicators:
```python
# Replace ta.RSI with:
def calculate_rsi(data, period=14):
    delta = data.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    rs = gain / loss
    return 100 - (100 / (1 + rs))
```

### Slow Loading

- First load after inactivity takes time (Render free tier)
- Subsequent loads are fast (cached data)
- Consider paid plan for instant loading

### Data Not Updating

- Check if market is open
- Click Refresh button
- Check browser console for errors

## 📈 Upgrade Options

### Render Paid Plan ($7/month)

- Always-on (no spin-down)
- Faster loading
- Custom domain support
- More resources

### Alternative Hosting

- **Heroku**: Similar to Render
- **PythonAnywhere**: Free tier available
- **AWS/GCP**: More complex but scalable

## ⚠️ Disclaimer

This scanner is for educational purposes only. Not financial advice.
Always use stop losses and trade at your own risk.
Past performance does not guarantee future results.

## 📞 Support

For issues:
1. Check browser console for errors
2. Verify market is open
3. Try refreshing the page
4. Check Render deployment logs

## 🎉 You're All Set!

Your scanner is now live and accessible from anywhere!
Share the link with friends or bookmark it for daily use.

**Happy Trading! 📊📈**

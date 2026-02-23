"""
Nifty 50 Intraday Scanner - Web Application
Hosted on Render - Access anytime for live intraday suggestions
"""

from flask import Flask, render_template, jsonify
import pandas as pd
import numpy as np
import yfinance as yf
from datetime import datetime, timedelta
import pytz
import os

app = Flask(__name__)

# Nifty 50 tickers (Updated as of Sep 30, 2024 - Added BEL & TRENT, Removed DIVISLAB & LTIM)
TICKERS = [
    "ADANIENT.NS", "ADANIPORTS.NS", "APOLLOHOSP.NS", "ASIANPAINT.NS", "AXISBANK.NS",
    "BAJAJ-AUTO.NS", "BAJFINANCE.NS", "BAJAJFINSV.NS", "BEL.NS", "BPCL.NS",
    "BHARTIARTL.NS", "BRITANNIA.NS", "CIPLA.NS", "COALINDIA.NS", "DRREDDY.NS",
    "EICHERMOT.NS", "GRASIM.NS", "HCLTECH.NS", "HDFCBANK.NS", "HDFCLIFE.NS",
    "HEROMOTOCO.NS", "HINDALCO.NS", "HINDUNILVR.NS", "ICICIBANK.NS", "ITC.NS",
    "INDUSINDBK.NS", "INFY.NS", "JSWSTEEL.NS", "KOTAKBANK.NS", "LT.NS",
    "M&M.NS", "MARUTI.NS", "NESTLEIND.NS", "NTPC.NS", "ONGC.NS",
    "POWERGRID.NS", "RELIANCE.NS", "SBILIFE.NS", "SBIN.NS", "SUNPHARMA.NS",
    "TCS.NS", "TATACONSUM.NS", "TATASTEEL.NS", "TECHM.NS", "TITAN.NS",
    "TMCV.NS", "TRENT.NS", "ULTRACEMCO.NS", "UPL.NS", "WIPRO.NS", "ETERNAL.NS"
]

# Cache for scanner data (refresh every 5 minutes)
cache = {'data': None, 'timestamp': None}
CACHE_DURATION = 300  # 5 minutes in seconds


def calculate_atr(df, period=14):
    """Calculate Average True Range"""
    high = df['High']
    low = df['Low']
    close = df['Close']
    tr1 = high - low
    tr2 = abs(high - close.shift())
    tr3 = abs(low - close.shift())
    tr = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)
    atr = tr.rolling(window=period).mean()
    return atr.iloc[-1] if len(atr) > 0 else 0


def calculate_rsi(data, period=14):
    """Calculate RSI using pandas"""
    delta = data.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    return rsi.iloc[-1] if len(rsi) > 0 else 50


def calculate_ema(data, period):
    """Calculate EMA using pandas"""
    ema = data.ewm(span=period, adjust=False).mean()
    return ema.iloc[-1] if len(ema) > 0 else data.iloc[-1]



def calculate_entry_exit(close, atr, vwap, signal, rsi):
    """Calculate precise entry, target, and stop loss levels"""
    if signal in ['STRONG BUY', 'BUY']:
        entry = round(close * 0.998, 2)
        stop_loss = round(entry - (atr * 0.5), 2)
        target1 = round(entry + (atr * 0.75), 2)
        target2 = round(entry + (atr * 1.5), 2)
        risk_reward = round((target1 - entry) / (entry - stop_loss), 2) if (entry - stop_loss) > 0 else 1.5
    elif signal in ['STRONG SELL', 'SELL']:
        entry = round(close * 1.002, 2)
        stop_loss = round(entry + (atr * 0.5), 2)
        target1 = round(entry - (atr * 0.75), 2)
        target2 = round(entry - (atr * 1.5), 2)
        risk_reward = round((entry - target1) / (stop_loss - entry), 2) if (stop_loss - entry) > 0 else 1.5
    else:
        entry = round(vwap, 2)
        stop_loss = round(entry - (atr * 0.3), 2)
        target1 = round(entry + (atr * 0.5), 2)
        target2 = round(entry + (atr * 1.0), 2)
        risk_reward = 1.5
    
    return entry, stop_loss, target1, target2, risk_reward


def analyze_stock(df, ticker):
    """Comprehensive analysis with entry/exit levels"""
    try:
        if len(df) < 20:
            return None
        
        close = df['Close'].iloc[-1]
        prev_close = df['Close'].iloc[-2]
        volume = df['Volume'].iloc[-1]
        avg_volume = df['Volume'].rolling(20).mean().iloc[-1]
        
        atr = calculate_atr(df)
        atr_pct = (atr / close) * 100 if close > 0 else 0
        vwap = ((df['High'] + df['Low'] + df['Close']) / 3 * df['Volume']).sum() / df['Volume'].sum()
        vwap_distance = ((close - vwap) / vwap) * 100
        rsi = calculate_rsi(df['Close'], period=14)
        ema9 = calculate_ema(df['Close'], period=9)
        ema21 = calculate_ema(df['Close'], period=21)
        volume_ratio = volume / avg_volume if avg_volume > 0 else 0
        price_change_pct = ((close - prev_close) / prev_close) * 100
        
        # Scoring
        momentum_score = 2 if close > ema9 > ema21 else (-2 if close < ema9 < ema21 else 0)
        volume_score = 2 if volume_ratio > 1.5 else (1 if volume_ratio > 1.2 else 0)
        volatility_score = 2 if atr_pct > 2.0 else (1 if atr_pct > 1.5 else 0)
        rsi_score = 2 if 40 < rsi < 60 else (1 if (60 < rsi < 70 or 30 < rsi < 40) else -1)
        final_score = momentum_score + volume_score + volatility_score + rsi_score
        
        # Signal
        if final_score >= 5:
            signal = "STRONG BUY"
        elif final_score >= 3:
            signal = "BUY"
        elif final_score <= -5:
            signal = "STRONG SELL"
        elif final_score <= -3:
            signal = "SELL"
        else:
            signal = "NEUTRAL"
        
        # Strategy
        if close > vwap and rsi < 70 and volume_ratio > 1.2:
            strategy = "VWAP Breakout"
        elif close < vwap and rsi > 30 and volume_ratio > 1.2:
            strategy = "VWAP Support"
        elif abs(price_change_pct) > 2:
            strategy = "Gap Trade"
        elif atr_pct > 2 and 40 < rsi < 60:
            strategy = "Momentum Scalp"
        else:
            strategy = "Range Trade"
        
        entry, stop_loss, target1, target2, risk_reward = calculate_entry_exit(close, atr, vwap, signal, rsi)
        
        return {
            'ticker': ticker.replace('.NS', '').replace('ETERNAL', 'ZOMATO').replace('TMCV', 'TATAMOTORS-CV'),
            'ltp': round(close, 2),
            'change_pct': round(price_change_pct, 2),
            'volume_ratio': round(volume_ratio, 2),
            'atr_pct': round(atr_pct, 2),
            'rsi': round(rsi, 1),
            'vwap': round(vwap, 2),
            'vwap_dist': round(vwap_distance, 2),
            'trend': 'Bullish' if close > ema9 > ema21 else 'Bearish' if close < ema9 < ema21 else 'Neutral',
            'score': final_score,
            'signal': signal,
            'strategy': strategy,
            'entry': entry,
            'stop_loss': stop_loss,
            'target1': target1,
            'target2': target2,
            'risk_reward': risk_reward
        }
    except:
        return None



def get_scanner_data():
    """Get scanner data with caching"""
    global cache
    
    # Check if cache is valid
    if cache['data'] is not None and cache['timestamp'] is not None:
        if (datetime.now() - cache['timestamp']).seconds < CACHE_DURATION:
            return cache['data']
    
    # Download fresh data
    end_date = datetime.now()
    start_date = end_date - timedelta(days=60)
    
    try:
        print(f"[Scanner] Downloading data for {len(TICKERS)} stocks...")
        data = yf.download(TICKERS, start=start_date, end=end_date, group_by='ticker', 
                          auto_adjust=True, threads=True, progress=False)
        
        print(f"[Scanner] Data downloaded. Shape: {data.shape}")
        
        # Analyze all stocks
        results = []
        errors = 0
        for ticker in TICKERS:
            try:
                df = data[ticker][['Open', 'High', 'Low', 'Close', 'Volume']].dropna()
                if len(df) >= 20:
                    result = analyze_stock(df, ticker)
                    if result:
                        results.append(result)
                else:
                    errors += 1
            except Exception as e:
                errors += 1
                print(f"[Scanner] Error analyzing {ticker}: {e}")
                continue
        
        print(f"[Scanner] Analysis complete: {len(results)} stocks, {errors} errors")
        
        # Sort by score
        results.sort(key=lambda x: x['score'], reverse=True)
        
        # Update cache
        cache['data'] = results
        cache['timestamp'] = datetime.now()
        
        return results
    except Exception as e:
        print(f"[Scanner] Error fetching data: {e}")
        return []


@app.route('/')
def index():
    """Main page"""
    return render_template('index.html')


@app.route('/api/scanner')
def api_scanner():
    """API endpoint for scanner data"""
    data = get_scanner_data()
    
    # Calculate statistics
    strong_buy = len([x for x in data if x['signal'] == 'STRONG BUY'])
    buy = len([x for x in data if x['signal'] == 'BUY'])
    avg_rr = sum([x['risk_reward'] for x in data]) / len(data) if data else 0
    
    # Convert UTC to IST (UTC + 5:30)
    utc_now = datetime.now(pytz.UTC)
    ist_tz = pytz.timezone('Asia/Kolkata')
    ist_time = utc_now.astimezone(ist_tz)
    
    return jsonify({
        'success': True,
        'timestamp': ist_time.strftime('%d %B %Y, %I:%M %p IST'),
        'stats': {
            'total': len(data),
            'strong_buy': strong_buy,
            'buy': buy,
            'avg_risk_reward': round(avg_rr, 2)
        },
        'data': data
    })


@app.route('/api/refresh')
def api_refresh():
    """Force refresh data"""
    global cache
    cache['data'] = None
    cache['timestamp'] = None
    data = get_scanner_data()
    return jsonify({'success': True, 'message': 'Data refreshed', 'count': len(data)})


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)

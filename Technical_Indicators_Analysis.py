import talib
import yfinance as yf

def analyze_technical_indicators(ticker, period='1y'):
    """
    تحليل المؤشرات الفنية للسهم
    """
    # جلب بيانات السهم
    data = yf.download(ticker, period=period)
    
    # حساب المؤشرات الفنية
    indicators = {
        'RSI': talib.RSI(data['Close'], timeperiod=14),
        'MACD': talib.MACD(data['Close'])[0],  # خط MACD
        'BB_Upper': talib.BBANDS(data['Close'])[0],  # بوليجر باند العلوي
        'BB_Lower': talib.BBANDS(data['Close'])[2],  # بوليجر باند السفلي
        'SMA50': talib.SMA(data['Close'], timeperiod=50),
        'SMA200': talib.SMA(data['Close'], timeperiod=200)
    }
    
    # تحليل الإشارات
    analysis = {
        'Trend': 'صاعد' if indicators['SMA50'][-1] > indicators['SMA200'][-1] else 'هابط',
        'RSI_Signal': 'تشبع بيع' if indicators['RSI'][-1] < 30 else 
                     'تشبع شراء' if indicators['RSI'][-1] > 70 else 'محايد',
        'MACD_Signal': 'إيجابي' if indicators['MACD'][-1] > 0 else 'سلبي',
        'BB_Signal': 'قرب المقاومة' if data['Close'][-1] > indicators['BB_Upper'][-1] else
                    'قرب الدعم' if data['Close'][-1] < indicators['BB_Lower'][-1] else 'في النطاق'
    }
    
    return indicators, analysis

# تحليل المؤشرات
ticker = 'AAPL'
indicators, analysis = analyze_technical_indicators(ticker)
print(f"\nتحليل مؤشرات {ticker}:")
for key, value in analysis.items():
    print(f"{key}: {value}")

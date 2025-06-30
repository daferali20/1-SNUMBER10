import requests
from io import BytesIO
from PIL import Image
import matplotlib.pyplot as plt

def fetch_tradingview_chart(ticker, interval='1D', study_params=None):
    """
    جلب شارت TradingView لأي سهم
    :param ticker: رمز السهم (مثل AAPL, MSFT)
    :param interval: الإطار الزمني (1D, 1W, 4H...)
    :param study_params: معاملات الدراسات الفنية
    :return: صورة الشارت
    """
    base_url = "https://www.tradingview.com/chart/"
    
    # إعداد معاملات الرسم البياني
    params = {
        'symbol': ticker,
        'interval': interval,
        'studies': study_params or 'MA5,MA20,RSI14'
    }
    
    try:
        response = requests.get(base_url, params=params, stream=True)
        img = Image.open(BytesIO(response.content))
        return img
    except Exception as e:
        print(f"Error fetching chart: {e}")
        return None

# مثال للاستخدام
chart = fetch_tradingview_chart('AAPL', interval='1W', study_params='MACD,BB,Volume')
plt.imshow(chart)
plt.axis('off')
plt.show()

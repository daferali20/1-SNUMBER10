# analysis_functions.py
import yfinance as yf
import pandas as pd
import numpy as np
import requests
from io import BytesIO
from PIL import Image
import talib
from datetime import datetime, timedelta

def fetch_tradingview_chart(ticker, interval='1D', study_params=None):
    """
    جلب شارت TradingView لأي سهم
    :param ticker: رمز السهم (مثل AAPL, MSFT)
    :param interval: الإطار الزمني (1D, 1W, 4H...)
    :param study_params: معاملات الدراسات الفنية
    :return: صورة الشارت ككائن PIL Image
    """
    base_url = "https://www.tradingview.com/chart/"
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
        raise Exception(f"Error fetching chart: {e}")

def preprocess_chart_image(image):
    """
    معالجة صورة الشارت للتحليل
    :param image: صورة الشارت ككائن PIL Image
    :return: صورة معالجة (حواف)
    """
    try:
        # تحويل إلى تدرجات الرمادي
        gray = cv2.cvtColor(np.array(image), cv2.COLOR_BGR2GRAY)
        
        # تحسين التباين
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
        enhanced = clahe.apply(gray)
        
        # كشف الحواف
        edges = cv2.Canny(enhanced, 50, 150)
        return edges
    except Exception as e:
        raise Exception(f"Image processing error: {e}")

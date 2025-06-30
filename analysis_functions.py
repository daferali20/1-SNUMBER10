# analysis_functions.py
import yfinance as yf
import pandas as pd
import numpy as np
import requests
import cv2
from io import BytesIO
from PIL import Image
import talib
from datetime import datetime, timedelta
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image as kimage

# ثوابت التطبيق
TECH_PATTERNS_MODEL = "tech_patterns_model.h5"

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

def load_pattern_recognition_model(model_path=TECH_PATTERNS_MODEL):
    """تحميل نموذج التعرف على الأنماط"""
    try:
        return load_model(model_path)
    except Exception as e:
        raise Exception(f"Failed to load model: {e}")

def detect_chart_patterns(processed_image):
    """
    الكشف عن الأنماط الفنية في الشارت
    :param processed_image: الصورة المعالجة
    :return: قائمة بالأنماط المكتشفة وثقتها
    """
    try:
        model = load_pattern_recognition_model()
        img = kimage.img_to_array(processed_image)
        img = np.expand_dims(img, axis=0)
        img = img / 255.0
        
        predictions = model.predict(img)
        patterns = ['Head & Shoulders', 'Double Top', 'Double Bottom', 
                   'Triangle', 'Wedge', 'Channel', 'Flag']
        
        detected_patterns = {pattern: float(prob) for pattern, prob in zip(patterns, predictions[0])}
        return sorted(detected_patterns.items(), key=lambda x: x[1], reverse=True)
    except Exception as e:
        raise Exception(f"Pattern detection error: {e}")

def analyze_technical_indicators(ticker, period='1y'):
    """
    تحليل المؤشرات الفنية للسهم
    :param ticker: رمز السهم
    :param period: الفترة الزمنية (1y, 6mo, etc.)
    :return: المؤشرات الفنية والتحليل
    """
    try:
        # جلب بيانات السهم
        data = yf.download(ticker, period=period)
        if data.empty:
            raise Exception("No data available for this ticker")
        
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
    except Exception as e:
        raise Exception(f"Technical analysis error: {e}")

def generate_trading_recommendation(ticker):
    """
    توليد توصية تداول بناء على التحليل الفني
    :param ticker: رمز السهم
    :return: توصية التداول مع التفاصيل
    """
    try:
        # جلب البيانات والتحليل
        chart_img = fetch_tradingview_chart(ticker)
        processed_img = preprocess_chart_image(chart_img)
        patterns = detect_chart_patterns(processed_img)
        indicators, analysis = analyze_technical_indicators(ticker)
        
        # تقييم شامل
        score = 0
        reasons = []
        
        # تقييم الاتجاه
        if analysis['Trend'] == 'صاعد':
            score += 30
            reasons.append('الاتجاه العام صاعد')
        else:
            score -= 20
            reasons.append('الاتجاه العام هابط')
        
        # تقييم RSI
        if analysis['RSI_Signal'] == 'تشبع بيع':
            score += 15
            reasons.append('RSI في منطقة التشبع البيع (فرصة شراء)')
        elif analysis['RSI_Signal'] == 'تشبع شراء':
            score -= 10
            reasons.append('RSI في منطقة التشبع الشراء (احتمال تصحيح)')
        
        # تقييم النمط الفني
        main_pattern, confidence = patterns[0]
        if main_pattern in ['Double Bottom', 'Channel']:
            score += 25
            reasons.append(f'نمط {main_pattern} صاعد ({confidence:.0%} ثقة)')
        elif main_pattern in ['Double Top', 'Head & Shoulders']:
            score -= 20
            reasons.append(f'نمط {main_pattern} هابط ({confidence:.0%} ثقة)')
        
        # توليد التوصية
        if score >= 50:
            recommendation = 'شراء قوي'
        elif score >= 30:
            recommendation = 'شراء'
        elif score >= 0:
            recommendation = 'حياد'
        else:
            recommendation = 'بيع'
        
        return {
            'Ticker': ticker,
            'Recommendation': recommendation,
            'Score': score,
            'Reasons': reasons,
            'Main_Pattern': f"{main_pattern} ({confidence:.0%})",
            'Trend': analysis['Trend'],
            'RSI': f"{indicators['RSI'][-1]:.2f} ({analysis['RSI_Signal']})"
        }
    except Exception as e:
        raise Exception(f"Recommendation generation error: {e}")

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
TECH_PATTERNS_MODEL = "tech_patterns_model.h5"  # تأكد من وجود الملف في نفس الدليل

def load_pattern_recognition_model(model_path=TECH_PATTERNS_MODEL):
    """تحميل نموذج التعرف على الأنماط الفنية"""
    try:
        return load_model(model_path)
    except Exception as e:
        raise Exception(f"فشل في تحميل النموذج: {e}. تأكد من وجود الملف في المسار الصحيح")

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
        'studies': study_params or 'MA5,MA20,RSI14'  # دراسات فنية افتراضية
    }
    
    try:
        response = requests.get(base_url, params=params, stream=True)
        response.raise_for_status()  # التحقق من وجود أخطاء في الطلب
        img = Image.open(BytesIO(response.content))
        return img
    except Exception as e:
        raise Exception(f"خطأ في جلب الشارت: {e}")

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
        raise Exception(f"خطأ في معالجة الصورة: {e}")

def detect_chart_patterns(processed_image):
    """
    الكشف عن الأنماط الفنية في الشارت
    :param processed_image: الصورة المعالجة
    :return: قائمة بالأنماط المكتشفة وثقتها
    """
    try:
        model = load_pattern_recognition_model()
        
        # تحضير الصورة للنموذج
        img = kimage.img_to_array(processed_image)
        img = np.expand_dims(img, axis=0)
        img = img / 255.0  # تطبيع القيم
        
        # التنبؤ بالأنماط
        predictions = model.predict(img)
        patterns = ['Head & Shoulders', 'Double Top', 'Double Bottom', 
                   'Triangle', 'Wedge', 'Channel', 'Flag']
        
        detected_patterns = {pattern: float(prob) for pattern, prob in zip(patterns, predictions[0])}
        return sorted(detected_patterns.items(), key=lambda x: x[1], reverse=True)
    except Exception as e:
        raise Exception(f"خطأ في اكتشاف الأنماط: {e}")

# يمكنك إضافة الدوال الأخرى مثل analyze_technical_indicators و generate_trading_recommendation هنا

def generate_trading_recommendation(ticker):
    """
    توليد توصية تداول بناء على التحليل الفني
    """
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

# توليد التوصية
recommendation = generate_trading_recommendation('AAPL')
print("\nالتوصية النهائية:")
for key, value in recommendation.items():
    if key != 'Reasons':
        print(f"{key}: {value}")
print("\nأسباب التوصية:")
for reason in recommendation['Reasons']:
    print(f"- {reason}")

from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image as kimage

def load_pattern_recognition_model(model_path='tech_patterns_model.h5'):
    """تحميل نموذج الذكاء الاصطناعي المدرب مسبقًا"""
    return load_model(model_path)

def detect_chart_patterns(processed_image):
    """
    الكشف عن الأنماط الفنية في الشارت
    """
    model = load_pattern_recognition_model()
    
    # تحضير الصورة للنموذج
    img = kimage.img_to_array(processed_image)
    img = np.expand_dims(img, axis=0)
    img = img / 255.0
    
    # التنبؤ بالأنماط
    predictions = model.predict(img)
    patterns = ['Head & Shoulders', 'Double Top', 'Double Bottom', 
                'Triangle', 'Wedge', 'Channel', 'Flag']
    
    detected_patterns = {pattern: float(prob) for pattern, prob in zip(patterns, predictions[0])}
    
    return sorted(detected_patterns.items(), key=lambda x: x[1], reverse=True)

# الكشف عن الأنماط
patterns = detect_chart_patterns(processed_chart)
print("الأنماط المكتشفة:")
for pattern, confidence in patterns[:3]:  # عرض أهم 3 أنماط
    print(f"- {pattern}: {confidence:.2%} ثقة")

import cv2
import numpy as np

def preprocess_chart_image(image):
    """
    معالجة صورة الشارت للتحليل
    """
    # تحويل إلى تدرجات الرمادي
    gray = cv2.cvtColor(np.array(image), cv2.COLOR_BGR2GRAY)
    
    # تحسين التباين
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
    enhanced = clahe.apply(gray)
    
    # كشف الحواف
    edges = cv2.Canny(enhanced, 50, 150)
    
    return edges

# معالجة الشارت
processed_chart = preprocess_chart_image(chart)
plt.imshow(processed_chart, cmap='gray')
plt.show()

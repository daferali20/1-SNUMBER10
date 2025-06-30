import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QLabel, QLineEdit, QPushButton, 
                             QComboBox, QTextEdit, QTabWidget, QTableWidget,
                             QTableWidgetItem, QGraphicsView, QGraphicsScene)
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import Qt
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
# استيراد دوال التحليل من ملف منفصل
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout,
    QHBoxLayout, QLabel, QLineEdit, QPushButton,
    QComboBox, QTextEdit, QTabWidget, QTableWidget,
    QTableWidgetItem, QGraphicsView, QGraphicsScene
)
class TechnicalAnalysisApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("نظام التحليل الفني المتقدم - الذكاء الاصطناعي")
        self.setGeometry(100, 100, 1200, 800)
        
        # العناصر الرئيسية
        self.initUI()
        
        # بيانات التطبيق
        self.current_ticker = None
        self.current_chart = None
        self.analysis_results = None
    
    def initUI(self):
        """تهيئة واجهة المستخدم"""
        main_widget = QWidget()
        main_layout = QHBoxLayout()
        
        # الشريط الجانبي
        sidebar = self.create_sidebar()
        main_layout.addLayout(sidebar, 1)
        
        # منطقة العرض الرئيسية
        self.main_area = self.create_main_area()
        main_layout.addWidget(self.main_area, 4)
        
        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)
    
    def create_sidebar(self):
        """إنشاء الشريط الجانبي للتحكم"""
        sidebar_layout = QVBoxLayout()
        
        # عنوان التطبيق
        title = QLabel("نظام التحليل الفني بالذكاء الاصطناعي")
        title.setStyleSheet("font-size: 18px; font-weight: bold;")
        sidebar_layout.addWidget(title)
        
        # حقل إدخال رمز السهم
        self.ticker_input = QLineEdit()
        self.ticker_input.setPlaceholderText("أدخل رمز السهم (مثل AAPL, MSFT)")
        sidebar_layout.addWidget(self.ticker_input)
        
        # إطار زمني
        self.timeframe_combo = QComboBox()
        self.timeframe_combo.addItems(["1 يوم", "1 أسبوع", "1 شهر", "4 ساعات", "1 ساعة"])
        sidebar_layout.addWidget(self.timeframe_combo)
        
        # مؤشرات فنية
        self.indicators_combo = QComboBox()
        self.indicators_combo.addItems(["المؤشرات الأساسية", "RSI + MACD", "بوليجر باند + حجم", "جميع المؤشرات"])
        sidebar_layout.addWidget(self.indicators_combo)
        
        # زر التحليل
        analyze_btn = QPushButton("تحليل السهم")
        analyze_btn.clicked.connect(self.analyze_stock)
        analyze_btn.setStyleSheet("background-color: #4CAF50; color: white;")
        sidebar_layout.addWidget(analyze_btn)
        
        # نتائج سريعة
        self.quick_results = QTextEdit()
        self.quick_results.setReadOnly(True)
        sidebar_layout.addWidget(self.quick_results)
        
        # زر حفظ التقرير
        save_btn = QPushButton("حفظ التقرير")
        save_btn.clicked.connect(self.save_report)
        sidebar_layout.addWidget(save_btn)
        
        # مساحة فارغة
        sidebar_layout.addStretch()
        
        return sidebar_layout
    
    def create_main_area(self):
        """إنشاء منطقة العرض الرئيسية"""
        tabs = QTabWidget()
        
        # تبويب الشارت
        self.chart_tab = QWidget()
        self.chart_layout = QVBoxLayout()
        
        self.chart_canvas = MplCanvas(self, width=10, height=6)
        self.chart_layout.addWidget(self.chart_canvas)
        
        self.chart_tab.setLayout(self.chart_layout)
        tabs.addTab(self.chart_tab, "الشارت الفني")
        
        # تبويب التحليل الفني
        self.analysis_tab = QWidget()
        self.analysis_layout = QVBoxLayout()
        
        self.patterns_table = QTableWidget()
        self.patterns_table.setColumnCount(3)
        self.patterns_table.setHorizontalHeaderLabels(["النمط", "الثقة", "التفسير"])
        self.analysis_layout.addWidget(self.patterns_table)
        
        self.indicators_table = QTableWidget()
        self.indicators_table.setColumnCount(2)
        self.indicators_table.setHorizontalHeaderLabels(["المؤشر", "القيمة"])
        self.analysis_layout.addWidget(self.indicators_table)
        
        self.analysis_tab.setLayout(self.analysis_layout)
        tabs.addTab(self.analysis_tab, "التحليل الفني")
        
        # تبويب التوصيات
        self.recommendation_tab = QWidget()
        self.recommendation_layout = QVBoxLayout()
        
        self.recommendation_text = QTextEdit()
        self.recommendation_text.setReadOnly(True)
        self.recommendation_layout.addWidget(self.recommendation_text)
        
        self.recommendation_tab.setLayout(self.recommendation_layout)
        tabs.addTab(self.recommendation_tab, "التوصية")
        
        return tabs
    
    def analyze_stock(self):
      """تحليل السهم المحدد"""
      ticker = self.ticker_input.text().strip().upper()
      if not ticker:
          self.show_error("الرجاء إدخال رمز سهم صالح")
          return
    
    self.current_ticker = ticker
    timeframe = self.timeframe_combo.currentText()
    indicators = self.indicators_combo.currentText()
    
    # جلب البيانات وعرضها (هنا نستخدم الدوال التي سبق تعريفها)
    try:
        # جلب الشارت وعرضه
        chart_img = fetch_tradingview_chart(ticker, self.map_timeframe(timeframe))
        self.display_chart(chart_img)
            
        # تحليل الأنماط
        processed_img = preprocess_chart_image(chart_img)
        patterns = detect_chart_patterns(processed_img)
        self.display_patterns(patterns)
            
        # تحليل المؤشرات
        indicators_data, analysis = analyze_technical_indicators(ticker)
        self.display_indicators(indicators_data, analysis)
            
        # توليد التوصية
        recommendation = generate_trading_recommendation(ticker)
        self.display_recommendation(recommendation)
            
        # عرض النتائج السريعة
        self.quick_results.setPlainText(
            f"النتائج لـ {ticker}:\n"
            f"الاتجاه: {analysis['Trend']}\n"
            f"إشارة RSI: {analysis['RSI_Signal']}\n"
            f"النمط الرئيسي: {patterns[0][0]} ({patterns[0][1]:.0%} ثقة)\n"
            f"التوصية: {recommendation['Recommendation']}"
        )
            
    except Exception as e:
        self.show_error(f"حدث خطأ أثناء تحليل السهم: {str(e)}")
    
    def display_chart(self, chart_img):
        """عرض الشارت في واجهة المستخدم"""
        # تحويل الصورة لتنسيق مناسب لـ matplotlib
        img_array = np.array(chart_img)
        self.chart_canvas.figure.clear()
        ax = self.chart_canvas.figure.add_subplot(111)
        ax.imshow(img_array)
        ax.axis('off')
        self.chart_canvas.draw()
    
    def display_patterns(self, patterns):
        """عرض الأنماط المكتشفة في الجدول"""
        self.patterns_table.setRowCount(len(patterns))
        
        for row, (pattern, confidence) in enumerate(patterns):
            self.patterns_table.setItem(row, 0, QTableWidgetItem(pattern))
            self.patterns_table.setItem(row, 1, QTableWidgetItem(f"{confidence:.2%}"))
            
            # إضافة تفسير للنمط
            explanation = self.get_pattern_explanation(pattern)
            self.patterns_table.setItem(row, 2, QTableWidgetItem(explanation))
    
    def display_indicators(self, indicators, analysis):
        """عرض المؤشرات الفنية"""
        indicators_to_show = [
            ('RSI', f"{indicators['RSI'][-1]:.2f} ({analysis['RSI_Signal']})"),
            ('MACD', f"{indicators['MACD'][-1]:.2f} ({analysis['MACD_Signal']})"),
            ('الاتجاه', analysis['Trend']),
            ('إشارة البولينجر باند', analysis['BB_Signal']),
            ('المتوسط المتحرك 50 يوم', f"{indicators['SMA50'][-1]:.2f}"),
            ('المتوسط المتحرك 200 يوم', f"{indicators['SMA200'][-1]:.2f}")
        ]
        
        self.indicators_table.setRowCount(len(indicators_to_show))
        
        for row, (indicator, value) in enumerate(indicators_to_show):
            self.indicators_table.setItem(row, 0, QTableWidgetItem(indicator))
            self.indicators_table.setItem(row, 1, QTableWidgetItem(value))
    
    def display_recommendation(self, recommendation):
        """عرض التوصية الكاملة"""
        text = f"توصية التداول لـ {recommendation['Ticker']}:\n\n"
        text += f"التوصية: {recommendation['Recommendation']} (درجة: {recommendation['Score']}/100)\n\n"
        text += "الأسباب:\n"
        
        for reason in recommendation['Reasons']:
            text += f"- {reason}\n"
        
        text += f"\nالنمط الرئيسي: {recommendation['Main_Pattern']}\n"
        text += f"الاتجاه: {recommendation['Trend']}\n"
        text += f"RSI: {recommendation['RSI']}"
        
        self.recommendation_text.setPlainText(text)
    
    def map_timeframe(self, tf_text):
        """تحويل الإطار الزمني من نص إلى قيمة TradingView"""
        mapping = {
            "1 يوم": "1D",
            "1 أسبوع": "1W",
            "1 شهر": "1M",
            "4 ساعات": "4H",
            "1 ساعة": "1H"
        }
        return mapping.get(tf_text, "1D")
    
    def get_pattern_explanation(self, pattern):
        """إرجاع تفسير للنمط الفني"""
        explanations = {
            "Head & Shoulders": "نمط انعكاسي هابط، يشير إلى نهاية الاتجاه الصاعد",
            "Double Top": "نمط انعكاسي هابط، يشير إلى مقاومة قوية",
            "Double Bottom": "نمط انعكاسي صاعد، يشير إلى دعم قوي",
            "Triangle": "نمط استمراري، يشير إلى استمرار الاتجاه بعد الاختراق",
            "Wedge": "نمط انعكاسي، إما صاعد أو هابط حسب السياق",
            "Channel": "نمط اتجاهي، يشير إلى استمرار الحركة في القناة",
            "Flag": "نمط استمراري، يشير إلى استمرار الاتجاه بعد التصحيح"
        }
        return explanations.get(pattern, "لا يوجد تفسير متاح لهذا النمط")
    
    def save_report(self):
        """حفظ التقرير كملف PDF"""
        # يمكن تنفيذ هذه الوظيفة باستخدام مكتبة مثل FPDF أو ReportLab
        pass
    
    def show_error(self, message):
        """عرض رسالة خطأ"""
        self.quick_results.setPlainText(f"خطأ: {message}")

class MplCanvas(FigureCanvas):
    """لوحة لعرض شارت matplotlib"""
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        self.fig, self.ax = plt.subplots(figsize=(width, height), dpi=dpi)
        super().__init__(self.fig)
        self.setParent(parent)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TechnicalAnalysisApp()
    window.show()
    sys.exit(app.exec_())

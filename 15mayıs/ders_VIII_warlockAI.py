import sys
import sqlite3
import requests
import  random
from PyQt5.QtWidgets import (QMainWindow, QApplication, QTabWidget, QWidget,
                             QVBoxLayout, QTextEdit, QPushButton, QTextBrowser)
from PyQt5.QtGui import QColor
from PyQt5.QtCore import QThread, pyqtSignal

api_key = "AIzaSyB4QcoH-GUEyCQWdgxdhRR85QqzFG_5gq0"
api_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={api_key}"

def apply_styles(self):
    # Modern tasarım için stil sayfası
    style = """
        QMainWindow {
            background-color: #F0F4F8;
        }
        QTabWidget::pane {
            border: 1px solid #D3DCE6;
            background: #FFFFFF;
            border-radius: 8px;
        }
        QTabBar::tab {
            background: #E1E8ED;
            border: 1px solid #D3DCE6;
            padding: 8px 16px;
            margin-right: 2px;
            border-top-left-radius: 6px;
            border-top-right-radius: 6px;
        }
        QTabBar::tab:selected {
            background: #4A90E2;
            color: #FFFFFF;
            border-bottom: 1px solid #4A90E2;
        }
        QTextEdit, QTextBrowser {
            border: 1px solid #D3DCE6;
            border-radius: 6px;
            padding: 8px;
            background: #FFFFFF;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        QPushButton {
            background-color: #4A90E2;
            color: #FFFFFF;
            border: none;
            padding: 8px 16px;
            border-radius: 6px;
            font-weight: bold;
            box-shadow: 0 2px 4px rgba(0,0,0,0.2);
        }
        QPushButton:hover {
            background-color: #357ABD;
        }
        QPushButton:disabled {
            background-color: #A0B4CC;
        }
    """
    self.setStyleSheet(style)

def init_db():
    conn = sqlite3.connect("history.db")
    c = conn.cursor()
    c.execute("""
            CREATE TABLE IF NOT EXISTS history
            (type TEXT, input TEXT, result TEXT, timestamp DATETIME CURRENT_TIMESTAMP)""")
    conn.commit()
    conn.close()

class GeminiThread(QThread):
    result = pyqtSignal(str,str)

    def __init__(self,prompt,mode):
        super().__init__()
        self.prompt = prompt
        self.mode =mode

    def run(self):
        headers = {
            'Content-Type': 'application/json'
        }
        data = {
            "contents": [{
                "parts": [{"text": self.prompt}]
            }],
            "generationConfig":{"maxOutputTokens":150}
        }
        try:
            response = requests.post(api_url, json=data, headers=headers)
            response.raise_for_status()
            result =response.json()['candidates'][0]['content']['parts'][0]['text']
            self.result.emit(result,"")
        except requests.exceptions.RequestException as e:
            self.result.emit("",f"Hata Oluştu : {e}")

class Dream(QMainWindow):
    def __init__(self):
        super().__init__()
        init_db()
        self.history = self.load_history
        self.init_ui()
        apply_styles(self)

    def init_ui(self):
        self.setWindowTitle("Rüya Yorumlayıcı")
        screen = QApplication.primaryScreen()
        screen_size = screen.size()
        self.resize(screen_size.width()//2,screen_size.height()//2)

        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)

        self.tab1 = QWidget()
        self.tabs.addTab(self.tab1,"Rüya Gir")
        layout1 = QVBoxLayout()
        self.ruya_input = QTextEdit()
        self.ruya_input.setPlaceholderText("Rüyanı Buraya Yaz")
        layout1.addWidget(self.ruya_input)

        self.ruya_button = QPushButton("Yorumla!")
        self.ruya_button.clicked.connect(self.yorumla_ruya)
        layout1.addWidget(self.ruya_button)

        self.ruya_result =  QTextBrowser()
        self.ruya_result.setHtml("<br>Rüyanın Yorumu Burada Gözükecek!</br>")
        layout1.addWidget(self.ruya_result)

        self.tab1.setLayout(layout1)

        self.tab2 = QWidget()
        self.tabs.addTab(self.tab2,"Gelecek tahmini")
        layout2 = QVBoxLayout()

        self.tahmin_input = QTextEdit()
        self.tahmin_input.setPlaceholderText("Gelecekle İlgili bir şey sor!")
        layout2.addWidget(self.tahmin_input)

        self.tahmin_button = QPushButton("Tahmni Et!")
        self.tahmin_button.clicked.connect(self.tahmin_et)
        layout2.addWidget(self.tahmin_button)

        self.tahmin_result = QTextBrowser()
        self.tahmin_result.setHtml("<br>Tahmin burada gözükecek!</br>")
        layout2.addWidget(self.tahmin_result)

        self.tab2.setLayout(layout2)

        self.tab3 = QWidget()
        self.tabs.addTab(self.tab3, "geçmiş")
        layout3 = QVBoxLayout()
        self.clear_button = QPushButton("Geçmişi sil")
        self.clear_button.clicked.connect(self.clear_history)
        layout3.addWidget(self.clear_button)

        self.history_browser = QTextBrowser()
        self.history_browser.setHtml("<br>geçmiş gözükecek!</br>")
        
        layout3.addWidget(self.history_browser)

        self.tab3.setLayout(layout3)

    def yorumla_ruya(self):
        ruya = self.ruya_input.toPlainText().strip()
        if not ruya:
            self.ruya_result.setHtml("<br> Lütfen bir rüya yaz!</br>")
            return
        self.ruya_button.setEnabled(False)
        self.ruya_result.setHtml("<br>Yükleniyor...</br>")
        prompt = f"Kullanıcı şu rüyayı gördü : '{ruya}'.Bu rüyanın anlamını objektif olarak yorumla."
        self.thread = GeminiThread(prompt,"ruya")
        self.thread.result.connect(self.ruya_sonuc_goster)
        self.thread.start()

    def tahmin_et(self):
        tahmin = self.tahmin_input.toPlainText().strip()
        if not tahmin:
            self.tahmin_result.setHtml("<br> Lütfen bir rüya yaz!</br>")
            return
        self.tahmin_button.setEnabled(False)
        self.tahmin_result.setHtml("<br>Yükleniyor...</br>")
        #prompt = f"Kullanıcı şu soruyu sordu : '{tahmin}'. Bu soruya eğlenceli, yaratıcı ve olumlu şekilde yorumla. Kıs ve ilgi çekici olsun."
        prompt = tahmin
        self.thread = GeminiThread(prompt, "tahmin")
        self.thread.result.connect(self.tahmin_sonuc_goster)
        self.thread.start()

    def ruya_sonuc_goster(self,result,error):
        self.ruya_button.setEnabled(True)
        if error:
            self.ruya_result.setHtml(f"<br>{error}</br>")
            return
        ruya = self.ruya_input.toPlainText().strip()
        self.save_history("Rüya",ruya,result)
        self.ruya_result.setHtml(f"<h3>Rüya Yorumu</h3><p>{result}</p>")

    def tahmin_sonuc_goster(self,result,error):
        self.tahmin_button.setEnabled(True)
        if error:
            self.tahmin_result.setHtml(f"<br>{error}</br>")
            return
        tahmin = self.tahmin_input.toPlainText().strip()
        self.save_history("tahmin", tahmin, result)
        self.tahmin_result.setHtml(f"<h3>Somuç</h3><p>{result}</p>")


    def save_history(self,type_,input_,result_):
        conn = sqlite3.connect("history.db")
        c = conn.cursor()
        c.execute("INSERT INTO history (type, input, result) VALUES (?,?,?)",(type_,input_,result_))
        conn.commit()
        conn.close()

    def load_history(self):
        conn = sqlite3.connect("history.db")
        c = conn.cursor()
        c.execute("SELECT type, input, result, timestamp FROM history ORDER BY timestamp DESC")
        history = c.fetchall()
        conn.close()
        self.update_history(history)

    def update_history(self, history):
        html = "<h2>Geçmiş</h2>"
        if not history:
            html += "<p>Henüz kayıt yok</p>"
        else:
            for tip, giris, sonuc, timestamp in history:
                html += f"<br><b>{tip}</b> ({timestamp})</br> {giris} <br> <b>Sonuç:</b> {sonuc}</br>"
        self.history_browser.setHtml(html)

    def clear_history(self):
        conn = sqlite3.connect("history.db")
        c = conn.cursor()
        c.execute("DELETE FROM history ")
        conn.commit()
        conn.close()
        self.history = []

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Dream()
    window.show()
    sys.exit(app.exec_())

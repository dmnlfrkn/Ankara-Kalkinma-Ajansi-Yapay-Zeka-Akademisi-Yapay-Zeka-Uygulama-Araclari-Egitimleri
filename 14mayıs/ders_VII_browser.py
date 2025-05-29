from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QToolBar, QAction, QLineEdit, QTabWidget, QToolButton, QWidget, QMenu, QFileDialog, QMessageBox, QTabBar, QLabel )

from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineDownloadItem
from PyQt5.QtCore import QUrl, QTimer
from datetime import datetime
from PyQt5.QtGui import QIcon, QPixmap
import os, sys

class MyBrowser(QMainWindow):
    def __init__(self):
        super(MyBrowser,self).__init__()
        self.init_ui()


    def init_ui(self):
        self.setWindowTitle("Tarayıcı")
        screen = QApplication.primaryScreen()
        screen_size=screen.size()
        self.resize(screen_size.width()//2,screen_size.height()//2)
        self.setStyleSheet("""
            QWidget{
                font-size: 14pt;
            }
            QlineEdit{
                font-size: 14pt;
            }
            QTabBar::tab{
                font-size:14pt;
            }
            QToolButton{
                font-size:14pt;
            }
        """)

        self.tabs = QTabWidget()
        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(self.close_current_tab)
        self.setCentralWidget(self.tabs)

        self.add_new_tab(QUrl("https://www.google.com"),"Google")
        self.add_plus_button()
        self.create_navbar()
        self.bookmarks = []
        self.history =[]

    def add_new_tab(self,qurl=None,label="Yeni Sekme"):
        try:
            browser = QWebEngineView()
            if qurl:
                browser.setUrl(qurl)
            else:
                browser.setUrl(QUrl("about:blank"))

            index = self.tabs.count()-1
            self.tabs.insertTab(index,browser,label)
            self.tabs.setCurrentIndex(index)

            browser.urlChanged.connect(lambda q:self.update_url(q,browser))
            browser.titleChanged.connect(lambda title: self.update_tab_title(title,browser))
            browser.urlChanged.connect(self.add_to_history)

        except Exception as e:
            print(f"Bir Hata Oluştu (Yeni Sekme Eklerken) : {e}")

    def add_plus_button(self):
        plus_button = QToolButton()
        plus_button.setText("+")
        plus_button.clicked.connect(self.add_new_tab)

        self.tabs.addTab(QWidget(),"")
        self.tabs.tabBar().setTabButton(self.tabs.count()-1,QTabBar.RightSide,plus_button)
        self.tabs.tabBar().setTabEnabled(self.tabs.count()-1,False)

    def create_navbar(self):
        navbar= QToolBar()
        self.addToolBar(navbar)

        back_button = QAction("geri",self)
        back_button.triggered.connect(lambda: self.tabs.currentWidget().back())
        navbar.addAction(back_button)

        forward_button = QAction("ileri",self)
        forward_button.triggered.connect(lambda: self.tabs.currentWidget().forward())
        navbar.addAction(forward_button)

        reload_button = QAction("yenile", self)
        reload_button.triggered.connect(lambda: self.tabs.currentWidget().reload())
        navbar.addAction(reload_button)

        self.url_bar = QLineEdit()
        self.url_bar.setPlaceholderText("Buraya bir url girin veya arama yapın...")
        self.url_bar.returnPressed.connect(self.load_url_or_search)
        navbar.addWidget(self.url_bar)

        self.bookmark_nemu = QMenu("Yer İmleri")
        navbar.addAction(self.bookmark_nemu.menuAction())

        add_bookmark_action = QAction("Bu sayfayı Yer İmlerine Ekle",self)
        add_bookmark_action.triggered.connect(self.add_bookmark)
        navbar.addAction(add_bookmark_action)

        self.historu_menu = QMenu("Geçmiş",self)
        navbar.addAction(self.historu_menu.menuAction())

        self.tabs.currentChanged.connect(self.update_url_bar)


    def load_url_or_search(self):
        try:
            url = self.url_bar.text()
            if "." in url:
                if not url.startswith("http") and not url.startswith("https"):
                    url = "https://"+url
                self.tabs.currentWidget().setUrl(QUrl(url))
            else:
                search_url = "https://www.google.com/search?q=" + url
                self.tabs.currentWidget().setUrl(QUrl(search_url))

        except Exception as e:
            print(f"Hatalı arama : {e}")

    def add_bookmark(self):
        current_widget = self.tabs.currentWidget()
        if isinstance(current_widget,QWebEngineView):
            url = current_widget.url().toString()
            title = current_widget.title()

            if url not in [bookmark['url'] for bookmark in self.bookmarks]:
                self.bookmarks.append({"title":title,"url":url})
                bookmark_action = QAction(title,self)
                bookmark_action.triggered.connect(lambda: self.load_bookmark(url))
                self.bookmark_nemu.addAction(bookmark_action)

    def load_bookmark(self,url):
        self.tabs.currentWidget().setUrl(QUrl(url))


    def update_url_bar(self):
        try:
            current_widget = self.tabs.currentWidget()

            if isinstance(current_widget,QWebEngineView):
                qurl= current_widget.url()

                if qurl.toString() == "about:blank":

                    self.url_bar.clear()

                else:
                    self.url_bar.setText(qurl.toString())
            else:
                self.url_bar.clear()

        except Exception as e:
            print(f"Hata : {e}")

    def update_url(self,q,browser=None):
        try:
            if browser ==self.tabs.currentWidget():
                self.url_bar.setText(q.toString())
        except Exception as e:
            print(f"Hata : {e}")


    def close_current_tab(self,i):
        try:
            if self.tabs.count() > 2:
                self.tabs.removeTab(i)

                if i > 0:
                    self.tabs.setCurrentIndex(i-1)
                else:
                    self.tabs.setCurrentIndex(0)
        except Exception as e:
            print(f"Bir hata oluştu (Sekme Kapatılırken) : {e}")


    def update_tab_title(self,title,browser):
        try:
            i = self.tabs.indexOf(browser)
            if i != -1:
                if title == "about:blank":
                    title = "Yeni Sekme"
                self.tabs.setTabText(i,title)
        except Exception as e:
            print("")

    def add_to_history(self):
        current_widget = self.tabs.currentWidget()
        if isinstance(current_widget,QWebEngineView):
            url = current_widget.url().toString()
            title = current_widget.title()

            if url not in [entry['url'] for entry in self.history]:
                visit_time = datetime.now().strftime("%Y-%m-%d %H:%M%S")
                self.history.append({"title":title,"url":url,"time":visit_time})
                url_sum = url
                if len(url) > 50:
                    url_sum = url[:50]+"..."

                history_action = QAction(f"{visit_time} - {url_sum}",self)
                history_action.triggered.connect(lambda: self.load_bookmark(url))
                self.historu_menu.addAction(history_action)

app = QApplication(sys.argv)
window = MyBrowser()
window.show()
sys.exit(app.exec_())

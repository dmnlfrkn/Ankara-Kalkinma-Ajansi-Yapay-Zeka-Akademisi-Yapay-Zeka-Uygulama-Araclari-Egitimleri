
"""
import sys
from PyQt5.QtWidgets import QApplication,QWidget

app = QApplication(sys.argv)

pencere = QWidget()
pencere.setWindowTitle("İlk PyQt5 Uygulaması")
pencere.setGeometry(500,500,500,500)
pencere.show()

sys.exit(app.exec_())

----------------------------------


import sys
from PyQt5.QtWidgets import QApplication,QMainWindow, QLabel, QWidget, QLineEdit, QPushButton, QVBoxLayout
from PyQt5.QtCore import Qt

class MyMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("QMainWindow Örneği")
        self.setGeometry(500,500,500,500)

        label= QLabel("Ana pensereye Hoşgeldiniz.",self)
        label.setStyleSheet("font-size: 16px;")
        self.setCentralWidget(label)




app = QApplication(sys.argv)
main_window = MyMainWindow()
main_window.show()

sys.exit(app.exec_())


----------------------------


import sys
from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout
#from PyQt5.QtCore import Qt
class MyMainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("QMainWindow Örneği")
        self.setGeometry(500,500,500,500)

        self.label = QLabel("Adınız : ")
        self.textbox = QLineEdit()
        self.button = QPushButton("Gönder")
        self. result_label = QLabel("")
        self.button.clicked.connect(self.display_name)

        vlayout = QVBoxLayout()
        vlayout.addWidget(self.button)
        vlayout.addWidget(self.textbox)
        hlayout = QHBoxLayout()
        hlayout.addLayout(vlayout)
        hlayout.addWidget(self.label)
        hlayout.addWidget(self.result_label)

        self.setLayout(hlayout)



    def display_name(self):
        name = self.textbox.text()
        self.result_label.setText(f"Hoşgeldiniz, {name}")




app = QApplication(sys.argv)
main_window = MyMainWindow()
main_window.show()

sys.exit(app.exec_())

--------------------------------

"""

import sys
from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout,QFormLayout, QMenu
#from PyQt5.QtCore import Qt
class MyMainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("QMainWindow Örneği")
        self.setGeometry(500,500,500,500)

        form_layout = QFormLayout()

        self.name_input = QLineEdit()
        self.email_input = QLineEdit()
        self.submit_button = QPushButton("Gönder")
        self.submit_button.clicked.connect( self.submit_form)
        self.yazi = QLabel()

        form_layout.addRow("Ad : ",self.name_input)
        form_layout.addRow("Email : ",self.email_input)
        form_layout.addRow(self.submit_button)
        form_layout.addRow("Bilgiler", self.yazi)
        self.setLayout(form_layout)


    def submit_form(self):
        name = self.name_input.text()
        email = self.email_input.text()
        self.yazi.setText(f"Ad : {name} --------- Email : {email}")




app = QApplication(sys.argv)
main_window = MyMainWindow()
main_window.show()

sys.exit(app.exec_())

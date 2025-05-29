from api_client import FinanceAPICLient
import sys
from PyQt5.QtWidgets import (
QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
QLineEdit, QPushButton, QTableWidget, QTableWidgetItem, QMessageBox,
QComboBox, QFormLayout, QDialog, QLabel
)
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas



class LoginDialog(QDialog):
    def __init__(self, api_client):
        super().__init__()
        self.api_client = api_client
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Giriş / Kayıt")

        layout = QFormLayout()
        self.username = QLineEdit()
        self.password = QLineEdit()
        self.password.setEchoMode(QLineEdit.Password)
        login_btn = QPushButton("Giriş Yap")
        login_btn.clicked.connect(self.login)
        register_btn = QPushButton("Kayıt Ol")
        register_btn.clicked.connect(self.register)

        layout.addRow("Kullanıcı Adı:",self.username)
        layout.addRow("Şifre:",self.password)
        layout.addRow(login_btn)
        layout.addRow(register_btn)
        self.setLayout(layout)

    def login(self):
        username = self.username.text().strip()
        password = self.password.text().strip()
        if not username or not password:
            QMessageBox.critical(self,"Hata","Kullanıcı adı veya şifre boş olamaz!")
            return
        try:
            self.api_client.login(username,password)
            self.accept()
        except Exception as e:
            QMessageBox.critical(self,"Hata",f"Giriş yapılamadı: {str(e)}")
    def register(self):
        username = self.username.text().strip()
        password = self.password.text().strip()
        if not username or not password:
            QMessageBox.critical(self,"Hata","Kullanıcı adı veya şifre boş olamaz!")
            return
        try:
            self.api_client.register(username,password)
            QMessageBox.information(self,"Başarılı","Kullanıcı oluşturuldu!")
        except Exception as e:
            QMessageBox.critical(self,"Hata",f"Kayıt yapılamadı: {str(e)}")

class FinanceApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.api_client = FinanceAPICLient()
        self.categories = ['Maaş','Fatura','Market','Eğlence','Diğer']
        if not self.show_login_dialog():
            sys.exit()
        self.init_ui()
        self.load_transaction()
    def init_ui(self):
        self.setWindowTitle("Kişisel Finans Yönetimi")
        screen = QApplication.primaryScreen()
        screen_size = screen.size()
        self.resize(screen_size.width() // 2, screen_size.height() // 2)
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QVBoxLayout(main_widget)

        form_layout = QFormLayout()
        self.amount_input = QLineEdit()
        self.category_combo = QComboBox()
        self.category_combo.addItems(self.categories)
        self.description_input = QLineEdit()
        self.is_income_combo = QComboBox()
        self.is_income_combo.addItems(['Gider','Gelir'])
        add_btn = QPushButton("Ekle")
        add_btn.clicked.connect(self.add_transaction)

        form_layout.addRow("Tutar:",self.amount_input)
        form_layout.addRow("Kategori:",self.category_combo)
        form_layout.addRow("Açıklama:",self.description_input)
        form_layout.addRow("Tür:",self.is_income_combo)
        form_layout.addRow(add_btn)
        layout.addLayout(form_layout)

        filter_layout = QHBoxLayout()
        self.filter_combo = QComboBox()
        self.filter_combo.addItems(['Tümü']+self.categories)
        self.filter_combo.currentTextChanged.connect(self.load_transaction)

        filter_layout.addWidget(QLabel("Kategoriye Göre Filtrele:"))
        filter_layout.addWidget(self.filter_combo)
        layout.addLayout(filter_layout)

        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(['ID','Tutar','Kategori','Açıklama','Sil'])
        self.table.setColumnWidth(3,500)
        layout.addWidget(self.table)

        self.figure, self.ax = plt.subplots()
        self.canvas = FigureCanvas(self.figure)
        layout.addWidget(self.canvas)


    def load_transaction(self):
        try:
            category = self.filter_combo.currentText() if self.filter_combo.currentText() != 'Tümü' else None
            transactions = self.api_client.get_transactions(category)
            self.table.setRowCount(len(transactions))

            for row, t in enumerate(transactions):
                self.table.setItem(row,0,QTableWidgetItem(str(t['id'])))
                self.table.setItem(row,1,QTableWidgetItem(f'{t["amount"]:.2f}'))
                self.table.setItem(row,2,QTableWidgetItem(t['category']))
                self.table.setItem(row,3,QTableWidgetItem(t['description']))
                delete_btn = QPushButton("Sil")
                delete_btn.clicked.connect(lambda _, t_id=t['id']:self.delete_transaction(t_id))
                self.table.setCellWidget(row,4,delete_btn)
            self.update_summary()
        except Exception as e:
            QMessageBox.critical(self,"Hata",f"İşlemler yüklenemedi: {str(e)}")



    def add_transaction(self):
        try:
            amount = float(self.amount_input.text())
            category = self.category_combo.currentText()
            description = self.description_input.text()
            is_income = self.is_income_combo.currentText() == 'Gelir'
            self.api_client.add_transaction(amount,category,description,is_income)
            self.amount_input.clear()
            self.description_input.clear()
            self.load_transaction()
        except ValueError:
            QMessageBox.critical(self,"Hata","Tutar sayısal bir değer olmalı!")
        except Exception as e:
            QMessageBox.critical(self,"Hata",f"İşlem eklenemedi: {str(e)}")
    def delete_transaction(self,t_id):
        try:
            self.api_client.delete_transaction(t_id)
            self.load_transaction()
        except Exception as e:
            QMessageBox.critical(self, "Hata", f"İşlem silinemedi: {str(e)}")

    def update_summary(self):
        try:
            transactions = self.api_client.get_transactions()
            income = sum(t['amount'] for t in transactions if t['is_income'])
            expense = sum(t['amount'] for t in transactions if not t['is_income'])

            self.ax.clear()
            self.ax.bar(['Gelir','Gider'],[income,expense],color=['green','red'])
            self.ax.set_title('Gelir-Gider Özeti')
            self.canvas.draw()
        except Exception as e:
            QMessageBox.critical(self, "Hata", f"Özet güncellenemedi: {str(e)}")


    def show_login_dialog(self):
        dialog = LoginDialog(self.api_client)
        return dialog.exec_() == QDialog.Accepted

if __name__=="__main__":
    app = QApplication(sys.argv)
    window = FinanceApp()
    window.show()
    sys.exit(app.exec_())

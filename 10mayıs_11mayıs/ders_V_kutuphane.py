import sys
import sqlite3
import os
from PyQt5.QtWidgets import  (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QFormLayout,
                              QLineEdit, QPushButton, QTableWidget,QTableWidgetItem, QLabel, QComboBox, QMessageBox, QDialog )
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import  QThread, pyqtSignal



class DatabaseWorker(QThread):
    finished = pyqtSignal()
    books_fetched = pyqtSignal(list)

    def __init__(self,action, title=None, author=None, category=None, book_id=None, search_query=None):
        super().__init__()
        self.action = action # işlem türü --- Ekle, sil, güncelle
        self.title = title
        self.author = author
        self.category = category
        self.book_id = book_id
        self.search_query = search_query # arama sonucu

    def run(self):
        try:
            with sqlite3.connect("library.db") as conn:
                cursor = conn.cursor()
                if self.action == "add":
                    cursor.execute("INSERT INTO books (title,author,category) VALUES (?,?,?)",(self.title,self.author,self.category))
                    conn.commit()
                elif self.action == "delete":
                    cursor.execute("DELETE FROM books WHERE id = ?",(self.book_id,))
                    conn.commit()
                elif self.action == "update":
                    cursor.execute("UPDATE books SET title = ?, author = ?, category = ? WHERE id = ?",(self.title,self.author,self.category,self.book_id))
                elif self.action == "search":
                    if self.search_query:
                        cursor.execute("SELECT * FROM books WHERE UPPER(title) LIKE UPPER(?) OR UPPER(author) LIKE UPPER(?)",(f"%{self.search_query}%",f"%{self.search_query}%"))
                    else:
                        cursor.execute("SELECT * FROM books")
                    books= cursor.fetchall()
                    self.books_fetched.emit(books)
                self.finished.emit()
        except sqlite3.Error as e:
            print(e)

class SearchDialog(QDialog):
    def __init__(self,parent=None):
        super().__init__(parent)
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Kitap Ara")
        self.setGeometry(200,200,500,400)

        layout = QVBoxLayout()
        search_layout = QHBoxLayout()

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Başlık veya Yazar ara...")
        self.search_button = QPushButton("ARA")
        self.search_button.clicked.connect(self.search_book)
        search_layout.addWidget(self.search_input)
        search_layout.addWidget(self.search_button)
        layout.addLayout(search_layout)

        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["ID","Başlık","Yazar","Kategori"])
        self.table.setSelectionBehavior(QTableWidget.SelectRows) # Sadece satırların düzenlenmesini sağlıyoruz
        self.table.setEditTriggers(QTableWidget.NoEditTriggers) # Tablo düzenlenmesini engelliyoruz
        layout.addWidget(self.table)

        self.setLayout(layout)



    def search_book(self):
        self.query= self.search_input.text().strip()
        self.worker = DatabaseWorker("search",search_query=self.query)
        self.worker.books_fetched.connect(self.update_table)
        self.worker.start()

    def update_table(self,books):
        self.table.clearContents()
        self.table.setRowCount(len(books))
        for row, book in enumerate(books):
            for col, data in enumerate(book):
                self.table.setItem(row,col,QTableWidgetItem(str(data)if data else ""))
        self.table.resizeColumnsToContents()

        if not books:
            QMessageBox.warning(self,"Hata","Bilgi Bulunamadı")
        elif self.query:
            QMessageBox.information(self,"Bilgi","Kitap Bulundu")

class LibraryApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_db()
        self.init_ui()

    def kaynak_yolu(self,goreceli_yol):
        if hasattr(sys,"_MEIPASS"):
            return os.path.join(sys._MEIPASS,goreceli_yol)
        return os.path.join(os.path.abspath("."),goreceli_yol)


    def init_db(self):
        with sqlite3.connect("library.db") as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS 'books' 
                    (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    author TEXT NOT NULL
                    )
                """)
            try:
                cursor.execute("ALTER TABLE 'books' ADD COLUMN category TEXT")
            except sqlite3.OperationalError:
                pass
            cursor.execute("UPDATE 'books' SET category ='Diğer' WHERE category IS NULL")
            conn.commit()


    def init_ui(self):
        self.setWindowTitle("Gelişmiş Kütüphane Uygulaması")
        self.setGeometry(500,500,800,600)
        self.setWindowIcon(QIcon(self.kaynak_yolu("library.ico")))

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout= QVBoxLayout()

        self.search_open_button =QPushButton("Kitap Ara")
        self.search_open_button.clicked.connect(self.open_search_dialog)
        main_layout.addWidget(self.search_open_button)

        form_widget = QWidget()
        form_layout = QFormLayout()
        self.title_input = QLineEdit()
        self.author_input = QLineEdit()
        self.category_combo = QComboBox()
        self.category_combo.addItems(["Roman","Bilim Kurgu","Polisiye","Biyorafi","Diğer"])

        self.add_button = QPushButton("Kitap Ekle")
        self.add_button.clicked.connect(self.add_book_thread)

        self.update_button = QPushButton("Kitabı Güncelle")
        self.update_button.clicked.connect(self.update_book_thread)
        self.update_button.setVisible(False)




        self.delete_button = QPushButton("Kitabı Sil")
        self.delete_button.clicked.connect(self.delete_book_thread)

        form_layout.addRow("Başlık:",self.title_input)
        form_layout.addRow("Yazar:", self.author_input)
        form_layout.addRow("Kategori:",self.category_combo)

        form_layout.addRow(self.add_button)
        form_layout.addRow(self.update_button)
        form_layout.addRow(self.delete_button)


        form_widget.setLayout(form_layout)
        main_layout.addWidget(form_widget)

        #Tablo Kısmı

        self.table=QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["ID","Başlık","Yazar","Kategori"])
        self.table.setSelectionBehavior(QTableWidget.SelectRows) # Satır seçimi modu açıldı
        self.table.setEditTriggers(QTableWidget.NoEditTriggers) # Tabloda veri düzenlenmesi engenlendi
        self.table.cellDoubleClicked.connect(self.load_book_to_form)
        main_layout.addWidget(self.table)

        central_widget.setLayout(main_layout)
        self.table.setAlternatingRowColors(True)
        self.setStyleSheet("""
            QMainWindow, QDialog {
                background-color: #2E3440;  /* Koyu mavi-gri */
            }

            QWidget {
                background-color: #3B4252;  /* Açık koyu ton */
            }

            QLabel {
                color: #D8DEE9;  /* Açık gri - okunabilir metin */
                font-size: 14px;
                font-family: 'Times New Roman';
            }

            QLineEdit {
                background-color: #434C5E;
                color: #ECEFF4;
                border: 1px solid #81A1C1;
                padding: 4px;
                border-radius: 4px;
                font-family: 'Times New Roman';
            }

            QLineEdit:focus {
                border: 1px solid #88C0D0;
                background-color: #4C566A;
            }

            QComboBox {
                font-family: 'Times New Roman';
                background-color: #434C5E;
                color: #ECEFF4;
                border: 1px solid #81A1C1;
                padding: 5px;
                border-radius: 4px;
                font-size: 14px;
                font-family: 'Times New Roman';
            }
            QComboBox QAbstractItemView {
                color: white;
                selection-background-color:#5E81AC;
            }
            QPushButton {
                background-color: #5E81AC;
                color: white;
                padding: 6px;
                border: none;
                border-radius: 5px;
                font-size: 14px;
                font-family: 'Times New Roman';
            }

            QPushButton:hover {
                background-color: #81A1C1;
            }

            QPushButton:disabled {
                background-color: #4C566A;
                color: #7A869A;
            }
            QPushButton:pressed {
                background-color: #4C566B;
            }

            QTableWidget {
                background-color: #3B4252;
                gridline-color: #4C566A;
                border: 1px solid #81A1C1;
                alternate-background-color: #434C5E;
                color: #ECEFF4;
                font-size: 14px;
                font-family: 'Times New Roman';
            }
            QTableWidget::item:selected {
                background-color: #4C566B;
            }
            
            QHeaderView::section {
                background-color: #4C566A;
                color: #ECEFF4;
                font-weight: bold;
                padding: 4px;
                border: 1px solid #5E81AC;
                font-size: 14px;
                font-family: 'Times New Roman';
            }
        """)

        self.load_books()

    def open_search_dialog(self):
        self.search_dialog = SearchDialog(self)
        self.search_dialog.exec_()

    def add_book_thread(self):
        title = self.title_input.text().strip()
        author = self.author_input.text().strip()
        category = self.category_combo.currentText()
        if not title or not author:
            QMessageBox.warning(self, "Hata", "Başlık ve yazar boş olamaz")
            return
        self.worker = DatabaseWorker("add", title=title, author=author, category=category)
        self.worker.finished.connect(self.load_books)
        self.worker.finished.connect(self.reset_form)
        self.worker.start()

    def update_book_thread(self):

        title= self.title_input.text().strip()
        author = self.author_input.text().strip()
        category= self.category_combo.currentText()

        if not title or not author:
            QMessageBox.warning(self,"Hata","Başlık ve yazar boş bırakılamaz")
            return

        self.worker = DatabaseWorker("update",title=title, author=author, category=category, book_id=self.current_book_id)
        self.worker.finished.connect(self.load_books)
        self.worker.finished.connect(self.reset_form)
        self.worker.start()

    def delete_book_thread(self):

        selected_row = self.table.currentRow()
        if selected_row < 0:
            QMessageBox.warning(self,"hata","Lütfen bir kitap seçiniz")
            return
        book_id = self.table.item(selected_row,0).text()
        self.worker = DatabaseWorker("delete",book_id=book_id)
        self.worker.finished.connect(self.load_books)
        self.worker.start()

    def load_book_to_form(self,row,col):
        book_id = self.table.item(row,0).text()
        title = self.table.item(row,1).text()
        author = self.table.item(row,2).text()
        category= self.table.item(row,3).text()

        self.title_input.setText(title)
        self.author_input.setText(author)
        self.category_combo.setCurrentText(category)
        self.add_button.setVisible(False)
        self.update_button.setVisible(True)
        self.current_book_id = book_id

    def load_books(self,search_query=""):

        self.worker= DatabaseWorker("search",search_query=search_query)
        self.worker.books_fetched.connect(self.update_table)
        self.worker.start()

    def reset_form(self):
        self.title_input.clear()
        self.author_input.clear()
        self.category_combo.setCurrentIndex(0)
        self.add_button.setVisible(True)
        self.update_button.setVisible(False)

    def update_table(self,books):

        self.table.clearContents()
        self.table.setRowCount(len(books))
        for row, book in enumerate(books):
            for col , data in enumerate(book):
                self.table.setItem(row,col,QTableWidgetItem(str(data)if data else ""))

        self.table.resizeColumnsToContents()



if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = LibraryApp()
    window.show()
    sys.exit(app.exec_())

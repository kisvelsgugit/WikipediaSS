import sys, os, sqlite3
from PyQt5.QtWidgets import QApplication, QDialog, QMainWindow, QMessageBox, QPushButton, QWidget, QTextEdit, QVBoxLayout
import wikipedia


def get_random_article():
    wikipedia.set_lang('ru')
    while True:
        title = wikipedia.random()
        try:
            return wikipedia.WikipediaPage(title)
        except wikipedia.exceptions.DisambiguationError:
            continue


def add_to_db(article):
    create_table = not os.path.exists('db.sqlite')
    conn = sqlite3.connect('db.sqlite')
    if create_table:
        conn.execute('CREATE TABLE articles(title text, url text, content text)')
    cur = conn.execute('INSERT INTO articles(title, url, content) values(?,?,?)', (article.title, article.url, article.content))
    conn.commit()
    conn.close()


def get_db_content():
    conn = sqlite3.connect('db.sqlite')
    cur = conn.execute('SELECT url, title FROM articles')
    res = '\n'.join(' | '.join(row) for row in cur.fetchall())
    conn.close()
    return res



class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Wikipedia")

        button = QPushButton("Случайная статья")
        button.clicked.connect(self.button_clicked)
        self.setCentralWidget(button)

    def button_clicked(self, s):
        article = get_random_article()
        button = QMessageBox.critical(self, "Случайная статья", article.title, buttons=QMessageBox.Yes | QMessageBox.No)
        if button == QMessageBox.Yes:
            win = ArticleWindow(self, article)
            win.show()



class ArticleWindow(QWidget):
    def __init__(self, parent, article):
        super().__init__(parent)

        add_to_db(article)

        self.setWindowTitle(article.title)
        self.resize(400,370)

        self.textEdit = QTextEdit()
        self.db = QTextEdit()
        self.button = QPushButton("Закрыть")

        layout = QVBoxLayout()
        layout.setSpacing(4)
        layout.addWidget(self.textEdit)
        layout.addWidget(self.db)
        layout.addWidget(self.button)
        self.setLayout(layout)
        self.db.setPlainText(get_db_content())
        self.textEdit.setPlainText(article.content)

        self.button.clicked.connect(self.button_clicked)

    def button_clicked(self):
        self.close()

        #def btnPress2_Clicked(self):
        #        self.textEdit.setHtml("<font color='red' size='6'><red>Hello PyQt5!\nHello</font>")



app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()



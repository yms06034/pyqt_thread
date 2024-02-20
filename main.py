import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QTextEdit, QPushButton, QProgressBar
from PyQt5.QtCore import QThread, pyqtSignal
from selenium import webdriver
import time

class SeleniumThread(QThread):
    log_signal = pyqtSignal(str)
    progress_signal = pyqtSignal(int)

    def run(self):
        self.log_signal.emit("Selenium 작업 시작")

        total_iterations = 100
        current_iteration = 0

        driver = webdriver.Chrome()
        driver.get("https://sungjinportfolio.netlify.app/")
        


        while current_iteration < total_iterations:
            time.sleep(0.1)
            current_iteration += 1
            progress = current_iteration * 100 / total_iterations
            self.progress_signal.emit(progress)

        driver.quit()

        self.log_signal.emit("Selenium 작업 종료")

class MyApp(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.text_edit = QTextEdit()
        self.progress_bar = QProgressBar()
        self.button = QPushButton('Start Selenium')

        layout = QVBoxLayout()
        layout.addWidget(self.text_edit)
        layout.addWidget(self.progress_bar)
        layout.addWidget(self.button)

        self.setLayout(layout)

        self.button.clicked.connect(self.start_selenium)

        self.setGeometry(300, 300, 300, 200)
        self.setWindowTitle('PyQt with Selenium')
        self.show()

    def start_selenium(self):
        self.thread = SeleniumThread()
        self.thread.log_signal.connect(self.update_log)
        self.thread.progress_signal.connect(self.update_progress)
        self.thread.start()

    def update_log(self, message):
        self.text_edit.append(message)

    def update_progress(self, value):
        self.progress_bar.setValue(value)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())

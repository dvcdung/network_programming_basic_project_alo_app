import sys
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow, QVBoxLayout, QPushButton, QWidget
from functools import partial

class WorkerThread(QThread):
    update_signal = pyqtSignal(list)

    def run(self):
        # Thực hiện công việc ở đây và gửi thông điệp cập nhật
        while (True):
            text = []
            self.update_signal.emit([] or text)
            self.sleep(1)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('QThread Update QLabel Example')

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        self.worker_thread = None

        layout = QVBoxLayout(central_widget)

        self.label = QLabel('Status: Ready', self)
        layout.addWidget(self.label)

        self.start_button = QPushButton('Start Worker Thread', self)
        self.start_button.clicked.connect(self.start_worker_thread)
        layout.addWidget(self.start_button)

    def start_worker_thread(self):
        if (self.worker_thread): 
            self.worker_thread.quit()
            self.worker_thread.wait()
            self.worker_thread = None
            print(self.worker_thread)
            return
        self.label.setText('Status: Working...')

        # Tạo một đối tượng thread
        self.worker_thread = WorkerThread()
        a = 0

        # Kết nối tín hiệu cập nhật từ thread với slot cập nhật giao diện người dùng
        self.worker_thread.update_signal.connect(partial(self.update_label_text, a))

        # Bắt đầu thread
        self.worker_thread.start()

    def update_label_text(self, a, text):
        # Slot này sẽ được gọi khi thread gửi tín hiệu cập nhật
        print(f"{a} + {text or ['Hello']}")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_win = MainWindow()
    main_win.show()
    sys.exit(app.exec_())

import sys
from PyQt5.QtWidgets import QApplication, QPushButton, QVBoxLayout, QWidget
import webbrowser

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        # Tạo nút
        btn_open_url = QPushButton('Mở trình duyệt Chrome', self)

        # Kết nối sự kiện click của nút đến hàm xử lý
        btn_open_url.clicked.connect(self.open_url_in_browser)

        # Tạo layout và thêm nút vào layout
        layout = QVBoxLayout(self)
        layout.addWidget(btn_open_url)

        # Đặt layout cho cửa sổ chính
        self.setLayout(layout)

        # Thiết lập kích thước và tiêu đề cửa sổ
        self.setGeometry(300, 300, 300, 150)
        self.setWindowTitle('Mở URL trong trình duyệt Chrome')
        
    def open_url_in_browser(self):
        # Đường link URL bạn muốn mở
        url_to_open = 'https://www.google.com'

        # Mở đường link URL trong trình duyệt Chrome
        webbrowser.open(url_to_open)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())

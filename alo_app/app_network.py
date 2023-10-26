import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLineEdit, QLabel
from PyQt5.QtCore import Qt

class MyApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.input_line = QLineEdit(self)
        self.input_line.setPlaceholderText('Nhập văn bản...')
        
        self.display_label = QLabel(self)
        self.display_label.setAlignment(Qt.AlignTop)
        self.display_label.setWordWrap(True)  # Thiết lập xuống dòng khi cần

        vbox = QVBoxLayout()
        vbox.addWidget(self.input_line)
        vbox.addWidget(self.display_label)

        self.setLayout(vbox)

        self.input_line.textChanged.connect(self.updateDisplay)

        self.setWindowTitle('My PyQt App')
        self.setGeometry(100, 100, 400, 300)
        self.show()

    def updateDisplay(self):
        text = self.input_line.text()
        self.display_label.setText(text)
        # Thiết lập kích thước cố định (ví dụ: 200px)
        self.display_label.setFixedWidth(200)  # Hoặc sử dụng setMaximumWidth(width) nếu bạn muốn giới hạn chiều rộng tối đa

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())

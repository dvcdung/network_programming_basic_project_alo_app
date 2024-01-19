from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QGridLayout
import sys

class EmojiTableExample(QWidget):
    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        # Tạo layout dạng lưới
        grid_layout = QGridLayout()

        # Thêm nút cho mỗi emoji vào layout
        emojis = ["😀", "😍", "🥳", "👿", "🌟", "🚀", "🐱", "🐶", "🍕", "🎉", "❤️", "🌈", "🎈", "🎂", "🍦", "🎸", "📷", "🚗", "⚽", "🎮", "📚", "🌺", "🍔", "☕", "🎧"]
        row, col = 0, 0
        for emoji in emojis:
            button = QPushButton(emoji)
            button.clicked.connect(self.on_button_click)
            button.setFixedSize(40, 40)  # Kích thước của mỗi nút
            grid_layout.addWidget(button, row, col)
            col += 1
            if col > 4:
                col = 0
                row += 1

        # Tạo một QWidget chứa QGridLayout
        widget2 = QWidget()
        widget2.setLayout(grid_layout)

        # Tạo layout chứa QWidget2
        layout = QGridLayout()
        layout.addWidget(widget2, 0, 0)
        
        # Tạo QWidget1 chứa layout và thiết lập sự kiện nhấp chuột để ẩn widget2
        widget1 = QWidget()
        widget1.setLayout(layout)
        widget1.mousePressEvent = self.hide_widget2

        # Thêm widget1 vào self
        layout_self = QGridLayout(self)
        layout_self.addWidget(widget1, 0, 0)

        self.setWindowTitle("Emoji Grid Example")
        self.setGeometry(100, 100, 300, 300)

    def on_button_click(self):
        # Xử lý sự kiện click vào nút
        sender = self.sender()
        print("Selected Emoji:", sender.text())

    def hide_widget2(self, event):
        # Ẩn widget2 khi click ra khỏi widget2
        if not self.layout().itemAt(0).widget().layout().itemAt(0).widget().geometry().contains(event.pos()):
            self.layout().itemAt(0).widget().layout().itemAt(0).widget().hide()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = EmojiTableExample()
    window.show()
    sys.exit(app.exec_())

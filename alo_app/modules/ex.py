import sys
from PyQt5.QtWidgets import QApplication, QWidget, QTableWidget, QTableWidgetItem, QVBoxLayout

class EmojiTable(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        # Tạo QTableWidget để hiển thị bảng emoji
        self.emoji_table = QTableWidget(self)
        self.emoji_table.setRowCount(2)  # Số dòng
        self.emoji_table.setColumnCount(3)  # Số cột

        # Đặt emoji vào các ô trong bảng
        emojis = ['😊', '❤️', '🎉', '👍', '🌟', '🔥']
        for row in range(2):
            for col in range(3):
                emoji_item = QTableWidgetItem(emojis[row * 3 + col])
                self.emoji_table.setItem(row, col, emoji_item)

        # Kết nối sự kiện khi chọn emoji
        self.emoji_table.cellClicked.connect(self.add_emoji_to_message)

        layout.addWidget(self.emoji_table)

        self.setLayout(layout)
        self.setWindowTitle('Emoji Table')

    def add_emoji_to_message(self, row, col):
        # Lấy emoji từ ô được chọn và thêm vào QLineEdit hoặc nơi khác
        selected_emoji_item = self.emoji_table.item(row, col)
        selected_emoji = selected_emoji_item.text()

        # Bạn có thể thêm emoji vào QLineEdit hoặc nơi khác theo yêu cầu của bạn
        print(f'Selected Emoji: {selected_emoji}')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    emoji_table = EmojiTable()
    emoji_table.show()
    sys.exit(app.exec_())

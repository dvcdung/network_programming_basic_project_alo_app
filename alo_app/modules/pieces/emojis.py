from PyQt5 import QtCore, QtWidgets
from functools import partial

class Emojis(QtWidgets.QWidget):
    def __init__(self, home):    
        self.emojisWidget = QtWidgets.QWidget(home)
        self.emojisWidget.setGeometry(QtCore.QRect(450, 290, 194, 162))
        self.emojisWidget.setStyleSheet("border: 1px solid rgb(230, 230, 230); border-radius: 2px")
        self.emojisWidget.setObjectName("emojisWidget")
        self.emojisGridLayout = QtWidgets.QGridLayout()
        self.emojisGridLayout.setSizeConstraint(QtWidgets.QLayout.SetFixedSize)
        self.emojisGridLayout.setSpacing(2)
        self.emojisGridLayout.setContentsMargins(2, 2, 2, 2)
        self.emojisGridLayout.setObjectName("emojisGridLayout")

        self.emojis = ["😀", "😍", "🥳", "👿", "🌟", "🚀", "🐱", "🐶", "🍕", "🎉", "❤️", "🌈", "🎈", "🎂", "🍦", "🎸", "📷", "🚗", "⚽", "🎮", "📚", "🌺", "🍔", "☕", "🎧"]
        row, col = 0, 0
        for emoji in self.emojis:
            button = QtWidgets.QPushButton(emoji)
            button.clicked.connect(partial(home.on_emoji_click, emoji))
            button.setFixedSize(30, 30)
            button.setStyleSheet("border: 1px solid rgb(230, 230, 230); font-size: 20px")
            self.emojisGridLayout.addWidget(button, row, col    )
            col += 1
            if col > 5:
                col = 0
                row += 1

        self.emojisWidget.setLayout(self.emojisGridLayout)
        self.emojisWidget.hide()

    def toggleEmojisWidget(self):
        if self.emojisWidget.isHidden(): self.emojisWidget.show()  
        else: self.emojisWidget.hide()
        
    def closeEmojisWidget(self):
        if not self.emojisWidget.isHidden():
            self.emojisWidget.hide()
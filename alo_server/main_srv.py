from PyQt5 import QtWidgets, QtGui, QtCore

class MainWindow(QtWidgets.QWidget):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.initUI()

    def initUI(self):
        # Tải hình ảnh vuông
        pixmap = QtGui.QPixmap("D:\\data0\\HOC_DAI_HOC_VKU\\NAM3_HK1\\Network Programing\\Projects\\do_an_mon_hoc\\AloApp\\flappy_bird.png")  # Thay đổi đường dẫn đến hình ảnh vuông của bạn
        pixmap = pixmap.scaled(200, 200, QtCore.Qt.KeepAspectRatio)  # Điều chỉnh kích thước hình ảnh

        # Tạo một QLabel
        label = QtWidgets.QLabel(self)

        # Hiển thị hình ảnh trong QLabel và thiết lập border-radius
        label.setPixmap(pixmap)
        label.setScaledContents(True)
        label.setStyleSheet("QLabel { border-radius: 100px; border: 2px solid gray; }")  # border-radius được thiết lập thành nửa chiều rộng của QLabel

        self.setWindowTitle("Hiển Thị Hình Ảnh Hình Tròn")
        self.setGeometry(100, 100, 200, 200)
        self.show()

if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    window = MainWindow()
    app.exec_()

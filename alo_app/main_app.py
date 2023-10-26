import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from ui.home_ui import Ui_home

class HomeUI(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_home()
        self.ui.setupUi(self)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    home = HomeUI()
    home.show()
    sys.exit(app.exec_())
    
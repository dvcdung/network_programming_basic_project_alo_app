from PyQt5 import QtCore, QtGui, QtWidgets
from uis.home_ui import Ui_home
from networks.app_network import Net

class HomeUI(QtWidgets.QMainWindow):
    def __init__(self, net: Net()):
        super().__init__()
        self.ui = Ui_home()
        self.ui.setupUi(self)

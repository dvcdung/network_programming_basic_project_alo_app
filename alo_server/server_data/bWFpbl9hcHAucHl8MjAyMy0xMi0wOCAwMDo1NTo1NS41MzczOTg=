import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from modules.home import HomeUI
from modules.log import LogUI
from networks.app_network import Net

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    net = Net()
    
    log_ui = LogUI(net)
    home_ui = HomeUI(net)

    log_ui.home_ui = home_ui
    home_ui.log_ui = log_ui
    
    log_ui.show()
    sys.exit(app.exec_())
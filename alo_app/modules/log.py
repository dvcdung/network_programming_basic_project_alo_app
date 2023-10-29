from PyQt5 import QtCore, QtGui, QtWidgets
from uis.log_ui import Ui_Log
from networks.app_network import Net

class LogUI(QtWidgets.QMainWindow):
    def __init__(self, net):
        super().__init__()
        self.ui = Ui_Log()
        self.ui.setupUi(self)
        self.set_login_widget()

    def set_login_widget(self, username="", password=""):
        self.ui.loginWidget.setVisible(True)
        self.ui.registerWidget.setVisible(False)
        self.ui.inputLoginUsername.setText(username)
        self.ui.inputLoginPassword.setText(password)

    def set_register_widget(self, username="", password="", repassword=""):
        self.ui.loginWidget.setVisible(False)
        self.ui.registerWidget.setVisible(True)
        self.ui.inputRegisterUsername.setText(username)
        self.ui.inputRegisterPassword.setText(password)
        self.ui.inputRegisterRePassword.setText(repassword)
    
    def create_account(self, net: Net):
        username = self.ui.inputRegisterUsername.text
        password = self.ui.inputRegisterPassword.text
        repassword = self.ui.inputRegisterRePassword.text
        if (password != repassword):
            self.ui.warningLabel1.setText("The passwords you entered are not the same!")
            return
        net.connect_to_server()
        data = f"{username}|{password}"
        net.send_to_server("0000", data)
        sv_status, sv_data = net.receive_from_server()
        if (sv_status == "OK"):
            self.set_register_widget()
            self.set_login_widget(username, password)
        else:
            self.ui.warningLabel1.setText(sv_data)

    def login(self, net: Net):
        username = self.ui.inputLoginUsername.text
        password = self.ui.inputLoginPassword.text
        if (not self.are_login_fields_valid(username, password)):
            self.ui.warningLabel.setText("Input fields must be filled!")
            return
        net.connect_to_server()
        data = f"{username}|{password}"
        net.send_to_server("0001", data)
        sv_status, sv_data = net.receive_from_server()
        if (sv_status == "OK"):
            self.home_ui.show()
        else:
            self.ui.warningLabel.setText(sv_data)

    def are_login_fields_valid(self, username, password):
        if (not username or not password):
            return False

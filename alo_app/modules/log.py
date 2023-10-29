from PyQt5 import QtCore, QtGui, QtWidgets
from uis.log_ui import Ui_Log
from networks.app_network import Net
from functools import partial

class LogUI(QtWidgets.QMainWindow):
    def __init__(self, net):
        super().__init__()
        self.ui = Ui_Log()
        self.ui.setupUi(self)
        self.ui.btnLoginWidget.clicked.connect(self.set_login_widget)
        self.ui.btnRegisterWidget.clicked.connect(self.set_register_widget)
        self.ui.btnRegister.clicked.connect(partial(self.create_account, net))
        self.ui.btnLogin.clicked.connect(partial(self.login, net))
        self.set_login_widget()

    def set_login_widget(self, username="", password=""):
        self.ui.loginWidget.setVisible(True)
        self.ui.registerWidget.setVisible(False)
        self.ui.inputLoginUsername.setText(username or "")
        self.ui.inputLoginPassword.setText(password or "")

    def set_register_widget(self, username="", password="", repassword=""):
        self.ui.loginWidget.setVisible(False)
        self.ui.registerWidget.setVisible(True)
        self.ui.inputRegisterUsername.setText(username or "")
        self.ui.inputRegisterPassword.setText(password or "")
        self.ui.inputRegisterRePassword.setText(repassword or "")
    
    def create_account(self, net: Net):
        username = self.ui.inputRegisterUsername.text()
        password = self.ui.inputRegisterPassword.text()
        repassword = self.ui.inputRegisterRePassword.text()
        isValid, error = self.validate_registration_input(username, password, repassword)
        if (not isValid):
            self.ui.warningLabel1.setText(error)
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
        username = self.ui.inputLoginUsername.text()
        password = self.ui.inputLoginPassword.text()
        isValid, error = self.validate_login_input(username, password)
        if (not isValid):
            self.ui.warningLabel.setText(error)
            return
        net.connect_to_server()
        data = f"{username}|{password}"
        net.send_to_server("0001", data)
        sv_status, sv_data = net.receive_from_server()
        if (sv_status == "OK"):
            self.home_ui.show()
            self.close()
        else:
            self.ui.warningLabel.setText(sv_data)

    def validate_login_input(self, username, password):
        if (not username or not password):
            return (False, "Input fields must be filled!")
        return (True, "")

    def validate_registration_input(self, username, password, repassword):
        if (not username or not password or not repassword):
            return (False, "Input fields must be filled!")
        elif (password != repassword):
            return (False, "The passwords you entered are not the same!")
        return (True, "")
import typing
from PyQt5 import QtCore, QtGui, QtWidgets
from uis.home_ui import Ui_home
from networks.app_network import Net
from functools import partial
import time
import json
        
from PyQt5.QtCore import QThread, QTimer, pyqtSignal

class LoadMsgsThread(QThread):
    update_signal = pyqtSignal(list)

    def __init__(self, net, session_id):
        super(LoadMsgsThread, self).__init__()
        self.net = net
        self.session_id = session_id

    def run(self):
        while self.session_id:
            msgs = self.load_msgs()
            # Send a signal to main thread
            self.update_signal.emit(msgs)
            self.msleep(1000)
            print("loading ...")

    def load_msgs(self):
        # Gọi hàm loadMsgs từ net và trả về kết quả
        self.net.send_to_server("0010", f"{self.session_id}")
        sv_status, sv_data = self.net.receive_from_server()
        if sv_status == "OK":
            try:
                msgs = json.loads(sv_data)
                return msgs
            except:
                pass
        elif str(sv_data) == "EMPTY":
            return []
        return []

class HomeUI(QtWidgets.QMainWindow):
    def __init__(self, net: Net()):
        super().__init__()
        self.ui = Ui_home()
        self.ui.setupUi(self)
        self.net = net
        self.load_msgs_thread = None
        self.ui.btnLogout.clicked.connect(partial(self.logout, net))
        self.ui.btnSearch.clicked.connect(partial(self.findUsers, net))
        self.ui.inputSearch.textChanged.connect(partial(self.findUsers, net))

    def keyPressEvent(self, event):
        key = event.key()
        if key == 16777220:
            self.ui.btnSend.click()

    def logout(self, net: Net):
        username = self.userData[1]
        net.send_to_server("0003", username)
        sv_status, sv_data = net.receive_from_server()
        if (sv_status == "OK"):
            if (self.load_msgs_thread):
                self.clearLoadMsgsThread()
            self.log_ui.show()
            self.log_ui.set_login_widget()
            self.userData = None
            self.close()

    # Search users
    def findUsers(self, net: Net):
        key = self.ui.inputSearch.text()
        if key:
            net.send_to_server("0004", f"{key}|{self.userData[0]}")
            sv_status, sv_data = net.receive_from_server()
            if (sv_status == "OK"):
                usersFound = json.loads(sv_data)
                self.ui.chatListWidget.clear()
                for userFound in usersFound:
                    userFound = {"session_id": userFound["user_id"],
                                 "session_name": userFound["display_name"],
                                 "is_a_friend": userFound["is_a_friend"]}
                    self.add_chat_item_widget(userFound, net)
            elif (sv_data == "EMPTY"):
                self.ui.chatListWidget.clear()
        else:
            self.loadChatList(net)

    # Add new chat
    def addFriend(self, net: Net, user_id): 
        net.send_to_server("0005", f"{self.userData[0]}|{user_id}")
        sv_status, _ = net.receive_from_server()
        if (sv_status):
            self.findUsers(net)

    def add_chat_item_widget(self, xfound, net: Net):
        newItem = QtWidgets.QListWidgetItem(self.ui.chatListWidget)
        newItem.setSizeHint(QtCore.QSize(191, 41))  # Đặt kích thước cho item

        chatItemWidget = QtWidgets.QWidget()
        chatItemWidget.setGeometry(QtCore.QRect(0, 5, 191, 31))
        chatItemWidget.setObjectName("chatItemWidget")
        chatItemWidget.setStyleSheet("background-color: none; border: none;")
        imgAvatar2 = QtWidgets.QLabel(chatItemWidget)
        imgAvatar2.setGeometry(QtCore.QRect(5, 5, 31, 31))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        imgAvatar2.setFont(font)
        imgAvatar2.setStyleSheet("border: 1px solid rgb(210, 210, 210);")
        imgAvatar2.setAlignment(QtCore.Qt.AlignCenter)
        imgAvatar2.setObjectName("imgAvatar2")
        imgAvatar2.setText(xfound["session_name"].strip()[:3])
        lblChatName2 = QtWidgets.QLabel(chatItemWidget)
        lblChatName2.setGeometry(QtCore.QRect(45, 10, 116, 21))
        lblChatName2.setObjectName("lblChatName2")
        lblChatName2.setText(xfound["session_name"])
        lblChatName2.setStyleSheet("border: none")
        if xfound["is_a_friend"] == 0:
            btnAddFriend = QtWidgets.QPushButton(chatItemWidget)
            btnAddFriend.setGeometry(QtCore.QRect(160, 5, 31, 31))
            btnAddFriend.setStyleSheet("border-radius: 5px; background-color: rgb(240, 240, 240);")
            btnAddFriend.setText("")
            icon7 = QtGui.QIcon()
            icon7.addPixmap(QtGui.QPixmap("uis\\../asset/icon/add_friend.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            btnAddFriend.setIcon(icon7)
            btnAddFriend.setObjectName("btnAddFriend")
            btnAddFriend.clicked.connect(partial(self.addFriend, net, xfound["session_id"]))

        self.ui.chatListWidget.addItem(newItem)
        self.ui.chatListWidget.setItemWidget(newItem, chatItemWidget)

    def loadChatList(self, net: Net):
        net.send_to_server("0006", f"{self.userData[0]}")
        sv_status, sv_data = net.receive_from_server()
        if (sv_status == "OK"):
            chatsFound = json.loads(sv_data)
            self.ui.chatListWidget.clear()
            for chatFound in chatsFound:
                self.add_chat_item_widget(chatFound, net)
            self.ui.chatListWidget.itemClicked.connect(lambda item: self.onClickChatItem(item, net, chatsFound))
        elif (sv_data == "EMPTY"):
            self.ui.chatListWidget.clear()

    def onClickChatItem(self, item, net, chatsFound):
        index = self.ui.chatListWidget.row(item)
        # chatName = self.ui.lblChatName1.text()
        # if (str(chatsFound[index]["session_name"]) != str(chatName)):
        self.ui.imgAvatar1.setText(chatsFound[index]["session_name"][:3])
        self.ui.lblChatName1.setText(chatsFound[index]["session_name"])
        self.ui.btnSend.disconnect()
        self.ui.btnSend.clicked.connect(partial(self.sendMsg, net, chatsFound[index]["session_id"]))
        self.ui.msgListWidget.clear()
        if (self.load_msgs_thread and self.load_msgs_thread.isRunning):
            print("Thread has been deleted.")
            self.clearLoadMsgsThread()
        # Tạo và kích hoạt luồng LoadMsgsThread
        self.load_msgs_thread = LoadMsgsThread(net, chatsFound[index]["session_id"])
        self.load_msgs_thread.update_signal.connect(partial(self.loadMsgs, net))
        self.load_msgs_thread.start()

    def clearLoadMsgsThread(self):
        self.load_msgs_thread.terminate()
        self.load_msgs_thread.wait()
        self.load_msgs_thread = None

    def loadMsgs(self, net: Net, msgs):
        itemsAmount = self.ui.msgListWidget.count()
        msgsLen = len(msgs)
        if (msgsLen != itemsAmount):
            for i in range(itemsAmount, msgsLen):
                self.add_msg_item_widget(msgs[i], net)

    def add_msg_item_widget(self, msg, net):
        newItem = QtWidgets.QListWidgetItem(self.ui.msgListWidget)
        newItem.setSizeHint(QtCore.QSize(501, 51))

        if (str(msg["sender_id"]) != str(self.userData[0])):
            chatMsgWidget = QtWidgets.QWidget()
            chatMsgWidget.setGeometry(QtCore.QRect(0, 0, 501, 51))
            chatMsgWidget.setAutoFillBackground(False)
            chatMsgWidget.setStyleSheet("background-color: rgba(0,0,0,0); border: none")
            chatMsgWidget.setObjectName("chatMsgWidget")
            imgAvatar3 = QtWidgets.QLabel(chatMsgWidget)
            imgAvatar3.setGeometry(QtCore.QRect(10, 20, 31, 31))
            font = QtGui.QFont()
            font.setBold(True)
            font.setWeight(75)
            imgAvatar3.setFont(font)
            imgAvatar3.setStyleSheet("border: 1px solid rgb(210, 210, 210); background-color: white")
            imgAvatar3.setAlignment(QtCore.Qt.AlignCenter)
            imgAvatar3.setObjectName("imgAvatar3")
            imgAvatar3.setText(msg["sender_name"][:3])
            txtMsg = QtWidgets.QLabel(chatMsgWidget)
            txtMsg.setGeometry(QtCore.QRect(50, 20, 391, 31))
            txtMsg.setStyleSheet("background-color: white; border: none;border-radius: 10px; padding: 5px;")
            txtMsg.setObjectName("txtMsg")
            txtMsg.setText(msg["message_text"])
            lblSender = QtWidgets.QLabel(chatMsgWidget)
            lblSender.setGeometry(QtCore.QRect(10, 0, 131, 20))
            lblSender.setObjectName("lblSender")
            lblSender.setText(msg["sender_name"])
        else:
            newItem.setSizeHint(QtCore.QSize(501, 41))
            chatMsgWidget = QtWidgets.QWidget()
            chatMsgWidget.setGeometry(QtCore.QRect(0, 110, 501, 31))
            chatMsgWidget.setAutoFillBackground(False)
            chatMsgWidget.setStyleSheet("background-color: rgba(0,0,0,0); border: none")
            chatMsgWidget.setObjectName("chatMsgWidget")
            txtMyMsg = QtWidgets.QLabel(chatMsgWidget)
            txtMyMsg.setGeometry(QtCore.QRect(110, 10, 391, 31))
            txtMyMsg.setStyleSheet("background-color: rgb(0, 160, 180); border: none;border-radius: 10px; padding: 5px; color: white")
            txtMyMsg.setObjectName("txtMyMsg")
            txtMyMsg.setText(msg["message_text"])

        self.ui.msgListWidget.addItem(newItem)
        self.ui.msgListWidget.setItemWidget(newItem, chatMsgWidget)
        self.ui.msgListWidget.scrollToBottom()

    def sendMsg(self, net: Net, session_id):
        msg = self.ui.inputMsg.text()
        if (msg):
            net.send_to_server("0011", f"{msg}|{self.userData[0]}|{session_id}")
            sv_status, sv_data = net.receive_from_server()
            if (sv_status == "OK"):
                pass
            else:
                pass
            self.ui.inputMsg.setText("")
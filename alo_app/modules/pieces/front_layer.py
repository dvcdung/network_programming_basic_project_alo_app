from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import *
from functools import partial
import json

class FrontLayer():
    def __init__(self, home):
        self.home = home 
        self.selected_friends = []
        self.frontLayerWidget = QWidget(self.home)
        self.frontLayerWidget.setFixedSize(self.home.window().size())
        self.frontLayerWidget.setStyleSheet("background-color: none")
        self.frontLayerLayout = QVBoxLayout(self.frontLayerWidget)
        
        self.coating = QWidget(self.frontLayerWidget)
        self.coating.setFixedSize(self.frontLayerWidget.screen().size())
        self.coating.setStyleSheet("background-color: rgba(0, 0, 0, 0.4)")

        self.btnClose = QtWidgets.QPushButton(self.frontLayerWidget)
        self.btnClose.setGeometry(QtCore.QRect(int(self.coating.window().size().width()-55), 5, 50, 30))
        self.btnClose.setStyleSheet("color: white; border-radius: 5px; background-color: red; border: 1px solid rgb(210, 210, 210); ")
        self.btnClose.setText("Close")

        self.mainContainer = QWidget(self.frontLayerWidget)
        self.mainContainer.setGeometry(QtCore.QRect(int(self.coating.window().size().width()/2-150), int(self.coating.window().size().height()/2-200), 300, 400))
        self.mainContainer.setStyleSheet("border: 1px solid rgb(210, 210, 210); background-color: rgb(240, 240, 240);")

        self.inputGroupName = QtWidgets.QLineEdit(self.mainContainer)
        self.inputGroupName.setGeometry(QtCore.QRect(10, 6, 231, 23))
        font = QtGui.QFont()
        font.setFamily("HoloLens MDL2 Assets")
        self.inputGroupName.setFont(font)
        self.inputGroupName.setStyleSheet("padding: 5px; border: 0px; border-radius: 10px; border: 1px solid rgb(210, 210, 210); ")
        self.inputGroupName.setText("")
        self.inputGroupName.setPlaceholderText("Enter group name ... ")

        self.btnCreateGroup = QtWidgets.QPushButton(self.mainContainer)
        self.btnCreateGroup.setGeometry(QtCore.QRect(250, 5, 41, 26))
        self.btnCreateGroup.setStyleSheet("border-radius: 5px; background-color: rgb(230, 230, 230); border: 1px solid rgb(210, 210, 210); ")
        self.btnCreateGroup.setText("Create")

        self.inputSearch = QtWidgets.QLineEdit(self.mainContainer)
        self.inputSearch.setGeometry(QtCore.QRect(10, 41, 241, 23))
        font = QtGui.QFont()
        font.setFamily("HoloLens MDL2 Assets")
        self.inputSearch.setFont(font)
        self.inputSearch.setStyleSheet("padding: 5px; border: 0px; border-radius: 10px; border: 1px solid rgb(210, 210, 210); ")
        self.inputSearch.setText("")
        self.inputSearch.setPlaceholderText("Enter for searching ... ")

        self.btnSearch = QtWidgets.QPushButton(self.mainContainer)
        self.btnSearch.setGeometry(QtCore.QRect(260, 40, 31, 26))
        self.btnSearch.setStyleSheet("border-radius: 5px; background-color: rgb(230, 230, 230); border: 1px solid rgb(210, 210, 210); ")
        self.btnSearch.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("./uis\\../asset/icon/search.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnSearch.setIcon(icon)

        self.friendListWidget = QtWidgets.QListWidget(self.mainContainer)
        self.friendListWidget.setGeometry(QtCore.QRect(0, 70, 300, 330))
        self.friendListWidget.setStyleSheet("border: 1px solid rgb(210, 210, 210); ")
        self.friendListWidget.setFrameShape(QtWidgets.QFrame.Box)
        self.friendListWidget.setFrameShadow(QtWidgets.QFrame.Plain)
        self.friendListWidget.setLineWidth(1)
        self.friendListWidget.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.friendListWidget.setVerticalScrollMode(QtWidgets.QAbstractItemView.ScrollPerItem)

        self.frontLayerWidget.hide()

        self.btnClose.clicked.connect(lambda: self.hideFrontLayer())
        self.btnCreateGroup.clicked.connect(lambda: self.createGroup())

    def showFrontLayer(self):
        self.loadFriendsList()
        self.frontLayerWidget.show()

    def hideFrontLayer(self):
        if not self.frontLayerWidget.isHidden():
            self.frontLayerWidget.hide()

    def loadFriendsList(self):
        self.home.net.send_to_server("0007", f"{self.home.userData[0]}")
        sv_status, sv_data = self.home.net.receive_from_server()
        if (sv_status == "OK"):
            friendsFound = json.loads(sv_data)
            self.setFriendsList(friendsFound)
        elif (sv_data == "EMPTY"):
            self.friendListWidget.clear()
           
    
    def setFriendsList(self, friendsFound):
        self.friendListWidget.clear()
        self.selected_friends = []
        for friend in friendsFound:
            newItem = QtWidgets.QListWidgetItem(self.friendListWidget)
            newItem.setSizeHint(QtCore.QSize(191, 41))  # Đặt kích thước cho item

            chatItemWidget = QtWidgets.QWidget()
            chatItemWidget.setGeometry(QtCore.QRect(0, 5, 191, 31))
            chatItemWidget.setStyleSheet("background-color: none; border: none;")

            checkbox = QCheckBox(friend["display_name"], chatItemWidget)
            checkbox.setGeometry(QtCore.QRect(10, 5, 181, 31))
            checkbox.clicked.connect(partial(self.checkSelectedFriends, friendsFound))

            self.friendListWidget.addItem(newItem)
            self.friendListWidget.setItemWidget(newItem, chatItemWidget)

    def checkSelectedFriends(self, friendsFound):
        for index in range(self.friendListWidget.count()):
            item = self.friendListWidget.item(index)
            item_widget = self.friendListWidget.itemWidget(item)
            checkbox = item_widget.findChild(QCheckBox)

            if checkbox.isChecked():
                if friendsFound[index]["user_id"] not in self.selected_friends:
                    self.selected_friends.append(friendsFound[index]["user_id"])
                    print(self.selected_friends)
            else:
                if friendsFound[index]["user_id"] in self.selected_friends:
                    self.selected_friends.remove(friendsFound[index]["user_id"])

    def createGroup(self):
        if self.inputGroupName.text() and len(self.selected_friends) >= 2:
            self.selected_friends.append(int(self.home.userData[0]))
            self.home.net.send_to_server("0008", f"{self.inputGroupName.text()}|{str(self.selected_friends)}")
            sv_status, sv_data = self.home.net.receive_from_server()
            print(sv_data)
            self.frontLayerWidget.hide()

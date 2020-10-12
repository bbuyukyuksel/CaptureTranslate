import sys
import datetime, time

import PyQt5
from PyQt5 import QtWidgets
from PyQt5 import QtCore, QtGui

from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtGui import QCursor

# Mac Test
sys.path.append('/Users/burak/Projects/Python/CaptureTranslate')
# Windows Test
sys.path.append(r'D:\Peresthayal\WorkStation\Projects\Python_Apps\CaptureTranslate')
from Database import DB
from TurengParser import Data


class Window(QtWidgets.QMainWindow):
    def showEvent(self, ev):
        self.initLayout()
        
    def __init__(self):
        super().__init__()
        self.db = DB()
        
        self.title = "Word List"
        #self.winIcon()
        self.width = 600
        self.height = 550
        if sys.platform.startswith('win'):
            sizeObject = QtWidgets.QDesktopWidget().screenGeometry(-1)
            h_width = sizeObject.width() // 2
            h_height = sizeObject.height() // 2
            top = h_height - (self.height//2) 
            left = h_width - (self.width//2)    
        else:
            top = 0
            left = 0
        self.top = top
        self.left = left

        self.initWindow()
        self.show()

    def initWindow(self):
        #self.showFullScreen()
        self.setObjectName("body")
        #self.setWindowIcon()
        self.setWindowTitle(self.title)
        self.setFixedSize(self.width, self.height)
        self.setGeometry(self.left, self.top, self.width, self.height)
        #self.setWindowFlag(QtCore.Qt.WindowCloseButtonHint, False)
        flags = QtCore.Qt.WindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint)
        self.setWindowFlags(flags)
        
    def initLayout(self):
        # DB
        self.items = list(map(lambda x: Data(ID=x[0], Type=x[1], Tr=x[2], En=x[3]), self.db.fetch()))

        ## Set Layout
        widget = QtWidgets.QWidget()
        self.setCentralWidget(widget)
        self.__UI = self.UI()
        widget.setLayout(self.__UI)
        
        #self.setLayout(self.__UI)
        
    
    def on_clicked(self):
        buttonReply = QMessageBox.question(self, 'Message', "Do you want to delete this?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if buttonReply == QMessageBox.Yes:
            button = self.sender()
            selected_id = int(button.property("ID"))
            selected_item = self.items[selected_id]
            print(selected_item.ID, selected_item.Type, selected_item.Tr, selected_item.En)
            self.db.delete(id=selected_item.ID)
            self.initLayout()
            
    def on_clicked_delete_all(self):
        buttonReply = QMessageBox.question(self, 'Message', "Do you want to delete all word list?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if buttonReply == QMessageBox.Yes:
            self.db.delete(id=None)
            self.initLayout()

    def callbackHide(self):
        self.hide()
        
    def UI(self):
        StyleSheet = '''
            QPushButton#item {
                background-color: none;
                min-width:  15px;
                max-width:  15px;
                min-height: 15px;
                max-height: 15px;
                border-radius: 10px;        
            }
            QPushButton#delete {
                background-color: #F0AB9C;
                color:white;
                min-height: 30px;
                max-height: 30px;
                border-radius: 10px;        
            }
            QPushButton#delete:hover {
                background-color: red;
                color: #fff;
                cursor:pointer;
            }

            QPushButton#delete:pressed {
                background-color: none;
            }
            QPushButton#hide {
                background-color: #886AEAFF;
                color:black;
                min-height: 30px;
                max-height: 30px;
                min-width:  200px;
                max-width:  200px;
                border-radius: 10px;        
            }
            QPushButton#hide:hover {
                background-color: #09DBFD;
                color: #fff;
                cursor:pointer;
            }

            QPushButton#hide:pressed {
                background-color: none;
            }
        '''
        self.setStyleSheet(StyleSheet)
        
        MainBox = QtWidgets.QVBoxLayout()
        MainBox.addWidget(QtWidgets.QLabel("Your Packet"))

        item_layout = QtWidgets.QVBoxLayout()
        if self.items:

            PushButton = QtWidgets.QPushButton("Delete All")
            PushButton.clicked.connect(self.on_clicked_delete_all)
            PushButton.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
            PushButton.setObjectName("delete")
            item_layout.addWidget(PushButton)

            for ID, item in enumerate(self.items):        
                row = QtWidgets.QHBoxLayout()
                PushButton = QtWidgets.QPushButton()
                PushButton.setObjectName("item")
                PushButton.setProperty("ID", str(ID))
                PushButton.setIcon(QtGui.QIcon("assets/icons/delete-80.png"))
                PushButton.setIconSize(QtCore.QSize(30,30))
                PushButton.setFixedWidth(70)
                PushButton.clicked.connect(self.on_clicked)
                PushButton.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
                row.addWidget(PushButton)

                # TYPE
                label = QtWidgets.QLabel(item.Type)
                row.addWidget(label)
                
                # EN
                label = QtWidgets.QLabel(item.En)
                row.addWidget(label)
                
                # TR        
                label = QtWidgets.QLabel(item.Tr)
                row.addWidget(label)
                item_layout.addLayout(row)
                
        w = QtWidgets.QWidget()
        w.setLayout(item_layout)

        # region scroll
        scroll = QtWidgets.QScrollArea()
        scroll.setWidget(w)
        scroll.setWidgetResizable(True)
        scroll.setFixedHeight(500)
        MainBox.addWidget(scroll)

        hideButton = QtWidgets.QPushButton("Hide")
        hideButton.setObjectName("hide")
        hideButton.clicked.connect(self.callbackHide)
        MainBox.addWidget(hideButton, alignment=QtCore.Qt.AlignCenter)
        return MainBox

        
if __name__ == '__main__':
    App = PyQt5.QtWidgets.QApplication(sys.argv)
    window = Window()
    sys.exit(App.exec())
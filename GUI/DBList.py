import sys
import datetime, time

import PyQt5
from PyQt5 import QtWidgets
from PyQt5 import QtCore, QtGui

from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtGui import QCursor


sys.path.append('/Users/burak/Projects/Python/CaptureTranslate')
from Database import DB
from TurengParser import Data


class Window(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        self.db = DB()

        self.title = "Word List"
        #self.winIcon()
        self.top = 0
        self.left = 0
        self.width = 600
        self.height = 550
    
        self.initWindow()
        self.initLayout()
        self.show()

    def initWindow(self):
        #self.showFullScreen()
        
        self.setObjectName("body")
        #self.setWindowIcon()
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.setFixedSize(self.width, self.height)
        

    def initLayout(self):
        # DB
        self.items = list(map(lambda x: Data(ID=x[0], Type=x[1], Tr=x[2], En=x[3]), self.db.fetch()))

        ## Set Layout
        widget = QtWidgets.QWidget()
        self.setCentralWidget(widget)
        self.__UI = self.UI()
        widget.setLayout(self.__UI)
        
    
    
    def on_clicked(self):

        buttonReply = QMessageBox.question(self, 'Message', "Do you want to delete this?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if buttonReply == QMessageBox.Yes:
            button = self.sender()
            selected_id = int(button.objectName())
            selected_item = self.items[selected_id]
            print(selected_item.ID, selected_item.Type, selected_item.Tr, selected_item.En)
            self.db.delete(id=selected_item.ID)
            self.initLayout()

    def on_clicked_delete_all(self):
        buttonReply = QMessageBox.question(self, 'Message', "Do you want to delete all word list?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if buttonReply == QMessageBox.Yes:
            self.db.delete(id=None)
            self.initLayout()
        
    def UI(self):
        StyleSheet = '''
            QPushButton {
                background-color: none;
                min-width:  15px;
                max-width:  15px;
                min-height: 15px;
                max-height: 15px;
                border-radius: 10px;        
            }
            '''
        StyleSheetDelete = '''
            QPushButton {
                background-color: #F0AB9C;
                color:white;
                min-height: 30px;
                max-height: 30px;
                border-radius: 10px;        
            }
            QPushButton:hover {
                background-color: red;
                color: #fff;
                cursor:pointer;
            }

            QPushButton:pressed {
                background-color: none;
            }
        '''
        MainBox = QtWidgets.QVBoxLayout()

        MainBox.addWidget(QtWidgets.QLabel("Your Packet"))

        layout = QtWidgets.QVBoxLayout()


        if self.items:
            PushButton = QtWidgets.QPushButton("Delete All")
            PushButton.clicked.connect(self.on_clicked_delete_all)
            PushButton.setStyleSheet(StyleSheetDelete)
            PushButton.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
            layout.addWidget(PushButton)

            for ID, item in enumerate(self.items):        

                row = QtWidgets.QHBoxLayout()

                PushButton = QtWidgets.QPushButton()
                PushButton.setObjectName(str(ID))
                PushButton.setIcon(QtGui.QIcon("assets/icons/delete-80.png"))
                PushButton.setIconSize(QtCore.QSize(30,30))
                PushButton.setFixedWidth(70)
                PushButton.setStyleSheet(StyleSheet)
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

                layout.addLayout(row)
        
        w = QtWidgets.QWidget()
        w.setLayout(layout)

        scroll = QtWidgets.QScrollArea()
        scroll.setWidget(w)
        scroll.setWidgetResizable(True)
        scroll.setFixedHeight(500)

        MainBox.addWidget(scroll)
        return MainBox

if __name__ == '__main__':
    App = PyQt5.QtWidgets.QApplication(sys.argv)
    window = Window()
    sys.exit(App.exec())
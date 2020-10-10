import sys
import datetime, time

import PyQt5
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMessageBox

from PyQt5 import QtCore, QtGui
from PyQt5.QtGui import QCursor

from GUI.MainWindowSignals import Translater
from Database import DB

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.db = DB()

        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        self.title = "Capture Translate"
        #self.winIcon()
        self.top = 0
        self.left = 0
        self.width = 600
        self.height = 600
        
        
        self.initWindow()

    def initWindow(self):
        #self.showFullScreen()
        
        self.setObjectName("body")
        #self.setWindowIcon()
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.setFixedSize(self.width, self.height)
        
        # Signals
        LabelUpdater = Translater()
        LabelUpdater.signal_data_ready.connect(self.onSignalDataReady)
        LabelUpdater.start()


    def initLayout(self):
        # Set Layout
        widget = QtWidgets.QWidget()
        self.setCentralWidget(widget)
        self.__UI = self.UI()
        widget.setLayout(self.__UI)


    def onSignalDataReady(self, items):
        self.items = items
        self.initWindow()
        self.initLayout()
        self.show()

    def on_clicked(self):
        button = self.sender()
        selected_id = int(button.objectName())
        selected_item = self.items[selected_id]
        
        buttonReply = QMessageBox().question(self, 'Message', f"Do you want to append '{selected_item.En.split('  ')[0]} - {selected_item.Tr}' to your word list?", QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
        
        if buttonReply == QMessageBox.Yes:
            self.db.delete(id=None)
            self.initLayout()

        print(selected_item.Type, selected_item.Tr, selected_item.En)
        self.hide()

    def UI(self):
        StyleSheet = '''
            QPushButton {
                background-color: none;
                /* Ограничьте минимальный размер */
                min-width:  30px;
                max-width:  30px;
                min-height: 30px;
                max-height: 30px;
                border-radius: 10px;        /* круглый */
            }

            QPushButton:hover {
                background-color: lightgreen;
                color: #fff;
            }

            QPushButton:pressed {
                background-color: none;
            }
            '''
        MainBox = QtWidgets.QVBoxLayout()

        MainBox.addWidget(QtWidgets.QLabel("Please select translate"))

        layout = QtWidgets.QVBoxLayout()

        if self.items:
            layout.addWidget(QtWidgets.QLabel(f"Clipboard Item: {self.items[0].En}"))
            for ID, item in enumerate(self.items):        
                row = QtWidgets.QHBoxLayout()

                PushButton = QtWidgets.QPushButton()
                PushButton.setObjectName(str(ID))
                PushButton.setIcon(QtGui.QIcon("assets/icons/check-mark-96.png"))
                PushButton.setIconSize(QtCore.QSize(30,30))
                PushButton.setFixedWidth(70)
                PushButton.setStyleSheet(StyleSheet)
                PushButton.clicked.connect(self.on_clicked)
                PushButton.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
                row.addWidget(PushButton)

                # TYPE
                label = QtWidgets.QLabel(item.Type)
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
    window = MainWindow()
    sys.exit(App.exec())
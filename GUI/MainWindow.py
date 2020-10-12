import sys
import datetime, time

import PyQt5
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMessageBox

from PyQt5 import QtCore, QtGui
from PyQt5.QtGui import QCursor

from GUI import DBList
from GUI.MainWindowSignals import Translater
from Database import DB

from pynput import keyboard

class HotKeyListener(QtCore.QThread):
    on_activate_wordlist =  QtCore.pyqtSignal()

    def __init__(self):
        super().__init__()

    def run(self):
        print("Listener")
        listener = None
        if sys.platform.startswith('win'):
            listener = keyboard.GlobalHotKeys({
                '<ctrl>+b':self.handler_activate_wordlist,
        })
        listener.start()
        listener.join()
    
    def handler_activate_wordlist(self):
        print("Emit")
        self.on_activate_wordlist.emit()




class MainWindow(QtWidgets.QMainWindow):
    # DBList Window
    w_dblist = None

    def __init__(self):
        super().__init__()
        self.db = DB()

        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        self.title = "Capture Translate"
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

    def initWindow(self):        
        # Window Flags
        flags = QtCore.Qt.WindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint)
        self.setWindowFlags(flags)
        
        self.setObjectName("body")
        #self.setWindowIcon()
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.setFixedSize(self.width, self.height)
        
        # Signals
        LabelUpdater = Translater()
        LabelUpdater.signal_data_ready.connect(self.onSignalDataReady)
        LabelUpdater.start()
        
        self.hkListener = HotKeyListener()
        self.hkListener.start()
        self.hkListener.on_activate_wordlist.connect(self.activate_wordlist)

    def activate_wordlist(self):
        if self.w_dblist == None:
            self.w_dblist = DBList.Window()
            self.w_dblist.show()
        else:
            self.w_dblist.show()

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
            # Append selected item into database.
            print(selected_item.Type, selected_item.Tr, selected_item.En)
            self.db.append(selected_item.Type, selected_item.Tr, selected_item.En.split('  ')[0])
            self.initLayout()

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
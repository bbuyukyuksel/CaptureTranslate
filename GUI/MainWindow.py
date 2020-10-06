import sys
import datetime, time

import PyQt5
from PyQt5 import QtWidgets
from PyQt5 import QtCore, QtGui

#from MainWindowSignals import Updater


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        self.title = "Test"
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

        # Set Layout
        widget = QtWidgets.QWidget()
        self.setCentralWidget(widget)
        UI = self.UI()
        widget.setLayout(UI)


        # Signals
        '''
        LabelUpdater = Updater()
        LabelUpdater.update.connect(self.onLabelUpdate)
        LabelUpdater.start()
        '''

        #self.show()

    def onLabelUpdate(self, text):
        pass
        #print("Updated", text)
    
    def on_clicked(self):
        button = self.sender()
        print(button.objectName())
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
        for i in range(15):        
            row = QtWidgets.QHBoxLayout()
            
            PushButton = QtWidgets.QPushButton()
            PushButton.setObjectName(f"Button#{i}")
            PushButton.setIcon(QtGui.QIcon("assets/icons/check-mark-96.png"))
            PushButton.setIconSize(QtCore.QSize(30,30))
            PushButton.setFixedWidth(70)
            PushButton.setStyleSheet(StyleSheet)
            PushButton.clicked.connect(self.on_clicked)
            row.addWidget(PushButton)
        
            label = QtWidgets.QLabel(f"TR {i}")
            row.addWidget(label)

            label = QtWidgets.QLabel(f"EN {i}")
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
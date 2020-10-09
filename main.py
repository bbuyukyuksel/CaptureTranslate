import PyQt5
import sys

from GUI.MainWindow import MainWindow

if __name__ == '__main__':
    App = PyQt5.QtWidgets.QApplication(sys.argv)
    mainWindow = MainWindow()
    sys.exit(App.exec())    
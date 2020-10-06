import globals

from tabulate import tabulate
from TurengParser import TurengParser
from ClipboardListener import ClipboardListener

from GUI.MainWindow import MainWindow
import PyQt5
import sys


def handler(text):
    global mainWindow

    items = TurengParser().search(text)
    table = map(lambda x: [x.Type, x.En, x.Tr], items)
    print(tabulate(table, headers=["Type", "En", "Tr"], showindex="always", tablefmt="fancy_grid"))

def main():
    ClipboardListener(handler).start()
    #globals.wait.wait()



if __name__ == '__main__':
    App = PyQt5.QtWidgets.QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    main()    
    sys.exit(App.exec())    
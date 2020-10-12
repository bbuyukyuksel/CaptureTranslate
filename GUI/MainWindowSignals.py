from PyQt5 import QtCore
import datetime, time

from tabulate import tabulate
from ClipboardListener import ClipboardListener
from TurengParser import TurengParser

class Translater(QtCore.QThread):

    signal_data_ready = QtCore.pyqtSignal(list)

    def __init__(self):
        super().__init__()
        ClipboardListener(self.handler).start()

    def run(self):
        while True:
            time.sleep(1)

    def handler(self,text):
        if text is not None:
            items = TurengParser().search(text)
            # Tabulate Console Print
            '''
            table = map(lambda x: [x.Type, x.En, x.Tr], items)
            print(tabulate(table, headers=["Type", "En", "Tr"], showindex="always",     tablefmt="fancy_grid"))
            '''
            self.signal_data_ready.emit(items)


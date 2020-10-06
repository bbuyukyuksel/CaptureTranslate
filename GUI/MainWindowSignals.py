from PyQt5 import QtCore
import datetime, time

class Updater(QtCore.QThread):
    update = QtCore.pyqtSignal(str)
    def run(self):
        while True:
            self.update.emit(f"Hello World {str(datetime.datetime.now())}")
            time.sleep(1)


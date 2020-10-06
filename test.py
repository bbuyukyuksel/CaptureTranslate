from PyQt5 import QtWidgets
import sys

app = QtWidgets.QApplication(sys.argv)

w = QtWidgets.QWidget()



label = QtWidgets.QLabel(w)
label.setText("Hello world")

w.show()
sys.exit(app.exec_())



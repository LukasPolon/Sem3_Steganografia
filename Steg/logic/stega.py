import sys
import os
from PyQt4 import QtCore, QtGui

import design
# from design import Ui_MainWindow

class Stega(QtGui.QMainWindow, design.Ui_MainWindow):
    def __init__(self, parent=None):
        super(Stega, self).__init__(parent)
        self.setupUi(self)

def main():
    app = QtGui.QApplication(sys.argv)
    form = Stega()
    form.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()

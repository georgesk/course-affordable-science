#!/usr/bin/python3

import sys
from PyQt4 import QtGui, QtCore
from UI_oscill import Ui_MainWindow
from qwt import QwtPlotCurve

class MyWindow(QtGui.QMainWindow):
    def __init__(self, parent=None):
        QtGui.QMainWindow.__init__(self, parent)
        self.ui=Ui_MainWindow()
        self.ui.setupUi(self)
        # connect methods to buttons' click signals
        self.ui.wakeUpButton.clicked.connect(self.wakeUp)
        self.ui.stopButton.clicked.connect(self.stop)
        self.ui.closeButton.clicked.connect(self.close)
        self.ui.saveButton.clicked.connect(self.save)
        self.ui.immediateButton.clicked.connect(self.immediate)
        self.ui.finalButton.clicked.connect(self.final)
        self.ui.fitButton.clicked.connect(self.fit)
        self.ui.action_Save_Ctrl_S.triggered.connect(self.save)
        self.ui.action_Quit_Ctrl_Q.triggered.connect(self.close)
        self.ui.actionManual.triggered.connect(self.manual)
        self.ui.actionAbout.triggered.connect(self.about)
        return

    def notImplemented(self):
        msg=QtGui.QMessageBox(QtGui.QMessageBox.Warning,"Sorry",
                              "not yet implemented", )
        msg.exec_()
        return

    wakeUp=stop=save=immediate=final=fit=manual=about=notImplemented


if __name__=="__main__":
    app=QtGui.QApplication(sys.argv)
    window=MyWindow()
    window.show()
    sys.exit(app.exec_())

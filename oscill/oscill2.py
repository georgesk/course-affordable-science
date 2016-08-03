#!/usr/bin/python3

import sys
from PyQt4 import QtGui, QtCore
from UI_oscill import Ui_MainWindow
from qwt import QwtPlotCurve
import numpy as np
# using the right module for expEYES Junior (alias: ej)
import expeyes.eyesj as ej

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
        # initialize an empty curve for the plot widget
        self.curve         = QwtPlotCurve()
        self.curve.attach(self.ui.qwtPlot)
        # expEYESdetection and initialization
        try:
            self.p             = ej.open()
            assert(self.p.fd)
            self.setWindowTitle("expEYES Junior found on port {}".format(
                self.p.fd.port
            ))
        except:
            self.setWindowTitle("ERROR: expEYES Junior NOT FOUND!")
            self.wakeUpButton.setEnabled(False)
        # custom properties
        self.isImmediate=True
        return
        
    def immediate(self):
        self.isImmediate=True
        return
        
    def final(self):
        self.isImmediate=False
        return

    def wakeUp(self):
        # get the duration of the experiment in µs
        duration = 1e6 * float(self.ui.durationEdit.text())
        samples  = 1800 # maximum sample number with 8 bit precision
        # ensure that samples * delay will be slightly bigger than duration
        delay=1+int(duration/1800)
        t,v = self.p.capture(1,samples, delay)
        self.curve.setData(t,v,len(t))
        # display the result
        self.ui.qwtPlot.replot()
        return

        
    def notImplemented(self):
        msg=QtGui.QMessageBox(QtGui.QMessageBox.Warning,"Sorry",
                              "not yet implemented", )
        msg.exec_()
        return

    stop=save=fit=manual=about=notImplemented


if __name__=="__main__":
    app=QtGui.QApplication(sys.argv)
    window=MyWindow()
    window.show()
    sys.exit(app.exec_())

#!/usr/bin/python3

import sys
from PyQt4 import QtGui, QtCore
from UI_oscill import Ui_MainWindow
from qwt import QwtPlotCurve, QwtPlot
import numpy as np
# using the right module for expEYES Junior (alias: ej)
import expeyes.eyesj as ej
import time

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
        # create a timer
        self.stopTime=time.time()
        self.timer=QtCore.QTimer()
        # connect the timer to the "tick" callback method
        self.timer.timeout.connect(self.tick)
        # 20 times per second
        self.timer.start(50)
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
        # get the duration of the experiment in s
        duration = float(self.ui.durationEdit.text())
        if duration < 3.5: # "final" mode is possible
            samples  = 1800 # maximum sample number with 8 bit precision
            # ensure that samples * delay will be slightly bigger than duration
            delay=1+int(duration*1e6/1800)
            t,v = self.p.capture(1,samples, delay)
            self.curve.setData(t,v,len(t))
            # not necessary since the widget has the autoreplot feature
            # self.ui.qwtPlot.replot()
        else:
            self.ui.immediateButton.setChecked(True)
            self.isImmediate=True
            self.ui.qwtPlot.setAxisScale(QwtPlot.xBottom, 0, duration)
            now=time.time()
            self.t=[]
            self.v=[]
            self.curve.setData([],[],0)
            self.startTime=now
            self.stopTime=now+duration
            # now the curve will grow until time.time >= self.stopTime
            # thanks to self.timer's timeout events
        return

    def tick(self):
        """ Callback for the timeout events """
        t=time.time()
        if t < self.stopTime:
            v = self.p.get_voltage(1)
            self.t.append(time.time()-self.startTime)
            self.v.append(v)
            self.curve.setData(self.t, self.v, len(self.t))
            # not necessary since the widget has the autoreplot feature
            # self.ui.qwtPlot.replot()
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

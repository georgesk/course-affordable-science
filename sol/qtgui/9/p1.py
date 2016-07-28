#!/usr/bin/python3

import sys
from PyQt4 import QtGui, QtCore
from UI_p1 import Ui_MainWindow
from qwt import QwtPlotCurve
import numpy as np
# using the right module for expEYES Junior (alias: ej)
import expeyes.eyesj as ej

class MyWindow(QtGui.QMainWindow):
    """
    This class implements a derivative of
    PyQt4.QtGui.QMainWindow, a complete application
    window, which can feature menus, submenus,
    status bar, etc. In this example, it uses
    few of those features.
    """

    def __init__(self, parent=None):
        """
        Constructor: creates an instance of MyWindow
        """
        #########################################
        # Necessary actions, which must be done #
        # for any project                       #
        #########################################
        # first, calling the ancestor's creator
        QtGui.QMainWindow.__init__(self, parent)
        # get the User Interface from the module UI_p1
        self.ui=Ui_MainWindow()
        # initialize the user interface
        self.ui.setupUi(self)
        #########################################
        # Custom actions, which can be written  #
        # in other ways for other projects.     #
        #########################################
        # aliases for some parts of the user interface
        self.plotWidget    = self.ui.qwtPlot
        self.measureButton = self.ui.measureButton
        self.closeButton   = self.ui.closeButton
        # connect methods to buttons' click signals
        self.measureButton.clicked.connect(self.measure)
        self.closeButton.clicked.connect(self.close)
        # initialize 4 empty curves for the plot widget
        self.curves=[]
        colors=[
          QtGui.QColor("#000000"), #black
          QtGui.QColor("#ff0000"), #red
          QtGui.QColor("#0000ff"), #blue
          QtGui.QColor("#00cc00"), #dark green
        ]
        for i in range(4):
            c=QwtPlotCurve()
            c.setPen(colors[i])
            self.curves.append(c)
            c.attach(self.plotWidget)
        # initialize the driver for expEYES Junior
        # prevent an error if the box is not detected
        try:
            self.p             = ej.open()
            assert(self.p.fd)
            self.setWindowTitle("expEYES Junior found on port {}".format(
                self.p.fd.port
            ))
        except:
            self.setWindowTitle("ERROR: expEYES Junior NOT FOUND!")
            self.measureButton.setEnabled(False)
        return

    def measure(self):
        """
        This is a custom method to connect to the
        button for measurements.
        There is no need for another custom method,
        since the method "close" is already inherited
        from the ancestor class.
        """
        sample=int(self.ui.samplesEdit.text())
        delay=int(self.ui.delayEdit.text())
        channels=self.inputCodes()
        duration=int(sample*delay/1000) # in ms
        if len(channels) < 1 or len(channels) > 4:
            self.ui.statusbar.showMessage("Bad number of channels selected. At least on channel, at most four channels!")
            return
        self.ui.statusbar.showMessage(
            "Measuring data for {} seconds, please be patient...".format(duration/1000),
            duration
        )
        self.ui.statusbar.repaint() # immediately shows the status
        # erase the curves
        for c in self.curves:
            c.setData([],[],0)
        if len(channels)==1:
            t,v = self.p.capture(channels[0], sample, delay)
            self.curves[0].setData(t,v,len(t))
        elif len(channels)==2:
            t0, v0, t1, v1 = self.p.capture2(
                channels[0], channels[1],
                sample, delay
            )
            self.curves[0].setData(t0,v0, len(t0))
            self.curves[1].setData(t1,v1, len(t1))
        elif len(channels)==3:
            t0, v0, t1, v1, t2, v2 = self.p.capture3(
                channels[0], channels[1], channels[2],
                sample, delay
            )
            self.curves[0].setData(t0,v0, len(t0))
            self.curves[1].setData(t1,v1, len(t1))
            self.curves[2].setData(t2,v2, len(t2))
        elif len(channels)==4:
            t0, v0, t1, v1, t2, v2, t3, v3 = self.p.capture4(
                channels[0], channels[1], channels[2], channels[3],
                sample, delay
            )
            self.curves[0].setData(t0,v0, len(t0))
            self.curves[1].setData(t1,v1, len(t1))
            self.curves[2].setData(t2,v2, len(t2))
            self.curves[3].setData(t3,v3, len(t3))
        # display the result
        self.plotWidget.replot()
        return

    def inputCodes(self):
        """
        considers the check buttons
        @return a list of codes for selected input channels
        """
        value={
            "A1":  1,
            "A2":  2,
            "IN1": 3,
            "IN2": 4,
            "SEN": 5,
        }
        result=[]
        chks=[c for c in self.ui.groupBox.children()
                  if isinstance(c, QtGui.QCheckBox)]
        for c in chks:
            if c.isChecked():
                result.append(value[c.text().strip()])
        return result

if __name__=="__main__":
    app=QtGui.QApplication(sys.argv)
    window=MyWindow()
    window.show()
    sys.exit(app.exec_())

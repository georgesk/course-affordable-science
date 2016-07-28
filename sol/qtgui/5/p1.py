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
        # initialize an empty curve for the plot widget
        self.curve         = QwtPlotCurve()
        self.curve.attach(self.plotWidget)
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
        sample=1000
        delay=2000                      # in µs
        duration=int(sample*delay/1000) # in ms
        self.ui.statusbar.showMessage(
            "Measuring data for {} seconds, please be patient...".format(duration/1000),
            duration
        )
        self.ui.statusbar.repaint() # immediately shows the status
        t,v = self.p.capture(1, sample, delay)
        self.curve.setData(t,v,len(t))
        # display the result
        self.plotWidget.replot()
        return

if __name__=="__main__":
    app=QtGui.QApplication(sys.argv)
    window=MyWindow()
    window.show()
    sys.exit(app.exec_())

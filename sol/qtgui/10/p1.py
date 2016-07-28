#!/usr/bin/python3

import sys
from PyQt4 import QtGui, QtCore
from UI_p1 import Ui_MainWindow
from qwt import QwtPlotCurve
import numpy as np
# using the right module for expEYES Junior (alias: ej)
import expeyes.eyesj as ej
from expeyes import eyemath
from qwt import QwtPlot

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
        self.measureButton = self.ui.measureButton
        self.closeButton   = self.ui.closeButton
        # connect methods to buttons' click signals
        self.measureButton.clicked.connect(self.measure)
        self.closeButton.clicked.connect(self.close)
        # initialize an empty curve for the signal plot widget
        self.signal = QwtPlotCurve()
        self.signal.attach(self.ui.signalPlot)
        self.ui.signalPlot.setAxisTitle(QwtPlot.xBottom, "t (ms)")
        self.ui.signalPlot.setAxisTitle(QwtPlot.yLeft, "voltage (V)")
        self.ui.signalPlot.setTitle("Signal")
        # and another for the fft plotwidget
        self.fft    = QwtPlotCurve()
        self.fft.attach(self.ui.fftPlot)
        self.ui.fftPlot.setAxisTitle(QwtPlot.xBottom, "f (Hz)")
        self.ui.fftPlot.setAxisTitle(QwtPlot.yLeft, "amplitude")
        self.ui.fftPlot.setTitle("Fourier Transform")
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
        channel=self.inputCode()
        duration=int(sample*delay/1000) # in ms
        self.ui.statusbar.showMessage(
            "Measuring data for {} seconds, please be patient...".format(duration/1000),
            duration
        )
        self.ui.statusbar.repaint() # immediately shows the status
        t,v = self.p.capture(channel, sample, delay)
        self.signal.setData(t,v,len(t))
        # compute the FFT data and plot them
        xa,ya = eyemath.fft(v,delay)
        xa=1000*xa #(convert kHz to Hz)
        self.fft.setData(xa, ya, len(xa))
        # display the result
        self.ui.signalPlot.replot()
        self.ui.fftPlot.replot()
        return

    def inputCode(self):
        """
        considers the radio buttons
        @return the code for the selected input channel
        """
        value={
            "A1":  1,
            "A2":  2,
            "IN1": 3,
            "IN2": 4,
            "SEN": 5,
        }
        radios=[r for r in self.ui.groupBox.children()
                  if isinstance(r, QtGui.QRadioButton)]
        for r in radios:
            if r.isChecked():
                return value[r.text().strip()]
        return 0

if __name__=="__main__":
    app=QtGui.QApplication(sys.argv)
    window=MyWindow()
    window.show()
    sys.exit(app.exec_())

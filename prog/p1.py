#!/usr/bin/python3

import sys
from PyQt4 import QtGui, QtCore
from UI_p1 import Ui_MainWindow
from qwt import QwtPlotCurve
import numpy as np

class MyWindow(QtGui.QMainWindow):
    """
    This class implements a derivative of PyQt4.QtGui.QMainWindow,
    a complete application widow, which can feature menus,submenus,
    status bar, etc. In this example, it uses few of those features.
    """

    def __init__(self, parent=None):
        """
        Constructor: creates an instance of MyWindow
        """
        ##########################################################
        # Necessary actions, which must be done for any project  #
        ##########################################################
        # first, calling the ancestor's creator
        QtGui.QMainWindow.__init__(self, parent)
        # get the User Interface from the module UI_p1
        self.ui=Ui_MainWindow()
        # initialize the user interface
        self.ui.setupUi(self)
        ##########################################################
        # Custom actions, which can be written in other ways     #
        # for other projects.                                    #
        ##########################################################
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
        return

    def measure(self):
        """
        This is a custom method to connect to the button for measurements.
        .
        There is no need for another custom method, since the method
        close is already inherited from the ancestor class.
        """
        # create data for a curve with some fixed and some random features
        import random
        x=np.arange(0,8,1e-2)      # abscissa: [0, 0.01, 0.02, ... 7.99]
        r=random.random()
        y=np.sin(x)+r*np.sin(3*x)  # calculated ordinate
        # feed new data into the curve
        self.curve.setData(x,y,len(x))
        # change the title of the plot on the fly
        self.plotWidget.setTitle("sin(x) + {} sin(3x)".format(r))
        # display the result
        self.plotWidget.replot()
        return

if __name__=="__main__":
    app=QtGui.QApplication(sys.argv)
    window=MyWindow()
    window.show()
    sys.exit(app.exec_())

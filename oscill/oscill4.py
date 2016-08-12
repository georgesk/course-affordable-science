#!/usr/bin/python3

license="""\
<pre>
This program is © 2016 by Georges Khaznadar <georgesk@debian.org>

Its purpose is to demonstrate how to create a user interface for
running an experiment with expEYES-Junior (see http://expeyes.in).

Its source is part of a course named "Affordable Science Experiments";
see: 
- <a href="http://www.schooleducationgateway.eu/en/pub/teacher_academy/catalogue/detail.cfm?id=16346">http://www.schooleducationgateway.eu ...</a>
- <a href="https://github.com/georgesk/course-affordable-science">https://github.com/ ...</a>

This program is free software: you can redistribute it and/or
modify it under the terms of the GNU General Public License as
published by the Free Software Foundation, either version 3 of the
License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see
<a href="http://www.gnu.org/licenses/">http://www.gnu.org/licenses/</a>.
</pre>
"""

import sys
from PyQt4 import QtGui, QtCore
from UI_oscill import Ui_MainWindow
from qwt import QwtPlotCurve, QwtPlot
import numpy as np
# using the right module for expEYES Junior (alias: ej)
import expeyes.eyesj as ej
import expeyes.eyemath as em
from scipy import optimize
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
        self.ui.durationEdit.textChanged.connect(self.durationChanged)
        # create a timer
        self.stopTime=time.time()
        self.timer=QtCore.QTimer()
        # connect the timer to the "tick" callback method
        self.timer.timeout.connect(self.tick)
        # 20 times per second
        self.timer.start(50)
        # initialize an empty curve for the plot widget
        self.curve         = QwtPlotCurve()
        self.curve0        = QwtPlotCurve()
        self.fitCurve1     = QwtPlotCurve()
        self.fitCurve2     = QwtPlotCurve()
        self.fitCurve3     = QwtPlotCurve()
        self.curve.attach(self.ui.qwtPlot)
        self.curve0.attach(self.ui.qwtPlot)
        self.fitCurve1.attach(self.ui.qwtPlot)
        self.fitCurve2.attach(self.ui.qwtPlot)
        self.fitCurve3.attach(self.ui.qwtPlot)
        # adjust the axis scales based on duration = 15 s
        self.durationChanged(15, ampl=5)
        # set the maxvalue for the threshold rate (in V/s)
        self.maxthreshold=150/15 # = 150/duration
        # expEYESdetection and initialization
        try:
            self.p             = ej.open()
            assert(self.p.fd)
            self.setWindowTitle("expEYES Junior found on port {}".format(
                self.p.fd.port
            ))
        except:
            self.setWindowTitle("ERROR: expEYES Junior NOT FOUND!")
            self.ui.wakeUpButton.setEnabled(False)
        # custom properties
        self.isImmediate=True
        return
        
    def durationChanged(self, value, ampl=0):
        """
        Callback function for changed in ui.durationEdit
        @param value the widget's value in case of an event
        @param ampl an amplitudes (defaults to 0)
        """
        try:
            duration=float(value)
        except:
            return
        # set the axis scales for the plot widget
        self.ui.qwtPlot.setAxisScale(QwtPlot.xBottom, 0, duration)
        # draw the "zero" line
        small=duration/1e6
        self.curve0.setData([0, small, 2*small, 3*small, duration],
                            [0, ampl,  -ampl,   0,       0], 5)
        # update the threshold rate 
        self.maxThreshold=150/duration
        self.ui.thresholdLabel.setText("{} V/s".format(self.maxThreshold))
        # erase fit curves
        self.fitCurve1.setData([],[],0)
        self.fitCurve2.setData([],[],0)
        self.fitCurve3.setData([],[],0)
        return
        
    def immediate(self):
        self.isImmediate=True
        return
        
    def final(self):
        self.isImmediate=False
        return
        
    def stop(self):
        # in "final" mode, this has no effect
        # in "immediate" mode, it forces the plot to
        # stop at the next tick call.
        self.stopTime=time.time()
        return

    def save(self):
        filename=self.ui.fileNameEdit.text()
        with open(filename,"w") as outfile:
            for i in range(len(self.t)):
                outfile.write("{} {}\n".format(
                   self.t[i], self.v[i]
                ))
        self.ui.statusbar.showMessage(
            "Saved data to {}".format(filename), 3000 # 3 seconds
        )
        return
        
    def waitForThreshold(self, threshold, duration, timeOut=None):
        """
        wait for the input to change quickly enough 
        @param threshold a minimal voltage slew rate (V/s)
        @param duration the duration of scheduled measurement series
        @param timeOut the longets wait time (defaults to None)
        """
        start=time.time()
        delay=int(duration/1000*1e6) # thousandth of duration, in µs
        if delay < 4:
            delay=4
        t, v = self.p.capture(1, 2, delay)
        slewRate=(v[1]-v[0])/(t[1]-t[0])*1000
        while abs(slewRate)<threshold:
            if timeOut != None and time.time()>start+timeOut:
                return
            t, v = self.p.capture(1, 2, delay)
            slewRate=(v[1]-v[0])/(t[1]-t[0])*1000
        return

    def wakeUp(self):
        # get the duration of the experiment in s
        duration = float(self.ui.durationEdit.text())
        self.durationChanged(duration)
        if duration < 0.5: # "final" mode is mandatory
            self.ui.finalButton.setChecked(True)
            self.isImmediate=False
        elif duration > 3.5: # "immediate" mode is mandatory
            self.ui.immediateButton.setChecked(True)
            self.isImmediate=True
        # wait until the slew rate is fast enough
        threshold = self.ui.thresholdSlider.value()*self.maxThreshold/100
        self.waitForThreshold(threshold, duration, timeOut=5)
        # start measuring
        if self.isImmediate:
            now=time.time()
            self.t=[]
            self.v=[]
            self.curve.setData([],[],0)
            self.startTime=now
            self.stopTime=now+duration
            # now the curve will grow until time.time >= self.stopTime
            # thanks to self.timer's timeout events
        else:
            samples  = 1800 # maximum sample number with 8 bit precision
            # ensure that samples * delay will be slightly bigger than duration
            delay=1+int(duration*1e6/1800)
            t, self.v = self.p.capture(1,samples, delay)
            self.t=[1e-3*date for date in t] # convert ms to s
            self.curve.setData(self.t, self.v, len(self.t))
        return

    def tick(self):
        """ Callback for the timeout events """
        t=time.time()
        if t < self.stopTime:
            v = self.p.get_voltage(1)
            self.t.append(time.time()-self.startTime)
            self.v.append(v)
            self.curve.setData(self.t, self.v, len(self.t))
        return
            
    
    def fit(self):
        """
        Fitting data in self.t, self.v with a damped oscillation model
        """
        # fitting is performed by eyemath (aka em) thanks to
        # scipy.optimize, and the error function defined by
        # the module eyemath (line 92):
        # p[0] * sin(2*pi*p[1]*x+p[2]) * exp(-p[4]*x) - p[3]
        # so the vector of parameters is:
        # amplitude, frequency, phase, DC average, damping factor.
        yfit, plsq = em.fit_dsine(self.t, self.v, mode="Hz")
        # display the fitting model
        msg="{0:4.2f}*sin(2*pi*{1:4.2f}*t+({2:3.1f}))*exp(-{4:4.2f}*t)+{3:3.1f}".format(
            *plsq
        )
        self.ui.fitEdit.setText(msg)
        # display three curves : model and model's envelopes
        t=np.array(self.t)
        f1=np.array(yfit)
        f2=plsq[0]*np.exp(-plsq[4]*t)
        f3=-1.0*f2
        average=plsq[3]*np.ones(len(t))
        red=QtGui.QColor("#ff0000")
        self.fitCurve1.setPen(red)
        self.fitCurve2.setPen(red)
        self.fitCurve3.setPen(red)
        self.fitCurve1.setData(t, f1, len(t))
        self.fitCurve2.setData(t, f2+average, len(t))
        self.fitCurve3.setData(t, f3+average, len(t))
        return
        
    def about(self):
        """
        show license stuff
        """
        with open("license.html","w") as licenseFile:
            licenseFile.write("""
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN"
"http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" lang="en" xml:lang="en">
<head>
<meta  http-equiv="Content-Type" content="text/html;charset=utf-8" />
<title> About ... </title>
</head>
<body>
""")
            licenseFile.write(license)
            licenseFile.write("</body></html>")
        self.aboutWidget=QtGui.QTextBrowser(self.parent())
        self.aboutWidget.resize(600,500)
        self.aboutWidget.show()
        self.aboutWidget.setOpenExternalLinks(True)
        self.aboutWidget.setSource(QtCore.QUrl("file:license.html"))
        self.aboutWidget.setWindowTitle("About oscill4.py")
        return
        
    def manual(self):
        """
        display the manual
        """
        self.manualWidget=QtGui.QTextBrowser(self.parent())
        self.manualWidget.resize(600,500)
        self.manualWidget.show()
        self.manualWidget.setOpenExternalLinks(True)
        self.manualWidget.setSource(QtCore.QUrl("file:oscill4.html"))
        self.manualWidget.setWindowTitle("User Manual of oscill4.py")
        return
        
    def notImplemented(self):
        msg=QtGui.QMessageBox(QtGui.QMessageBox.Warning,"Sorry",
                              "not yet implemented", )
        msg.exec_()
        return



if __name__=="__main__":
    app=QtGui.QApplication(sys.argv)
    window=MyWindow()
    window.show()
    sys.exit(app.exec_())

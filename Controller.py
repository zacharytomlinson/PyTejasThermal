# -*- coding: utf-8 -*-
import serial, sys, dashboard, PyQt5, RPi.GPIO as GPIO 
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QThread, pyqtSignal, Qt
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtWidgets import QApplication, QWidget, QLabel
from time import sleep

def CelciusToFahrenheit(celcius):
    return celcius * (9.0 / 5.0) + 32

class MainWindow(QMainWindow, dashboard.Ui_StillDashboard):
    def __init__(self):
        super(self.__class__, self).__init__()
        self.setupUi(self)
				self.GPIO_1 = 18
        self.GPIO_2 = 23
				self.SetupGPIO
        self.IsRunning = False
        self.RunningStyleSheet = "QPushButton {border-radius: 7px;background: #41CD52;height: 40px;}"
        self.StoppedStyleSheet = "QPushButton {border-radius: 7px;background: #ec7063;height: 40px;}"
        self.horizontalSlider_2.valueChanged.connect(self.TemperatureChanged)
        self.pushButton.clicked.connect(self.RunDistillation)
        self.TempThread = TempThread(self)
        self.TempThread.temp1.connect(self.label_4.setText)
        self.TempThread.temp2.connect(self.label_6.setText)
        self.TempThread.temp1.connect(self.TemperatureChanged)
        self.TempThread.temp2.connect(self.TemperatureChanged)
        self.TempThread.start()

    def TemperatureChanged(self):
        newTemp = CelciusToFahrenheit(self.horizontalSlider_2.value())
        thermo1 = int(self.label_4.text()[:-2])
        thermo2 = int(self.label_6.text()[:-2])
        remain1 = (thermo1 / newTemp) * 100
        remain2 = (thermo2 / newTemp) * 100
        self.progressBar.setValue(remain1)
        self.progressBar_2.setValue(remain2)
        self.label_2.setText(str(newTemp) + "°F")
        if self.IsRunning:
            if thermo1 >= newTemp and thermo2 >= newTemp:
                self.RunDistillation 
        
    def RunDistillation(self):
        if self.IsRunning:
            self.pushButton.setStyleSheet(self.RunningStyleSheet)
            self.pushButton.setText("Start Run")
            self.IsRunning = False
            GPIO.output(self.GPIO_1,GPIO.LOW)
            GPIO.output(self.GPIO_2,GPIO.LOW)
        else:
            self.pushButton.setStyleSheet(self.StoppedStyleSheet)
            self.pushButton.setText("Stop Run")
            self.IsRunning = True
            GPIO.output(self.GPIO_1,GPIO.HIGH)
            GPIO.output(self.GPIO_2,GPIO.HIGH)
            
    def closeEvent(self, event):
        self.TempThread.stop()
        QWidget.closeEvent(self, event)
    
    def SetupGPIO(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.GPIO_1,GPIO.OUT)
				GPIO.setup(self.GPIO_2,GPIO.OUT)

class TempThread(QThread):
    temp1 = pyqtSignal(str)
    temp2 = pyqtSignal(str)
    
    def __init__(self, parent=None):
        QThread.__init__(self, parent=parent)
        self.isRunning = True
        self.SerialConn = serial.Serial('/dev/ttyACM0', 115200)

    def run(self):     
        while self.isRunning:
            line = (((self.SerialConn.readline()).decode('ASCII')).strip()).split("|")
            thermo1 = CelciusToFahrenheit(float(line[0]))
            thermo2 = CelciusToFahrenheit(float(line[1]))
            self.temp1.emit(str(int(thermo1)) + "°F")
            self.temp2.emit(str(int(thermo2)) + "°F")
        
    def stop(self):
        self.isRunning = False
        self.quit()
        self.wait()
 
def main():
    app = QApplication(sys.argv)
    form = MainWindow()
    form.setWindowFlags(PyQt5.QtCore.Qt.FramelessWindowHint)
    form.setWindowIcon(PyQt5.QtGui.QIcon("icon.ico"))
    form.show()
    sys.exit(app.exec_())
 
if __name__ == "__main__":
    main()

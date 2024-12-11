"""
Module implementing myMainWindow.
"""
import sys
from PyQt5.QtCore import pyqtSlot, QThread
from PyQt5.QtWidgets import QMainWindow, QApplication, QMessageBox

from Ui_matplotlib_pyqt import Ui_MainWindow
import Recorder


class myMainWindow(QMainWindow, Ui_MainWindow):
    """
    Class documentation goes here.
    """

    def __init__(self, parent=None):
        """
        Constructor

        @param parent reference to the parent widget
        @type QWidget
        """
        super(myMainWindow, self).__init__(parent)
        self.setupUi(self)
        self.widget.setVisible(False)  # The drawing area is initialized to be invisible

    @pyqtSlot()
    def on_startButton_clicked(self):
        """
        Slot documentation goes here.
        """
        self.widget.setVisible(True)
        self.widget.startAudio()  # Trigger the startAudio function of MatplotlibWidget


@pyqtSlot()
def on_endButton_clicked(self):
    """
    Slot documentation goes here.
    """
    self.widget.setVisible(False)
    self.widget.endAudio()  # Trigger the endAudio function of MatplotlibWidget


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ui = myMainWindow()
    ui.show()
    sys.exit(app.exec_())

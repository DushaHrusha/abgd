import sys
import matplotlib

matplotlib.use("Qt5Agg")
from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QSizePolicy, QWidget
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
import numpy as np
import pyaudio
import threading
import queue
import matplotlib.lines as line
import matplotlib.animation as animation
from scipy import signal

CHUNK = 1024
WIDTH = 2
CHANNELS = 2
RATE = 44100


class MyMplCanvas(FigureCanvas):
    """The ultimate parent class of FigureCanvas is actually QWidget."""


def __init__(self, parent=None, width=5, height=4, dpi=100):
    # Configure Chinese display
    plt.rcParams['font.family'] = ['SimHei']  # Used to display Chinese labels normally
    plt.rcParams['axes.unicode_minus'] = False  # Used to display negative signs normally

    # The initialization subgraph must be before the initialization function


    self.fig = plt.figure()
    self.rt_ax = plt.subplot(111, xlim=(0, CHUNK * 2), ylim=(-20000, 20000))
    plt.axis('off')

    FigureCanvas.__init__(self, self.fig)
    self.setParent(parent)

    '''Defines the size strategy of FigureCanvas. This part means setting FigureCanvas to fill the space as far as possible. '''
    FigureCanvas.setSizePolicy(self,
                               QSizePolicy.Expanding,
                               QSizePolicy.Expanding)
    FigureCanvas.updateGeometry(self)


class MatplotlibWidget(QWidget):
    def __init__(self, parent=None):
        super(MatplotlibWidget, self).__init__(parent)
        self.initUi()
        self.initariateV()

        # Initialize member variables

    def initariateV(self):
        self.p = None
        self.q = queue.Queue()
        self.t = None
        self.ad_rdy_ev = None
        self.stream = None
        self.window = None
        self.ani = None
        self.rt_line = line.Line2D([], [])  # line object

        self.rt_x_data = np.arange(0, CHUNK * 2, 1)
        self.rt_data = np.full((CHUNK * 2,), 0)
        self.rt_line.set_xdata(self.rt_x_data)  # initialize the abscissa
        self.rt_line.set_ydata(self.rt_data)  # initialize the ordinate


def initUi(self):
    self.layout = QVBoxLayout(self)
    self.mpl = MyMplCanvas(self, width=15, height=15, dpi=100)
    self.layout.addWidget(self.mpl)

    # Start recording trigger function


def startAudio(self, *args, **kwargs):
    self.mpl.fig.suptitle('wave curve')


    self.ani = animation.FuncAnimation(self.mpl.fig, self.plot_update,
                                       init_func=self.plot_init,
                                       frames=1,
                                       interval=30,
                                       blit=True)
    # In fact, the essence of the animation method is to open a thread to update the image

    # Microphone starts to get audio
    self.p = pyaudio.PyAudio()
    self.stream = self.p.open(format=pyaudio.paInt16,
                              channels=CHANNELS,
                              rate=RATE,
                              input=True,
                              output=False,
                              frames_per_buffer=CHUNK,
                              stream_callback=self.callback)
    self.stream.start_stream()

    # Normally distributed array, related operations with audio data can ensure that both ends of the waveform are fixed
    self.window = signal.hamming(CHUNK * 2)

    # Initialization thread
    self.ad_rdy_ev = threading.Event()  # thread event variable
    self.t = threading.Thread(target=self.read_audio_thead,
                              args=(self.q, self.stream, self.ad_rdy_ev))  # add function read_audio_thead in thread t
    self.t.start()  # thread starts running
    self.mpl.draw()


# animation update function
def plot_update(self, i):
    self.rt_line.set_xdata(self.rt_x_data)
    self.rt_line.set_ydata(self.rt_data)
    return self.rt_line,

    # animation initialization function


def plot_init(self):
    self.mpl.rt_ax.add_line(self.rt_line)
    return self.rt_line,

    # pyaudio's callback function


def callback(self, in_data, frame_count, time_info, status):
    global ad_rdy_ev
    self.q.put(in_data)
    return (None, pyaudio.paContinue)


def read_audio_thead(self, q, stream, ad_rdy_ev):
    # Get the data in the queue
    while stream.is_active():
        self.ad_rdy_ev.wait(timeout=0.1)  # thread event, wait for 0.1s
    if not q.empty():
        data = q.get()
        while not q.empty():  # Throw away excess data, otherwise the queue will grow longer
            q.get()
            self.rt_data = np.frombuffer(data, np.dtype('<i2'))
            self.rt_data = self.rt_data * self.window  # The purpose of this is to fix both ends of the curve to avoid fluctuations in the overall curve


    self.ad_rdy_ev.clear()


def endAudio(self):
    # Stop getting audio information
    self.stream.stop_stream()
    self.stream.close()
    self.p.terminate()
    # Clear the queue
    while not self.q.empty():
        self.q.get()
        # Reinitialize variables
    self.initariateV()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ui = MatplotlibWidget()
    ui.startAudio()
    ui.show()
    sys.exit(app.exec_())

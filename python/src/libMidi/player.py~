from PyQt4 import QtGui, QtCore
from PyQt4.phonon import Phonon # sudo apt-get install python3-pyqt4.phonon

class Window(QtGui.QPushButton):
    def __init__(self):
        QtGui.QPushButton.__init__(self, 'Choose File')
        self.mediaObject = Phonon.MediaObject(self)
        self.audioOutput = Phonon.AudioOutput(Phonon.MusicCategory, self)
        Phonon.createPath(self.mediaObject, self.audioOutput)
        self.mediaObject.stateChanged.connect(self.handleStateChanged)
        self.clicked.connect(self.handleButton)

    def handleButton(self):
        if self.mediaObject.state() == Phonon.PlayingState:
            self.mediaObject.stop()
        else:
            path = QtGui.QFileDialog.getOpenFileName(self, self.text())
            if path:
                self.mediaObject.setCurrentSource(Phonon.MediaSource(path))
                self.mediaObject.play()

    def handleStateChanged(self, newstate, oldstate):
        if newstate == Phonon.PlayingState:
            self.setText('Stop')
        elif newstate == Phonon.StoppedState:
            self.setText('Choose File')
        elif newstate == Phonon.ErrorState:
            source = self.mediaObject.currentSource().fileName()
            print ('ERROR: could not play:', source.toLocal8Bit().data())

if __name__ == '__main__':

    import sys
    app = QtGui.QApplication(sys.argv)
    app.setApplicationName('Phonon')
    win = Window()
    win.resize(200, 100)
    win.show()
    sys.exit(app.exec_())
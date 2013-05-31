from PyQt4 import QtCore, QtGui

class CommunicateMonfConversion(QtCore.QObject) :
    ajouterNote = QtCore.pyqtSignal(int)
    finir = QtCore.pyqtSignal()

class ProgressBarThread(QtCore.QThread) :
    def __init__(self, parent) :
        QtCore.QThread.__init__(self)
        self.run = parent.run

class ProgressBarMonf(QtGui.QProgressBar) :
    def __init__(self, parent) :
        QtGui.QProgressBar.__init__(self, parent)

        self.setMinimum(0)
        self.boutton = None
        self.communicateMonfConversion= CommunicateMonfConversion()

        self.communicateMonfConversion.ajouterNote.connect(self.add)
        self.communicateMonfConversion.finir.connect(self.finir)

    def setMonf(self, monf) :
        self.monf = monf
        self.setValue(self.minimum())

    def setBouton(self, bouton) :
        self.bouton = bouton

    def reloadMaximum(self) :
        self.nombreDeNotes = len(self.monf.morceau().getNotesBetween()) +1
        self.setMaximum(self.nombreDeNotes)

    def start(self) :
        if not self.bouton is None : self.bouton.setDisabled(True)
##        if not hasattr(self, "progressBarThread") or not self.progressBarThread.isRunning() :
##        self.progressBarThread = ProgressBarThread(self)
##        self.progressBarThread.start(QtCore.QThread.LowestPriority)
        self.run()

    def run(self) :
        # Appeller la fonction self.start() pour lancer la conversion
        #
        self.reloadMaximum()
        self.setValue(self.minimum())
        self.monf.conversion(self.communicateMonfConversion)

    def add(self, valeur=1):
        self.setValue(self.value()+valeur)

    def finir(self) :
        self.setValue(self.maximum())
        msgBox = QtGui.QMessageBox(self)
        msgBox.setWindowTitle("Ça c'est fait !")
        msgBox.setText("Conversion effectuée !")
        msgBox.setIcon(QtGui.QMessageBox.Information)
        msgBox.setInformativeText("Vous pouvez désormais lancer l'impression")
        msgBox.setStandardButtons(QtGui.QMessageBox.Ok)
        msgBox.setDefaultButton(QtGui.QMessageBox.Ok)
        ret = msgBox.exec_()

        if not self.bouton is None : self.bouton.setEnabled(True)


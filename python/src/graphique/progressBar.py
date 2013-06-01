from PyQt4 import QtCore, QtGui

class CommunicateMonfConversion(QtCore.QObject) :
    ajouterNote = QtCore.pyqtSignal(int)
    finir = QtCore.pyqtSignal()

class ConversionMonfThread(QtCore.QThread) :
    def __init__(self, parent) :
        QtCore.QThread.__init__(self)
        self.parent = parent

    def initialisation(self) :
        self.emit(QtCore.SIGNAL("initialisation()"))

    def reloadMaximum(self) :
        self.initialisation()
        notes = self.parent.monf.morceau().getNotesBetween()
        self.emit(QtCore.SIGNAL("setMaximum(int)"), len(notes) +1)
        return notes

    def run(self) :
        notes = self.reloadMaximum()
        self.parent.monf.conversion(self, notes)

    def addValue(self, valeur) :
        self.emit(QtCore.SIGNAL("addValue(int)"), valeur)

    def raz(self) :
        self.emit(QtCore.SIGNAL("raz()"))


class ImpressionThread(QtCore.QThread) :
    def __init__(self, parent) :
        QtCore.QThread.__init__(self)
        self.parent = parent




class ProgressBarMonf(QtGui.QProgressBar) :
    def __init__(self, parent) :
        QtGui.QProgressBar.__init__(self, parent)
        self.setMinimum(0)
        self.boutton = None
        self.thread = ConversionMonfThread(self)

        self.connect(self.thread, QtCore.SIGNAL("finished()"), self.finir)
        self.connect(self.thread, QtCore.SIGNAL("terminated()"), self.finir)
        self.connect(self.thread, QtCore.SIGNAL("addValue(int)"), self.addValue)
        self.connect(self.thread, QtCore.SIGNAL("setMaximum(int)"), self.setMaximum)
        self.connect(self.thread, QtCore.SIGNAL("initialisation()"), self.initialisation)
        self.connect(self.thread, QtCore.SIGNAL("raz()"), self.raz)

    def setMonf(self, monf) :
        self.monf = monf
        self.setValue(self.minimum())

    def setBouton(self, bouton) :
        self.bouton = bouton

    def start(self) :
        if not self.bouton is None : self.bouton.setDisabled(True)
        self.thread.start(QtCore.QThread.TimeCriticalPriority)

    def initialisation(self) :
        self.setMaximum(self.minimum())

    def raz(self) :
        self.setValue(self.minimum())

    def addValue(self, valeur):
        """
        Ajoute une note
        """
        self.setValue(self.value()+valeur)

    def finir(self) :
        self.setValue(self.maximum())
        msgBox = QtGui.QMessageBox(self)
        msgBox.setWindowTitle("Ça c'est fait !")
        msgBox.setText("Conversion effectuée ! " + str(self.monf.getNombrePoincons()) + " coups de poinçons seront imprimés.") #8466
        msgBox.setIcon(QtGui.QMessageBox.Information)
        msgBox.setInformativeText("Vous pouvez désormais lancer l'impression")
        msgBox.setStandardButtons(QtGui.QMessageBox.Ok)
        msgBox.setDefaultButton(QtGui.QMessageBox.Ok)
        msgBox.exec_()

        if not self.bouton is None : self.bouton.setEnabled(True)

class ProgressBarImpression(QtGui.QProgressBar) :
    def __init__(self, parent) :
        QtGui.QProgressBar.__init__(self, parent)
        self.setMinimum(0)
        self.boutton = None
        self.thread = ImpressionThread(self)
        

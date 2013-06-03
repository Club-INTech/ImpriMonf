from PyQt4 import QtCore, QtGui

class AbstractProgressBar(QtGui.QProgressBar) :
    def __init__(self, parent) :
        QtGui.QProgressBar.__init__(self, parent)
        self.setMinimum(0)
        self.boutton = None
        self.monf = None
        self.imprimante = None
        self.thread = None
        self.parent = parent

    def setMonf(self, monf) :
        self.monf = monf

    def setImprimante(self, imprimante) :
        self.imprimante = imprimante

    def setBouton(self, bouton, forceDisabling=True) :
        self.bouton = bouton
        self.forceDisablingBouton = forceDisabling
##        self.bouton.clicked.connect(self.start)

    def start(self) :
        if not self.bouton is None and self.forceDisablingBouton: self.bouton.setDisabled(True)
        self.thread.start()

    def initialisation(self) :
        self.setMaximum(self.minimum())

    def raz(self) :
        self.setValue(self.minimum())

    def finir(self) :
        if not self.bouton is None and self.forceDisablingBouton: self.bouton.setEnabled(True)
        self.setValue(self.maximum())


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
        self.connect(self.parent, QtCore.SIGNAL("pauseImpression()"), self.pauseImpression)
        self.connect(self.parent, QtCore.SIGNAL("reprendreImpression()"), self.reprendreImpression)

    def run(self) :
        self.parent.monf.imprimer(self.parent.imprimante, self)

    def poinconFait(self) :
        self.emit(QtCore.SIGNAL("poinconFait()"))

    def pauseImpression(self) :
        self.parent.monf.pauseImpression()

    def reprendreImpression(self) :
        self.parent.monf.reprendreImpression()


class ProgressBarMonf(AbstractProgressBar) :
    def __init__(self, parent) :
        AbstractProgressBar.__init__(self, parent)
        self.thread = ConversionMonfThread(self)
        self.connect(self.thread, QtCore.SIGNAL("finished()"), self.finir)
        self.connect(self.thread, QtCore.SIGNAL("terminated()"), self.finir)
        self.connect(self.thread, QtCore.SIGNAL("addValue(int)"), self.addValue)
        self.connect(self.thread, QtCore.SIGNAL("setMaximum(int)"), self.setMaximum)
        self.connect(self.thread, QtCore.SIGNAL("initialisation()"), self.initialisation)
        self.connect(self.thread, QtCore.SIGNAL("raz()"), self.raz)

    def setMonf(self, monf) :
        AbstractProgressBar.setMonf(self,monf)
        self.setValue(self.minimum())

    def addValue(self, valeur):
        """
        Ajoute une note
        """
        self.setValue(self.value()+valeur)

    def finir(self) :
        AbstractProgressBar.finir(self)
        msgBox = QtGui.QMessageBox(self)
        msgBox.setWindowTitle("Ça c'est fait !")
        msgBox.setText("Conversion effectuée ! " + str(self.monf.getNombrePoincons()) + " coups de poinçons seront imprimés.") #8466
        msgBox.setIcon(QtGui.QMessageBox.Information)
        msgBox.setInformativeText("Vous pouvez désormais lancer l'impression")
        msgBox.setStandardButtons(QtGui.QMessageBox.Ok)
        msgBox.setDefaultButton(QtGui.QMessageBox.Ok)
        msgBox.exec_()

class ProgressBarImpression(AbstractProgressBar) :
    def __init__(self, parent) :
        AbstractProgressBar.__init__(self, parent)
        self.thread = ImpressionThread(self.parent)
        self.parent = parent

        self.connect(self.thread, QtCore.SIGNAL("finished()"), self.finir)
        self.connect(self.thread, QtCore.SIGNAL("terminated()"), self.finir)
        self.connect(self.thread, QtCore.SIGNAL("poinconFait()"), self.poinconFait)

    def poinconFait(self) :
        self.setValue(self.value() + 1)


    def start(self) :
        self.setMaximum(self.monf.getNombrePoincons())

        msgBox = QtGui.QMessageBox(self)
        msgBox.setWindowTitle("ATTENTION !")
        msgBox.setText("Avez-vous pensé à lancer la procédure de recalage du poinçon ?") #8466
        msgBox.setIcon(QtGui.QMessageBox.Warning)
        msgBox.setInformativeText("Si vous ne l'avez pas fait, cliquez sur Annuler, lancer la procédure, puis relancez l'impression. Cliquez sur OK si la procédure a déjà été faite.")
        msgBox.setStandardButtons(QtGui.QMessageBox.Ok | QtGui.QMessageBox.Cancel)
        msgBox.setDefaultButton(QtGui.QMessageBox.Cancel)
        ret = msgBox.exec_()

        if ret == QtGui.QMessageBox.Ok : AbstractProgressBar.start(self)


    def finir(self) :
        AbstractProgressBar.finir(self)



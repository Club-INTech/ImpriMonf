import time
from PyQt4 import QtCore, QtGui

class SleepProgress(QtCore.QThread):

    def __init__(self, morceau) :
        QtCore.QThread.__init__(self)
        self.morceau = morceau
        self.add = None
        self.fini = None
        self.communicate = Communicate()

    def connection(self) :
        self.communicate.ajouterNote.connect(self.add)
        self.communicate.finir.connect(self.fini)

    def run(self):
        self.monf = self.morceau.parseOutput(self.communicate)
        self.communicate.finir.emit()

class Communicate(QtCore.QObject) :
    ajouterNote = QtCore.pyqtSignal(int)
    finir = QtCore.pyqtSignal()

class ProgressBarLoadingMonf(QtGui.QWidget):
    def __init__(self, parent, morceau):
        QtGui.QWidget.__init__(self, None)
        self.parent=parent
        self.morceau = morceau
        self.thread = SleepProgress(morceau)

        nombreDeNotes = len(morceau.getNotesBetween())

        self.progressbar = QtGui.QProgressBar()
        self.valeurProgression = 0
        self.progressbar.setMinimum(0)
        self.progressbar.setMaximum(nombreDeNotes)

        texte = QtGui.QLabel("Importation du fichier MiDi en cours...", self)

        mainLayout = QtGui.QGridLayout()
        mainLayout.addWidget(self.progressbar, 1, 0)
        mainLayout.addWidget(texte, 0,0)

        self.setLayout(mainLayout)
        self.setWindowTitle("Ça vient, ça vient")

        self.thread.add = self.updatePBar
        self.thread.fini = self.fini
        self.thread.connection()

        self.thread.start()

        self.show()

    def updatePBar(self, valeur=1):
        self.progressbar.setValue(self.valeurProgression+valeur)
        self.valeurProgression += valeur




    def fini(self):
        self.parent.conteneurMonf.reloadMonf(self.thread.monf)
        self.parent.statusbar.showMessage("Fichier MiDi importé  !")
        self.close(True)
        self.thread.quit()

    def close(self, force = False) :
        if force : QtGui.QWidget.close(self)
        else : pass


if __name__ == '__main__':
    import sys
    app = QtGui.QApplication(sys.path)

    pbarwin = ProgressBarLoadingMonf()
    pbarwin.show()

    sys.exit(app.exec_())
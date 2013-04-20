#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      Thibaut
#
# Created:     29/04/2013
# Copyright:   (c) Thibaut 2013
# Licence:     <your licence>
#-------------------------------------------------------------------------------

from PyQt4 import QtGui, QtCore
from monfEditor import ConteneurMonf

import sys

sys.path.append("../libMidi")
sys.path.append("../libMidi/midi")

import morceau
import monf

class FenetrePrincipale(QtGui.QMainWindow) :
    def __init__(self) :
        QtGui.QMainWindow.__init__(self)
        self.initUID()

    def initUID(self) :

        # NOUVEAU MONF
        texte = "Nouveau"
        nouveauAction = QtGui.QAction(QtGui.QIcon('../../../multimedia/ICONS/document-new.png'), texte, self)
        nouveauAction.setShortcut('Ctrl+N')
        nouveauAction.setStatusTip(texte)
        nouveauAction.triggered.connect(self.nouveau)

        # OUVRIR UN FICHIER SON
        texte = 'Ouvrir un fichier MiDi'
        openMidiAction = QtGui.QAction(QtGui.QIcon('../../../multimedia/ICONS/document-open.png'), texte, self)
        openMidiAction.setShortcut('Ctrl+O')
        openMidiAction.setStatusTip(texte)
        openMidiAction.triggered.connect(self.openMidi)


        # QUITTER L'APPLICATION
        texte = 'Quitter l\'Application'
        exitAction = QtGui.QAction(QtGui.QIcon('../../../multimedia/ICONS/close.png'), texte, self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip(texte)
        exitAction.triggered.connect(self.close)

        self.statusbar = self.statusBar()
        self.statusbar.showMessage("L'application a été lancée avec succès !")

        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&Fichier')
        fileMenu.addAction(nouveauAction)
        fileMenu.addAction(openMidiAction)
        fileMenu.addSeparator()
        fileMenu.addAction(exitAction)

        toolbar = self.addToolBar('Barre de Menus')
        toolbar.addAction(nouveauAction)
        toolbar.addAction(openMidiAction)

        # Ajout de l'éditeur de monf
        self.conteneurMonf = ConteneurMonf(self)

        self.setCentralWidget(self.conteneurMonf)
        self.setWindowTitle('Monf Editor')
        self.show()

    # Nouveau fichier.
    def nouveau(self) :
        pass

    # Action suivant l'ouverture d'un fichier MiDi
    def openMidi(self) :
        midiFileName = QtGui.QFileDialog.getOpenFileName(self, "Ouvrir un fichier MiDi", filter="Fichiers Midi (*.mid *.midi)")
        if midiFileName is None or midiFileName=="":
            return

        morc = morceau.Morceau(midiFileName)
        monf = morc.parseOutput()
        notesQuiBugguent = monf.checkForUnprintablePistes()

        if notesQuiBugguent != [] :
            print ("Notes qui buggent :", notesQuiBugguent)

        self.conteneurMonf.reloadMonf(monf)
        self.statusbar.showMessage("Fichier MiDi " + midiFileName + " ouvert  !")







if __name__ == "__main__" :

    app = QtGui.QApplication(sys.argv)
    app.setApplicationName('monfEditor')

    win = FenetrePrincipale()

    win.show()
    sys.exit(app.exec_())
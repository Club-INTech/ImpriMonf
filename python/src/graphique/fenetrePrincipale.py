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
from progressBar import ProgressBarLoadingMonf

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

        # OUVRIR UN FICHIER MONF
        texte = 'Ouvrir un fichier Monf'
        openMonfAction = QtGui.QAction(QtGui.QIcon('../../../multimedia/ICONS/document-open.png'), texte, self)
        openMonfAction.setShortcut('Ctrl+O')
        openMonfAction.setStatusTip(texte)
        openMonfAction.triggered.connect(self.openMonf)

        # ENREGISTRER UN FICHIER MONF
        texte = 'Enregistrer au format Monf'
        saveMonfAction = QtGui.QAction(QtGui.QIcon('../../../multimedia/ICONS/document-save.png'), texte, self)
        saveMonfAction.setShortcut('Ctrl+S')
        saveMonfAction.setStatusTip(texte)
        saveMonfAction.triggered.connect(self.saveMonf)

        # OUVRIR UN FICHIER SON
        texte = 'Ouvrir un fichier MiDi'
        openMidiAction = QtGui.QAction(QtGui.QIcon('../../../multimedia/ICONS/import-audio.png'), texte, self)
        openMidiAction.setShortcut('Ctrl+Shift+O')
        openMidiAction.setStatusTip(texte)
        openMidiAction.triggered.connect(self.openMidi)


        # QUITTER L'APPLICATION
        texte = 'Quitter l\'application'
        exitAction = QtGui.QAction(QtGui.QIcon('../../../multimedia/ICONS/close.png'), texte, self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip(texte)
        exitAction.triggered.connect(self.close)

        self.statusbar = self.statusBar()
        self.statusbar.showMessage("L'application a été lancée avec succès !")

        menubar = self.menuBar()

        # BARS DE MENU
        fileMenu = menubar.addMenu('&Fichier')
        fileMenu.addAction(nouveauAction)
        fileMenu.addAction(openMonfAction)
        fileMenu.addAction(saveMonfAction)
        fileMenu.addSeparator()
        fileMenu.addAction(openMidiAction)
        fileMenu.addSeparator()
        fileMenu.addAction(exitAction)

        # TOOLBARS
        toolbarMenu = self.addToolBar('Barre de Menus')
        toolbarMenu.addAction(nouveauAction)
        toolbarMenu.addAction(openMonfAction)
        toolbarMenu.addAction(saveMonfAction)
        toolbarMenu.addSeparator()
        toolbarMenu.addAction(openMidiAction)

        # Ajout de l'éditeur de monf
        self.conteneurMonf = ConteneurMonf(self)

        self.setCentralWidget(self.conteneurMonf)
        self.setWindowTitle('Monf Editor')
        self.resize(500,500)
        self.show()

    # Nouveau fichier.
    def nouveau(self) :
        self.conteneurMonf.reloadMonf()

    # Ouvrir un fichier Monf
    def openMonf(self) :
        monfFileName = QtGui.QFileDialog.getOpenFileName(self, "Ouvrir un fichier Monf", filter="Fichiers Monf (*.monf *.monfrini)")
        if monfFileName is None or monfFileName=="":
            return

        monf_ = monf.openMonf(monfFileName)

        self.conteneurMonf.reloadMonf(monf_)
        self.statusbar.showMessage("Fichier Monf " + monfFileName + " ouvert  !")

    # Enregistrer le fichier Monf
    def saveMonf(self) :
        monfFileName = QtGui.QFileDialog.getSaveFileNameAndFilter(self, "Enregistrer au format Monf", filter = "Fichiers Monf (*.monf *.monfrini)")
        if monfFileName == "" :
            return

        self.conteneurMonf.getMonf().save(monfFileName[0])
        self.statusbar.showMessage("Fichier Monf " + monfFileName[0] + " sauvegardé  !")

    # Action suivant l'ouverture d'un fichier MiDi
    def openMidi(self) :
        midiFileName = QtGui.QFileDialog.getOpenFileName(self, "Importer un fichier MiDi", filter="Fichiers Midi (*.mid *.midi)")
        if midiFileName is None or midiFileName=="":
            return

        morc = morceau.Morceau(midiFileName)
        # Lancement de la conversion
        popup = ProgressBarLoadingMonf(self, morc)
##        notesQuiBugguent = monf_.checkForUnprintablePistes()

##        if notesQuiBugguent != [] :
##            print ("Notes qui buggent :", notesQuiBugguent)
##
##        self.conteneurMonf.reloadMonf(monf_)
##        self.statusbar.showMessage("Fichier MiDi " + midiFileName + " importé  !")







if __name__ == "__main__" :

    app = QtGui.QApplication(sys.argv)
    app.setApplicationName('monfEditor')

    win = FenetrePrincipale()

    win.show()
    sys.exit(app.exec_())
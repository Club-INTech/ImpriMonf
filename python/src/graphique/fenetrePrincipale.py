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
from popups import *
from imprimante import Imprimante
from dockWidgets import *
import fenetreAide
import time
import threading

from playerMONF import Player




import morceau
import monf

class FenetrePrincipale(QtGui.QMainWindow) :
    def __init__(self, QApplication) :
        QtGui.QMainWindow.__init__(self)
        self.app = QApplication
        Player.init()
        self.modifie = False
        self.monfFileName = None
        self.initUID()



    def initUID(self) :

        # NOUVEAU MONF
        texte = "Nouveau"
        nouveauAction = QtGui.QAction(QtGui.QIcon('icons/document-new.png'), texte, self)
        nouveauAction.setShortcut('Ctrl+N')
        nouveauAction.setStatusTip(texte)
        nouveauAction.triggered.connect(self.nouveau)

        # OUVRIR UN FICHIER MONF
        texte = 'Ouvrir un fichier Monf'
        openMonfAction = QtGui.QAction(QtGui.QIcon('icons/document-open.png'), texte, self)
        openMonfAction.setShortcut('Ctrl+O')
        openMonfAction.setStatusTip(texte)
        openMonfAction.triggered.connect(self.openMonf)

        # ENREGISTRER UN FICHIER MONF
        texte = 'Enregistrer au format Monf'
        saveMonfAction = QtGui.QAction(QtGui.QIcon('icons/document-save.png'), texte, self)
        saveMonfAction.setShortcut('Ctrl+S')
        saveMonfAction.setStatusTip(texte)
        saveMonfAction.triggered.connect(self.saveMonf)

        # ENREGISTRER SOUS
        texte = 'Enregistrer sous...'
        saveAsMonfAction = QtGui.QAction(QtGui.QIcon('icons/document-save-as.png'), texte, self)
        saveAsMonfAction.setShortcut('Ctrl+Shift+S')
        saveAsMonfAction.setStatusTip(texte)
        saveAsMonfAction.triggered.connect(self.saveAs)

        # OUVRIR UN FICHIER MIDI
        texte = 'Importer un fichier MiDi'
        openMidiAction = QtGui.QAction(QtGui.QIcon('icons/import-audio.png'), texte, self)
        openMidiAction.setShortcut('Ctrl+Shift+O')
        openMidiAction.setStatusTip(texte)
        openMidiAction.triggered.connect(self.openMidi)

        # EXPORTER AU FORMAT MIDI
        texte = 'Exporter au format MiDi'
        exportMidiAction = QtGui.QAction(QtGui.QIcon('icons/export-audio.png'), texte, self)
        exportMidiAction.setShortcut('Ctrl+Alt+S')
        exportMidiAction.setStatusTip(texte)
        exportMidiAction.triggered.connect(self.exportMidi)

        # PLAY
        texte = 'Play'
        playAction = QtGui.QAction(QtGui.QIcon('icons/play.png'), texte, self)
        playAction.setShortcut('Space')
        playAction.setStatusTip(texte)
        playAction.triggered.connect(self.play)
        self.playAction = playAction
        Player.setAction(self.playAction)

        # OPTIONS PLAYER
        texte = 'Options du player'
        playerOptionsAction = QtGui.QAction(QtGui.QIcon('icons/settings.png'), texte, self)
        playerOptionsAction.setStatusTip(texte)
        playerOptionsAction.triggered.connect(self.playerOptions)

        # NEW NOTE
        texte = 'Ajouter une note'
        newNoteAction = QtGui.QAction(QtGui.QIcon('icons/new-note.png'), texte, self)
##        newNoteAction.setShortcut('Ctrl+')
        newNoteAction.setStatusTip(texte)
        newNoteAction.setCheckable(True)
        newNoteAction.triggered.connect(self.newNote)
        self.newNoteAction = newNoteAction

        # DEL NOTE
        texte = 'Ajouter une note'
        delNoteAction = QtGui.QAction(QtGui.QIcon('icons/del-note.png'), texte, self)
##        delNoteAction.setShortcut('Ctrl+')
        delNoteAction.setStatusTip(texte)
        delNoteAction.setCheckable(True)
        delNoteAction.triggered.connect(self.delNote)
        self.delNoteAction = delNoteAction

        # SELECTION
        texte = 'Outil de sélection'
        selectionAction = QtGui.QAction(QtGui.QIcon('icons/selection.png'), texte, self)
##        selectionAction.setShortcut('Ctrl+')
        selectionAction.setStatusTip(texte)
        selectionAction.setCheckable(True)
        selectionAction.triggered.connect(self.outilSelection)
        self.selectionAction = selectionAction


        # CONNEXION AVEC L'IMPRIMANTE
        texte = 'Réinitialiser la connexion avec l\'imprimante'
        lancerPoinconnageAction = QtGui.QAction(QtGui.QIcon('icons/printer.png'), texte, self)
        lancerPoinconnageAction.setShortcut('Ctrl+P')
        lancerPoinconnageAction.setStatusTip(texte)
        lancerPoinconnageAction.triggered.connect(self.reloadImprimante)

        # ANNULER
        texte = 'Annuler'
        annulerAction = QtGui.QAction(QtGui.QIcon('icons/edit-undo.png'), texte, self)
        annulerAction.setShortcut('Ctrl+Z')
        annulerAction.setStatusTip(texte)
        annulerAction.triggered.connect(self.annuler)
        self.annulerAction = annulerAction

        # REFAIRE
        texte = 'Refaire'
        refaireAction = QtGui.QAction(QtGui.QIcon('icons/edit-redo.png'), texte, self)
        refaireAction.setShortcut('Ctrl+Y')
        refaireAction.setStatusTip(texte)
        refaireAction.triggered.connect(self.refaire)
        self.refaireAction = refaireAction

        # QUITTER L'APPLICATION
        texte = 'Quitter l\'application'
        exitAction = QtGui.QAction(QtGui.QIcon('icons/close.png'), texte, self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip(texte)
        exitAction.triggered.connect(self.close)

        # OUVRIR L'AIDE
        texte = 'Aide'
        aideAction = QtGui.QAction(QtGui.QIcon('icons/help-browser.png'), texte, self)
        aideAction.setShortcut('F1')
        aideAction.setStatusTip(texte)
        aideAction.triggered.connect(self.openAide)

        # OUVRIR LES CRÉDITS
        texte = 'Crédits'
        creditsAction = QtGui.QAction(QtGui.QIcon('icons/system-users.png'), texte, self)
        creditsAction.setStatusTip(texte)
        creditsAction.triggered.connect(self.openCredits)

        self.statusbar = self.statusBar()
        self.statusbar.showMessage("L'application a été lancée avec succès !")

        menubar = self.menuBar()

        # BARS DE MENU
        fileMenu = menubar.addMenu('&Fichier')
        fileMenu.addAction(nouveauAction)
        fileMenu.addAction(openMonfAction)
        fileMenu.addAction(saveMonfAction)
        fileMenu.addAction(saveAsMonfAction)
        fileMenu.addSeparator()
        fileMenu.addAction(openMidiAction)
        fileMenu.addAction(exportMidiAction)
        fileMenu.addSeparator()
        fileMenu.addAction(lancerPoinconnageAction)
        fileMenu.addSeparator()
        fileMenu.addAction(exitAction)

        editMenu = menubar.addMenu("&Edition")
        editMenu.addAction(annulerAction)
        editMenu.addAction(refaireAction)

        morceauMenu = menubar.addMenu("&Morceau")
        morceauMenu.addAction(newNoteAction)
        morceauMenu.addAction(delNoteAction)
        morceauMenu.addAction(selectionAction)

        playMenu = menubar.addMenu("&Player")
        playMenu.addAction(playAction)
        playMenu.addAction(playerOptionsAction)

        aideMenu = menubar.addMenu("&Aide")
        aideMenu.addAction(aideAction)
        aideMenu.addAction(creditsAction)

        # TOOLBARS
        toolbarMenu = self.addToolBar('Barre de Menus')
        toolbarMenu.addAction(nouveauAction)
        toolbarMenu.addAction(openMonfAction)
        toolbarMenu.addAction(saveMonfAction)
        toolbarMenu.addAction(saveAsMonfAction)
        toolbarMenu.addSeparator()
        toolbarMenu.addAction(lancerPoinconnageAction)
        toolbarMenu.addSeparator()
        toolbarMenu.addAction(annulerAction)
        toolbarMenu.addAction(refaireAction)
        toolbarMenu.addSeparator()
        toolbarMenu.addAction(openMidiAction)
        toolbarMenu.addAction(exportMidiAction)

        toolbarMorceau = self.addToolBar("Barre d'édition de morceau")
        toolbarMorceau.addAction(newNoteAction)
        toolbarMorceau.addAction(delNoteAction)

        toolbarPlayback = self.addToolBar("Barre de playback")
        toolbarPlayback.addAction(playAction)
        toolbarPlayback.addAction(playerOptionsAction)


        # Ajout de l'éditeur de monf et des dockwidget
        self.conteneurMonf = ConteneurMonf(self)
        self.lanceurConversion = LanceurConversion(self)
        self.optionsCarton = OptionsCarton(self)
        self.impression = Impression(self)
        self.recalageEtFinDImpression = RecalageEtFinDImpression(self)
##        self.editionMorceau = EditionMorceau(self)

        self.setCentralWidget(self.conteneurMonf)
        self.addDockWidget(QtCore.Qt.BottomDockWidgetArea, self.optionsCarton)
        self.addDockWidget(QtCore.Qt.BottomDockWidgetArea, self.lanceurConversion)
        self.addDockWidget(QtCore.Qt.BottomDockWidgetArea, self.impression)
        self.addDockWidget(QtCore.Qt.BottomDockWidgetArea, self.recalageEtFinDImpression)
##        self.addDockWidget(QtCore.Qt.BottomDockWidgetArea, self.editionMorceau)

        self.setWindowTitle('Monf Editor')
        self.resize(900,600)
        self.refreshAnnulerRefaire()
        self.nouveau()
        self.show()
        self.reloadImprimante()

    # Indiquer qu'il y a eu des modifications
    def modificate(self) :
        if not self.modifie :
            self.modifie = True
            self.setWindowTitle("* " + self.windowTitle() + " *")

    # Nouveau fichier.
    def nouveau(self) :
        if not self.askSave() : return
        self.reloadMonf(monf.Monf())
        self.modifie = False
        self.refreshAnnulerRefaire()

    # Ouvrir un fichier Monf
    def openMonf(self) :
        if not self.askSave() : return
        monfFileName = QtGui.QFileDialog.getOpenFileName(self, "Ouvrir un fichier Monf", filter="Fichiers Monf (*.monf *.monfrini)")
        if monfFileName is None or monfFileName=="":
            return

        monf_ = monf.openMonf(monfFileName)

        self.reloadMonf(monf_)
        self.statusbar.showMessage("Fichier Monf " + monfFileName + " ouvert  !")

        self.setWindowTitle("Monf Editor - " +  monfFileName)
        self.modifie = False
        self.monfFileName = monfFileName
        self.refreshAnnulerRefaire()

    # Enregistrer le fichier Monf
    def saveMonf(self, forceNewFile=False) :
        if self.monfFileName is None or forceNewFile:
            monfFileName = QtGui.QFileDialog.getSaveFileNameAndFilter(self, "Enregistrer au format Monf", filter = "Fichiers Monf (*.monf *.monfrini)")
            monfFileN = monfFileName[0]
            if monfFileN == "" : return
            else : self.monfFileName = monfFileN
        else :
            monfFileN = self.monfFileName

        self.conteneurMonf.getMonf().save(monfFileN)
        self.statusbar.showMessage("Fichier Monf " + monfFileN + " sauvegardé  !")

        self.setWindowTitle("Monf Editor - " +  monfFileN)
        self.modifie = False

    # Enregistrer Sous
    def saveAs(self) :
        self.saveMonf(forceNewFile=True)

    # Annuler
    def annuler(self) :
        self.annulerAction.setEnabled(self.conteneurMonf.monfEditor.controlZ.annuler())
        self.refaireAction.setEnabled(True)
        self.conteneurMonf.monfEditor.update()

    # Refaire
    def refaire(self) :
        self.refaireAction.setEnabled(self.conteneurMonf.monfEditor.controlZ.refaire())
        self.annulerAction.setEnabled(True)
        self.conteneurMonf.monfEditor.update()

    # Action suivant l'ouverture d'un fichier MiDi
    def openMidi(self) :
        if not self.askSave() : return
        midiFileName = QtGui.QFileDialog.getOpenFileName(self, "Importer un fichier MiDi", filter="Fichiers Midi (*.mid *.midi)")
        if midiFileName is None or midiFileName=="":
            return

        morc = morceau.Morceau(midiFileName)

        nouveauMonf = monf.Monf(morc)

        self.reloadMonf(nouveauMonf)

        self.setWindowTitle("Monf Editor - " + midiFileName)
        self.modificate()
        self.refreshAnnulerRefaire()

    # Exporter au format Midi
    def exportMidi(self) :
        midiFileName = QtGui.QFileDialog.getSaveFileNameAndFilter(self, "Exporter au format MiDi", filter="Fichiers Midi (*.mid *.midi)")[0]
        if midiFileName is None or midiFileName=="":
            return

        popup = PopupSave(self)
        popup.exec_()

        if not hasattr(popup, "resultat") or popup.resultat == None :return

        self.monf._morceau.exporter(midiFileName, popup.resultat[0], popup.resultat[1])

    def askSave(self) :
        """
        Retourne True si le script doit continuer, False sinon (=Annuler)
        S'occupe de sauvegarder si besoin est.
        """
        if not self.modifie : return True
        msgBox = QtGui.QMessageBox(self)
        msgBox.setWindowTitle("Attention !")
        msgBox.setText("Le fichier a été modifié.")
        msgBox.setIcon(QtGui.QMessageBox.Question)
        msgBox.setInformativeText("Voulez-vous sauvegarder les modifications ?")
        msgBox.setStandardButtons(QtGui.QMessageBox.Save | QtGui.QMessageBox.Discard | QtGui.QMessageBox.Cancel)
        msgBox.setDefaultButton(QtGui.QMessageBox.Save)
        ret = msgBox.exec_()

        if ret == QtGui.QMessageBox.Save :
            self.saveMonf()
            return True
        elif ret == QtGui.QMessageBox.Cancel :
            return False
        else :
            return True


    def openAide(self) :
        fenetreAide.Aide(self)
    def openCredits(self) :
        fenetreAide.Credits(self)


    def refreshAnnulerRefaire(self) :
        self.annulerAction.setDisabled(True)
        self.refaireAction.setDisabled(True)

    def closeEvent(self, event) :
        if not self.askSave() : event.ignore()
        else : event.accept()

    def getMonf(self) :
        return self.monf

    # Play
    def play(self) :
        if not Player.isPlaying :
            Player.play(self.getMonf().morceau(), self.conteneurMonf.monfEditor.playbackTime)
            self.playAction.setIcon(QtGui.QIcon("icons/pause.png"))
        else :
            Player.stop()
            self.playAction.setIcon(QtGui.QIcon("icons/play.png"))

    def playerOptions(self) :
        popup = PopupPlayerOptions(self)
        popup.exec_()

        if not hasattr(popup, "resultat") or popup.resultat == None :return

        Player.setInstrument(popup.resultat[0])

    def reloadImprimante(self) :
        try :
            self.imprimante = Imprimante()
        except :
            msgBox = QtGui.QMessageBox(self)
            msgBox.setWindowTitle("Imprimante non trouvée !")
            msgBox.setText("L'imprimante n'a pas été trouvée.")
            msgBox.setIcon(QtGui.QMessageBox.Critical)
            msgBox.setInformativeText("Vérifiez sa connexion, puis réessayez.")
            msgBox.setStandardButtons(QtGui.QMessageBox.Ok)
            ret = msgBox.exec_()
            self.imprimante = None

        if not self.imprimante is None :
            self.recalageEtFinDImpression.reloadImprimante(self.imprimante)
            self.impression.reloadImprimante(self.imprimante)

    def reloadMonf(self, nouveauMonf):
        self.monf = nouveauMonf
        self.optionsCarton.reloadMonf(self.monf)
        self.conteneurMonf.reloadMonf(self.monf)
        self.lanceurConversion.reloadMonf(self.monf)
        self.recalageEtFinDImpression.reloadMonf(self.monf)
        self.impression.reloadMonf(self.monf)

    def disableTools(self) :
        self.delNoteAction.setChecked(False)
        self.newNoteAction.setChecked(False)
        self.selectionAction.setChecked(False)

    def newNote(self) :
        if not self.newNoteAction.isChecked() :
            self.conteneurMonf.monfEditor.setTool(None)
            return
        self.disableTools()
        self.newNoteAction.setChecked(True)

    def delNote(self) :
        if not self.delNoteAction.isChecked() :
            self.conteneurMonf.monfEditor.setTool(None)
            return
        self.disableTools()
        self.delNoteAction.setChecked(True)

    def outilSelection(self) :
        if not self.selectionAction.isChecked() :
            self.conteneurMonf.monfEditor.setTool(None)
            return
        self.disableTools()
        self.selectionAction.setChecked(True)


if __name__ == "__main__" :

    app = QtGui.QApplication(sys.argv)
    app.setApplicationName('Monf Editor')

    win = FenetrePrincipale(app)

    win.show()
    sys.exit(app.exec_())

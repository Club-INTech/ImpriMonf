#-------------------------------------------------------------------------------
# Name:        monfEditor.py
# Purpose:
#
# Author:      Thibaut
#
# Created:     14/03/2013
# Copyright:   (c) Thibaut 2013
# Licence:     WTF
#-------------------------------------------------------------------------------

from PyQt4 import QtGui, QtCore, Qt

from note import Note
from controlZ import ControlZ, Action

class MonfEditor(QtGui.QWidget) :

    hauteurPiste = 18
    DST = 200. #Distance, en pixels, correspondant a 1s de musique

    couleurFond = QtGui.QColor(230,230,230)
    couleurPortee = QtGui.QColor(200,200,200)

    margin_interieur_note = 1

    def __init__(self, parent=None, monf=None) :
        self._monf = monf
        self._parent = parent
        QtGui.QWidget.__init__(self, self._parent)

        self.sizeX, self.sizeY = 600, 700


        # Longueurs/Hauteurs constantes
        self.hauteurPiste = MonfEditor.hauteurPiste
        self.sizeY = 27*self.hauteurPiste # 27 = nombre de pistes
        self.startX = 0

        self._DST = MonfEditor.DST

        self.modifNote = None
        self.controlZ = ControlZ()

        if not monf is None :
            self.taillePoincon = monf._morceau._taillePoincon / monf._morceau._DST
            self.getPoincons()

        self.show()
        self.setMouseTracking(True)
        self.currentNote = None

    def getPoincons(self) :
        self.poincons = self._monf.getAllPoincons()
##        print (self._monf.getNombrePoincons(self.poincons))

    def getFenetrePrincipale(self) :
        return self._parent.parent

    def resize(self, x, y) :
        self.sizeX , self.sizeY = x, y
        QtGui.QWidget.resize(self, x, y)

    def paintEvent(self, e) :
        self.resize(self.parent().width(), self.sizeY)

        qp = QtGui.QPainter()
        qp.begin(self)

        # Rectangle blanchatre de fond
        qp.fillRect(0,0, self.sizeX, self.sizeY, QtGui.QBrush(MonfEditor.couleurFond))
        # Ajout des portees
        for i in range(27) :
            qp.fillRect(0,(i+.5)*self.hauteurPiste, self.sizeX, 2, QtGui.QBrush(MonfEditor.couleurPortee))

        # Si on n'a pas de monf, on s'arrete ici
        if self._monf is None :
            return
        # Sinon, on continue

        timeLeft = self.startX
        timeRight = self.startX + self.width()/MonfEditor.DST



        # Repères verticaux
        temps_noire = self._monf._morceau._output.temps_dune_noire
        for i in range(int(timeLeft//temps_noire), int(timeRight//temps_noire)+1) :
            temps_du_temps = i*temps_noire
            qp.fillRect(MonfEditor.DST*(temps_du_temps-self.startX), 0, 2, self.height(), QtGui.QColor(150,150,170))

        # On affiche les notes
        notes = self._monf._morceau.getNotesBetween(timeLeft-10, timeRight)
        self.notesAffichees = notes


        for note in notes :
            try :
                self.drawNote(qp, note)
            except KeyError :
                pass

        if self.currentNote != None :
            self.drawNote(qp, self.currentNote, option="ALPHA")

    def drawNote(self, qp, note, option=None):
        couleur = note.color.darker(140)
        couleur.setAlpha(200)
        couleurInterieur = note.color.lighter(130)
        couleurInterieur.setAlpha(127)

        if option=="ALPHA" :
            couleurInterieur.setAlpha(80)
            couleur.setAlpha(80)

        pen = QtGui.QPen(couleur)
        pen.setWidthF(1.5)

        qp.setBrush(couleurInterieur)
        qp.setPen(pen)
        qp.drawRoundedRect(MonfEditor.DST*(note.timeIn-self.startX)+MonfEditor.margin_interieur_note, self._monf.getNumeroPisteOfNote(note)*self.hauteurPiste + 2+MonfEditor.margin_interieur_note, max(1, MonfEditor.DST*(note.timeOut - note.timeIn))-2*MonfEditor.margin_interieur_note, self.hauteurPiste - 4-2*MonfEditor.margin_interieur_note, 4,4)

    def getNoteAtPixelPosition(self, pos) :
        """
        Retourne un objet modifNote contenant la note et la type d'évenement
        """
        if self._monf is None :
            return None

        temps, numero_piste = self.getTimeAndPisteNumberAtPosition(pos)

        modif = self._monf._morceau.getNoteAtPosition(numero_piste, temps, self.notesAffichees) # Objet ModifNote ou None
        return modif

    def getTimeAndPisteNumberAtPosition(self, pos) :
        temps = pos.x()/MonfEditor.DST + self.startX
        numero_piste = pos.y()//self.hauteurPiste
        return [temps, numero_piste]

    def mouseMoveEvent(self, event) :

        # modification de position de la note
        if QtCore.Qt.LeftButton == QtGui.QApplication.mouseButtons() and self.modifNote != None:
            if self.modifNote.isPosModif() :
                time_diff = self.getTimeAndPisteNumberAtPosition(self.lastMousePos)[0] - self.getTimeAndPisteNumberAtPosition(event.pos())[0]
                self.modifNote.note.timeIn -= time_diff
                self.modifNote.note.timeOut -= time_diff
                self.update()
                self.getFenetrePrincipale().modificate()

            elif self.modifNote.type == "BORNEIN" :
                time_diff = self.getTimeAndPisteNumberAtPosition(self.lastMousePos)[0] - self.getTimeAndPisteNumberAtPosition(event.pos())[0]
                self.modifNote.note.timeIn -= time_diff
                self.modifNote.note.checkTime(priority = "timeIn")
                self.update()
                self.getFenetrePrincipale().modificate()

            elif self.modifNote.type == "BORNEOUT" :
                time_diff = self.getTimeAndPisteNumberAtPosition(self.lastMousePos)[0] - self.getTimeAndPisteNumberAtPosition(event.pos())[0]
                self.modifNote.note.timeOut -= time_diff
                self.modifNote.note.checkTime(priority = "timeOut")
                self.update()
                self.getFenetrePrincipale().modificate()


        else :
            self.modifNote = None


        self.refreshCursor(event.pos())
        self.lastMousePos = event.pos()

    def mousePressEvent(self, event) :

        if QtGui.QApplication.mouseButtons() == QtCore.Qt.LeftButton :
            modifNote = self.getNoteAtPixelPosition(event.pos())
            if modifNote is None : return
            self.modifNote = modifNote
            self.currentNote = modifNote.note.copy()
            self.modifNote.note.backupTimes()

        self.refreshCursor(event.pos())

##        elif QtGui.QApplication.mouseButtons() == QtCore.Qt.MidButton :
##            pass


    def mouseReleaseEvent(self, event) :
        """
        Relâchement d'un bouton
        """
        self.refreshCursor(event.pos())

        if self.modifNote is None : return

        note = self.modifNote.note
        if not [self.modifNote.note.timeIn, self.modifNote.note.timeOut] == self.modifNote.note.getBackup() :
            self.controlZ.addAction(Action(note, ["timeIn", "timeOut"], self.modifNote.note.getBackup(), [self.modifNote.note.timeIn, self.modifNote.note.timeOut]))
            self._parent.parent.annulerAction.setEnabled(True)

        self.currentNote = None
        self.update()

    def wheelEvent(self, event) :
        """
        Roulette
        """
        fac = .1
        MonfEditor.DST += event.delta()*fac

        if MonfEditor.DST > 500 : MonfEditor.DST=500
        elif MonfEditor.DST < 20 : MonfEditor.DST = 20
        self.update()

    def refreshCursor(self, pos) :
        """
        S'occupe du rafraîchissement du curseur, passer la position de la souris en argument
        """

        modifNote = self.getNoteAtPixelPosition(pos)
        if modifNote is None :
            self.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
            return


        if modifNote.isPosModif() :
            if QtCore.Qt.LeftButton == QtGui.QApplication.mouseButtons() :
                self.setCursor(QtGui.QCursor(QtCore.Qt.ClosedHandCursor))
            else :
                self.setCursor(QtGui.QCursor(QtCore.Qt.OpenHandCursor))

        elif modifNote.isSizeModif() : self.setCursor(QtGui.QCursor(QtCore.Qt.SizeHorCursor))


    def reloadMonf(self, monf=None) :
        if monf is None :
            self._monf = None
        else :
            self._monf = monf
        self.update()
        self.controlZ = ControlZ()


class AfficheurNotes(QtGui.QWidget) :
    size        = 30
    textColor   = QtGui.QColor(10,10,0)
    marge       = 5

    def __init__(self, parent) :
        self.parent = parent
        QtGui.QWidget.__init__(self, parent)

    def paintEvent(self, event) :
        self.resize(AfficheurNotes.size, self.parent.height())
        qp = QtGui.QPainter()
        qp.begin(self)

        qp.fillRect(0,0,self.width(),self.height(),MonfEditor.couleurFond)

        for i in range(0,27) :
            qp.fillRect(0,(i+.5)*MonfEditor.hauteurPiste, self.width(), 2, MonfEditor.couleurPortee.lighter(110))
            qp.drawText(AfficheurNotes.marge,(i+.75)*MonfEditor.hauteurPiste, Note.pisteNumberToNote[i])

class ConteneurMonf(QtGui.QWidget) :
    def __init__(self, parent=None, monf=None) :
        QtGui.QWidget.__init__(self, parent)
        self.parent = parent
        self.layout = QtGui.QGridLayout(self)
        self.barreHorizontale = QtGui.QScrollBar(0x01, self)
        self.afficheurNotes = AfficheurNotes(self)
        self.monfEditor = MonfEditor(self, monf)

        self.barreHorizontale.valueChanged.connect(self.horizontalScrollChanged)


        self.initialize()
        self.updateLimits()
        self.show()


    def initialize(self) :
        self.layout.setContentsMargins(0,0,0,0)
        self.layout.setMargin(0)
        self.layout.addWidget(self.barreHorizontale,1,1)
        self.layout.addWidget(self.monfEditor,0,1)
        self.layout.addWidget(self.afficheurNotes, 0,0)

        self.layout.setColumnStretch(0,0)
        self.layout.setColumnMinimumWidth(0,AfficheurNotes.size)
        self.layout.setColumnStretch(1,1)

        self.setMinimumSize(200, self.monfEditor.sizeY+self.barreHorizontale.height())
        self.resize(self.monfEditor.sizeX, self.monfEditor.sizeY+self.barreHorizontale.height())

    def reloadMonf(self, monf=None) :
        self.monfEditor.reloadMonf(monf)
        self.updateLimits()

    def getMonf(self) :
        return self.monfEditor._monf

    def updateLimits(self) :
        monf = self.getMonf()
        if not monf is None :
            self.barreHorizontale.setRange(-1, self.getMonf().getTimeLength())
        else :
            self.barreHorizontale.setRange(-1,1)

    def horizontalScrollChanged(self, value) :
        self.monfEditor.startX = value
        self.monfEditor.update()

if __name__ == '__main__':
    import sys

    sys.path.append("../libMidi")
    sys.path.append("../libMidi/midi")

    import morceau
    import monf
    m = morceau.Morceau("../../../multimedia/MIDIFILES/TEST1.mid")
    monfFile = m.parseOutput()



    app = QtGui.QApplication(sys.argv)
    app.setApplicationName('monfEditor')
    win = ConteneurMonf(monf=monfFile)
##    win.resize(200, 100)
    win.show()
    sys.exit(app.exec_())

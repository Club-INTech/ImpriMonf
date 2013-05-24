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

class MonfEditor(QtGui.QWidget) :

    hauteurPiste = 18
    DST = 100. #Distance, en pixels, correspondant a 1s de musique

    couleurFond = QtGui.QColor(230,230,230)
    couleurPortee = QtGui.QColor(200,200,200)

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

        if not monf is None :
            self.taillePoincon = monf._morceau._taillePoincon / monf._morceau._DST
            self.getPoincons()

        self.show()
        self.setMouseTracking(True)

    def getPoincons(self) :
        self.poincons = self._monf.getAllPoincons()
##        print (self._monf.getNombrePoincons(self.poincons))

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
        # On affiche les notes
        notes = self._monf._morceau.getNotesBetween(self.startX-10, self.startX + self.width()/self._DST)
        self.notesAffichees = notes
        for note in notes :
            try :
                qp.fillRect(self._DST*(note.timeIn-self.startX), self._monf.getNumeroPisteOfNote(note)*self.hauteurPiste + 2 , max(1, self._DST*(note.timeOut - note.timeIn)), self.hauteurPiste - 4, note.color)
            except KeyError :
                pass

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
        temps = pos.x()/self._DST + self.startX
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

            elif self.modifNote.type == "BORNEIN" :
                time_diff = self.getTimeAndPisteNumberAtPosition(self.lastMousePos)[0] - self.getTimeAndPisteNumberAtPosition(event.pos())[0]
                self.modifNote.note.timeIn -= time_diff
                self.modifNote.note.checkTime(priority = "timeIn")
                self.update()

            elif self.modifNote.type == "BORNEOUT" :
                time_diff = self.getTimeAndPisteNumberAtPosition(self.lastMousePos)[0] - self.getTimeAndPisteNumberAtPosition(event.pos())[0]
                self.modifNote.note.timeOut -= time_diff
                self.modifNote.note.checkTime(priority = "timeOut")
                self.update()

        else :
            self.modifNote = None

        self.lastMousePos = event.pos()

    def mousePressEvent(self, event) :

        if QtGui.QApplication.mouseButtons() == QtCore.Qt.LeftButton :
            modifNote = self.getNoteAtPixelPosition(event.pos())
            if modifNote is None : return
            self.modifNote = modifNote

##        elif QtGui.QApplication.mouseButtons() == QtCore.Qt.MidButton :
##            pass

    def mouseReleaseEvent(self, event) :
##        print ("MOUSE RELEASE D:")
        pass

    def reloadMonf(self, monf=None) :
        if monf is None :
            self._monf = None
        else :
            self._monf = monf
        self.update()


class AfficheurNotes(QtGui.QWidget) :
    size        = 30
    textColor   = QtGui.QColor(10,10,0)
    marge       = 5

    def __init__(self, parent) :
        self.parent = parent
        QtGui.QWidget.__init__(self, parent)
        self.resize(AfficheurNotes.size, parent.height())

    def paintEvent(self, event) :
        self.resize(50, self.parent.height())
        qp = QtGui.QPainter()
        qp.begin(self)

        qp.fillRect(0,0,self.width(),self.height(),MonfEditor.couleurFond)

        for i in range(0,27) :
            qp.fillRect(0,(i+.5)*MonfEditor.hauteurPiste, self.width(), 2, MonfEditor.couleurPortee.lighter(110))
            qp.drawText(AfficheurNotes.marge,(i+.75)*MonfEditor.hauteurPiste, Note.pisteNumberToNote[i])

class ConteneurMonf(QtGui.QWidget) :
    def __init__(self, parent=None, monf=None) :
        QtGui.QWidget.__init__(self, parent)
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
        self.layout.addWidget(self.barreHorizontale,0,0,1,0)
        self.layout.addWidget(self.monfEditor,1,1)
        self.layout.addWidget(self.afficheurNotes, 1,0)

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
            self.barreHorizontale.setRange(-1, self.getMonf().getTimeLength()+3)
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

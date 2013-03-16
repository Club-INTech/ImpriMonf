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

from PyQt4 import QtGui, QtCore

class MonfEditor(QtGui.QWidget) :
    def __init__(self, parent=None, monf=None) :
        self._monf = monf
        self._parent = parent
        QtGui.QWidget.__init__(self, self._parent)

        self.sizeX, self.sizeY = 600, 700

        # Couleurs de base
        self.couleurFond    = QtGui.QColor(230,230,230)
        self.couleurPortee  = QtGui.QColor(200,200,200)
        self.couleurPiste   = QtGui.QColor(200,10,30)

        # Longueurs/Hauteurs constantes
        self.hauteurPiste = 24
        self.sizeY = 27*self.hauteurPiste # 27 = nombre de pistes

        self._DST = 5 #Distance, en pixels, correspondant a 1s de musique

        if not monf is None : self.taillePoincon = monf._morceau._taillePoincon / monf._morceau._DST

        self.getPoincons()

        self.show()

    def getPoincons(self) :
        self.poincons = self._monf.getAllPoincons()

    def paintEvent(self, e) :
        self.resize(self.sizeX, self.sizeY)

        qp = QtGui.QPainter()
        qp.begin(self)

        # Rectangle blanchatre de fond
        qp.fillRect(0,0, self.sizeX, self.sizeY, QtGui.QBrush(self.couleurFond))
        # Ajout des portees
        for i in range(27) :
            qp.fillRect(0,(i+.5)*self.hauteurPiste, self.sizeX, 2, QtGui.QBrush(self.couleurPortee))

        # Si on n'a pas de monf, on s'arrete ici
        if self._monf is None :
            return
        # Sinon, on continue
        hauteursNotesPasUtilisees = []
        # On affiche les coups de poincon
        for note in self.poincons.keys() :
            for dist in self.poincons[note] :

                try:
                    piste = self._monf.noteToPisteNumber[note]
                    qp.fillRect(self._DST*dist, piste*self.hauteurPiste + 2 , max(1, self.taillePoincon*self._DST), self.hauteurPiste - 4, self.couleurPiste)
                except KeyError :
                    if note not in hauteursNotesPasUtilisees : hauteursNotesPasUtilisees.append(note)
        print (hauteursNotesPasUtilisees)


if __name__ == '__main__':
    import sys

    sys.path.append("../libMidi")
    sys.path.append("../libMidi/midi")
##    import monf
##    monfFile = monf.easyMonf()
    import morceau
    m = morceau.Morceau("../../../multimedia/MIDIFILES/linkin_park-blackout.mid")
    m.addIgnoredPiste(2)
    monfFile = m.parseOutput()

    app = QtGui.QApplication(sys.argv)
    app.setApplicationName('monfEditor')
    win = MonfEditor(monf=monfFile)
    win.resize(200, 100)
    win.show()
    sys.exit(app.exec_())

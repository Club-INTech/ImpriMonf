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

        # Longueurs/Hauteurs constantes
        self.hauteurPiste = 24
        self.sizeY = 27*self.hauteurPiste # 27 = nombre de pistes

        self.show()

    def paintEvent(self, e) :
        self.resize(self.sizeX, self.sizeY)

        qp = QtGui.QPainter()
        qp.begin(self)

        # Rectangle blanchâtre de fond
        qp.fillRect(0,0, self.sizeX, self.sizeY, QtGui.QBrush(self.couleurFond))
        # Ajout des portées
        for i in range(27) :
            qp.fillRect(0,(i+.5)*self.hauteurPiste, self.sizeX, 2, QtGui.QBrush(self.couleurPortee))

        # Si on n'a pas de monf, on s'arrête ici
        if self._monf is None :
            return
        # Sinon, on continue




if __name__ == '__main__':
    import sys

    sys.path.append("../libMidi")
    import monf

    monfFile = monf.easyMonf()

    app = QtGui.QApplication(sys.argv)
    app.setApplicationName('monfEditor')
    win = MonfEditor()
    win.resize(200, 100)
    win.show()
    sys.exit(app.exec_())

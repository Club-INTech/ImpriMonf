from PyQt4 import QtCore, QtGui


class Credits(QtGui.QDialog) :
    def __init__(self, parent) :
        QtGui.QDialog.__init__(self, None)

        mainLayout = QtGui.QGridLayout()
        texte = QtGui.QLabel("© Team Sopal'INT 2013", self)
        mainLayout.addWidget(texte, 0, 0)
        self.setLayout(mainLayout)

        self.setWindowTitle("Crédits")
        QtGui.QDialog.exec_(self)

class Aide(QtGui.QDialog) :
    def __init__(self, parent) :
        QtGui.QDialog.__init__(self, None)

        mainLayout = QtGui.QGridLayout()
        texte = QtGui.QLabel("LOL Rien pour l'instant", self)
        mainLayout.addWidget(texte, 0, 0)
        self.setLayout(mainLayout)

        self.setWindowTitle("Aide")
        QtGui.QDialog.exec_(self)
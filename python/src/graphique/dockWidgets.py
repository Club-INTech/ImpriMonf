from PyQt4 import QtGui, QtCore

class OptionsCarton(QtGui.QDockWidget) :
    def __init__(self, parent) :
        QtGui.QDockWidget.__init__(self, parent)
        self.parent = parent
        self.setWindowTitle("Options")
        self.setFeatures(QtGui.QDockWidget.DockWidgetMovable)
        self.initialize()

    def initialize(self) :
        self.widget = QtGui.QWidget(self)
        layout = QtGui.QGridLayout(self)

        self.vitesseDefilementTexte = QtGui.QLabel("Vitesse de défilement :", self.widget)
        self.vitesseDefilement = QtGui.QDoubleSpinBox(self.widget)
        self.vitesseDefilement.setRange(1,20)
        self.vitesseDefilement.setDecimals(1)
        self.vitesseDefilement.setValue(5)
        self.vitesseDefilement.setSuffix(" cm/s")

        layout.addWidget(self.vitesseDefilementTexte, 0,0)
        layout.addWidget(self.vitesseDefilement,0,1)

        self.widget.setLayout(layout)

        self.setWidget(self.widget)

class LanceurImpression(QtGui.QDockWidget) :
    def __init__(self, parent) :
        QtGui.QDockWidget.__init__(self, parent)
        self.parent = parent
        self.setWindowTitle("Lancement de l'impression")
        self.setFeatures(QtGui.QDockWidget.DockWidgetMovable)
        self.initialize()

    def initialize(self) :
        self.widget = QtGui.QWidget(self)
        layout = QtGui.QGridLayout(self)

        self.boutonLancement = QtGui.QPushButton("Lancer l'impression", self.widget)
        self.progressBar = QtGui.QProgressBar(self.widget)

        layout.addWidget(self.boutonLancement, 0, 0)
        layout.addWidget(self.progressBar, 1, 0)

        self.widget.setLayout(layout)

        self.setWidget(self.widget)

class EditionMorceau(QtGui.QDockWidget) :
    def __init__(self, parent) :
        QtGui.QDockWidget.__init__(self, parent)
        self.parent = parent
        self.setWindowTitle("Édition du morceau")
        self.setFeatures(QtGui.QDockWidget.DockWidgetMovable)
        self.initialize()

    def initialize(self) :
        self.widget = QtGui.QWidget(self)
        layout = QtGui.QGridLayout(self)

        self.boutonLancement = QtGui.QPushButton("Lancer l'impression", self.widget)
        self.progressBar = QtGui.QProgressBar(self.widget)

        layout.addWidget(self.boutonLancement, 0, 0)
        layout.addWidget(self.progressBar, 1, 0)

        self.widget.setLayout(layout)

        self.setWidget(self.widget)
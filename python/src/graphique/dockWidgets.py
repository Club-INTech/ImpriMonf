from PyQt4 import QtGui, QtCore

from progressBar import ProgressBarMonf, ProgressBarImpression

class OptionsCarton(QtGui.QDockWidget) :
    def __init__(self, parent) :
        QtGui.QDockWidget.__init__(self, parent)
        self.parent = parent
        self.setWindowTitle("Options")
        self.setFeatures(QtGui.QDockWidget.NoDockWidgetFeatures)
        self.monf = None
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

    def reloadMonf(self, monf) :
        self.monf = monf

class LanceurConversion(QtGui.QDockWidget) :
    def __init__(self, parent) :
        QtGui.QDockWidget.__init__(self, parent)
        self.parent = parent
        self.setWindowTitle("Lancement de la conversion")
        self.setFeatures(QtGui.QDockWidget.NoDockWidgetFeatures)
        self.monf = None
        self.initialize()

    def initialize(self) :
        self.widget = QtGui.QWidget(self)
        layout = QtGui.QGridLayout(self)

        self.boutonConversion = QtGui.QPushButton("Convertir", self.widget)
        self.progressBarMonf = ProgressBarMonf(self.widget)
        self.progressBarMonf.setBouton(self.boutonConversion)

        layout.addWidget(self.boutonConversion,0,0)
        layout.addWidget(self.progressBarMonf, 0,1)

        self.widget.setLayout(layout)

        self.setWidget(self.widget)

    def reloadMonf(self, monf) :
        self.monf = monf
        self.progressBarMonf.setMonf(self.monf)

class RecalageEtFinDImpression(QtGui.QDockWidget) :
    def __init__(self, parent) :
        QtGui.QDockWidget.__init__(self, parent)
        self.parent = parent
        self.setWindowTitle("Recalage et Fin d'impression")
        self.setFeatures(QtGui.QDockWidget.NoDockWidgetFeatures)
        self.monf = None
        self.imprimante = None
        self.initialize()

    def initialize(self) :
        self.widget = QtGui.QWidget(self)
        layout = QtGui.QGridLayout(self)

        self.boolRecalage = "Recaler"
        self.recalerBouton = QtGui.QPushButton(self.boolRecalage, self.widget)
        self.recalerBouton.clicked.connect(self.recalerAction)
        self.recalerBouton.setEnabled(False)

        self.boolFin = "Sortir le carton"
        self.finBouton = QtGui.QPushButton(self.boolFin, self.widget)
        self.finBouton.clicked.connect(self.finAction)
        self.finBouton.setEnabled(False)

        layout.addWidget(self.recalerBouton,0,0)
        layout.addWidget(self.finBouton,1,0)

        self.widget.setLayout(layout)

        self.setWidget(self.widget)

    def reloadMonf(self, monf) :
        self.monf = monf

    def reloadImprimante(self, imprimante) :
        self.imprimante = imprimante
        if not self.imprimante is None :
            self.recalerBouton.setEnabled(True)
            self.finBouton.setEnabled(True)

    def recalerAction(self) :
        if self.boolRecalage == "Recaler" :
            if not self.imprimante is None :
                self.imprimante.debut_rentrer_poincon()
                self.boolRecalage = "OK"
        else :
            if not self.imprimante is None :
                self.imprimante.fin_rentrer_poincon()
                self.boolRecalage = "Recaler"

        self.recalerBouton.setText(self.boolRecalage)

    def finAction(self) :
        if self.boolFin == "Sortir le carton" :
            if not self.imprimante is None :
                self.imprimante.debut_sortir_carton()
                self.boolFin = "Arrêter"
        else :
            if not self.imprimante is None :
                self.imprimante.fin_sortir_carton()
                self.boolFin = "Sortir le carton"

        self.finBouton.setText(self.boolFin)


class Impression(QtGui.QDockWidget) :
    def __init__(self, parent) :
        QtGui.QDockWidget.__init__(self, parent)
        self.parent = parent
        self.setWindowTitle("Impression")
        self.setFeatures(QtGui.QDockWidget.NoDockWidgetFeatures)
        self.monf = None
        self.imprimante = None
        self.initialize()

    def initialize(self) :
        self.widget = QtGui.QWidget(self)
        layout = QtGui.QGridLayout(self)

        self.imprimerBouton = QtGui.QPushButton("Imprimer", self.widget)
        self.imprimerBouton.setEnabled(False)

        self.progressBarImpression = ProgressBarImpression(self)
        self.progressBarImpression.setBouton(self.imprimerBouton)

        layout.addWidget(self.imprimerBouton,0,0)
        layout.addWidget(self.progressBarImpression, 1,0)

        self.widget.setLayout(layout)

        self.setWidget(self.widget)

    def reloadMonf(self, monf) :
        self.monf = monf
        self.progressBarImpression.setMonf(monf)

    def reloadImprimante(self, imprimante) :
        self.imprimante = imprimante
        self.progressBarImpression.setImprimante(self.imprimante)

        if not self.imprimante is None :
            self.imprimerBouton.setEnabled(True)

# USELESS BITCH
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
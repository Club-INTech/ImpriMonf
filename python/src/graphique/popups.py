from PyQt4 import QtGui

import constantes

class PopupSave(QtGui.QDialog):
    def __init__(self, parent) :
        QtGui.QWidget.__init__(self, parent)
        self.initUID()
        self.result = None
        self.setMaximumSize(500,600)
        self.setWindowTitle("Options d'exportation MiDi")
        self.setModal(True)

    def initUID(self) :
        layout = QtGui.QGridLayout(self)
        self.setLayout(layout)

        label = QtGui.QLabel("Choix de l'instrument :", self)

        # Construction de la liste d'instruments
        self.liste = QtGui.QListWidget(self)
        for i, instrument in enumerate(constantes.instruments) :
            # Switch pour l'instrument par défaut, "Flûte de Pan"
            if i == 0x4B :
                widget = QtGui.QListWidgetItem(instrument)
                self.liste.addItem(widget)
                self.liste.setCurrentItem (widget)
            else:
                self.liste.addItem(QtGui.QListWidgetItem(instrument))

        self.case = QtGui.QCheckBox("Applatir les pistes", self)

        self.boutonOk = QtGui.QPushButton("Exporter", self)
        self.boutonCancel = QtGui.QPushButton("Annuler", self)

        self.boutonOk.setIcon(QtGui.QIcon("icons/ok.png"))
        self.boutonCancel.setIcon(QtGui.QIcon("icons/nope.png"))

        self.boutonOk.clicked.connect(self.accepted)
        self.boutonCancel.clicked.connect(self.rejected)

        layout.addWidget(label, 0,0,1,2)
        layout.addWidget(self.liste, 1, 0,1,2)
        layout.addWidget(self.case,2,0,1,2)
        layout.addWidget(self.boutonOk, 3, 1)
        layout.addWidget(self.boutonCancel, 3, 0)

    def accepted(self) :
        self.resultat = [constantes.instruments.index(self.liste.selectedItems()[0].text()), self.case.isChecked()]
        QtGui.QDialog.accept(self)

    def rejected(self) :
        self.resultat = None
        QtGui.QDialog.reject(self)
        
class PopupPlayerOptions(QtGui.QDialog) :
    def __init__(self, parent) :
        QtGui.QWidget.__init__(self, parent)
        self.initUID()
        self.result = None
        self.setMaximumSize(500,600)
        self.setWindowTitle("Options du player")
        self.setModal(True)

    def initUID(self) :
        layout = QtGui.QGridLayout(self)
        self.setLayout(layout)

        label = QtGui.QLabel("Choix de l'instrument :", self)

        # Construction de la liste d'instruments
        self.liste = QtGui.QListWidget(self)
        for i, instrument in enumerate(constantes.instruments) :
            # Switch pour l'instrument par défaut, "Flûte de Pan"
            if i == 0x4B :
                widget = QtGui.QListWidgetItem(instrument)
                self.liste.addItem(widget)
                self.liste.setCurrentItem (widget)
            else:
                self.liste.addItem(QtGui.QListWidgetItem(instrument))

        self.boutonOk = QtGui.QPushButton("Ok", self)
        self.boutonCancel = QtGui.QPushButton("Annuler", self)

        self.boutonOk.setIcon(QtGui.QIcon("icons/ok.png"))
        self.boutonCancel.setIcon(QtGui.QIcon("icons/nope.png"))

        self.boutonOk.clicked.connect(self.accepted)
        self.boutonCancel.clicked.connect(self.rejected)

        layout.addWidget(label, 0,0,1,2)
        layout.addWidget(self.liste, 1, 0,1,2)
        layout.addWidget(self.boutonOk, 2, 1)
        layout.addWidget(self.boutonCancel, 2, 0)

    def accepted(self) :
        self.resultat = [constantes.instruments.index(self.liste.selectedItems()[0].text())]
        QtGui.QDialog.accept(self)

    def rejected(self) :
        self.resultat = None
        QtGui.QDialog.reject(self)






from PyQt4 import QtGui, QtCore

class ChannelComboBox(QtGui.QComboBox) :
    def __init__(self, parent) :
        QtGui.QComboBox.__init__(self, parent)

    def setMonf(self, monf) :
        self.monf = monf
        abstractView = QtGui.QAbstractItemView()
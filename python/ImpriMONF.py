import sys

sys.path.append("src")
sys.path.append("src/graphique")
sys.path.append("src/libMidi")
sys.path.append("src/libMidi/midi")
sys.path.append("../pathfinding.py")

from PyQt4 import QtGui
from fenetrePrincipale import FenetrePrincipale

app = QtGui.QApplication(sys.argv)
app.setApplicationName('Monf Editor')

win = FenetrePrincipale(app)

win.show()
sys.exit(app.exec_())
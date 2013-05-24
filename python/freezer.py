import sys, os
import PyQt4
from cx_Freeze import setup, Executable


sys.path.append(os.path.join(os.getcwd(), "src/Graphique"))
sys.path.append(os.path.join(os.getcwd(), "src/libMidi"))
sys.path.append(os.path.join(os.getcwd(), "src/libMidi/midi"))
sys.path.append(os.getcwd())

include_files = []
# Dependencies are automatically detected, but it might need fine tuning.
build_exe_options = {"packages": ["os", "PyQt4"],
                     "include_files":include_files
                     }

# GUI applications require a different base on Windows (the default is for a
# console application).
base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(  name = "Impri'Monf",
        version = "1.0",
        author="Sopal'INT TEAM",
        url="www.nyan.cat",
        maintainer="Thibaut REMY",
        description = "Poinçonneur de cartons d'orgue de barbarie",
        options = {"build_exe": build_exe_options},
        executables = [Executable("src/Graphique/fenetrePrincipale.py", base=base)])

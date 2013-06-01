import sys, os
from cx_Freeze import setup, Executable
import serial


sys.path.append(os.path.join(os.getcwd(), "src/Graphique"))
sys.path.append(os.path.join(os.getcwd(), "src/libMidi"))
sys.path.append(os.path.join(os.getcwd(), "src/libMidi/midi"))
sys.path.append(os.path.join(os.getcwd(), "src"))
sys.path.append(os.getcwd())

include_files = ["icons/"]
# Dependencies are automatically detected, but it might need fine tuning.
build_exe_options = {"packages": ["os", "serial"],
                     "excludes": ["PyQt4.QtOpenGL", "PyQt4.QtNetwork", "PyQt4.QtScript", "PyQt4.QtSql", "PyQt4.QtSvg", "PyQt4.QtTest", "PyQt4.QtXml"],
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
        executables = [Executable("ImpriMONF.py", base=base)])

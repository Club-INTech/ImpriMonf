from PyQt4 import QtGui
import morceau

class Note :
    numbers = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
    noteToPisteNumber = {"D7":0, "C7":1, "B6":2, "A#6":3, "A6":4, "G#6":5, "G6":6, "F#6":7, "F6":8, "E6":9, "D#6":10, "D6":11, "C#6":12, "C6":13, "B5":14, "A#5":15, "A5":16, "G5":17, "F#5":18, "F5":19, "E5":20, "D5":21, "C5":22, "G4":23, "F4":24, "D4":25, "C4":26}
    pisteNumberToNote = {0:"D7", 1:"C7", 2:"B6", 3:"A#6", 4:"A6", 5:"G#6", 6:"G6", 7:"F#6", 8:"F6", 9:"E6", 10:"D#6", 11:"D6", 12:"C#6", 13:"C6", 14:"B5", 15:"A#5", 16:"A5", 17:"G5", 18:"F#5", 19:"F5", 20:"E5", 21:"D5", 22:"C5", 23:"G4", 24:"F4", 25:"D4", 26:"C4"}
    minimalInterval = morceau.Morceau.taillePoincon /morceau.Morceau.DST

    def __init__(self, byte=None, number=None, octave=None, timeIn=0, timeOut=0, velocity=0,color=None, QColor=None) :
        self.numer=number
        self.octave=octave
        self.timeIn=timeIn
        self.timeOut=timeOut

        self.lastTimeIn = timeIn
        self.lastTimeOut = timeOut
        self.velocity=velocity
        if not color is None and QColor is None: self.color=QtGui.QColor(*color)
        elif not QColor is None : self.color=QColor
        else : self.color = QtGui.QColor(0,255,0)

        if not byte is None : self.setByte(byte)

    # Permet de configurer la note selon un byte comme specifie dans la
    # norme Midi
    def setByte(self, byte) :
        self.number=Note.numbers[byte%12]
        self.octave=byte//12
        self.byte = byte


    # Cast as String
    def __str__(self) :
        try :
            return self.number + str(self.octave)
        except :
            return "#INCONNU"

    def setTimeOut(self, timeOut):
        self.timeOut=timeOut
        self.checkTime()

    def setColor(self, r, g, b) :
        self.color = QtGui.QColor(r, g, b)

    def setChannel(self, channel) :
        self.channel = channel

    def containsTime(self, temps, margin=0) :
        """
        return "INSIDE" si le temps donné en argument est à  l'intérieur de la note
        return "BORNEIN" ou "BORNEOUT" si le temps donné est à proximité des temps d'entrée ou de sortie
        return "OUTSIDE" si le temps donné est complètement HS.

        """
        if self.timeIn+margin <= temps and self.timeOut-margin >= temps : return "INSIDE"
        elif abs(self.timeIn-temps) <= margin : return "BORNEIN"
        elif abs(self.timeOut-temps) <= margin : return "BORNEOUT"
        else : return "OUTSIDE"

    def checkTime(self, priority="timeOut") :
        """
        Fonction à appeller pour vérifier que TimeIn et TimeOut sont bien compatibles
        Priority montre quel est la borne à ne pas modifier si besoin est.
        """
        if priority=="timeOut":
            if self.timeIn + Note.minimalInterval >= self.timeOut : self.timeOut = self.timeIn + Note.minimalInterval
        else :
            if self.timeIn + Note.minimalInterval >= self.timeOut : self.timeIn = self.timeOut - Note.minimalInterval

    def backupTimes(self) :
        self.lastTimeIn = self.timeIn
        self.lastTimeOut = self.timeOut
    def getBackup(self) :
        return [self.lastTimeIn, self.lastTimeOut]

    def copy(self) :
        return Note(self.byte, self.number, self.octave, self.timeIn, self.timeOut, self.velocity, QColor = self.color)

def isOk(bytenote) :
    testNote = Note()
    testNote.setByte(bytenote)
    return str(testNote) in Note.noteToPisteNumber.keys()

def getNumberOctave(number) :
    note = Note.pisteNumberToNote[number]
    number = note[:len(note)-1]
    octave = int(note[-1])
    return [number, octave]


if __name__ == "__main__" :
    n = Note()
    n.setByte(127)
    print (n.number, n.octave)

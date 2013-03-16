class Note :
    numbers = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A", "B"]
    def __init__(self, byte=None, number=None, octave=None, timeIn=0, timeOut=0, velocity=0,) :
        self.numer=number
        self.octave=octave
        self.timeIn=timeIn
        self.timeOut=timeOut
        self.velocity=velocity

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

if __name__ == "__main__" :
    n = Note()
    n.setByte(127)
    print (n.number, n.octave)
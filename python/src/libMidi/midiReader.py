from mmap import mmap
from piste import Piste
from note import Note

class midiReader :
    def __init__(self, midiFile) :
        with open(midiFile, "r+b") as f:
            self._midiFile = midiFile
            self._mmap = mmap(f.fileno(), 0)
            self._f = f
            self._fileFormat = None
            self._numberOfTracks = 0
            self._deltaTimeTicks = 0

            self.posCurseur = 0

            self._pistes = []
            self._tempo  = 0

            self.read()

            self._f.close()

        #except :
            #raise IOError("Impossible d'ouvrir le fichier " + midiFile)

    # Lit un nombre donnee de bytes du fichier MiDi
    def readBytes(self, nombre=1) :
        result = 0
        for i in range(nombre) :
            result += 256**(nombre-1-i)*self._mmap.read_byte()
        self.posCurseur+=nombre
        return result

    def getDelay(self) :
        b = self.readBytes()
        if b < 128 : result = b
        else : result = 0

        while b >= 128 :
            result += b-128
            b = self.readBytes()
        return result


    # Retourne une chaine de caracteres
    def readString(self, nombre=1) :
        string = ""
        for i in range(nombre) :
            a = self.readBytes()
            string += str(chr(a))
        return string

    # Permet d'avancer dans le fichier
    def moveInFile(self, nombreBytes=0) :
        for i in range(nombreBytes) : self._mmap.read_byte()
        self.posCurseur+=nombreBytes

    # Lit et stocke les donnees du fichier
    def read(self) :
        # Recuperation des informations de Header
        self._mmap.seek(8)
        self._fileFormat = self.readBytes(2)
        self._numberOfTracks = self.readBytes(2)
        self._deltaTimeTicks = self.readBytes(2)

        print ("------ INFOS ------")
        print (self._fileFormat, self._numberOfTracks, self._deltaTimeTicks)

        # Lecture de chaque pistes
        for id_piste in range(self._numberOfTracks) :
            piste = Piste()
            self._pistes.append(piste)
            self.moveInFile(4)
            nombreBytes = self.readBytes(4)
            self.posCurseur = 0
            currentTime = 0

            while self.posCurseur < nombreBytes :
                delay = self.getDelay()
                try : currentTime += delay*self._tempo
                except : pass

                b1 = self.readBytes()


                if b1 == 0xFF :
                    b2 = self.readBytes()
                    # TEMPO
                    if b2 == 0x51 :
                        b3 = self.readBytes()
                        if b3 == 0x03 :
                            self._tempo = self.readBytes(3)
                    # NOM DE LA PISTE
                    elif b2 == 0x03 :
                        longueur = self.readBytes()
                        piste._nom = self.readString(longueur+1)
                    elif b2 == 0x06 :
                        self.readString(self.readBytes()+1)
                    # Fin de la piste
                    elif b2 == 0x2F :
                        b3 = self.readBytes()
                        if b3 == 0x00 :
                            break
                    # WARNING non gÃ©rÃ©
                    elif b2 == 0x58 : self.moveInFile(5)
                    elif b2 == 0x54 : self.moveInFile(6)
                    elif b2 == 0x59 : self.moveInFile(3)
                    elif b2 == 0x21 : self.moveInFile(1)
                    else :
                        print("OULALALALALAL", b2)

                # Note ON
                if b1 >= 0x90 and b1 < 0xA0 :
                    channel = b1%16
                    byteNote = self.readBytes()
                    velocity = self.readBytes()
                    if not velocity == 0 :
                        piste.addNote(channel, Note(byte=byteNote, timeIn=currentTime, velocity=self.readBytes()))
                    else :
                        piste.getLastNote(channel, byteNote).timeOut = currentTime
                # Note OFF
                elif b1 >= 0x80 and b1 < 0x90 :
                    channel = b1%16
                    byteNote = self.readBytes()
                    velocity = self.readBytes()
                    #piste.getLastNote(channel, byteNote).timeOut = currentTime

                # WARNING non utilisÃ©s
                elif b1 >=0xA0 and b1 < 0xC0:
                    self.moveInFile(2)
                elif b1 >= 0xC0 and b1 < 0xE0 :
                    self.moveInFile(1)
                elif b1 >= 0xE0 :
                    self.moveInFile(2)
                #else : print ("OULALALALALAL", b1, "=", hex(b1))

            print(piste.check())

if __name__ == "__main__" :
    print ("________________________ FILE LINKIN PARK BLACKOUT ________________________________")
    m1 = midiReader("../files/linkin_park-blackout.mid")
    print ("________________________ FILE BEAT IT ________________________________")
    m2 =midiReader("../files/beat-it.mid")
    #print(m2.

    #print ("________________________ FILE GANGNAM STYLE ________________________________")
    #midiReader("../files/psy-gangnam_style.mid")

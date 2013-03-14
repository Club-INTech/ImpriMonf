import sys
sys.path.append("midi")
from MidiInFile import MidiInFile

from outputMidi import OutputMidi
from monf import Monf

class Morceau :
    def __init__(self, nomFichier=None) :
        self._ignoredPistes = []
        self._DST = 20   # Distance (en mm) correspondant Ã  1s de musique
        self._taillePoincon = 3 # Taille (en mm) du poinÃ§on

        if not nomFichier is None :
            self._nomFichier = nomFichier
            self.parseNomFichier()

    def parseNomFichier(self) :
        self._output = OutputMidi()
        self._in = MidiInFile(self._output, self._nomFichier)
        self._in.read()

    def addIgnoredPiste(self, id_) :
        if not id_ in self._ignoredPistes and id_ in self._output._tracks.keys() :
            self._ignoredPistes.append(id_)

        else :
            raise Exception("La piste à ignorer n'est pas dans les clés des pistes du morceau")

    # Doit Ãªtre appellÃ© en diffÃ©rÃ©, aprÃ¨s avoir inclu les pistes ignorÃ©es
    def parseOutput(self) :
        """
        Retourne un objet Monf
        """
        m = Monf(self._nomFichier, self)
        for id_track in self._output._tracks.keys() :
            if not id_track in self._ignoredPistes :
                monfOneTrack = self._output._tracks[id_track].getMonf(self)
                m.addMonfOneTrack(monfOneTrack)
        return m


if __name__=="__main__" :
    m = Morceau("../files/linkin_park-blackout.mid")
    m.addIgnoredPiste(10)
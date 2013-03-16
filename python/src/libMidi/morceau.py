import sys
sys.path.append("midi")
from MidiInFile import MidiInFile

from outputMidi import OutputMidi

class Morceau :
    def __init__(self, nomFichier=None) :
        self._ignoredPistes = []
        self._DST = 200   # Distance (en mm) correspondant a 1s de musique
        self._taillePoincon = 4 # Escpacement (en mm) entre deux poincons

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
            raise Exception("La piste aÃ‚Â  ignorer n'est pas dans les cles des pistes du morceau")

    # Doit etre appelle en differe.
    def parseOutput(self) :
        """
        Retourne un objet Monf
        """
        from monf import Monf
        m = Monf(self._nomFichier, self)
        for id_track in self._output._tracks.keys() :
            if not id_track in self._ignoredPistes :
                monfOneTrack = self._output._tracks[id_track].getMonf(self)
                m.addMonfOneTrack(monfOneTrack)
        print (m._morceau)
        return m


if __name__=="__main__" :
    m = Morceau("../../../multimedia/MIDIFILES/linkin_park-blackout.mid")
    m.addIgnoredPiste(10)
    m.parseOutput()
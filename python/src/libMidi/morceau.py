import sys
sys.path.append("midi")
from MidiInFile import MidiInFile

from outputMidi import OutputMidi

class Morceau :
    DST             = 50 # Distance (en mm) correspondant a 1s de musique
    taillePoincon   = 3.5 # Escpacement (en mm) entre deux poincons
    def __init__(self, nomFichier=None) :
        self._ignoredPistes = []
        self._DST           = Morceau.DST
        self._taillePoincon = Morceau.taillePoincon

        if not nomFichier is None :
            self._nomFichier = nomFichier
            self.parseNomFichier()
        else :
            self._output = OutputMidi()

    def parseNomFichier(self) :
        self._output = OutputMidi()
        self._in = MidiInFile(self._output, self._nomFichier)
        self._in.read()

    def addIgnoredPiste(self, id_) :
        if not id_ in self._ignoredPistes and id_ in self._output._tracks.keys() :
            self._ignoredPistes.append(id_)

        else :
            raise Exception("La piste a ignorer n'est pas dans les cles des pistes du morceau")

    def getNotesBetween(self, time0=None, time1=None) :
        """
        Retourne un ensemble de notes compris entre time0 et time1
        Mettre un des arguments a None revient a ne pas prendre en compte
        ce parametre.

        """
        return self._output.getNotesBetween(time0, time1)

    def getTimeLength(self) :
        """
        Retourne le temps total du morceau
        """
        notes = self.getNotesBetween()
        if notes == [] : return 1
        else : return max(map(lambda a: a.timeOut, notes))

    def getNoteAtPosition(self, numero_piste, temps, notesAffichees):
        """
        Retourne la note la plus proche d'une certaine position
        """
        return self._output.getNoteAtPosition(numero_piste, temps, notesAffichees)

    def ajouterNote(self, note) :
        """
        Ajoute une note
        """
        self._output.ajouterNote(note)

if __name__=="__main__" :
    m = Morceau("../../../multimedia/MIDIFILES/TEST1.mid")
    print(m.getNotesBetween(5, 10))
    m.parseOutput()

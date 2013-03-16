import note
from monf import MonfOneTrack

class Piste :
    def __init__(self) :
        self._channels = [[]]*16
        self._nom = ""

    def addNote(self, channel, note) :
        self._channels[channel].append(note)

    def getLastNote(self, channel, byteNote) :
        chan = self._channels[channel]
        for note in chan :
            if note.byte == byteNote :
                return note

    def setNom(self, nom) :
        self._nom = nom
    def getNom(self, nom) :
        return self._nom

    def check(self) :
        for chan in self._channels :
            for note in chan :
                if note.timeOut == 0 : return False
        else : return True

    def getHauteurNotes(self) :
        """
        Retourne un tableau contenant l'ensemble des différentes hauteur
        de note présentes
        """
        tab = []
        for c in self._channels :
            for note in c : # On parcourt chaque note
                if not note.number in tab : tab.append(note.number)
        return tab


    def getMonf(self, morceau) :
        """
        Retourne un objet MonfOneTrack a partir de self
        """
        m = MonfOneTrack(self._nom)
        for c in self._channels :
            for note in c : # On parcourt chaque note
                # On recupere l'instant le plus proche
                morceau._DST / morceau._taillePoincon
        print (self.getHauteurNotes())

        return m
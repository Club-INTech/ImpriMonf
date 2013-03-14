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
        
    def getMonf(self, morceau) :
        """
        Retourne un objet MonfOneTrack à partir de self
        """
        m = MonfOneTrack(self._nom)
        
        
        
        for c in self._channels :
            for note in c : # On parcourt chaque note
                
        return m
import note
from monf import MonfOneTrack

class Piste :
    def __init__(self) :
        self._channels = [[]]*16
        self._lastNotes = [[]]*16
        self._nom = ""

    def addNote(self, channel, noteInstance) :
        self._channels[channel].append(noteInstance)
        self._lastNotes[channel].append(noteInstance)

    def getLastNote(self, channel, byteNote) :
        chan, lastNotes = self._channels[channel], self._lastNotes[channel]
        for noteInstance in self._lastNotes[channel] :
            if noteInstance.byte == byteNote :
                self._lastNotes[channel].remove(noteInstance)
                return noteInstance

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
        Retourne un tableau contenant l'ensemble des differentes hauteur
        de note presentes
        """
        tab = []
        for c in self._channels :
            for note in c : # On parcourt chaque note
                if not note.number in tab : tab.append(note.number)
        return tab


    def getMonf(self, morceau) :
        """
        Retourne un objet MonfOneTrack a partir de self

        ATTENTION CETTE METHODE N'EST PAS INSTANTANNEE
        """
        m = MonfOneTrack(self._nom)
        for c in self._channels :
            for note in c : # On parcourt chaque note
                # On recupere l'instant le plus proche du dÃ©but de la note
                dureePoincon = float(morceau._taillePoincon / morceau._DST)
                idPoinconIn = int(note.timeIn // dureePoincon)
                idPoinconOut = int(note.timeOut // dureePoincon)

                if (not idPoinconOut == 0) :
                    for idPoincon in range(idPoinconIn, idPoinconOut) :
                        m.addPoincon(str(note), idPoincon*dureePoincon)
##                else :
##                    print(idPoinconIn, idPoinconOut)

        return m
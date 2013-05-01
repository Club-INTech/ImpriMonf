class MonfOneTrack :
    """
    Classe MonfOneTrack

    Contient les coups de poincon pour un instrument
    """
    def __init__(self, nom="") :
        # Dico de type : {NoteA#:[Temps_ou_il_y_a_des_poincons_pour_cette_note], noteA:[etc..], etc...}
        self._poincons = {}
        self._nom = nom

    # Ajout d'un coup de poincon
    def addPoincon(self, hauteurNote, temps) :
        if hauteurNote in self._poincons.keys() and not temps in self._poincons[hauteurNote]:
            self._poincons[hauteurNote].append(temps)
        else :
            self._poincons[hauteurNote] = [temps]

    # Remove un coup de poincon
    def removePoincon(self, hauteurNote, temps) :
        try : self._poincons[hauteurNote].remove(temps)
        except : pass


class Monf :
    """
    Classe Monf

    Contient les coups de poincons de tout un morceau
    """
    def __init__(self, nom="", morceau=None) :
        self._monfsOneTrack = []
        self._nom=nom

        if not morceau is None : self._morceau = morceau # Instance de Morceau
        else :
            import morceau
            self._morceau = morceau.Morceau()

        self.noteToPisteNumber = {"C3":1, "D3":2, "F3":3, "G3":4, "C4":5, "D4":6, "E4":7, "F4":8, "F#4":9, "G4":10, "A5":11, "A#4":12, "B4":13, "C5":14, "C#5":15, "D5":16, "D#5":17, "E5":18, "F5":19, "F#5":20, "G5":21, "G#5":22, "A5":23, "A#5":24, "B5":25, "C6":26, "D6":27}


    def addMonfOneTrack(self, m) :
        self._monfsOneTrack.append(m)

    def getAllPoincons(self) :
        """
        Retourne l'ensemble des poincons du morceau. Merge l'ensemble des poincons de toutes les tracks
        """
        poincons = {}
        for monfTrack in self._monfsOneTrack :
            for note in monfTrack._poincons.keys() :
                if not note in poincons.keys() :
                    poincons[note] = monfTrack._poincons[note]
                else :
                    poincons[note] += monfTrack._poincons[note]
        return poincons

    def getNombrePoincons(self, poincons=None):
        if poincons is None : poincons = self.getAllPoincons()
        a = 0
        for k in poincons.keys() :
            a += len(poincons[k])
        return a

    def getNumeroPisteOfNote(self, note) :
        """
        Retourne le numero de piste d'une note
        """
        return self.noteToPisteNumber[str(note)]

    def save(self, filename) :
        import pickle

        with open(filename, "wb") as file :
            pickle.dump(self, file)

    def checkForUnprintablePistes(self) :
        notes = self._morceau.getNotesBetween()
        cles = self.noteToPisteNumber.keys()
        notesQuiBugguent = []
        for note in notes:
            if str(note) not in cles :
                notesQuiBugguent.append(str(note))

        return notesQuiBugguent


def easyMonf() :
    """ Fonction de test. Retourne un Monf assez simple """
    monf = Monf("Test")
    monf1 = MonfOneTrack()
    monf2 = MonfOneTrack()
    monf1.addPoincon("A#", 0.1)
    monf1.addPoincon("A#", 0.12)
    monf1.addPoincon("B#", 0.15)
    monf2.addPoincon("A#", 0.2)
    monf2.addPoincon("C#", 0.2)
    monf2.addPoincon("C", 1)

    monf.addMonfOneTrack(monf1)
    monf.addMonfOneTrack(monf2)

    return monf

def openMonf(filename) :
    """
    Fonction a utiliser pour sauvegarder un monf.
    """
    with open(filename, "rb") as file :
        import pickle
        obj = pickle.load(file)
        if isinstance(obj,Monf) :
            print (obj._morceau)
            return obj

        else :
            raise Exception("Fichier .monf corronmpu")

if __name__=="__main__" :
    m = easyMonf()
    m.save("lolcat.monf")

    n = openMonf("lolcat.monf")





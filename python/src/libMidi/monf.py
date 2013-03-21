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

        self.noteToPisteNumber = {"A1":1, "A2":2, "A3":3, "A4":4, "A5":5, "A6":6, "A7":7, "A#1":8, "A#2":9, "A#3":10, "A#4":11, "A#5":12, "A#6":13, "A#7":14, "B1":15, "B2":16, "B3":17, "B4":18, "B5":19, "C1":20, "C2":21, "C3":22, "C4":23, "C5":24}


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

def easyMonf() :
    """ Fonction de test. Retourne un Monf assez simple """
    monf = Monf()
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

if __name__=="__main__" :
    m = easyMonf()
    print (m.getAllPoincons())
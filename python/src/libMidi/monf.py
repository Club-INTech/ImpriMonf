class MonfOneTrack :
    """
    Classe MonfOneTrack

    Contient les coups de poinçon pour un instrument
    """
    def __init__(self, nom="") :
        # Dico de type : {NoteA#:[Temps_où_il_y_a_des_poinçons_pour_cette_note], noteA:[etc..], etc...}
        self._poincons = {}
        self._nom = nom

    # Ajout d'un coup de poinÃ§on
    def addPoincon(self, hauteurNote, temps) :
        if hauteurNote in self._poincons.keys() :
            self._poincons[hauteurNote].append(temps)
        else :
            self._poincons[hauteurNote] = [temps]

    # Remove un coup de poinÃ§on
    def removePoincon(self, hauteurNote, temps) :
        try : self._poincons[hauteurNote].remove(temps)
        except : pass


class Monf :
    """
    Classe Monf

    Contient les coups de poinçons de tout un morceau
    """
    def __init__(self, nom="", morceau=None) :
        self._monfsOneTrack = []
        self._nom=nom
        self._morceau = morceau

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

    monf.addMonfOneTrack(monf1)
    monf.addMonfOneTrack(monf2)

    return monf

if __name__=="__main__" :
    m = easyMonf()
    print (m.getAllPoincons())
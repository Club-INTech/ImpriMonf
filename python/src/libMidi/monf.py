class MonfOneTrack :
    """
    Classe MonfOneTrack

    Contient les coups de poinÃƒÆ’Ã‚Â§on pour un instrument
    """
    def __init__(self, nom="") :
        # Dico de type : {NoteA#:[Temps_ou_il_y_a_des_poincons_pour_cette_note], noteA:[etc..], etc...}
        self._poincons = {}
        self._nom = nom

    # Ajout d'un coup de poincon
    def addPoincon(self, hauteurNote, temps) :
        if hauteurNote in self._poincons.keys() :
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

    Contient les coups de poinÃƒÆ’Ã‚Â§ons de tout un morceau
    """
    def __init__(self, nom="", morceau=None) :
        self._monfsOneTrack = []
        self._nom=nom

        if not morceau is None : self._morceau = morceau # Instance de Morceau
        else :
            import morceau
            self._morceau = morceau.Morceau()

        self.noteToPisteNumber = {"A#":1, "A":2, "B#":3, "C#":4, "C":5}


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
    monf2.addPoincon("C", 1)

    monf.addMonfOneTrack(monf1)
    monf.addMonfOneTrack(monf2)

    return monf

if __name__=="__main__" :
    m = easyMonf()
    print (m.getAllPoincons())
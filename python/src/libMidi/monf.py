class MonfOneTrack :
    """
    Classe MonfOneTrack
    
    Contient les coups de poinçon pour une piste    
    """
    def __init__(self, nom="") :
        # Dico de type : {NoteA#:[Temps_où_il_y_a_des_poinçons_pour_cette_note], noteA:[etc..], etc...}
        self._poincons = {}
        self._nom = nom
        
    # Ajout d'un coup de poinçon
    def addPoincon(self, hauteurNote, temps) :
        if hauteurNote in self._poincons.keys() :
            self._poincons[hauteurNote].append(temps)
        else :
            self._poincons[hauteurNote] = [temps]
    
    # Remove un coup de poinçon
    def removePoincon(self, hauteurNote, temps) :
        try : self._poincons[hauteurNote].remove(temps)
        except : pass
        
        
class Monf :
    def __init__(self, nom, morceau) :
        self._monfsOneTrack = []
        self._nom=nom
        self._morceau = morceau
        
    def addMonfOneTrack(self, m) :
        self._monfsOneTrack.append(m)
        
        
if __name__=="__main__" :
    m = Monf()
    m.addPoincon("A#", 0.1)
    m.addPoincon("A#", 0.12)
    m.addPoincon("A#", 0.15)
    m.removePoincon("A#", 0.11)
    
    print (m._poincons)
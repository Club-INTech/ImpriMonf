import note
from pathfinding import LinKernighan, Point

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

        self.noteToPisteNumber = note.Note.noteToPisteNumber


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

    def getTimeLength(self) :
        """
        Retourne le temps total du morceau
        """
        return self._morceau.getTimeLength()

    def rechercheChemin(self) :
        pointsPoincons = []
        x = 3.5
        print("entrée dans rechercheChemin")
        i=0
        for hauteurNote in self.getAllPoincons().keys() :	#On parcourt tous les coups de poinçon. #Attention : vérifier si les notes sont dans l'ordre : peu probable
            print("boucle "+str(i)+" "+hauteurNote)
            for temps in self.getAllPoincons()[hauteurNote] :
                y = temps * self._morceau._DST
                pointsPoincons.append(Point(x, y))
            x += 5.5
            i = i+1
        print("Recherche de chemin LinKernighan en cours ("+str(len(pointsPoincons))+" points)")
        pointsPoincons = LinKernighan(pointsPoincons)
        return pointsPoincons

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





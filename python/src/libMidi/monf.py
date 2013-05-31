import note
from pathfinding import LinKernighan, Point

class Monf :
    """
    Classe Monf

    Contient les coups de poincons de tout un morceau
    """
    def __init__(self, morceau=None) :

        self._poincons = {} #Tableau de type {NoteA#=[temps_où_y'a_des_coups_de_poincon]}
        if not morceau is None : self._morceau = morceau # Instance de Morceau
        else :
            import morceau
            self._morceau = morceau.Morceau()

        self.noteToPisteNumber = note.Note.noteToPisteNumber

    def conversion(self, communication=None) :
        """
        Rempli le tableau self._poincons à partir de self._morceau
        La partie communication à passer en paramètre sert à remplir une éventuelle barre de chargement
        """
        notesPassees = 0
        notes = self._morceau._output.getNotesBetween()
        for note in notes :
            dureePoincon = float(self._morceau._taillePoincon / self._morceau._DST)
            temps_courant = note.timeIn
            while temps_courant < note.timeOut:
                if temps_courant + dureePoincon < note.timeOut : self.addPoincon(str(note), temps_courant)
                else : self.addPoincon(str(note), note.timeOut)

                temps_courant += 0.9*dureePoincon

            # Barre de progression
            if not communication is None and notesPassees > 100:
                communication.ajouterNote.emit(notesPassees)
                notesPassees=0
            notesPassees += 1

        if not communication is None : communication.finir.emit()

    def addPoincon(self, hauteurNote, temps) :
        """
        Ajoute un poincon
        """
        if hauteurNote in self._poincons.keys() :
            self._poincons[hauteurNote].append(temps)
        else :
            self._poincons[hauteurNote] = [temps]

    def getAllPoincons(self) :
        """
        Retourne l'ensemble des poincons du morceau. Merge l'ensemble des poincons de toutes les tracks
        """
        return self._poincons

    def getNombrePoincons(self, poincons=None):
        if poincons is None : poincons = self.getAllPoincons()
        else : poincons = self._poincons
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
        i=0
        for hauteurNote in self.getAllPoincons().keys() :	#On parcourt tous les coups de poinçon. #Attention : vérifier si les notes sont dans l'ordre : peu probable
            x = 5.5*self.noteToPisteNumber[hauteurNote]
            for temps in self.getAllPoincons()[hauteurNote] :
                y = temps * self._morceau._DST
                pointsPoincons.append(Point(x, y))
            i = i+1
        linKernighan = LinKernighan(pointsPoincons)
        return linKernighan

    def morceau(self) :
        return self._morceau

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





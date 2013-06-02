import note
from pathfinding import LinKernighan, Point
from imprimante import Imprimante
import time

class Monf :
    """
    Classe Monf

    Contient les coups de poincons de tout un morceau
    """
    def __init__(self, morceau=None) :

        self.initPoincons() #Tableau de type {NoteA#=[temps_où_y'a_des_coups_de_poincon]}
        if not morceau is None : self._morceau = morceau # Instance de Morceau
        else :
            import morceau
            self._morceau = morceau.Morceau()

        self.noteToPisteNumber = note.Note.noteToPisteNumber

    def initPoincons(self) :
        self._poincons = {}

    def conversion(self, communication=None, notesAConvertir=None) :
        """
        Rempli le tableau self._poincons à partir de self._morceau
        La partie communication à passer en paramètre sert à remplir une éventuelle barre de chargement
        """
        self.initPoincons()
        if notesAConvertir is None : notes = self._morceau._output.getNotesBetween()
        else : notes = notesAConvertir


        if notes == [] : return

        if not communication is None : communication.addValue(1)
        # Merge notes
        newNotes = []
        notesPassees = 0
        for note in notes :
            if newNotes == [] : newNotes.append(note.copy())
            else :
                noteAjoutee = False
                for newNote in newNotes :
                    if str(note) == str(newNote) and note.timeIn <= newNote.timeOut and note.timeOut >= newNote.timeIn :
                        newNote.timeIn = min(newNote.timeIn, note.timeIn)
                        newNote.timeOut = max(newNote.timeOut, note.timeOut)
                        noteAjoutee = True
                        break
                if not noteAjoutee : newNotes.append(note.copy())

                notesPassees += 1
                if not communication is None and notesPassees > 20:
                    communication.addValue(notesPassees)
                    notesPassees = 0


        if not communication is None : communication.raz()

        notesPassees = 0
        for note in newNotes :
            dureePoincon = float(self._morceau._taillePoincon / self._morceau._DST)
            temps_courant = note.timeIn
            while temps_courant < note.timeOut:
                if temps_courant + dureePoincon < note.timeOut : self.addPoincon(str(note), temps_courant)
                else : self.addPoincon(str(note), note.timeOut)

                temps_courant += 0.9*dureePoincon

            # Barre de progression
            if not communication is None and notesPassees > 20:
                communication.addValue(notesPassees)
                notesPassees=0
            notesPassees += 1

    def addPoincon(self, hauteurNote, temps) :
        """
        Ajoute un poincon
        """
        if hauteurNote in self._poincons.keys() :
            self._poincons[hauteurNote].append(temps)
        else :
            self._poincons[hauteurNote] = [temps]

    def getAllPoincons(self, force=False) :
        """
        Retourne l'ensemble des poincons du morceau. Merge l'ensemble des poincons de toutes les tracks
        """
        if not hasattr(self, "_poinconsImpression") or force : self._poinconsImpression = dict(self._poincons)

        return self._poinconsImpression

    def getNombrePoincons(self, poincons=None):
        if poincons is None : poincons = self.getAllPoincons(force=True)
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

    def imprimer(self, imprimante, communication = None) :
        """
        Lance l'impression
        """
        linKernighan = self.rechercheChemin()
        nb_segments = linKernighan.getNbSegments()
        segments = []

        i=0
        id_segment = 0
        linKernighan.calculSegment(0)
        while id_segment < nb_segments :
            while not linKernighan.getLastSegmentPret() >= id_segment :
                time.sleep(0.1)
            segmentAImprimer = linKernighan.getDernierSegmentCalcule()
            if id_segment+1 < nb_segments and linKernighan.getLastSegmentPret() == id_segment: #Si ce n'est pas le dernier segment
                 thread = threading.Thread(None, linKernighan.calculSegment, None, (id_segment+1,))
                 thread.start()
            for point in segmentAImprimer :
                i+=1
                x=round(point.getX(), 2)
                y=round(point.getY(), 2)
                avancementImpression = i/self.getNombrePoincons()*100
                imprimante.poinconne(x, y)
##                time.sleep(1)
                if not communication is None :
                    communication.poinconFait()
            id_segment+=1
            imprimante.recalage_x()
        imprimante.fin_impression()

    def rechercheChemin(self) :
        pointsPoincons = []
        i=0
        for hauteurNote in self.getAllPoincons().keys() :	#On parcourt tous les coups de poinçon. #Attention : vérifier si les notes sont dans l'ordre : peu probable
            x = 5.5*self.noteToPisteNumber[hauteurNote]
            for temps in self.getAllPoincons()[hauteurNote] :
                y = temps * self._morceau._DST
                pointsPoincons.append(Point(x, y))
                print("points.append(Point("+str(x)+", "+str(y)+"))")
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





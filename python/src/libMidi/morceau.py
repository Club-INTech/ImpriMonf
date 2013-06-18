import sys
sys.path.append("midi")
from MidiInFile import MidiInFile
from MidiOutFile import MidiOutFile

from outputMidi import OutputMidi

class EventMidi :
    events = []
    def __init__(self, time, on, channel, byte) :
        self.time = time
        self.on = on
        self.channel = channel
        self.byte = byte
        EventMidi.events.append(self)

    def __str__(self) :
        return str(self.time) + " " + str(self.on) + " " + str(self.channel) + " " + str(self.byte)

    def trier() :
        EventMidi.events = sorted(EventMidi.events, key=lambda a : a.time)
    def purge() :
        EventMidi.events = []

class Morceau :
    DST             = 50 # Distance (en mm) correspondant a 1s de musique
    taillePoincon   = 3.5 # Escpacement (en mm) entre deux poincons
    def __init__(self, nomFichier=None) :
        self._ignoredPistes = []
        self._DST           = Morceau.DST
        self._taillePoincon = Morceau.taillePoincon

        if not nomFichier is None :
            self._nomFichier = nomFichier
            self.parseNomFichier()
        else :
            self._output = OutputMidi()

    def parseNomFichier(self) :
        self._output = OutputMidi()
        self._in = MidiInFile(self._output, self._nomFichier)
        self._in.read()

    def addIgnoredPiste(self, id_) :
        if not id_ in self._ignoredPistes and id_ in self._output._tracks.keys() :
            self._ignoredPistes.append(id_)

        else :
            raise Exception("La piste a ignorer n'est pas dans les cles des pistes du morceau")

    def getNotesBetween(self, time0=None, time1=None) :
        """
        Retourne un ensemble de notes compris entre time0 et time1
        Mettre un des arguments a None revient a ne pas prendre en compte
        ce parametre.

        """
        return self._output.getNotesBetween(time0, time1)

    def getTimeLength(self) :
        """
        Retourne le temps total du morceau
        """
        notes = self.getNotesBetween()
        if notes == [] : return 1
        else : return max(map(lambda a: a.timeOut, notes))

    def getNoteAtPosition(self, numero_piste, temps, notesAffichees):
        """
        Retourne la note la plus proche d'une certaine position
        """
        return self._output.getNoteAtPosition(numero_piste, temps, notesAffichees)

    def ajouterNote(self, note) :
        """
        Ajoute une note
        """
        self._output.ajouterNote(note)

    def exporter(self, nom_fichier, instrument, aplatir) :
        midi = MidiOutFile(nom_fichier)
        midi.header(0, self._output.nTracks, self._output.division)

        midi.start_of_track(0)
##        midi.sequence_name('Type 0')
        midi.tempo(self._output.tempovalue)
        midi.time_signature(self._output.nn, self._output.dd, self._output.cc, self._output.bb)

        for chan in range(1, 16) :
            midi.patch_change(chan, instrument)

        if not aplatir : allNotes = self._output.getNotesBetween()
        else : allNotes = self._output.mergeNotesBetween()

        # Sorting
        for note in allNotes :
            if not aplatir : channel = note.channel
            else : channel = 1
            
            EventMidi(self._output.human_timeToAbs_time(note.timeIn), True, channel, note.byte)
            EventMidi(self._output.human_timeToAbs_time(note.timeOut), False, channel, note.byte)

        EventMidi.trier()

        lastTime = 0
        for event in EventMidi.events :
##            print (event.time)
##            if event.time > lastTime :
##                lastTime = event.time
            midi.update_time(event.time,0)
##                print ("UPDATE")

            if event.on :
                midi.note_on(event.channel, event.byte, 0x40)
            else :
                midi.note_off(event.channel, event.byte, 0x40)

        EventMidi.purge()

        midi.end_of_track()

        midi.eof() # currently optional, should it do the write instead of write??
        midi.write()

if __name__=="__main__" :
    m = Morceau("../../../multimedia/MIDIFILES/TEST1.mid")
    print(m.getNotesBetween(5, 10))
    m.parseOutput()

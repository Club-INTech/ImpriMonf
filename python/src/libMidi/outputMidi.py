import sys
sys.path.append("midi")

from MidiOutStream import MidiOutStream
from MidiInFile import MidiInFile

from piste import Piste
from note import Note

class OutputMidi(MidiOutStream):
    def __init__(self) :
        self._tracks = {} #Dico type "id":Piste()

    def header(self, format=0, nTracks=1, division=96) :
        self.format = format
        self.nTracks = nTracks
        self.division = division

    def tempo(self, value) :
        self.tempovalue = value
        self._bpm = int (60000000./value)


    def start_of_track(self, track) :
        self.currentTrack = Piste()
        self._tracks[track]=self.currentTrack

    def sequence_name(self, texte) :
        self.currentTrack.setNom(texte)
    def end_of_track(self) :
        self.currentTrack = None

    def sysex_event(self, data) :
        pass

    def note_on(self, channel=0, note=0x40, velocity=0x40):
        if velocity == 0 :
            print ("Ca chie dans la colle pute")
        self.currentTrack.addNote(channel, Note(byte=note, timeIn=self.getCurrentTime()))
##        print ("ON - ", note, self.getCurrentTime(), self.abs_time(), "CHANNEL :", channel)

    def note_off(self, channel=0, note=0x40, velocity=0x40) :
        ancienneNote = self.currentTrack.getLastNote(channel, note)
        ancienneNote.setTimeOut(self.getCurrentTime())
##        print ("NOTE OFF - ", ancienneNote, self.getCurrentTime(), "CHANNEL :", channel)


    def getCurrentTime(self) :
        nombre_de_noires_depuis_debut = (self.abs_time()/self.division)
        temps_en_s_depuis_debut = nombre_de_noires_depuis_debut / self._bpm * 60
##        print ("TEMPS : ", temps_en_s_depuis_debut)
        return temps_en_s_depuis_debut

    def getNotesBetween(self, time0=None, time1=None) :
        notes = []
        for piste in self._tracks.keys() :
            for channel in self._tracks[piste]._channels :
                for note in channel :
                    if (time1 is None or note.timeIn <= time1) and (time0 is None or note.timeOut >= time0):
                        notes.append(note)
        return notes


if __name__ == "__main__" :
    event_handler = OutputMidi()

    in_file = '../../../multimedia/MIDIFILES/LP.mid'
    midi_in = MidiInFile(event_handler, in_file)
    midi_in.read()

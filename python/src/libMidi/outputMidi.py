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
        """
        Y'A DES PUTAIN DE BUGS DANS CETTE FONCTION WTFFFFFFFFFFF FDPPPPPPPPPPPPPPPPPPPPP
        """

        return self.abs_time()*self.division/float(self.tempovalue)

if __name__ == "__main__" :
    event_handler = OutputMidi()

    in_file = '../files/psy-gangnam_style.mid'
    midi_in = MidiInFile(event_handler, in_file)
    midi_in.read()
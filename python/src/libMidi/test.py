import sys
sys.path.append("midi")

from MidiOutStream import MidiOutStream
from MidiInFile import MidiInFile

class NoteOnPrinter(MidiOutStream):
    
    def header(self, format=0, nTracks=1, division=96) :
        self.format = format
        self.nTracks = nTracks
        self.division = division
    def tempo(self, value) :
        print(value)
        self.tempovalue = value
    def sequence_name(self, texte) :
        print(texte)
    def start_of_track(self, track) :
        print (track)
    def end_of_track(self) :
        print ("END")
        
    #def note_on(self, channel=0, note=0x40, velocity=0x40):
        #print ("ON", channel, note, velocity, self.abs_time()*self.division/float(self.tempovalue))
    #def note_off(self, channel=0, note=0x40, velocity=0x40) :
        #print ("OFF", channel, note, velocity, self.abs_time()*self.division/float(self.tempovalue))

event_handler = NoteOnPrinter()

in_file = 'files/linkin_park-blackout.mid'
midi_in = MidiInFile(event_handler, in_file)
midi_in.read()
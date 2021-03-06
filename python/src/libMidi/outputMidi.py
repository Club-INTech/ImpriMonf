﻿import sys
sys.path.append("midi")

from MidiOutStream import MidiOutStream
from MidiInFile import MidiInFile

from piste import Piste
from modifNote import ModifNote

import morceau, monfEditor
import note as note_mod

class OutputMidi(MidiOutStream):
    colors = [[200,20,0],[20,0,200], [0,20,200], [200,0,20], [0,200,20], [20,200,0], [100,200,100], [200,100,100], [100,100,200], [10,10,100]]
    def __init__(self) :
        self._tracks = {0:Piste()} #Dico type "id":Piste()
        self.format = 0
        self.nTracks = 1
        self.division = 192
        self.tempovalue = 359281
        self.calculateTempo()
        
        self.mergedNotes = None
        self.remergeNotes = False

        self.nn = 4
        self.dd = 4
        self.cc = 24
        self.bb = 8

    def header(self, format=0, nTracks=1, division=192) :
        self.format = format
        self.nTracks = nTracks
        self.division = division

    def tempo(self, value) :
        self.tempovalue = value
        self.calculateTempo()

    def calculateTempo(self) :
        self._bpm = int (60000000./self.tempovalue)
        self.temps_dune_noire = 60./self._bpm

    def start_of_track(self, track) :
        self.currentTrack = Piste()
        self._tracks[track]=self.currentTrack
        self.currentTrack.setColor(OutputMidi.colors[len(self._tracks)%len(OutputMidi.colors)])

    def sequence_name(self, texte) :
        self.currentTrack.setNom(texte)
    def end_of_track(self) :
        self.currentTrack = None

    def sysex_event(self, data) :
        pass


    def note_on(self, channel=0, note=0x40, velocity=0x40):
        if note_mod.isOk(note) :
            noteAAjouter = note_mod.Note(byte=note, timeIn=self.getCurrentTime(), color=OutputMidi.colors[channel%len(OutputMidi.colors)])
            self.currentTrack.addNote(channel, noteAAjouter)


    def note_off(self, channel=0, note=0x40, velocity=0x40) :
        if note_mod.isOk(note) :
            ancienneNote = self.currentTrack.getLastNote(channel, note)
            ancienneNote.setTimeOut(self.getCurrentTime())
##            ancienneNote.setColor(*OutputMidi.colors[channel%len(OutputMidi.colors)])


    def abs_timeToHuman_time(self, abs_time) :
        nombre_de_noires_depuis_debut = (abs_time/self.division)
        temps_en_s_depuis_debut = nombre_de_noires_depuis_debut / self._bpm * 60
##        print ("TEMPS : ", temps_en_s_depuis_debut)
        return temps_en_s_depuis_debut

    def getCurrentTime(self) :
        return self.abs_timeToHuman_time(self.abs_time())

    def human_timeToAbs_time(self, human_time) :
        return int(self.division*human_time*self._bpm/60)

    def time_signature(self,  nn, dd, cc, bb) :
        """
        nn: Numerator of the signature as notated on sheet music
        dd: Denominator of the signature as notated on sheet music
            The denominator is a negative power of 2: 2 = quarter
            note, 3 = eighth, etc.
        cc: The number of MIDI clocks in a metronome click
        bb: The number of notated 32nd notes in a MIDI quarter note
            (24 MIDI clocks)
        """
        self.nn = nn
        self.dd = dd
        self.cc = cc
        self.bb = bb


    def getNotesBetween(self, time0=None, time1=None) :
        notes = []
        for piste in self._tracks.keys() :
            for channel in self._tracks[piste]._channels :
                for note in channel :
                    if (time1 is None or note.timeIn <= time1) and (time0 is None or note.timeOut >= time0):
                        notes.append(note)
        notes_ok = []
        for note in notes :
            if not note in notes_ok :
                notes_ok.append(note)

        return notes_ok
        
    def remergeNotesAction(self, communication=None) :
        """
        Crée de nouvelles notes mergées sur la base des anciennes
        """
        newNotes = []
        notesPassees = 0
        notes = self.getNotesBetween()
        
        print ("Remerge")
        self.remergeNotes = False
        
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
                    
        self.mergedNotes = newNotes
        
    def mergeNotesBetween(self, time0=None, time1=None, communication=None, notes=None) :
        """
        Crée de nouvelles notes mergées sur la base des anciennes
        """
        if self.mergedNotes is None or self.remergeNotes:
            self.remergeNotesAction(communication)
            
        notes = []
        for note in self.mergedNotes :
            if (time1 is None or note.timeIn <= time1) and (time0 is None or note.timeOut >= time0):
                notes.append(note)
                
        return notes

    def getNoteAtPosition(self, numero_piste, temps, notesAffichees) :
        lastTimeOut=0
        modif = None
        for note in notesAffichees :
            try :
                if note_mod.Note.noteToPisteNumber[str(note)] == numero_piste :
                    """ Ici, on n'a que les notes de la ligne du curseur"""
                    pixelLimite = 2
                    pixelLimite/monfEditor.MonfEditor.DST

                    contains = note.containsTime(temps, pixelLimite/monfEditor.MonfEditor.DST)
                    if contains != "OUTSIDE" :
                        modif =  ModifNote(note, contains)

            except KeyError :
                pass
        return modif

    def ajouterNote(self, note) :
        self._tracks[0].addNote(1, note)

    def enleverNote(self, note) :
        for piste in self._tracks.keys() :
            for channel in self._tracks[piste]._channels :
                if note in channel:
                   channel.remove(note)
            

if __name__ == "__main__" :
    event_handler = OutputMidi()

    in_file = '../../../multimedia/MIDIFILES/LP.mid'
    midi_in = MidiInFile(event_handler, in_file)
    midi_in.read()

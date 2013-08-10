import pygame.midi
from PyQt4 import QtCore, QtGui
import time

import monfEditor
    
class ThreadPlayer(QtCore.QThread) :
    def __init__(self, endMethod) :
        QtCore.QThread.__init__(self)
        self.morceau = None
        self.endMethod = endMethod
        
        self.connect(self, QtCore.SIGNAL("terminated()"), self.terminated)
        self.connect(self, QtCore.SIGNAL("finished()"), self.terminated)
        self.connect(self, QtCore.SIGNAL("refreshMonfToTime(float)"), self.refreshMonfToTime)
        
        
    def setTimeIn(self, timeIn) :
        self.timeIn = timeIn
    def setMorceau(self, morceau):
        self.morceau = morceau
        
    def refreshMonfToTimeThrower(self, time) :
        self.emit(QtCore.SIGNAL("refreshMonfToTime(float)"), time)
    def refreshMonfToTime(self, time) :
        monfEditor.MonfEditor.editor.setPlaybackTime(time)
        
    def stop(self) :
        if self.morceau is None : return
        self.morceau.stopPlayback()
        
    def run(self) :
        if self.morceau is None : return
        self.setPriority(QtCore.QThread.TimeCriticalPriority)
        self.morceau.play(self.timeIn, self.refreshMonfToTimeThrower)
        
    def terminated(self) :
        self.endMethod()
        QtCore.QThread.terminate(self)
        
    def finished(self) :
        self.terminated()
    
class Player :
    def init() :
        pygame.midi.init()
        Player.output = pygame.midi.Output(0)
        for chan in range(0,16) :
            Player.output.set_instrument(0x4B, chan)
        Player.thread = ThreadPlayer(Player.stop)
        Player.isPlaying = False
        
    def setAction(action) :
        Player.action = action
        
    def setInstrument(instrument) :
        for chan in range(0,16) :
            Player.output.set_instrument(instrument, chan)
            
    def play(morceau, timeIn) :
        Player.thread.setMorceau(morceau)
        Player.thread.setTimeIn(timeIn)
        Player.isPlaying = True
        Player.thread.start()
        
    def stop() :
        Player.thread.stop()
        Player.isPlaying = False
        Player.action.setIcon(QtGui.QIcon("icons/play.png"))
        
        
        
    

if __name__ == "__main__" :
    midi.init()
      
    print (midi.get_count())
    print (midi.get_default_output_id())
    output = midi.Output(0)
      
    output.set_instrument(0x4B,0)
    output.note_on( 64 ,127,1)
    time.sleep( 1 )
    output.note_off( 64 ,127,1) 
    
    time.sleep(1)
  

import pyaudio  
import wave 
import os
import numpy as np
#from scikits.audiolab import wavread
from pydub import AudioSegment

def Finalsong(directory):
    os.chdir(os.path.join(directory,"FinalSong"))
    infiles = []

    for root, dirs, files in os.walk(os.path.join(directory,"FinalSong")):  
        for filename in files:
            infiles.append(filename)
    print(infiles)    
    #infiles = ["sound_1.wav", "sound_2.wav"]
    sound_string = []#*(len(infiles)*2-1)
    combined_sounds=[]
    #cut
    ii=0
    time_overlap_old=0
    while ii in range(len(infiles)-1):       #ii is the sound file currently being analized
    
        
        file_ii = AudioSegment.from_wav(infiles[ii])
        time_overlap=len(file_ii)/2
        
        t1 = 0 * 1000 #Works in milliseconds
        t2 = len(file_ii) - time_overlap #############################
        half_1 = file_ii[0:t2]
        half_2 = file_ii[t2:-1]
    
        #half_1.export('half_1.wav', format="wav") #Exports to a wav file in the current path.
        #half_2.export('half_2.wav', format="wav")
    
        file_ii_1 = AudioSegment.from_wav(infiles[ii+1])
        #t1 = 0 * 1000 #Works in milliseconds
        t3 =  time_overlap #############################
        half_1_1 = file_ii_1[0:t3]
        half_2_1 = file_ii_1[t3:-1]
        
        
        overlap = half_2.overlay(half_1_1)

        #overlap.export("overlap_x.wav", format='wav')
        if ii==0:
            sound_string.append(half_1)
        
            sound_string.append(overlap)
        else:
            print(time_overlap_old)
            middle=file_ii[time_overlap_old:len(file_ii)-t3]
            sound_string.append(middle)
            sound_string.append(overlap)
        ii=ii+1
        if ii==len(infiles)-1:
       
            sound_string.append(half_2_1)
        time_overlap_old=time_overlap
       


#while jj in range(size
#sound1 = AudioSegment.from_wav("/path/to/file1.wav")
#sound2 = AudioSegment.from_wav("/path/to/file2.wav")

    combined_sounds = sum(sound_string)
    print(combined_sounds)
    combined_sounds.export(os.path.join(directory,"final.wav"), format="wav")

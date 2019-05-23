import pyaudio  
import wave 
import os
import numpy as np
#from scikits.audiolab import wavread
from pydub import AudioSegment

def Overlapsong(k):
    os.chdir("C:\\Users\\heito\\Desktop\\UCSB\\Spring 2019\\15C\\Music\\Separate_Sounds")
    infiles = []
    for root, dirs, files in os.walk(r"C:\Users\heito\Desktop\UCSB\Spring 2019\15C\Music\Separate_Sounds"):  
        for filename in files:
           infiles.append(filename)
        
    infiles = ['sound_1.wav', 'sound_2.wav', 'sound_3.wav']
    print(infiles)
    sound_string = []#*(len(infiles)*2-1)
    combined_sounds=[]
    #cut
    ii=0
    time_overlap=500
    file_1 = AudioSegment.from_wav(infiles[0])
    file_2 = AudioSegment.from_wav(infiles[1])
    file_3 = AudioSegment.from_wav(infiles[2])
    overlap_1 = file_1.overlay(file_2)
    overlap_2=overlap_1.overlay(file_3)
        

    overlap_2.export(r"C:\Users\heito\Desktop\UCSB\Spring 2019\15C\Music\FinalSong\overlap" +str(k)+".wav", format='wav')
    
     
#Overlapsong(0)
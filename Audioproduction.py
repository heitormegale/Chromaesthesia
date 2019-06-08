#import matplotlib.pyplot as plt
import numpy as np
import time
import threading
import pyaudio
from scipy.io import wavfile
#import FinalOverlap
import os
from pydub import AudioSegment
import wave

fs = 8000
p = pyaudio.PyAudio()

class Sound(threading.Thread):
    def __init__(self, f, stretch_factor, volume, j, directory):
        threading.Thread.__init__(self)
        self.f = f
        self.directory=directory
        self.stretch_factor = stretch_factor
        self.volume = volume
        self.fs = 8000
        self.j = j
        self.p = pyaudio.PyAudio()
        
    def karplus_strong_decay(self, wavetable, n_samples, stretch_factor):
        """Synthesizes a new waveform from an existing wavetable, modifies last sample by averaging.
        Uses a stretch_factor to control for decay."""
        samples = []
        current_sample = 0
        previous_value = 0
        print(stretch_factor)
        while len(samples) < n_samples:
            r = np.random.binomial(1, 1 - 1/stretch_factor)
            if r == 0:
                wavetable[current_sample] =  0.5 * (wavetable[current_sample] + previous_value)
            samples.append(wavetable[current_sample])
            previous_value = samples[-1]
            current_sample += 1
            current_sample = current_sample % wavetable.size
        return np.array(samples)
    
    def edit(self, wave):
        x = int(0.25*len(wave))
        print(x)
        wave_new = wave[0:x]
        return wave_new
    

    
    def run(self):
        wavetable_size1 = fs // int(self.f)
        #wavetable1 = sine(freq[0], fs, 0.2, 5)
        self.wavetable = (2 * np.random.randint(0, 2, wavetable_size1) - 1).astype(np.float)
        
        self.sample1 = self.karplus_strong_decay(self.wavetable, 2 * self.fs, self.stretch_factor)
    
        #self.sample1 = self.edit(self.sample1)
    
        self.sample1 = self.volume*self.sample1
        
        self.stream = self.p.open(format=pyaudio.paFloat32, channels=1, rate=self.fs, output =True,frames_per_buffer=1024)
        
        self.stream.write(self.sample1.astype(np.float32).tostring())
        
        self.stream.close()
        
        self.p.terminate()
        
        path1=os.path.join(self.directory,'Separate_Sounds')
        #wavfile.write(os.path.join(path1,"sound_" + str(self.j) + ".wav"), self.fs, self.sample1.astype('float32'))      
        #wavfile.write(r"C:\Users\heito\Desktop\UCSB\Spring 2019\15C\Music\Separate_Sounds\sound_" + str(self.j) + ".wav", self.fs, self.sample1.astype('float32'))      
       # self.sample1.export(r"C:\Users\heito\Desktop\UCSB\Spring 2019\15C\Music\Separate_Sounds\sound_" + str(self.j) + ".wav", format="wav")
        #f = wave.open(os.path.join(path1,"sound_" + str(self.j) + ".wav"),'w')
        #f.setparams((1, 2, 8000, wavetable_size1, "NONE", "Uncompressed"))
        #f.writeframesraw(self.sample1.astype('float32'))
        #f.close()
        wavfile.write(os.path.join(path1,"sound_" + str(self.j) + ".wav"),8000, self.sample1.astype('float32'))

#objs = []
#number_of_threads = 3
def sound(color1, color2, color3, k, directory):
    objs = [Sound(color1[0], color1[1], color1[2], 1, directory), Sound(color2[0], color2[1], color2[2], 2, directory), Sound(color3[0], color3[1], color3[2], 3, directory)]

    for i in range(len(objs)):
        objs[i].start()

    for i in range(len(objs)):
        objs[i].join()
        
    Overlapsong(k,directory)
    
def Overlapsong(k,directory):
    os.chdir(os.path.join(directory,'Separate_Sounds'))
    infiles = []
    for root, dirs, files in os.walk(os.path.join(directory,'Separate_Sounds')):  
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
        

    overlap_2.export(os.path.join(directory,'IndividualSounds\overlap000' +str(k)+'.wav'), format='wav')

def sound1(color1, color2, color3, i):
    exp1 = 36*color1[0]/360
    exp2 = 36*color2[0]/360
    exp3 = 36*color3[0]/360
    color1[0] = (2**(exp1/12))*440
    color2[0] = (2**(exp2/12))*440
    color3[0] = (2**(exp3/12))*440
    
    color1[1] = color1[1]*50+3
    color2[1] = color2[1]*50+3
    color3[1] = color3[1]*50+3
    
    color1[2] = color1[2]/5+0.2
    color2[2] = color2[2]/5+0.2
    color3[2] = color3[2]/5+0.2
        
    #volume = [color1[1]/10, color2[1]/10, color3[1]/10]
    #length = [color1[2]*20, color2[2]*20, color3[2]*20]

    sound(color1, color2, color3, i)
    return color1, color2, color3


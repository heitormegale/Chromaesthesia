import matplotlib.pyplot as plt
import numpy as np
import time
import threading
import pyaudio
from scipy.io import wavfile
import FinalOverlap


fs = 8000
p = pyaudio.PyAudio()

class Sound(threading.Thread):
    def __init__(self, f, stretch_factor, volume, j):
        threading.Thread.__init__(self)
        self.f = f
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
        
        self.stream = self.p.open(format=pyaudio.paFloat32, channels=1, rate=self.fs, output=True)
        
        self.stream.write(self.sample1.astype(np.float32).tostring())
        
        self.stream.close()
        
        self.p.terminate()
        
        wavfile.write(r"C:\Users\heito\Desktop\UCSB\Spring 2019\15C\Music\Separate_Sounds\sound_" + str(self.j) + ".wav", self.fs, self.sample1.astype('float32'))      
       # self.sample1.export(r"C:\Users\heito\Desktop\UCSB\Spring 2019\15C\Music\Separate_Sounds\sound_" + str(self.j) + ".wav", format="wav")
        
        
        print("Pyaudio terminated")
        

#objs = []
#number_of_threads = 3
def sound(color1, color2, color3, k):
    objs = [Sound(color1[0], color1[1], color1[2], 1), Sound(color2[0], color2[1], color2[2], 2), Sound(color3[0], color3[1], color3[2], 3)]

    for i in range(len(objs)):
        objs[i].start()

    for i in range(len(objs)):
        objs[i].join()
        
    FinalOverlap.Overlapsong(k)

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






color1 = [261.63, 10, 0.4]
color2 = [329.63, 10, 0.4]
color3 = [392, 10, 0.4]

color11 = [461.63, 10, 0.4]
color22 = [429.63, 10, 0.4]
color33 = [492, 10, 0.4]

#sound(color1, color2, color3, 0)
#sound(color11, color22, color33, 1)
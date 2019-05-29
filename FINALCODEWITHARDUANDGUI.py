import os
os.chdir(r'C:\Users\Switthaus\Documents\UCSB\PhysicsCS15\FinalFolder')
import sys 
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QMessageBox
import time
import numpy as np
import seaborn as sns
import webcolors
import cv2
import Image_algorithm as imalgo
import numpy as np
import matplotlib.pyplot as plt
import FINALAUDIO as rlrlsound
import time
import Audiofinal2 as adfin
import serial
import glob
import AudioFinalcompl4 as adfincmplx

#video = cv2.VideoCapture(0)
directory = r'C:\Users\Switthaus\Documents\UCSB\PhysicsCS15\FinalFolder\Music'

class Window(QWidget):
    def __init__(self, pressed, directory):
        super().__init__()
        self.pressed = pressed
        self.directory = directory
        MAlgo = QPushButton("Math Algorithm", self)
        MAlgo.move(150, 50)
        MExpo = QPushButton('Fitted Algorithm Expo', self)
        MExpo.move(150, 250)
        MLine = QPushButton('Fitted Algorithm Linear', self)
        MLine.move(150, 450)
        
        MAlgo.clicked.connect(self.clickedMAlgo)
        MExpo.clicked.connect(self.clickedMExpo)
        MLine.clicked.connect(self.clickedMLine)        
        

        
    def clickedMAlgo(self):
        Sound(1, self.directory)
        
    def clickedMExpo(self):
        Sound(2, self.directory)
          
    def clickedMLine(self):
        Sound(3, self.directory)

    
class Sound():
    def __init__(self, l, directory):
        self.l = l
        self.run(directory)
                                        
                                        
    def RGB_HSI(self, x):
        x = np.array(x)
        #print("color in RGB...")
        #print(x)
        x = x/255
        Cmax = max(x)
        Cmin = min(x)
        d = Cmax-Cmin
        if d == 0:
            H = 0
        if Cmax == x[0]:
            H = 60*((x[1]-x[2])/d % 6)
        if Cmax == x[1]:
            H = 60*((x[2]-x[0])/d % 6)
        if Cmax == x[2]:
            H = 60*((x[0]-x[1])/d % 6)

        if Cmax == 0:
            S = 0
        else:
            S = d/Cmax

        I = np.sum(x)/3
    
        return np.array([H, S, I])

    def sound(self, color1, color2, color3):
        f = [0, 0, 0]
        exp1 = 36*color1[0]/360
        exp2 = 36*color2[0]/360
        exp3 = 36*color3[0]/360
        f[0] = (2**(exp1/12))*220
        f[1] = (2**(exp2/12))*220
        f[2] = (2**(exp3/12))*220
    
    
        stretch = [0, 0, 0]
        stretch[0] = color1[1]*50+3
        stretch[1] = color2[1]*50+3
        stretch[2] = color3[1]*50+3
        
        volume = [0, 0, 0]
        volume[0] = color1[2]/5+0.2
        volume[1] = color2[2]/5+0.2
        volume[2] = color3[2]/5+0.2
            
        #volume = [color1[1]/10, color2[1]/10, color3[1]/10]
        #length = [color1[2]*20, color2[2]*20, color3[2]*20]
    
        return [f[0], stretch[0], volume[0]], [f[1], stretch[1], volume[1]], [f[2], stretch[2], volume[2]]
    
    def sound_tuned(color1, color2, color3):
        f = [0, 0, 0]
        f[0] = np.exp(3.298)*np.exp(0.001966*color1[0])
        f[1] = np.exp(3.298)*np.exp(0.001966*color2[0])
        f[2] = np.exp(3.298)*np.exp(0.001966*color3[0])
    
        stretch = [0, 0, 0]
        stretch[0] = color1[1]*50+3
        stretch[1] = color2[1]*50+3
        stretch[2] = color3[1]*50+3
    
        volume = [0, 0, 0]
        volume[0] = color1[2]/5+0.2
        volume[1] = color2[2]/5+0.2
        volume[2] = color3[2]/5+0.2
        
        #volume = [color1[1]/10, color2[1]/10, color3[1]/10]
        #length = [color1[2]*20, color2[2]*20, color3[2]*20]

    
        return [f[0], stretch[0], volume[0]], [f[1], stretch[1], volume[1]], [f[2], stretch[2], volume[2]]    
                
    def run(self, directory):
        connected= False
        ok =1
        ser=serial.Serial("COM3", 9600, timeout=1) #port arduino is connected to

        while not connected:
            serin=ser.read()
            connected = True
        self.video = cv2.VideoCapture(0)
        t_begin = time.perf_counter()

        Final_song=os.path.join(directory,'FinalSong')
        Final_folder=os.path.join(directory,'FinalFolder')
        #files = glob.glob(r"C:\Users\heito\Desktop\UCSB\Spring 2019\15C\Music\FinalSong\*")
        files = glob.glob(os.path.join(Final_song,"*"))
        for f in files:
            os.remove(f)


    
        start=input("Type 1 to start program:")
        start_1=float(start)
        if (start_1==1):
            ser.write(b'1') #tell arduino to start
    
        ser.write(b'0')
        #print(ser.read())
        #while ser.read()==1: #wating for arduino to signal second limit switch
        #   ser.read()

        #x = b'\x01'
        l = []    
        print(ser.read())  
        while ok==1:   
        
            ardu_input=ser.read()         
            if ardu_input.decode("ascii")=='2': #Arduino said second limit has been reached
        
                ser.write(b'0')
                k = 0
        
                while True:
                    print('hello there')
                    t_start = time.perf_counter()
                    check, frame = self.video.read()
                    height, width, channels = frame.shape
                    frame = frame[int(1/3*(height)):int(2/3*(height)), int(1/3*(width)):int(2/3*(width))]
    
                    cv2.imwrite(os.path.join(Final_folder,"image.jpg"), frame)
        
    
                    ser.write(b'1')
            
    
    
                    os.chdir(Final_folder)
    
    
                    b = imalgo.colorz('image.jpg')
        
                    x = np.split(b[1], 3)
                    t_start = time.perf_counter()
                    height, width, channels = frame.shape
    
                    color1 = x[0]
                    color2 = x[1]
                    color3 = x[2]
            


                    x = webcolors.rgb_to_hex(np.array(color1).astype(int))
                    y = webcolors.rgb_to_hex(np.array(color2).astype(int))
                    z = webcolors.rgb_to_hex(np.array(color3).astype(int))
                      
                    flatui = [x, y, z]
                    sns.palplot(sns.color_palette(flatui))
                    plt.show()
            
    
                    color1HSI = self.RGB_HSI(color1)
                    color2HSI = self.RGB_HSI(color2)
                    color3HSI = self.RGB_HSI(color3)
                    print(color1HSI)
                    print(color2HSI)
                    print(color3HSI)
            
                    l.append(np.array(color1HSI))
                    l.append(np.array(color2HSI))
                    l.append(np.array(color3HSI))
            
                    color1_edited, color2_edited, color3_edited = self.sound(color1HSI, color2HSI, color3HSI)
                    rlrlsound.sound(color1_edited, color2_edited, color3_edited, k, self.directory)
                    plt.close()
                    k = k+1
            
                    print(time.perf_counter()-t_start)
                    ardu_input=ser.read()
                    if ardu_input.decode("ascii")=='3': # we reached the end, so take one more pic, process, etc then program
                        print('sven is the best coder')
                        t_start = time.perf_counter()
                        check, frame = self.video.read()
                        height, width, channels = frame.shape
                        frame = frame[int(1/3*(height)):int(2/3*(height)), int(1/3*(width)):int(2/3*(width))]
    
                        #cv2.imwrite(r'C:\Users\heito\Desktop\UCSB\Spring 2019\15C\Music\FinalFolder\image.jpg', frame)
                        cv2.imwrite(os.path.join(Final_folder,"image.jpg"), frame)
    
   
    
                        #os.chdir(r"C:\Users\heito\Desktop\UCSB\Spring 2019\15C\Music\FinalFolder")
                        os.chdir(Final_folder)
    
                        b = imalgo.colorz('image.jpg')
        
                        x = np.split(b[1], 3)
                        t_start = time.perf_counter()
                        height, width, channels = frame.shape
        
                        color1 = x[0]
                        color2 = x[1]
                        color3 = x[2]


                        x = webcolors.rgb_to_hex(np.array(color1).astype(int))
                        y = webcolors.rgb_to_hex(np.array(color2).astype(int))
                        z = webcolors.rgb_to_hex(np.array(color3).astype(int))
                        
                        flatui = [x, y, z]
                        sns.palplot(sns.color_palette(flatui))
                        plt.show()
    
                        color1HSI = self.RGB_HSI(color1)
                        color2HSI = self.RGB_HSI(color2)
                        color3HSI = self.RGB_HSI(color3)
                        print(color1HSI)
                        print(color2HSI)
                        print(color3HSI)
                        color1_edit, color2_edit, color3_edit = self.sound(color1HSI, color2HSI, color3HSI)
                        rlrlsound.sound(color1_edit, color2_edit, color3_edit, k+1, directory)
                        plt.close()
                        print(time.perf_counter()-t_start)
                        
                        ser.write(b'4')
                        print('stop!')
                        break
                
                break
    
                
        ser.close()
        #adfin.Finalsong(directory)
        #adfincompl.sound(l)
if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    pressed = [0, 0, 0]
    w = Window(pressed, directory)
    w.resize(500, 500)
    w.show()
    sys.exit(app.exec())
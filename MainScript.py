import os
#os.chdir(r'C:\Users\Switthaus\Documents\UCSB\PhysicsCS15\FinalFolder')
import sys 
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QMessageBox, QColorDialog, QHBoxLayout
from PyQt5 import QtCore, QtGui
import time
import numpy as np
import seaborn as sns
import webcolors
import cv2
import ImageAlgorithm as imalgo
import numpy as np
import matplotlib.pyplot as plt
import FINALAUDIO as rlrlsound
import time
import Audiofinal as adfin
import serial
import glob
#import AudioFinalcompl as adfincmplx

#video = cv2.VideoCapture(0)
directory = r'C:\Users\heito\Desktop\UCSB\Spring 2019\15C\Music'

class Window(QWidget):
    def __init__(self, pressed, directory):
        super().__init__()
        self.pressed = pressed
        self.directory = directory
        self.color = QtCore.Qt.white
        self.rgb = [255, 0, 0]
        w = QWidget()
        
        MAlgo = QPushButton("Math Algorithm", self)
        #Algo.move(150, 50)
        MExpo = QPushButton('Fitted Algorithm Expo', self)
        #MExpo.move(150, 250)
        MLine = QPushButton('Fitted Algorithm Linear', self)
        #MLine.move(150, 450)
        ColorChoice = QPushButton("Set 0 color", self)
        
        vbox = QVBoxLayout()
        
        vbox.addWidget(MAlgo)
        vbox.addWidget(MExpo)
        vbox.addWidget(MLine)
        
        hbox = QHBoxLayout()
        
        hbox.addLayout(vbox)
        hbox.addWidget(ColorChoice)
        
        w.setLayout(hbox)
        
        MAlgo.clicked.connect(self.clickedMAlgo)
        MExpo.clicked.connect(self.clickedMExpo)
        MLine.clicked.connect(self.clickedMLine)
        ColorChoice.clicked.connect(self.color_picker)        
        
        w.show()
        sys.exit(app.exec())
        
    def clickedMAlgo(self):
        Sound(1, self.directory, self.rgb)
        
    def clickedMExpo(self):
        Sound(2, self.directory, self.rgb)
          
    def clickedMLine(self):
        Sound(3, self.directory, self.rgb)
        
    def color_picker(self):
        print(self.color)
        col = QColorDialog.getColor(self.color, self)
        
        if col.isValid():
            rgb = (col.red(), col.green(), col.blue())
            self.setStyleSheet("QWidget { background-color: rgb(%d,%d,%d) }" % rgb)
            self.rgb = rgb
            self.color = col

    
class Sound():
    def __init__(self, h, directory, rgb):
        self.h = h
        self.q = np.array(rgb)
        self.qHSV = self.RGB_HSV(self.q)
        self.run(directory)
                                        
                                        
    def RGB_HSV(self, x):
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

        V = Cmax
    
        return np.array([H, S, V])

    def sound(self, color):
    
        if (color[0]-self.qHSV[0]) < 0:
            color[0] = 360-color[0]+self.qHSV[0]
        else:    
            color[0] = color[0]-self.qHSV[0]
    
        exp1 = 36*color[0]/360
        f = (2**(exp1/12))*220
    
        if (color[1]-self.qHSV[1]) < 0:
            color[1] = 1-color[1]+self.qHSV[1]
        else:
            color[1]=color[1]-self.qHSV[1]
  
        stretch = color[1]*50+3

        if (color[2]-q[2]) < 0:
            color[2] = 1-color[2]+self.qHSV[2]
        else:
            color[2]=color[2]-self.qHSV[2]

        volume = color[2]/5+0.2
    
        return [f, stretch, volume]
    
    def sound_tuned(self, color1, color2, color3):
        if color1[2] >=0:
            if color1[1] <= 0.15:
                if color1[2] <= 0.85:
                    color1[0] = 220*np.exp(color1[0]/(12*360))
                    print(color1[0])
                else:
                    color1[0] = 880*np.exp(color1[0]/(12*360)) 
                    print(color1[0])
            else:
                if color1[2] <= 0.15:
                    color1[0] = 110*np.exp(color1[0]/(12*360))
                    print(color1[0])
                else:
                    if color1[2] <= 0.35:
                        color1[0] = 220*np.exp(color1[0]/(12*360))
                        print(color1[0])
                    else:
                        color1[0] = 440*np.exp(color1[0]/(12*360))
                        print(color1[0])  
        if color2[2] >=0:
            if color2[1] <= 0.15:
                if color2[2] <= 0.85:
                    color2[0] = 220*np.exp(color2[0]/(12*360))
                    print(color2[0])
                else:
                    color2[0] = 880*np.exp(color2[0]/(12*360))
                    print(color2[0]) 
            else:
                if color2[2] <= 0.15:
                    color2[0] = 110*np.exp(color2[0]/(12*360))
                    print(color2[0])
                else:
                    if color2[2] <= 0.35:
                        color2[0] = 220*np.exp(color2[0]/(12*360))
                        print(color2[0])
                    else:
                        color2[0] = 440*np.exp(color2[0]/(12*360))
                        print(color2[0])  
    
        if color3[2] >=0:
            if color3[1] <= 0.15:
                if color3[2] <= 0.85:
                    color3[0] = 220*np.exp(color3[0]/(12*360))
                    print(color3[0])
                else:
                    color3[0] = 880*np.exp(color3[0]/(12*360))
                    print(color3[0]) 
            else:
                if color3[2] <= 0.15:
                    color3[0] = 110*np.exp(color3[0]/(12*360))
                    print(color3[0])
                else:
                    if color3[2] <= 0.35:
                        color3[0] = 220*np.exp(color3[0]/(12*360))
                        print(color3[0])
                    else:
                        color3[0] = 440*np.exp(color3[0]/(12*360))
                        print(color3[0])  
        
        color1[1] = color1[1]*50+3
        color2[1] = color2[1]*50+3
        color3[1] = color3[1]*50+3
        

        color1[2] = color1[2]/5+0.2
        color2[2] = color2[2]/5+0.2
        color3[2] = color3[2]/5+0.2
        return color1, color2, color3    
                
    def run(self, directory):
        connected= False
        ok =1
        ser=serial.Serial("COM3", 9600, timeout=1) #port arduino is connected to

        while not connected:
            serin=ser.read()
            connected = True
        self.video = cv2.VideoCapture(1)
        t_begin = time.perf_counter()

        Final_song=os.path.join(directory,'IndividualSounds')
        Final_folder=os.path.join(directory,'ImageFolder')
        #files = glob.glob(r"C:\Users\heito\Desktop\UCSB\Spring 2019\15C\Music\FinalSong\*")
        files = glob.glob(os.path.join(Final_song,"*"))
        for f in files:
            os.remove(f)


    
        start=input("Type 1 to start program:")
        start_1=float(start)
        if (start_1==1):
            ser.write(b'5') #tell arduino to start
    
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
    
                    cv2.imwrite(os.path.join(Final_folder,"image" + str(k) + ".jpg"), frame)
        
    
                    ser.write(b'1')
            
    
    
                    os.chdir(Final_folder)
    
    
                    b = imalgo.RGBcolors('image' + str(k) + '.jpg')
                    
        
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
            
    
                    color1HSI = self.RGB_HSV(color1)
                    color2HSI = self.RGB_HSV(color2)
                    color3HSI = self.RGB_HSV(color3)
                    print(color1HSI)
                    print(color2HSI)
                    print(color3HSI)
            
                    l.append(np.array(color1HSI))
                    l.append(np.array(color2HSI))
                    l.append(np.array(color3HSI))
                    
                    if self.h == 1:
                        color1_edited = self.sound(color1HSI)
                        color2_edited = self.sound(color2HSI)
                        color3_edited = self.sound(color3HSI)
                        
                    if self.h == 2:
                        color1_edited, color2_edited, color3_edited = self.sound_tuned(color1HSI, color2HSI, color3HSI)
                        
                    rlrlsound.sound(color1_edited, color2_edited, color3_edited, k, directory)
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
    
                        b = imalgo.RGBcolors('image.jpg')
        
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
    
                        color1HSI = self.RGB_HSV(color1)
                        color2HSI = self.RGB_HSV(color2)
                        color3HSI = self.RGB_HSV(color3)
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
        adfin.Finalsong(directory)
        #adfincompl.sound(l)
if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    pressed = [0, 0, 0]
    w = Window(pressed, directory)
    #w.resize(500, 500)
    #w.show()
    #sys.exit(app.exec())
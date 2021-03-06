import os
#os.chdir(r'C:\Users\Switthaus\Documents\UCSB\PhysicsCS15\FinalFolder')
import sys 
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QMessageBox, QColorDialog, QHBoxLayout
from PyQt5 import QtCore, QtGui
import time
import numpy as np
import cv2
import ImageAlgorithm as imalgo
import numpy as np
import matplotlib.pyplot as plt
import Audioproduction as rlrlsound
import SawAlgorithm as rlrlsound1
import time
import Finalsongoutput as adfin
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
        
        MAlgo = QPushButton("Exponential Algorithm", self)
        #Algo.move(150, 50)
        MExpo = QPushButton('Exponential Algorithm with Thresholds', self)
        #MExpo.move(150, 250)
        MLine = QPushButton('Fitted Linear Algorithm', self)
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
            H = 60*((x[2]-x[0])/d + 2)
        if Cmax == x[2]:
            H = 60*((x[0]-x[1])/d + 4)

        if Cmax == 0:
            S = 0
        else:
            S = d/Cmax

        V = Cmax
    
        return np.array([H, S, V])

    def sound(self, color):
    
        #if (color[0]-self.qHSV[0]) < 0:
        #    color[0] = 360-color[0]+self.qHSV[0]
        #else:    
        #    color[0] = color[0]-self.qHSV[0]
        if color[0]>340:
            color[0]=0
            
        exp1 = 36*color[0]/360
        f = (2**(exp1/12))*196
    
        if (color[1]-self.qHSV[1]) < 0:
            color[1] = 1-color[1]+self.qHSV[1]
        else:
            color[1]=color[1]-self.qHSV[1]
  
        stretch = color[1]*20+3
        #print(stretch)

        if (color[2]-self.qHSV[2]) < 0:
            color[2] = 1-color[2]+self.qHSV[2]
        else:
            color[2]=color[2]-self.qHSV[2]

        volume = color[2]/5+0.2
    
        return [f, stretch, volume]
    

    def sound_tuned(self, color):
        #Hue 0
        if (color[0]-self.qHSV[0]) < 0:
            color[0] = 360-color[0]+self.qHSV[0]
        else:    
            color[0] = color[0]-self.qHSV[0] 
        if color[0]>340:
            color[0]=0
                  
        #Daniele Sound
        if color[2] >=0:
       
            if color[1] <= 0.15:
           
                if color[2] <= 0.85:
                    color[0] = 220*(2**(color[0]/360))
                    print(color[0])
                    
                else:
                    color[0] = 880*(2**(color[0]/360)) 
                    print(color[0])
               
            else:
           
                if color[2] <= 0.25:
                    color[0] = 110*(2**(color[0]/360))
                    print(color[0])
               
                else:
               
                    if color[2] <= 0.5:
                        color[0] = 220*(2**(color[0]/360))
                        print(color[0])
                   
                    else:
                        color[0] = 440*(2**(color[0]/360))
                        print(color[0]) 
                        
        #Stretch                  
        if (color[1]-self.qHSV[1]) < 0:
            color[1] = 1-color[1]+self.qHSV[1]
        else:
            color[1]=color[1]-self.qHSV[1]
  
        color[1] = color[1]*20+3

        #Volume
        if (color[2]-self.qHSV[2]) < 0:
            color[2] = 1-color[2]+self.qHSV[2]
        else:
            color[2]=color[2]-self.qHSV[2]

        color[2] = color[2]/5+0.2        

        return color    
    
    def sound_linear(self, color):
        if color[2] <= 0.25:
            color[0] = 0.307*color[0]+110
            print(color[0])
        else:
            if color[2] <= 0.5:
               color[0] = 0.603995*color[0]+220
               print(color[0])
            else:
                color[0] = 1.251*color[0]+440
                print(color[0])                    
        
                #Stretch                  
        if (color[1]-self.qHSV[1]) < 0:
            color[1] = 1-color[1]+self.qHSV[1]
        else:
            color[1]=color[1]-self.qHSV[1]
  
        color[1] = color[1]*20+3

        #Volume
        if (color[2]-self.qHSV[2]) < 0:
            color[2] = 1-color[2]+self.qHSV[2]
        else:
            color[2]=color[2]-self.qHSV[2]

        color[2] = color[2]/5+0.2        

        return color                      
                                                                    
                                                    
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
                    ardu_input=ser.read()
                    print(ardu_input)
                    t_start = time.perf_counter()
                    check, frame = self.video.read()
                    height, width, channels = frame.shape
                    frame = frame[int(1/8*(height)):int(7/8*(height)), int(1/5*(width)):int(4/5*(width))]
    
                    cv2.imwrite(os.path.join(Final_folder,"image" + str(k) + ".jpg"), frame)
        
    
                    ser.write(b'1')
            
    
    
                    os.chdir(Final_folder)
    
    
                    b = imalgo.RGBcolors('image' + str(k) + '.jpg')
                    
        
                    #x = np.split(b[1], 3)
                    t_start = time.perf_counter()
                    height, width, channels = frame.shape
    
                    color1 = b[0]
                    color2 = b[1]
                    color3 = b[2]
            
                    print(color1)
            
    
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
                        color1_edited = self.sound_tuned(color1HSI)
                        color2_edited = self.sound_tuned(color2HSI)
                        color3_edited = self.sound_tuned(color3HSI)
                    
                    if self.h == 3:
                        color1_edited = self.sound_tuned(color1HSI)
                        color2_edited = self.sound_tuned(color2HSI)
                        color3_edited = self.sound_tuned(color3HSI)   
                                
                    rlrlsound.sound(color1_edited, color2_edited, color3_edited, k+1, directory) ##################################
                    k = k+1
            
                    print(time.perf_counter()-t_start)
                    ardu_input=ser.read()
                    if ardu_input.decode("ascii")=='3': # we reached the end, so take one more pic, process, etc then program
                        print('sven is the best coder')
                       
                        
                        ser.write(b'4')
                        
                        print('stop!')
                        break
                
                break   
    
        time.sleep(10)        
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
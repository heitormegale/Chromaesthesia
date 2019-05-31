# Chromaesthesia
The creators are: Daniele Offidani, Heitor Megale and Sven Witthaus.


This is a python project where we convert colors from an image to a melody. Our objective was to simulate a type of synesthesia. Synesthesia is a sensorial condition where different senses activate each other, that is the perception of one sense leads to an involuntary perception of another sense. In our case we would be creating a reverse Chromaestesia.
Chromaestesia is a natural conditional where sounds produce the sensation of color.


On top of the programing we built a mechanical scanner that moves a camera to take multiple pictures of the image being analyzed. Each picture is transformed into three tones and the full image will sound like a music.


The code can be used independently of the scanner and it can analyze pictures in your computer or an image from your webcamera. However, in this case it would produce a individual sound since it analyzes one picture. You could modify the code to run throught multiple images and produce a song or analyze piece by piece a individual image.


Since the maping of sounds to color varies from person to person with Chrmaestesia, there is no clear pattern to follow and is thus open to artistic interpretation. is very unique and doesn't follow a pattern across the who has the condition, our task to reverse this process isn't dictated by any defined translation. Thus, we created multiple methods, each with its downsides and upsides, that we will describe later. Of course, anyone is encouraged to expand on these methods with innovative ideas that could improve the experience.

The following is an example of an image scanned in a grid of XxY and the sound output produced:

![DemoImage](demos/demo.jpg)  


![DemoAudio](demos/demosong1.mp3)  

# Necessary libraries and instalation

You will need several python lybraries and programs in order to execute our project.

Apart from the conventional libraries you will need the following:

* pydub

* pygame

* pyserial

* cv2

* scipy / numpy / Matplotlib

* pyaudio

* glob

In order to visualize the colors we have implemented a function, to try to visualize the most dominant colors promted. For this, one will need the libraries:

* seaborn

* webcolors

Another aspect of our code is the GUI, which, while still in a very primitive state requires installation of:

* PyQt5

Cv2 might be the trickest to install, however you can find instructions on their website https://pypi.org/project/opencv-python/ ,
while the others can be installed by running ``` pip install 'library' ``` on your python shell command prompt.

PyAudio is also, one of the libraries to be cautious of. Pyaudio is somewhat outdated, making the process of installing it tricky depending on what device you are using. Specificially, one should look into portaudio error files.

The program utilizes three folders in the directory of your choice to store the sounds that will be used during the composition.
To create this folders download the ``` Setup.py ``` script and alocate it to the directory you want he program to be ran and used.
On the script you will need to change the path to your directory's path as indicated below:

```pythonscript
#SetUp
import os
directory="C:\\Users\\heito\\Desktop\\UCSB\\Spring 2019\\15C\\Music" #<-- your directory
os.chdir(directory)
def createFolder(folder):
    try:
        if not os.path.exists(folder):
            os.makedirs(folder)
    except OSError:
        print('Error: Creating directory. ' + folder)
#createFolder('.\\test\\')

createFolder('\\FinalSong\\')
createFolder('\\FinalFolder\\')
createFolder('\\Separate_Sounds\\')
```

Once the setup is ran you will need to alocate all the following scripts to the same folder you allocated and ran ``` Setup.py ```.
 * all the codes
 
 What each script does is described in their own descriotions and will also be explained here.
 


















Our goal was to create a scanner that would transform an image to a song, based on its colors.
The approach we took was to develop a two axis system, powered by stepper motors that move a camera around the image. This enables us to scan images of diverse size, being only limited by the size of the box where the scanner is mounted and the chromium rods that hold the camera.
The movement of the camera is controled by an Arduino that is connected via a serial port to a Python code.
In this Python scirpt we signal the Arduino when a picture has been taken, analyze the colors in the picture, colect the 3 most dominant colors and transform each color to a specific sound. These 3 tones are then combined into a sound that is played.
After the hole image has been scaned a separe script combines all the tones captured by the camera and turns them into a melody.


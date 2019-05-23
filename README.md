# Chromaesthesia
This project was realized in a Physics class laboratory in the University of California Santa Barbara.
The creators are: Daniele Offidani, Heitor Megale and Sven Witthaus.
Our goal was to create a scanner that would transform a image to a song, based on its colors.
The approach we took was to develop a two axis system, powered by stepper motors that move a camera around the image. This enables us to scan images of diverse size, being only limited by the size of the box where the scanner is mounted and the chromium rods that hold the camera.
The movement of the camera is controled by an Arduino that is connected via serial to a Python code.
In this Python scirpt we signal the Arduino when a picture has been taken, analyze the colors in the picture, colect the 3 most dominant colors and transform each color to a specific sound. These 3 tones are then combined into a sound that is played.
After the hole image has been scaned a sebare script combines all the tones captured by the camera and combines them into a melody.


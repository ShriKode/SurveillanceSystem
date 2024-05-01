# Proximity Surveillance System
ECE 4180 Final Project Spring 2024 <br />
Project Members: Nihit Agarwal, Shriyanshu Kode, Nidhish Shanmugasundaram, Mark Jang


# Table of Contents
- [Overview](https://github.com/ShriKode/SurveillanceSystem/blob/main/README.md#overview)
- [Digrams](https://github.com/markjang03/ECE4180_finalP.github.io/blob/main/README.md#diagrams)

- [Parts List](https://github.com/markjang03/ECE4180_finalP.github.io/blob/main/README.md#partslist)
- [Instructions](https://github.com/markjang03/ECE4180_finalP.github.io/blob/main/README.md#overview)
- [Demo Video](https://github.com/markjang03/ECE4180_finalP.github.io/blob/main/README.md#overview)


# Overview
A security camera system that will use a Raspberry Pi 3 and an mbed to send video data to an online server when an object is within a certain distance of the system. A speaker will also sound an alarm when this occurs. We will use the sonar sensor to determine the proximity of the object/person to the system. Finally, we will use a capacitive sensor that when a specific code is entered, the system will be overridden to reset.


## Digrams
### Schematic Diagram
![](https://github.com/ShriKode/SurveillanceSystem/blob/main/images/Schematic_ece4180_2024-04-30.svg)
### Block Diagram
![](https://github.com/ShriKode/SurveillanceSystem/blob/main/images/1.jpeg)


# Parts List
- Mbed LPC1768: https://os.mbed.com/platforms/mbed-LPC1768/ <br />
![](https://os.mbed.com/media/cache/platforms/LPC1768.jpg.250x250_q85.jpg)
- Raspberry Pi 3: https://www.raspberrypi.com/products/raspberry-pi-3-model-b/ <br />
![](https://www.canakit.com/Media/700/1368.jpg)
- Raspberry Pi Camera Module 2: https://www.raspberrypi.com/products/camera-module-v2/ <br />
![](https://m.media-amazon.com/images/I/6169R+wUp8L.jpg)
- MPR121 I2C Capacitive Touch Sensor: https://os.mbed.com/users/4180_1/notebook/mpr121-i2c-capacitive-touch-sensor/ <br />
![](https://os.mbed.com/media/uploads/4180_1/touchpad.jpg)
- Speaker: https://os.mbed.com/users/4180_1/notebook/using-a-speaker-for-audio-output/ <br />
![](https://os.mbed.com/media/uploads/4180_1/pcbspeaker.jpg)
- 2N3904 NPN BJT <br />
![](https://cdn.sparkfun.com/assets/parts/2/9/9/00521-1.jpg)
- Pushbuttons x 3: https://os.mbed.com/users/4180_1/notebook/pushbuttons/ <br />
![](https://mm.digikey.com/Volume0/opasdata/d220001/medias/images/4220/MFG_TS02-Sm-BK-LCR.jpg)
- Ultrasonic Distance Sensor <br />
![](https://github.com/ShriKode/SurveillanceSystem/blob/main/images/sonar.jpeg)
 

# Setup
### Mbed and Components
- Setup all the components as shown in the schematic.

### Raspberry Pi
- OS Setup
   - Install 64-bit Legacy Bullseye Linux OS on Raspberry Pi-3 . <a href = "https://projects.raspberrypi.org/en/projects/noobs-install">Click here for information.</a>
- Setup Camera
   -  Attach the piCamera to the Raspberry Pi 3. <a href="https://www.dexterindustries.com/howto/installing-the-raspberry-pi-camera/">Click here for instructions.</a>
   - Run the following command to access configuration of pi
   ```console
   sudo raspi-config
   ```
   - Navigate to the I2C section and enable it.
- Installations
   - Install dlib, cv2, and face_recognition libraries with pip.
     '''console
      pip install dlib
      pip install cv2
      pip install face_recognition
      '''
  - Face Recognition setup inspired by: https://github.com/rithikachowta08/face-recognition-security


# Instructions
## How to start the project on Keil Studio
1. Download the zip file (make sure to extract them)
![](https://github.com/ShriKode/SurveillanceSystem/blob/main/images/keil3.jpeg)
2. Log into Keil Studio
![](https://github.com/ShriKode/SurveillanceSystem/blob/main/images/keil1.jpeg)
3. Drag and drop the file 
![](https://github.com/ShriKode/SurveillanceSystem/blob/main/images/keil2.jpeg)

## Writing software to run on the Pi

1. Start the Raspberry Pi 3. Create two python scripts with the code provided in the files face_recog.py and stream_server.py.
2. Upload an image of the person the system needs to recognize as a verified user to the Raspberry Pi  using the file transfer feature iin VNC viewer.
3. Follow the example code given in image_processing.py to process the image and store its encoding as pickled file.
4. Make changes to stream_server.py to load the pickled data containing encodings of the verified person's image.
5. A shortcut can be created on the iPhone to run the shell script on the pi. Go to the shortcuts app on iPhone and create a new shortcut. Inside it add an action of "Run script over SSH". Fill in the details of the pi's host, user and password. Type in the following in teh script region:

```console
cd Desktop
python3 stream_server.py
```
6. The code on the pi can be run remotely if it is switched on and the iPhone and the pi are on the same local network. Alternatively, a global IP can be obtained for the pi to have remote global access.

## Running the system
1. Once the Mbed and the pi are connected via USB serial, and the pi is run using the shortcut, the video streaming web page can be accessed. Go to the webpage \<IP address of pi>:8000 and you should be able to see the video feed.
2. Watch the demo video below for a more detailed undestanding of what the surveillance system is capable of doing.

# Demo Video

[![Youtube Video for Demo](https://img.youtube.com/vi/DDzpSAghQFE/0.jpg)](https://www.youtube.com/watch?v=DDzpSAghQFE)


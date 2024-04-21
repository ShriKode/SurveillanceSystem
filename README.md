# SurveillanceSystem
ECE 4180 Final Project Spring 2024 <br />
Project Members: Nihit Agarwal, Shriyanshu Kode, Nidhish Shanmugasundaram, Mark Jang



# Table of Contents
- [Overview](https://github.com/markjang03/ECE4180_finalP.github.io/blob/main/README.md#overview)
- [Digrams](https://github.com/markjang03/ECE4180_finalP.github.io/blob/main/README.md#overview)

- [Parts List](https://github.com/markjang03/ECE4180_finalP.github.io/blob/main/README.md#overview)
- [Instructions](https://github.com/markjang03/ECE4180_finalP.github.io/blob/main/README.md#overview)
- [Demo Video](https://github.com/markjang03/ECE4180_finalP.github.io/blob/main/README.md#overview)


# Overview
A security camera system that will use a Raspberry Pi (Zero W or 3) and an mbed to send video data to an online server when an object is within a certain distance of the system. A speaker will also sound an alarm when this occurs. We will use the lidar or sonar sensor to determine the proximity of the object/person to the system. We will utilize LCD display as a GUI to deliver the security access result to the user (Access Granted or Denied) and possibly other information as well. Finally, we will use a capacitive sensor that when a specific code is entered, the system will be overridden to reset.


## Digrams
### Schematic Diagram
 [schematic image]
### State Diagram
  [state diagram]


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
- LIDAR TOF Distance Sensor: https://www.adafruit.com/product/3317 <br />
![](https://cdn-shop.adafruit.com/970x728/3317-06.jpg)
 

# Setup
### Mbed and Components

### Raspberry Pi
- Setup Camera
- Installations
   - Install dlib, cv2, and face_recognition libraries with pip.
   - pip install dlib
   - pip install cv2
   - pip install face_recognition


# Instructions


# Demo Video



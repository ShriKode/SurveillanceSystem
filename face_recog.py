import face_recognition
import cv2
import sys, time
import os
import numpy as np

import io
import logging
import socketserver
from http import server
from threading import Condition, Lock
from PIL import Image

from picamera2 import Picamera2
from picamera2.encoders import JpegEncoder
from picamera2.outputs import FileOutput
import pickle


# This program processes frames from live video to detect faces and compares againts a list of known face encodings. 
# If the face is unrecognised, they are regarded as an intruder and an email is sent along with the frame attached by invoking a shell script.
# If the face is known, nothing is done.



"""
# Load a sample picture and learn how to recognize it.
harry_image = face_recognition.load_image_file("known/harry_potter.jpg")
harry_face_encoding = face_recognition.face_encodings(harry_image)[0]


# Load a second sample picture and learn how to recognize it.
rachana_image = face_recognition.load_image_file("known/rachana_chowta.jpg")
rachana_face_encoding = face_recognition.face_encodings(rachana_image)[0]


# Load a third sample picture and learn how to recognize it.
rithika_image = face_recognition.load_image_file("known/rithika_chowta.jpg")
rithika_face_encoding = face_recognition.face_encodings(rithika_image)[0]

shri_image = face_recognition.load_image_file("known/shriyanshu")
shri_face_encoding = face_recognition.face_encodings(shri_image)[0]

"""

with open("encodings", "rb") as f:
	face_encodings = pickle.load(f)
	rachana_face_encoding = face_encodings[0]
	rithika_face_encoding = face_encodings[1]
	shri_face_encoding = face_encodings[2]
	
print(shri_face_encoding)	

# Create arrays of known face encodings and their names
known_face_encodings = [
    rachana_face_encoding,
    rithika_face_encoding,
    shri_face_encoding,
    
]
known_face_names = [
    "Rachana",
    "Rithika",
    "Shri",
]

# Initialize some variables
face_locations = []
face_encodings = []
face_names = []
#process_this_frame = True



def id_frame(frame):
	valid = 0
	#global process_this_frame
	#print(known_face_names)
	#print(type(frame))
	frame = np.asarray(bytearray(frame), dtype="uint8")
	frame = cv2.imdecode(frame, cv2.IMREAD_COLOR)
	#cv2.imshow('initial frame', frame)
	small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
	# Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
	rgb_small_frame = np.ascontiguousarray(small_frame[:, :, ::-1])
	#print("Saving Image")
	im = Image.fromarray(rgb_small_frame)
	im.save("test_small.jpeg")
	

	# Only process every other frame of video to save time
	if True:
		
		# Find all the faces and face encodings in the current frame of video
		face_locations = face_recognition.face_locations(rgb_small_frame, model='hog')
		print("Faces: ", len(face_locations))
		print("rgb small frame type: ", type(rgb_small_frame))
		print("face locations type: ", type(face_locations))
		# Testing without face locations
		#face_encodings = face_recognition.face_encodings(rgb_small_frame)
		face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)
		face_names = []
		
		print("Checkpoint 1")

		for face_encoding in face_encodings:
			# See if the face is a match for the known faces
			matches = face_recognition.compare_faces(known_face_encodings, face_encoding, 0.55)
			distances = face_recognition.face_distance(known_face_encodings, face_encoding)
			print("Checkpoint 2")
			name = "Not Verified"

			valid = 0
			# If a match was found in known_face_encodings, use the one which had minimum face distance i.e. the closest match
			if True in matches:
				best_match_index = distances.argmin()
				name = known_face_names[best_match_index]
				valid = 1

			face_names.append(name)

	#process_this_frame = not process_this_frame

	print("Checkpoint 3")
	# Display the results
	for (top, right, bottom, left), name in zip(face_locations, face_names):
		# Scale back up face locations since the frame we detected in was scaled to 1/4 size
		top *= 4
		right *= 4
		bottom *= 4
		left *= 4

		# Draw a box around the face
		frame = cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

		# Draw a label with a name below the face
		frame = cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), 5)
		font = cv2.FONT_HERSHEY_DUPLEX
		frame = cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

	#print("End Type: ", type(frame))
	#im = Image.fromarray(frame)
	#im.save("test.jpeg")
	
	img_bytes = cv2.imencode('.jpg', frame)[1].tobytes()

	# You can now use the img_bytes object, for example, to save it as a file
	
	return img_bytes, valid













   


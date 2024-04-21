import face_recognition
import pickle 

# Load a second sample picture and learn how to recognize it.
rachana_image = face_recognition.load_image_file("known/rachana_chowta.jpg")
rachana_face_encoding = face_recognition.face_encodings(rachana_image)[0]

# Load a third sample picture and learn how to recognize it.
rithika_image = face_recognition.load_image_file("known/rithika_chowta.jpg")
rithika_face_encoding = face_recognition.face_encodings(rithika_image)[0]

shri_image = face_recognition.load_image_file("known/shriyanshu")
shri_face_encoding = face_recognition.face_encodings(shri_image)[0]
 
print(shri_face_encoding)
face_encodings = [rachana_face_encoding, rithika_face_encoding, shri_face_encoding]
with open('encodings', 'wb') as f:
	pickle.dump(face_encodings, f)
	
	




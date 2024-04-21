#!/usr/bin/python3

# Mostly copied from https://picamera.readthedocs.io/en/release-1.13/recipes2.html
# Run this script, then point a web browser at http:<this-ip-address>:8000
# Note: needs simplejpeg to be installed (pip3 install simplejpeg).

import face_recog
import io
import logging
import socketserver
from http import server
from threading import Condition, Lock

from picamera2 import Picamera2
from picamera2.encoders import JpegEncoder
from picamera2.outputs import FileOutput

import threading
from time import sleep
from PIL import Image



import serial
ser = serial.Serial('/dev/ttyACM0', baudrate=9600, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE)
process_this_frame = True
cameraLock = Lock()
closeBy = False
valid = 0

serialLock = Lock()

PAGE = """
<html>
<style>
.content {
  max-width: 500px;
  margin: auto;
}
</style>
<head>
<title>picamera2 MJPEG streaming demo</title>
</head>
<body>
<h1>Picamera2 MJPEG Streaming Demo</h1>
<img src="stream.mjpg" width="640" height="480" />
</body>
</html>
"""

with open('cameoff.jpg', "rb") as image_file:
    image_bytes = image_file.read()
cameraOffFrame = image_bytes


def stream():
    address = ('', 8000)
    server = StreamingServer(address, StreamingHandler)
    server.serve_forever()



class StreamingOutput(io.BufferedIOBase):
    def __init__(self):
        self.frame = None
        self.condition = Condition()

    def write(self, buf):
        with self.condition:
            self.frame = buf
            self.condition.notify_all()


class StreamingHandler(server.BaseHTTPRequestHandler):
    def do_GET(self):
        global process_this_frame
        global valid
        if self.path == '/':
            self.send_response(301)
            self.send_header('Location', '/index.html')
            self.end_headers()
        elif self.path == '/index.html':
            content = PAGE.encode('utf-8')
            self.send_response(200)
            self.send_header('Content-Type', 'text/html')
            self.send_header('Content-Length', len(content))
            self.end_headers()
            self.wfile.write(content)
        elif self.path == '/stream.mjpg':
            self.send_response(200)
            self.send_header('Age', 0)
            self.send_header('Cache-Control', 'no-cache, private')
            self.send_header('Pragma', 'no-cache')
            self.send_header('Content-Type', 'multipart/x-mixed-replace; boundary=FRAME')
            self.end_headers()
            try:
                while True:
                    with output.condition:
                        #print("Waiting for Frame")
                        output.condition.wait()
                        frame = output.frame
                        #print("Frame: ", type(frame))
                        cameraLock.acquire()
                        print("Frame")
                        if not closeBy:
                            frame = cameraOffFrame
                            #print("Null Frame", type(frame))
                    #print("Received frame")
                        else:
                            if process_this_frame:
                                frame, valid = face_recog.id_frame(frame)
                                #print("Before Stream Lock")
                                #serialLock.acquire()
                                #print("After Stream Lock")

                                #serialLock.release()

                            process_this_frame = not process_this_frame
                        cameraLock.release()
                        sleep(0.01)


                    self.wfile.write(b'--FRAME\r\n')
                    self.send_header('Content-Type', 'image/jpeg')
                    self.send_header('Content-Length', len(frame))
                    self.end_headers()

                    self.wfile.write(frame)
                    self.wfile.write(b'\r\n')

                    #break;

            except Exception as e:
                logging.warning(
                    'Removed streaming client %s: %s',
                    self.client_address, str(e))


        else:
            self.send_error(404)
            self.end_headers()


class StreamingServer(socketserver.ThreadingMixIn, server.HTTPServer):
    allow_reuse_address = True
    daemon_threads = True
picam2 = Picamera2()
try:
    picam2.configure(picam2.create_video_configuration(main={"size": (640, 480)}))
    output = StreamingOutput()

    picam2.start_recording(JpegEncoder(), FileOutput(output))
    t1 = threading.Thread(target=stream)
    t1.start()

    while (1):
        # print("Before Lock")
        serialLock.acquire()
        if ser.readable():
            data = ser.read()
            #print("Mbed: ", data)
            if data == b'1':
                #output = StreamingOutput()
                #picam2.start_recording(JpegEncoder(), FileOutput(output))
                cameraLock.acquire()
                print("Change")
                # print("Turn on Camera")
                closeBy = True
                cameraLock.release()
            else:
                #picam2.stop_recording()
                cameraLock.acquire()
                print("Change")
                # print("Turn off Camera")
                closeBy = False
                cameraLock.release()
        # print("Valid: ", valid)
        if (valid):
            ser.write(b'1')
        else:
            ser.write(b'0')
        # print(valid.to_bytes(1, 'big'))
        # ser.write(valid.to_bytes(1, 'big') )
        serialLock.release()




finally:
        picam2.stop_recording()
        t1.join()
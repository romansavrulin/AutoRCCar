"""
Reference:
PiCamera documentation
https://picamera.readthedocs.org/en/release-1.10/recipes2.html

"""

import io
import socket
import struct
import time
import cv2
import pickle


# create socket and bind host
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('127.0.0.1', 8000))
connection = client_socket.makefile('wb')

try:
    #with cv2.VideoCapture(0) as camera:
    camera = cv2.VideoCapture(0)
    #camera.resolution = (320, 240)      # pi camera resolution
    #camera.framerate = 10               # 10 frames/sec
    camera.set( cv2.CAP_PROP_FRAME_WIDTH, 320)
    camera.set( cv2.CAP_PROP_FRAME_HEIGHT, 240)
    time.sleep(2)                       # give 2 secs for camera to initilize
    start = time.time()
    stream = io.BytesIO()
    
    # send jpeg format video stream
    while(True):
        #foo in camera.capture_continuous(stream, 'jpeg', use_video_port = True):
        ret, frame = camera.read()
        img = cv2.imencode(".jpg", frame)
        stream.write(pickle.dumps(img, -1))
        print ("f: %d" % stream.tell())
        connection.write(struct.pack('<L', stream.tell()))
        connection.flush()
        stream.seek(0)
        connection.write(stream.read())
        if time.time() - start > 600:
            break
        stream.seek(0)
        stream.truncate()
    connection.write(struct.pack('<L', 0))
finally:
    connection.close()
    client_socket.close()

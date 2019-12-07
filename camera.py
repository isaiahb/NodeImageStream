import cv2
import numpy as np
# import matplotlib.pyplot as plt
import os
import sys
import select
import time
import socketio
from dotenv import load_dotenv
import base64

load_dotenv()
id = ""
try:
    id = sys.argv[1]
except:
    print("no argument passed")

print(id)

sio = socketio.Client()
# port = os.getenv("PORT") if os.getenv("PORT") else ""
port = os.getenv("PORT") or 3000
# sio.connect('http://localhost:' + str(port))
sio.connect("http://image-stream.herokuapp.com/")


def emit(data):
    # print(data)
    sio.emit('stream', data)


@sio.on('python'+id)
def message(data):
    print("received message")
    print(data)


cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 300)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 300)

while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()
    image = cv2.imencode(".jpg", frame)[1]  # .tostring()
    jpg_as_text = base64.b64encode(image)
    emit(jpg_as_text)
    # time.sleep(1/20)
    # listen for terminal input then stop streaming
    i, o, e = select.select([sys.stdin], [], [], 0.0001)
    if i == [sys.stdin]:
        break


# When everything done, release the capture
cap.release()
sio.disconnect()

print("streaming finished")

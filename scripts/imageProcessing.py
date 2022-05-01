import numpy as np
import cv2
import requests

# Constants
contrast = 30
brightness = 0
bt = bytes()
url = 'http://192.168.10.235/cam-hi.jpg'


def process_image():
    while True:
        frame = requests.get(url, stream=True)
        if (frame.status_code == 200): 
            global bt
            for chunk in frame.iter_content(chunk_size=1024):
                bt += chunk
                a = bt.find(b'\xff\xd8')
                b = bt.find(b'\xff\xd9')
                if a != -1 and b != -1:
                    jpg = bt[a:b+2]
                    bt = bt[b+2:]
                    frame = cv2.imdecode(np.frombuffer(jpg, dtype=np.uint8), cv2.IMREAD_COLOR)
                    frame = np.int16(frame)
                    frame = frame * (contrast/127+1) - contrast + brightness
                    frame = np.clip(frame,0,255)
                    frame = np.uint8(frame)

                    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
                    brown_lower = np.array([10,100,20],np.uint8)
                    brown_higher = np.array([20,255,200],np.uint8)

                    mask = cv2.inRange(hsv,brown_lower,brown_higher)
                    kernel = np.ones((5,5),"uint8")

                    brown_mask = cv2.dilate(mask,kernel)
                    contours,_ = cv2.findContours(brown_mask, cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
                    for _, contour in enumerate(contours):
                        area = cv2.contourArea(contour)
                        if (area > 200):
                            x,y,w,h = cv2.boundingRect(contour)
                            frame = cv2.rectangle(frame, (x,y), (x + w, y+h),(0,0,255),2)
                            cv2.putText(frame, "Dry",(x,y), cv2.FONT_HERSHEY_SIMPLEX,1.0, (0,0,0))
                    
                    _, buffer = cv2.imencode('.jpg',frame)
                    frame = buffer.tobytes()
                    yield(b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

def capture_frame():
    frameCount = 0
    while (frameCount < 10):
        frame = requests.get(url, stream=True)
        if (frame.status_code == 200): 
            global bt
            for chunk in frame.iter_content(chunk_size=1024):
                bt += chunk
                a = bt.find(b'\xff\xd8')
                b = bt.find(b'\xff\xd9')
                if a != -1 and b != -1:
                    jpg = bt[a:b+2]
                    bt = bt[b+2:]
                    frame = cv2.imdecode(np.frombuffer(jpg, dtype=np.uint8), cv2.IMREAD_COLOR)
                    frame = np.int16(frame)
                    frame = frame * (contrast/127+1) - contrast + brightness
                    frame = np.clip(frame,0,255)
                    frame = np.uint8(frame)
                    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
                    brown_lower = np.array([10,100,20],np.uint8)
                    brown_higher = np.array([20,255,200],np.uint8)

                    mask = cv2.inRange(hsv,brown_lower,brown_higher)
                    kernel = np.ones((5,5),"uint8")

                    brown_mask = cv2.dilate(mask,kernel)
                    contours,_ = cv2.findContours(brown_mask, cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
                    for _, contour in enumerate(contours):
                        area = cv2.contourArea(contour)
                        if (area > 200):
                            x,y,w,h = cv2.boundingRect(contour)
                            frame = cv2.rectangle(frame, (x,y), (x + w, y+h),(0,0,255),2)
                            cv2.putText(frame, "Dry",(x,y), cv2.FONT_HERSHEY_SIMPLEX,1.0, (0,0,0))
                    
                    cv2.imwrite('downloads/'+'frame'+str(frameCount)+'.png',frame)

        frameCount += 1

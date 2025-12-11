import cv2
import time
import requests
import os

if not os.path.exists("uploads"):
    os.makedirs("uploads")

def capture_image():
    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()

    if ret:
        filename = time.strftime("capture_%Y-%m-%d_%H-%M-%S.jpg")
        filepath = os.path.join("uploads", filename)
        cv2.imwrite(filepath, frame)
        cap.release()
        return filepath  

filename = capture_image()

if filename is None:
    print("Failed to capture image")
    exit()

url = "http://127.0.0.1:5000/api/upload"

files = {"image": open(filename, "rb")}
data = {"device_id": "Laptop-01"}

response = requests.post(url, data=data, files=files)
print(response.text)

import cv2
import time

def capture_image():
    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()

    if ret:
        filename = time.strftime("capture_%Y-%m-%d_%H-%M-%S.jpg")
        cv2.imwrite(filename, frame)
        cap.release()
        return filename  

    cap.release()
    return None

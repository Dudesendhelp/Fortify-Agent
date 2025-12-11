from image_cap import capture_image
import requests

filename=capture_image()

if filename is None:
    print("Failed to capture image")
    exit()

url = "http://127.0.0.1:5000/api/upload"

files = {"image": open(filename, "rb")}
data = {"device_id": "Laptop-01"}

response = requests.post(url, data=data, files=files)
print(response.text)
import cv2
from time import sleep
import requests
import io
import json
import os
import random

resim = "download.jpg"
img = cv2.imread(resim)
print("Picture is Detected")

# api = img

api = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
dim = (api.shape[1]*1, api.shape[0]*1)
api = cv2.resize(api, dim)
for i in range(api.shape[0]):
    for j in range(api.shape[1]):
        if (api[i][j] < 200):
            api[i][j] = 0
        else:
            api[i][j] = 255
       # // api[i][j] =(255-api[i][j]-10)
cv2.imshow("ok", api)

# Ocr
url_api = "https://api.ocr.space/parse/image"
_, compressedimage = cv2.imencode(".jpg", api, [1, 90])
file_bytes = io.BytesIO(compressedimage)

result = requests.post(url_api,
                       files={resim: file_bytes},
                       data={"apikey": "helloworld",
                             "language": "eng"})

result = result.content.decode()
print(result)
result = json.loads(result)

parsed_results = result.get("ParsedResults")[0]
text_detected = parsed_results.get("ParsedText")
print(text_detected)

print("Text is writing to file...")
f = open("text_detected.txt", "w+")
f.write(text_detected)
f.close()
print("Operation is successful")


cv2.imshow("roi", api)
cv2.imshow("Img", img)
cv2.waitKey(0)
# os.remove(resim)

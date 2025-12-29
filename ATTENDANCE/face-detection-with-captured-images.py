import pandas as pd
import cv2
import urllib.request
import numpy as np
import os
from datetime import datetime
import face_recognition

# Define paths
base_dir = 'D:\\project espcam\\ATTENDANCE'
attendance_file = os.path.join(base_dir, 'Attendance.csv')
image_folder = os.path.join(base_dir, 'image_folder')
captured_screenshots_folder = os.path.join(base_dir, 'captured_screenshots')

# Ensure the directories exist
os.makedirs(base_dir, exist_ok=True)
os.makedirs(captured_screenshots_folder, exist_ok=True)

# Initialize or clear the attendance CSV file
if os.path.exists(attendance_file):
    print("Attendance file exists. Removing it.")
    os.remove(attendance_file)

# Create a new empty DataFrame and save it to Attendance.csv
df = pd.DataFrame(columns=['Name', 'Time'])
df.to_csv(attendance_file, index=False)

# Load images and class names
images = []
classNames = []
try:
    myList = os.listdir(image_folder)
    print(f"Images found: {myList}")
    for cl in myList:
        curImg = cv2.imread(os.path.join(image_folder, cl))
        images.append(curImg)
        classNames.append(os.path.splitext(cl)[0])
    print(f"Class names: {classNames}")
except FileNotFoundError as e:
    print(f"Error: {e}")
    print("Ensure that the image folder path is correct.")
    exit()

def findEncodings(images):
    encodeList = []
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        try:
            encode = face_recognition.face_encodings(img)[0]
            encodeList.append(encode)
        except IndexError:
            print("No face found in the image.")
    return encodeList

def markAttendance(name):
    with open(attendance_file, 'r+') as f:
        myDataList = f.readlines()
        nameList = [line.split(',')[0] for line in myDataList]
        if name not in nameList:
            now = datetime.now()
            dtString = now.strftime('%H:%M:%S')
            f.writelines(f'\n{name},{dtString}')

def saveScreenshot(img, name):
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    screenshot_path = os.path.join(captured_screenshots_folder, f'{name}_{timestamp}.jpg')
    cv2.imwrite(screenshot_path, img)
    print(f"Screenshot saved to {screenshot_path}")

encodeListKnown = findEncodings(images)
print('Encoding Complete')

# URL to fetch the image from the ESP32 camera
url = 'http://192.168.54.31/cam-hi.jpg'

while True:
    try:
        img_resp = urllib.request.urlopen(url)
        imgnp = np.array(bytearray(img_resp.read()), dtype=np.uint8)
        img = cv2.imdecode(imgnp, -1)
    except Exception as e:
        print(f"Error fetching image from URL: {e}")
        break
    
    imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

    facesCurFrame = face_recognition.face_locations(imgS)
    encodesCurFrame = face_recognition.face_encodings(imgS, facesCurFrame)

    for encodeFace, faceLoc in zip(encodesCurFrame, facesCurFrame):
        matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
        faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)
        matchIndex = np.argmin(faceDis)

        if matches[matchIndex]:
            name = classNames[matchIndex].upper()
            y1, x2, y2, x1 = faceLoc
            y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4  # Scale back up the face location coordinates
            print(f"Detected face coordinates: ({y1}, {x2}, {y2}, {x1})")
            cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.rectangle(img, (x1, y2 - 35), (x2, y2), (0, 255, 0), cv2.FILLED)
            cv2.putText(img, name, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)
            markAttendance(name)
            saveScreenshot(img, name)

    cv2.imshow('Webcam', img)
    key = cv2.waitKey(5)
    if key == ord('q'):
        break

cv2.destroyAllWindows()

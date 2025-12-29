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
screenshot_folder = os.path.join(base_dir, 'screenshots')

# Ensure the ATTENDANCE and screenshots directories exist
os.makedirs(base_dir, exist_ok=True)
os.makedirs(screenshot_folder, exist_ok=True)

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
print(f"Loading images from: {image_folder}")
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

# Function to encode faces from the image folder
def findEncodings(images):
    encodeList = []
    for img in images:
        if img is not None:
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            try:
                encode = face_recognition.face_encodings(img)[0]
                encodeList.append(encode)
            except IndexError:
                print("No face found in one of the images. Skipping it.")
        else:
            print("Image could not be read. Skipping it.")
    return encodeList

# Function to mark attendance
def markAttendance(name):
    with open(attendance_file, 'r+') as f:
        myDataList = f.readlines()
        nameList = [line.split(',')[0] for line in myDataList]
        if name not in nameList:
            now = datetime.now()
            dtString = now.strftime('%H:%M:%S')
            f.writelines(f'\n{name},{dtString}')
            print(f"Attendance marked for: {name}")

# Function to save a screenshot
def saveScreenshot(img, name):
    now = datetime.now()
    dtString = now.strftime('%Y%m%d_%H%M%S')
    filename = f"{name}_{dtString}.jpg"
    filepath = os.path.join(screenshot_folder, filename)
    cv2.imwrite(filepath, img)
    print(f"Screenshot saved: {filename}")

# Encode faces from the image folder
encodeListKnown = findEncodings(images)
print(f"Encoding Complete. Found {len(encodeListKnown)} known encodings.")

# URL to fetch the image from the ESP32 camera
url = 'http://192.168.43.164/1024x768.jpg'  # Adjust URL for your ESP32-CAM setup

while True:
    try:
        # Fetch the image from the ESP32-CAM
        img_resp = urllib.request.urlopen(url)
        imgnp = np.array(bytearray(img_resp.read()), dtype=np.uint8)
        img = cv2.imdecode(imgnp, -1)
    except Exception as e:
        print(f"Error fetching image from URL: {e}")
        break

    # Scale down the frame for faster face recognition
    imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

    # Detect faces in the current frame
    facesCurFrame = face_recognition.face_locations(imgS)
    encodesCurFrame = face_recognition.face_encodings(imgS, facesCurFrame)
    print(f"Detected {len(facesCurFrame)} faces in the current frame.")

    for encodeFace, faceLoc in zip(encodesCurFrame, facesCurFrame):
        matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
        faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)
        matchIndex = np.argmin(faceDis)

        if matches[matchIndex] and faceDis[matchIndex] < 0.6:
            name = classNames[matchIndex].upper()
            print(f"Recognized: {name}")
            y1, x2, y2, x1 = faceLoc
            y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4  # Scale back up to original size
            cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.rectangle(img, (x1, y2 - 35), (x2, y2), (0, 255, 0), cv2.FILLED)
            cv2.putText(img, name, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)
            markAttendance(name)
            saveScreenshot(img, name)

    # Display the frame with recognized faces
    cv2.imshow('ESP32-CAM Attendance', img)

    # Break the loop on pressing 'q'
    key = cv2.waitKey(5)
    if key == ord('q'):
        print("Exiting...")
        break

# Cleanup
cv2.destroyAllWindows()

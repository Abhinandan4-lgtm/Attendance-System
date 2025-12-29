# Smart Attendance System using ESP32-CAM

## 📖 Overview
This project implements a smart attendance system using the ESP32-CAM module.
The system captures live video, detects registered faces, and automatically marks
attendance. Attendance records are stored in CSV format for easy access and review.
A web-based interface allows real-time monitoring through a local IP address.

---

## ⚙️ Features
- Real-time camera streaming using ESP32-CAM
- Face detection for automatic attendance
- CSV-based attendance logging
- Web interface for live monitoring
- Low-cost embedded system solution

---

## 🧰 Hardware Requirements
- ESP32-CAM module
- FTDI USB-to-Serial Converter
- Jumper wires
- 5V power supply

---

## 💻 Software Requirements
- Arduino IDE
- ESP32 board package
- Python 3.x
- OpenCV (basic usage)

---

## 🔧 System Working
1. ESP32-CAM captures live video.
2. Face detection identifies registered users.
3. Attendance is marked automatically.
4. Data is saved in CSV format.
5. User can monitor the system through a browser using a local IP address.

---

## 📁 Project Structure
    ```text
    ATTENDANCE/
    │
    ├── CameraWebServer/
    │ ├── CameraWebServer.ino # ESP32-CAM main firmware
    │ ├── app_httpd.cpp # HTTP streaming and server logic
    │ ├── camera_index.h # Web interface HTML
    │ ├── camera_pins.h # ESP32-CAM pin configuration
    │ ├── ci.json # Build / config file
    │ ├── partitions.csv # Flash memory partition table
    │
    ├── image_folder/
    │ └── (Captured images stored here)
    │
    ├── screenshots/
    │ └── (Project output screenshots)
    │
    ├── Attendance.xlsx # Attendance record file
    │
    ├── facedetection5thsem.py # Face detection & attendance logic
    │
    ├── face-detection-inbuilt-camera.py
    │ # Face detection using laptop camera


---

## 🎯 Project Objective

To design a **smart attendance system** that:
- Uses camera-based face detection
- Automatically marks attendance
- Stores attendance data digitally
- Minimizes manual intervention and errors

---

## 🔧 Hardware Requirements

- ESP32-CAM (AI Thinker module)
- FTDI USB to TTL Programmer
- USB Cable
- Stable Power Supply
- Laptop / PC

---

## 💻 Software Requirements

- Arduino IDE
- Python 3.x
- OpenCV
- NumPy
- Pandas
- Excel (for attendance record)

---

## ⚙️ Working Principle

1. ESP32-CAM runs a camera web server.
2. Live video or images are captured.
3. Python script processes frames for face detection.
4. Detected faces are matched.
5. Attendance is marked automatically in an Excel file.

---

## 🧠 Modules Description

### 🔹 ESP32-CAM Module
- Captures images or video stream.
- Hosts a local web server for camera access.

### 🔹 Face Detection Module
- Uses OpenCV Haar cascades.
- Works with ESP32-CAM feed or inbuilt laptop camera.

### 🔹 Attendance Management
- Stores name, date, and time.
- Saves data in an Excel sheet.

---

## 🧪 How to Run the Project

### Step 1: Upload ESP32-CAM Code
- Open `CameraWebServer.ino` in Arduino IDE.
- Select correct board and COM port.
- Upload the code.

### Step 2: Install Python Dependencies
    ```bash
    pip install -r requirements.txt

###Step 3: Run Face Detection Script
python facedetection5thsem.py
or (for laptop camera):
python face-detection-inbuilt-camera.py

###Step 4: Check Attendance
Open Attendance.xlsx to view records.




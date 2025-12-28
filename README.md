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
ESP32-CAM-Attendance-System/
│── esp32_cam_code/
│── python_face_detection/
│── attendance_logs/
│── screenshots/
│── README.md


---

## ▶️ How to Run
1. Install ESP32 board support in Arduino IDE.
2. Upload ESP32-CAM code using FTDI.
3. Run the Python face detection script.
4. Open the local IP address in a browser.
5. View live feed and attendance logs.

---

## 📸 Output
- Live camera feed on browser
- Face detection in real time
- Attendance saved in CSV files

---

## 🔐 Note
This project focuses on functional implementation.
Advanced security mechanisms are not included.

---

## 🔮 Future Improvements
- Cloud-based attendance storage
- Improved face recognition accuracy
- Mobile application integration





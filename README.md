

# Automated Attendance Monitoring System

This project uses Python and face detection methodology to automatically monitor student attendance in real-time. The system collects student images, detects faces, and records data (name, roll number, and timestamp) in an Excel sheet or other storage locations.

## Features

- Real-time face detection for attendance marking.
- Collects student images and detects faces.
- Stores attendance data with name, roll number, and timestamp.
- Excel sheet or CSV file for storing attendance records.
- Admin panel to view and manage attendance data (optional).

## Requirements

- Python 3.x
- OpenCV
- NumPy
- Pandas
- Dlib (or any other face detection library)
- Tkinter (for GUI, optional)
- XLWT or openpyxl (for Excel file handling)

- 2. Install required dependencies:

pip install -r requirements.txt

3. (Optional) Install OpenCV, if not already installed:

pip install opencv-python

4. (Optional) Install Dlib for face detection:

pip install dlib

Usage
1. Set up student profiles:
You need to register the students in the system. You can either upload student images or manually input the name, roll number, etc.

2. Start the attendance monitoring:
Run the following script to start monitoring:

Step1 : infocollection.py
Step2 : face_encoding_script.py
Step3 : attendance.py

step4(optional):attendance_gui.py - this will create a gui environment

Output
Attendance records will be stored in an Excel sheet (e.g., attendance.xlsx) with the following columns:

Name
Roll Number
Timestamp

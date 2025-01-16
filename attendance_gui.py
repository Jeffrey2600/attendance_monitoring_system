import face_recognition
import cv2
import pickle
import pandas as pd
from datetime import datetime
import openpyxl
import tkinter as tk
from tkinter import messagebox

class AttendanceApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Automated Attendance Monitoring System")
        self.root.geometry("400x200")

        # Default file paths
        self.encoding_file = "face_encodings.pkl"
        self.excel_file = "attendance.xlsx"

        # GUI Elements
        tk.Label(root, text="Automated Attendance Monitoring System", font=("Arial", 12, "bold")).pack(pady=10)
        tk.Button(root, text="Start Attendance", command=self.mark_attendance, bg="green", fg="white").pack(pady=10)
        tk.Button(root, text="Quit", command=root.quit, bg="red", fg="white").pack(pady=10)

    def mark_attendance(self, video_source=0):
        try:
            # Load face encodings
            with open(self.encoding_file, "rb") as f:
                known_faces = pickle.load(f)

            # Load or create Excel file
            try:
                # Load existing data into a DataFrame
                df = pd.read_excel(self.excel_file)
                print(f"Existing data loaded from {self.excel_file}")
            except FileNotFoundError:
                # Create a new DataFrame with headers if the file doesn't exist
                df = pd.DataFrame(columns=["Roll Number", "Name", "Timestamp", "Accuracy"])
                print(f"No existing data found. A new file will be created at {self.excel_file}")

            # Start video capture
            cap = cv2.VideoCapture(video_source)
            messagebox.showinfo("Instructions", "Press 'q' to quit the attendance system.")

            while True:
                ret, frame = cap.read()
                if not ret:
                    break

                rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                face_locations = face_recognition.face_locations(rgb_frame)
                face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

                for face_encoding, face_location in zip(face_encodings, face_locations):
                    for roll_no, data in known_faces.items():
                        matches = face_recognition.compare_faces([data["encoding"]], face_encoding, tolerance=0.5)

                        if any(matches):
                            name = data["name"]
                            distance = face_recognition.face_distance([data["encoding"]], face_encoding)[0]
                            accuracy = round((1 - distance) * 100, 2)

                            if accuracy >= 70:  # Accuracy threshold
                                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                                # Check if attendance has already been marked for the same day
                                is_duplicate = (
                                    (df["Roll Number"] == roll_no) &
                                    (df["Timestamp"].str.contains(timestamp[:10]))
                                ).any()

                                if not is_duplicate:
                                    # Append to the DataFrame
                                    new_row = {"Roll Number": roll_no, "Name": name, "Timestamp": timestamp, "Accuracy": accuracy}
                                    df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
                                    print(f"Attendance marked for {name} ({roll_no}) with accuracy {accuracy}%")

                                # Display rectangle and name with accuracy
                                top, right, bottom, left = face_location
                                cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
                                cv2.putText(frame, f"{name} ({accuracy}%)", (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
                            else:
                                print(f"Skipped {name} ({roll_no}) due to low accuracy: {accuracy}%")

                cv2.imshow("Face Detection", frame)

                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

            cap.release()
            cv2.destroyAllWindows()

            # Save the updated DataFrame back to the Excel file
            df.to_excel(self.excel_file, index=False)
            print(f"Attendance saved to {self.excel_file}.")
            messagebox.showinfo("Success", "Attendance process completed and saved.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

# Run the GUI application
if __name__ == "__main__":
    root = tk.Tk()
    app = AttendanceApp(root)
    root.mainloop()

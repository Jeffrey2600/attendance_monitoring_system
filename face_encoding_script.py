import face_recognition
import os
import pickle
import numpy as np

def encode_faces(image_directory="students", encoding_file="face_encodings.pkl"):
    encoded_faces = {}
    for student_dir in os.listdir(image_directory):
        student_path = os.path.join(image_directory, student_dir)
        if os.path.isdir(student_path):
            roll_number, student_name = student_dir.split("_")
            encodings = []

            for img_name in os.listdir(student_path):
                img_path = os.path.join(student_path, img_name)
                try:
                    image = face_recognition.load_image_file(img_path)
                    face_encoding = face_recognition.face_encodings(image)[0]
                    encodings.append(face_encoding)
                except IndexError:
                    print(f"Face not detected in {img_name}, skipping...")
                except Exception as e:
                    print(f"Error processing {img_name}: {e}")

            if encodings:
                average_encoding = np.mean(encodings, axis=0)
                encoded_faces[roll_number] = {
                    "name": student_name,
                    "encoding": average_encoding
                }
                print(f"Encoded {len(encodings)} images for {student_name} ({roll_number})")

    # Save encoded data
    with open(encoding_file, "wb") as f:
        pickle.dump(encoded_faces, f)
    print("Face data encoded and saved successfully.")

encode_faces()

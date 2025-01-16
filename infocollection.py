import cv2
import os
import time

def collect_images(student_name, roll_number, save_path="students"):
    # Create a directory for the student if it doesn't exist
    student_dir = os.path.join(save_path, f"{roll_number}_{student_name}")
    os.makedirs(student_dir, exist_ok=True)

    # Start video capture
    cap = cv2.VideoCapture(0)
    print("Press 'q' to quit.")
    count = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        cv2.imshow("Capture Images", frame)

        # Save image to student folder
        img_path = os.path.join(student_dir, f"{roll_number}_{count}.jpg")
        cv2.imwrite(img_path, frame)
        count += 1
        
        print(f"Captured image {count} for {student_name}")

        # Wait for the specified time before capturing the next image
        time.sleep(1)

        # Quit capturing on 'q' key press
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    print(f"Images saved for {student_name}.")

# Example usage:
collect_images("Jeffrey Benson s", "22uad005")

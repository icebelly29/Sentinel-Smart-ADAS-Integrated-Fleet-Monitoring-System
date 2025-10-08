import cv2
import dlib
import requests
import time
import numpy as np

# Load the pre-trained face detector and shape predictor
face_detector = dlib.get_frontal_face_detector()
eye_detector = dlib.shape_predictor('src/shape_predictor_68_face_landmarks.dat')

def eye_aspect_ratio(eye_points):
    # eye_points: list of 6 dlib points [p1..p6] for one eye
    p1 = np.array([eye_points[0].x, eye_points[0].y], dtype=np.float32)
    p2 = np.array([eye_points[1].x, eye_points[1].y], dtype=np.float32)
    p3 = np.array([eye_points[2].x, eye_points[2].y], dtype=np.float32)
    p4 = np.array([eye_points[3].x, eye_points[3].y], dtype=np.float32)
    p5 = np.array([eye_points[4].x, eye_points[4].y], dtype=np.float32)
    p6 = np.array([eye_points[5].x, eye_points[5].y], dtype=np.float32)
    # Standard EAR formula
    ear = (np.linalg.norm(p2 - p6) + np.linalg.norm(p3 - p5)) / (2.0 * np.linalg.norm(p1 - p4))
    return float(ear) if np.isfinite(ear) and ear > 0 else 0.0

# Function for playing an alarm sound
# def sound_alarm(path):
#     # Play an alarm sound (replace with your desired alarm sound path)
#     music = pyglet.resource.media('alarm.wav')
#     music.play()
#     pyglet.app.run()

# Define constants
EAR_THRESH = None  # Will be set after calibration
CONSECUTIVE_CLOSED_FRAMES_THRESHOLD = 15  # Frames required under threshold
# ALARM_SOUND_PATH = 'alarm.wav'  # Replace with your alarm sound path

# Initialize variables
eye_closed_count = 0
alarm_on = False
calibration_frames = 50
ear_samples = []
ear_min_threshold = 0.15
vehicle_id = "TRUCK_01"
BACKEND_URL = "http://127.0.0.1:5000/driver-monitoring"
last_post_time = 0
post_interval_seconds = 2
def post_status(is_drowsy):
    try:
        payload = {
            "vehicle_id": vehicle_id,
            "drowsy": bool(is_drowsy),
            "timestamp": int(time.time())
        }
        requests.post(BACKEND_URL, json=payload, timeout=3)
    except Exception:
        pass

# Start the video capture
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: Could not open video stream or file")
else:
    print("Camera successfully started")

while True:
    ret, frame = cap.read()

    if not ret:
        print("Error: Could not read frame from camera")
        break

    # Convert the frame to grayscale (needed for dlib face detection)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect faces
    faces = face_detector(gray)

    # Loop over each face detected
    for face in faces:
        # Draw a rectangle around the face
        x1, y1 = face.left(), face.top()
        x2, y2 = face.right(), face.bottom()
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

        # Detect facial landmarks
        landmarks = eye_detector(gray, face)

        # Get specific eye landmarks
        left_eye_landmarks = [landmarks.part(i) for i in range(36, 42)]
        right_eye_landmarks = [landmarks.part(i) for i in range(42, 48)]

        # Calculate EAR for each eye and average
        left_eye_ear = eye_aspect_ratio(left_eye_landmarks)
        right_eye_ear = eye_aspect_ratio(right_eye_landmarks)
        ear = (left_eye_ear + right_eye_ear) / 2.0

        # Calibrate EAR threshold over initial frames when user eyes are open
        if EAR_THRESH is None:
            if 0.15 <= ear <= 0.5:
                ear_samples.append(ear)
            if len(ear_samples) >= calibration_frames:
                baseline = float(np.median(ear_samples))
                # Set threshold at 75% of baseline, but not below a minimum
                threshold = max(ear_min_threshold, baseline * 0.75)
                globals()['EAR_THRESH'] = threshold
                print(f"Calibration complete. Baseline EAR={baseline:.3f}, Threshold={EAR_THRESH:.3f}")
        
        # Show EAR value on frame for debugging
        display_thresh = EAR_THRESH if EAR_THRESH is not None else 0.0
        cv2.putText(frame, f"EAR: {ear:.3f} (thr {display_thresh:.3f})", (10, 60),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 0), 2)

        # Skip drowsiness logic until calibrated
        if EAR_THRESH is None:
            continue

        # Check if either eye is closed (using average EAR)
        if ear < EAR_THRESH:
            eye_closed_count += 1
        else:
            eye_closed_count = 0  # Reset counter if eyes open

        # Check for consecutive closed frames
        if eye_closed_count >= CONSECUTIVE_CLOSED_FRAMES_THRESHOLD:
            print("Driver fatigue detected! Eyes closed for too long")
            now = int(time.time())
            if now - last_post_time >= post_interval_seconds:
                post_status(True)
                last_post_time = now
            # sound_alarm(ALARM_SOUND_PATH)
            # alarm_on = True

        # Draw an alarm on the frame if the alarm is on
        if alarm_on:
            cv2.putText(frame, "DROWSINESS ALERT!", (10, 30),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

        # If eyes are not closed consecutively, send normal status periodically
        if eye_closed_count == 0:
            now = int(time.time())
            if now - last_post_time >= post_interval_seconds:
                post_status(False)
                last_post_time = now

    # Display the frame with the face and landmark detection
    cv2.imshow("Driver Monitoring", frame)

    # Press 'q' to exit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the camera and close windows
cap.release()
cv2.destroyAllWindows()
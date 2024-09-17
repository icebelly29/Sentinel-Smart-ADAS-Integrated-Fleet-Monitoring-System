import cv2
import dlib

# Load the pre-trained face detector and shape predictor
face_detector = dlib.get_frontal_face_detector()
eye_detector = dlib.shape_predictor('shape_predictor_68_face_landmarks.dat')

# Function for eye aspect ratio calculation
def calculate_EAR(eye_landmarks):
    # Extract relevant landmarks
    left_eye_top = eye_landmarks[1].y
    left_eye_bottom = eye_landmarks[5].y
    left_eye_left = eye_landmarks[0].x
    left_eye_right = eye_landmarks[3].x

    # Calculate vertical and horizontal distances
    vertical_distance = abs(left_eye_bottom - left_eye_top)
    horizontal_distance = abs(left_eye_left - left_eye_right)

    # Calculate EAR
    EAR = vertical_distance / horizontal_distance
    return EAR

# Function for playing an alarm sound
# def sound_alarm(path):
#     # Play an alarm sound (replace with your desired alarm sound path)
#     music = pyglet.resource.media('alarm.wav')
#     music.play()
#     pyglet.app.run()

# Define constants
EAR_THRESH = 0.2  # Adjust threshold as needed
CONSECUTIVE_CLOSED_FRAMES_THRESHOLD = 3  # Adjust threshold as needed
# ALARM_SOUND_PATH = 'alarm.wav'  # Replace with your alarm sound path

# Initialize variables
eye_closed_count = 0
alarm_on = False

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

        # Get specific eye landmarks (adjust indices if needed)
        left_eye_landmarks = [landmarks.part(i) for i in range(36, 42)]
        right_eye_landmarks = [landmarks.part(i) for i in range(42, 48)]

        # Calculate EAR for each eye
        left_eye_ear = calculate_EAR(left_eye_landmarks)
        right_eye_ear = calculate_EAR(right_eye_landmarks)

        # Check if either eye is closed
        if left_eye_ear < EAR_THRESH or right_eye_ear < EAR_THRESH:
            eye_closed_count += 1
        else:
            eye_closed_count = 0  # Reset counter if both eyes open

        # Check for consecutive closed frames
        if eye_closed_count >= CONSECUTIVE_CLOSED_FRAMES_THRESHOLD:
            print("Driver fatigue detected! Eyes closed for too long")
            # sound_alarm(ALARM_SOUND_PATH)
            # alarm_on = True

        # Draw an alarm on the frame if the alarm is on
        if alarm_on:
            cv2.putText(frame, "DROWSINESS ALERT!", (10, 30),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

        # ... (Add code for other actions if needed)

    # Display the frame with the face and landmark detection
    cv2.imshow("Driver Monitoring", frame)

    # Press 'q' to exit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the camera and close windows
cap.release()
cv2.destroyAllWindows()
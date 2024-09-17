import cv2
import numpy as np

# Paths to them YOLO files
weights_path = "src/yolov3.weights"
config_path = "src/yolov3.cfg"
class_names_path = "src/coco.names"

# Load YOLO
net = cv2.dnn.readNet(weights_path, config_path)
layer_names = net.getLayerNames()

# Fix for indexing issues I had 
unconnected_layers = net.getUnconnectedOutLayers()

# Handle scalar or 2D array case for unconnected_layers
if isinstance(unconnected_layers, (list, np.ndarray)) and unconnected_layers.ndim == 2:
    output_layers = [layer_names[i[0] - 1] for i in unconnected_layers]
else:
    output_layers = [layer_names[i - 1] for i in unconnected_layers]

# Load class names from the file
with open(class_names_path, "r") as f:
    classes = [line.strip() for line in f.readlines()]

def count_passengers(frame):
    height, width, channels = frame.shape
    blob = cv2.dnn.blobFromImage(frame, 0.00392, (416, 416), (0, 0, 0), True, crop=False)
    net.setInput(blob)
    outs = net.forward(output_layers)

    class_ids = []
    confidences = []
    boxes = []

    for out in outs:
        for detection in out:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            if confidence > 0.5 and class_id == 0:  # Class ID 0 is 'person' in COCO dataset, I love github copilot
                center_x = int(detection[0] * width)
                center_y = int(detection[1] * height)
                w = int(detection[2] * width)
                h = int(detection[3] * height)
                x = int(center_x - w / 2)
                y = int(center_y - h / 2)
                boxes.append([x, y, w, h])
                confidences.append(float(confidence))
                class_ids.append(class_id)

    indices = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)

    all_detections = []
    
    # Check if any detections are found and draw bounding boxes
    if len(indices) > 0:
        # Ensure `indices` is iterable (it may be a scalar)
        for i in indices.flatten():
            box = boxes[i]
            x, y, w, h = box
            all_detections.append((x, y, w, h))
            cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
    else:
        print("No detections found.")
        
    return len(all_detections), frame

def monitor_video_for_overcrowding(video_path):
    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        print("Error: Could not open video file. Check codec support or file path.")
        return

    print("Video file opened successfully.")

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            print("End of video or error reading the video.")
            break

        passenger_count, frame_with_detections = count_passengers(frame)

        if passenger_count > 7:  # Assuming 7 is the maximum capacity for the bus
            issue_overcrowding_alert()
            print("Passenger count:", passenger_count) # Display the passenger count in the console for debugging

        # Display the frame with detections (bounding boxes)
        cv2.imshow('Bus Passenger Monitoring', frame_with_detections)

        # Break the loop on 'q' key press or end of video
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

def issue_overcrowding_alert():
    print("Alert: Bus is overcrowded!")

if __name__ == "__main__":
    # Use a .webm video of a crowded bus for testing
    video_path = 'src/crowded_bus.webm'
    monitor_video_for_overcrowding(video_path)

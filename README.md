# Sentinel: Smart ADAS-Integrated Fleet Monitoring System

**Sentinel** is an advanced fleet monitoring solution designed to improve the safety and management of buses and trucks. It integrates cutting-edge Advanced Driver Assistance Systems (ADAS) such as collision detection, driver monitoring, and adaptive cruise control with real-time fleet management capabilities, ensuring both safety and operational efficiency.

## Features

1. **Driver Monitoring**: 
   - Uses `dlib` and `OpenCV` to monitor driver attentiveness and behavior.
   - Detects signs of drowsiness or distraction, triggering warnings.

2. **Collision Detection**:
   - Real-time detection of potential collisions using LIDAR sensors.
   - Provides early warnings to avoid accidents.

3. **Passenger Overcrowding Detection**:
   - Utilizes YOLO object detection for real-time monitoring of passenger overcrowding in vehicles.
   - Ensures adherence to safety guidelines by preventing overcrowding.

4. **Fleet Tracking Simulation**:
   - GPS-based vehicle tracking system implemented using a Flask backend.
   - Provides real-time location data for fleet management.

5. **Adaptive Cruise Control with LIDAR**:
   - Enables adaptive speed regulation based on distance from other vehicles.
   - Ensures smooth and safe driving conditions.

6. **Web Dashboard for Fleet Management**:
   - Provides a comprehensive overview of vehicle locations, driver behavior, and passenger conditions.
   - Enables real-time decision-making and fleet oversight.

## System Architecture

```
Sentinel-Smart-ADAS-Integrated-Fleet-Monitoring-System
├── src
│   ├── coco.names
│   ├── crowded_bus.webm
│   ├── shape_predictor_68_face_landmarks.dat 
│   ├── yolov3.cfg
│   └── yolov3.weights                #Needs to be downloaded and placed here         
├── driver_monitoring.py          # Driver attentiveness system
├── collision_detection_lidar.py  # Collision detection using LIDAR
├── adaptive_cruise_control_lidar.py # Adaptive cruise control system
├── passenger_counting.py         # Passenger overcrowding detection
├── fleet_tracker_simulation.py   # Fleet tracking and simulation
├── app.py                        # Flask API for fleet tracking
├── index.html                    # React or plain HTML dashboard (based on use case)
├── README.md                         # Project documentation
├── main.py                           # Script to run all the Python scripts simultaneously
├── requirements.txt                  # Dependencies
└── .vscode                           # VS Code settings
```
## System Flow
1. **Driver Monitoring**: Uses the `driver_monitoring.py` script to ensure driver attentiveness through face tracking and blink detection.
2. **Collision Detection**: The `collision_detection.py` script continuously monitors the vehicle's surroundings using LIDAR sensors to prevent collisions.
3. **Adaptive Cruise Control**: The `adaptive_cruise_control_lidar.py` script dynamically adjusts the vehicle's speed based on LIDAR input.
4. **Passenger Counting**: The `passenger_counting.py` script monitors the vehicle’s interior to track overcrowding using YOLO detection models.
5. **Fleet Tracker Simulation**: The `fleet_tracker_simulation.py` script simulates real-time vehicle location and reports it to the Flask backend.
6. **Web Dashboard**: Fleet managers can access real-time data from all subsystems through the web dashboard (backend hosted in `app.py`).

## How to Run

### Setup

### Download YOLOv3 Weights
To use the YOLO model for passenger overcrowding detection, you need to download the pre-trained weights file `yolov3.weights`. This file is not included in the repository due to its size.

Follow these steps to download it:

1. Download the `yolov3.weights` file from the official YOLO website or using the following link:
   - [Download YOLOv3 Weights](https://pjreddie.com/media/files/yolov3.weights)

2. After downloading, place the `yolov3.weights` file in the `/src` directory


### Prerequisites
- Python 3.10+
- Flask for the backend
- OpenCV, Dlib, YOLO for computer vision tasks
- LIDAR simulation libraries

### Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/icebelly29/Sentinel-Smart-ADAS-Integrated-Fleet-Monitoring-System.git
    cd Sentinel-Smart-ADAS-Integrated-Fleet-Monitoring-System
    ```

2. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

### Running the System

1. **Run the Flask backend**:
    ```bash
    python backend/app.py
    ```

2. **Run the main system components simultaneously using the main script**:
    ```bash
    python main.py
    ```

3. **Access the web dashboard**:  
    Open a browser and navigate to `http://127.0.0.1:5000` to view fleet and driver data.

## Tech Stack
- **Python**: Core language used for ADAS, driver monitoring, and passenger counting.
- **Flask**: Backend framework to handle vehicle tracking and dashboard API.
- **OpenCV + Dlib**: For real-time computer vision in driver monitoring.
- **YOLO**: Used for passenger overcrowding detection.
- **LIDAR**: Simulated LIDAR data for collision detection and adaptive cruise control.
- **HTML + JavaScript**: Used for the web dashboard frontend.

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
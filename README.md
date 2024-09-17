# Sentinel - Smart Fleet Management and Safety System (SFMS)

## Overview

**Smart Fleet Management and Safety System (SFMS)** is an integrated platform designed to enhance the safety, efficiency, and comfort of buses and trucks. It incorporates several features like Advanced Driver Assistance Systems (ADAS), real-time fleet tracking, driver fatigue monitoring, passenger overcrowding detection, and road hazard mapping.

The system is modular, supporting driver safety with collision detection, blind-spot monitoring, and adaptive cruise control (ACC). It also provides fleet managers with a centralized dashboard for monitoring vehicle status, location, and driver behavior, and it includes a mobile app for passengers to track crowding and real-time updates.

---

## Key Features

- **Driver Monitoring (Fatigue and Distraction Detection)**: Uses computer vision to monitor the driver for signs of fatigue or distraction and issue real-time alerts.
- **Collision Detection**: Detects obstacles in the path of the vehicle using ultrasonic sensors and triggers automatic braking or driver alerts.
- **Adaptive Cruise Control (ACC)**: Adjusts vehicle speed based on the distance to the vehicle ahead using LiDAR or radar sensors.
- **Fleet Management**: Tracks vehicles in real-time using GPS, monitors driver behavior, and offers a centralized dashboard for fleet managers.
- **Passenger Overcrowding Detection**: Uses cameras or infrared sensors to monitor passenger numbers and detect overcrowding.
- **Seat Availability Information**: Mobile app for passengers to view seat availability in real-time.
- **Road Condition Detection**: Detects potholes and other road hazards, providing real-time alerts to the driver.

---

## Tech Stack

- **Backend**: Python (Flask/Django), Node.js (for REST API)
- **Frontend**: React.js (for web dashboard), React Native/Flutter (for mobile app)
- **Machine Learning/Computer Vision**: OpenCV, TensorFlow (for driver monitoring, road hazard detection)
- **Hardware**: Raspberry Pi (for sensor integration), Ultrasonic/LiDAR sensors, GPS modules
<!-- - **Database**: PostgreSQL, MongoDB (for storing fleet data)
- **Cloud**: AWS IoT, Google Cloud, or Azure (for real-time data processing)
- **Simulation**: CARLA/ MATLAB Simulink (for simulating vehicle dynamics and sensor data) -->

---

## System Architecture

```
SFMS_Project/
├── sensors/                                 # Contains modules for interacting with various sensors (LiDAR, Radar, Camera)
├── adas/                                    # Contains collision detection, adaptive cruise control logic
├── driver_monitoring/                       # Contains driver fatigue detection using OpenCV
├── fleet_management/                        # Contains GPS tracking and fleet analytics
├── passenger_management/                    # Contains seat availability, overcrowding detection
├── web_dashboard/                           # Frontend and backend code for the fleet management dashboard
├── requirements.txt                         # Python dependencies
├── README.md                                # Project overview and documentation
└── main.py                                   # Main script to run the system integration
```
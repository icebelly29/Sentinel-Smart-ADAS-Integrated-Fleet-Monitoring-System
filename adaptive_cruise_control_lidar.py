# adaptive_cruise_control_lidar.py (Windows-compatible version for testing)

import time
import platform
import random # Just for testing only on Windows
# Mock function for testing on Windows
def read_lidar_distance():
    if platform.system() == 'Windows':
        # Simulate distance in meters for testing purposes
        return random.randint(5, 100) # Example: 25 meters ahead
    else:
        # Actual I2C code to read from the LiDAR sensor
        import smbus2
        I2C_BUS = 1
        LIDAR_ADDRESS = 0x62
        LIDAR_COMMAND = 0x00
        LIDAR_DISTANCE = 0x8f
        bus = smbus2.SMBus(I2C_BUS)

        bus.write_byte_data(LIDAR_ADDRESS, LIDAR_COMMAND, 0x04)
        time.sleep(0.02)
        dist_high = bus.read_byte_data(LIDAR_ADDRESS, LIDAR_DISTANCE)
        dist_low = bus.read_byte_data(LIDAR_ADDRESS, LIDAR_DISTANCE + 1)
        distance = (dist_high << 8) + dist_low
        return distance / 100.0  # Convert distance to meters

class AdaptiveCruiseControl:
    def __init__(self):
        self.speed = 0  # Initial speed in km/h
        self.safe_distance = 20  # Safe distance in meters
    
    def adjust_speed(self, distance):
        if distance < self.safe_distance:
            self.decelerate()  # Decelerate if too close
        elif distance > self.safe_distance:
            self.accelerate()  # Speed up if it's safe

    def accelerate(self):
        self.speed += 5
        print(f"Accelerating to {self.speed} km/h")

    def decelerate(self):
        self.speed -= 5
        if self.speed < 0:
            self.speed = 0  # Prevent negative speed
        print(f"Decelerating to {self.speed} km/h")

def monitor_distance_and_control_speed():
    acc = AdaptiveCruiseControl()
    
    while True:
        distance = read_lidar_distance()  # Measure distance with LiDAR or mock
        print(f"Distance: {distance} meters")
        acc.adjust_speed(distance)
        time.sleep(1)

if __name__ == "__main__":
    try:
        monitor_distance_and_control_speed()
    except KeyboardInterrupt:
        print("Program terminated")
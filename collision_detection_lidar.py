import time
import platform
import random  # random module to simulate distances for

# Mock function for testing on Windows
def read_lidar_distance():
    if platform.system() == 'Windows':
        # Simulate random distance in cm for testing purposes
        return random.randint(5, 100)  # Random distance between 5 and 100 cm
    else:
        # Actual I2C code to read from the LiDAR sensor
        import smbus2
        I2C_BUS = 1  # For Raspberry Pi, the I2C bus is usually 1
        LIDAR_ADDRESS = 0x62  # LIDAR-Lite v3 I2C address
        LIDAR_COMMAND = 0x00
        LIDAR_DISTANCE = 0x8f
        
        bus = smbus2.SMBus(I2C_BUS)
        
        # Write to command register to initiate distance measurement
        bus.write_byte_data(LIDAR_ADDRESS, LIDAR_COMMAND, 0x04)
        time.sleep(0.02)  # Wait for the measurement to be completed (20ms)
        
        # Read two bytes of distance data
        dist_high = bus.read_byte_data(LIDAR_ADDRESS, LIDAR_DISTANCE)
        dist_low = bus.read_byte_data(LIDAR_ADDRESS, LIDAR_DISTANCE + 1)
        
        # Combine high and low byte to get the distance in cm
        distance = (dist_high << 8) + dist_low
        return distance

def collision_warning():
    dist = read_lidar_distance()
    print(f"Distance: {dist} cm")
    if dist < 30:  # Threshold distance
        print("Warning: Object detected ahead!")
        issue_braking()

def issue_braking():
    print("Automatic braking applied!")

if __name__ == '__main__':
    try:
        while True:
            collision_warning()
            time.sleep(1)
    except KeyboardInterrupt:
        print("Program terminated")

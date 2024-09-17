import smbus2
import time

# Set up I2C communication with LIDAR-Lite sensor
I2C_BUS = 1  # For Raspberry Pi, the I2C bus is usually 1
LIDAR_ADDRESS = 0x62  # LIDAR-Lite v3 I2C address

# LIDAR registers
LIDAR_COMMAND = 0x00
LIDAR_DISTANCE = 0x8f

# Initialize I2C bus
bus = smbus2.SMBus(I2C_BUS)

def read_lidar_distance():
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
    if dist < 30:  # Threshold distance
        print("Warning: Object detected ahead!")
        issue_braking()

def issue_braking():
    print("Automatic braking applied!")
    # Logic to apply automatic braking can go here

if __name__ == '__main__':
    try:
        while True:
            collision_warning()
            time.sleep(1)
    except KeyboardInterrupt:
        print("Program terminated")

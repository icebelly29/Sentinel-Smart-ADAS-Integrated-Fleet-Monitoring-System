import time
import requests
import random

API_ENDPOINT = "https://httpbin.org/post"

def simulate_movement(start_lat, start_lon, speed=0.01):
    """
    Simulate movement by incrementing or decrementing latitude and longitude.
    Speed controls the rate of change of the coordinates.
    """
    lat, lon = start_lat, start_lon
    
    while True:
        # Simulate the vehicle moving by incrementing latitude and longitude
        lat += random.uniform(-speed, speed)
        lon += random.uniform(-speed, speed)
        
        send_location_to_server(lat, lon)
        
        # Simulate different speeds by adjusting delay (e.g., 1 second for fast movement)
        time.sleep(random.uniform(1, 3))  # Delay between 1 to 3 seconds

def send_location_to_server(lat, lon):
    data = {"latitude": lat, "longitude": lon, "vehicle_id": "TRUCK_01"}
    try:
        response = requests.post(API_ENDPOINT, json=data)
        print(f"Sent GPS data to server: {response.status_code}")
        print(f"Latitude: {lat}, Longitude: {lon}")
        
        # Simulate occasional network issues or server downtime
        if random.random() < 0.1:  # 10% chance of a simulated network failure
            raise requests.exceptions.ConnectionError("Simulated network error")

    except requests.exceptions.ConnectionError as e:
        print(f"Failed to connect to server: {e}")
    except requests.exceptions.Timeout as e:
        print(f"Request timed out: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == '__main__':
    # Start simulation at a fixed point, e.g., some initial coordinates
    start_latitude = 12.9715987  # Example: Starting point (Bangalore, India)
    start_longitude = 77.594566  # Example: Starting point (Bangalore, India)
    
    # Simulate vehicle movement along a route
    simulate_movement(start_latitude, start_longitude, speed=0.05)

import concurrent.futures
import subprocess

def run_script(script_name):
    """Run a Python script using subprocess."""
    try:
        result = subprocess.run(['python', script_name], check=True, text=True, capture_output=True)
        print(f"Output of {script_name}:\n{result.stdout}")
    except subprocess.CalledProcessError as e:
        print(f"Error running {script_name}:\n{e.stderr}")

if __name__ == "__main__":
    # List of scripts to run
    scripts = [
        'driver_monitoring.py',
        'collision_detection_lidar.py',
        'passenger_counting.py',  
        'fleet_tracker_simulation.py',
        'adaptive_cruise_control_lidar.py'
    ]

    # Run each script in parallel
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(run_script, script) for script in scripts]
        for future in concurrent.futures.as_completed(futures):
            try:
                future.result()
            except Exception as e:
                print(f"An error occurred: {e}")

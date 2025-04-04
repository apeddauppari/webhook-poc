import os
import time

mount_path = "/mnt/disk1/data"
start_time = time.time()
timeout = 600  # 10 minutes in seconds

print("Starting directory listing script...")
print(f"Monitoring directory: {mount_path}")

while True:
    elapsed_time = time.time() - start_time
    if elapsed_time > timeout:
        print("Timeout reached. Exiting script.")
        break  # Exit after 10 minutes

    try:
        contents = os.listdir(mount_path)
        print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] Contents of {mount_path}: {contents}")
    except FileNotFoundError:
        print(f"[ERROR] Directory {mount_path} not found. Check if the volume is mounted correctly.")
    except PermissionError:
        print(f"[ERROR] Permission denied while accessing {mount_path}.")
    except Exception as e:
        print(f"[ERROR] Unexpected error: {e}")
    
    time.sleep(5)  # Sleep for 5 seconds

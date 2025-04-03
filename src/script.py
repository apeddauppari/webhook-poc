import os
import time

mount_path = "/mnt/disk1/data"

while True:
    print(f"Contents of {mount_path}:")
    try:
        print(os.listdir(mount_path))
    except Exception as e:
        print(f"Error accessing {mount_path}: {e}")
    time.sleep(10)


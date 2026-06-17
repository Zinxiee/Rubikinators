import subprocess
import time

# Wait 5 seconds to ensure USB webcams are fully booted and recognized by the Pi (toggle if running at boot!)
# time.sleep(5)

# --- CONFIGURE YOUR CAMERAS HERE ---
# Check 'v4l2-ctl --list-devices' in terminal to find your ports. 
CAMERA_PORTS = [0, 2] 

# Tweak these values based on your room/LED lighting
EXPOSURE_VAL = 250  # Lower = darker, Higher = brighter
WB_TEMP = 4000      # Color temperature

def init_cameras():
    print("Locking Logitech C270 Webcams (Disabling Auto-correction)...")
    for port in CAMERA_PORTS:
        device = f"/dev/video{port}"
        commands = [
            # Disable Auto White Balance
            f"v4l2-ctl -d {device} -c white_balance_temperature_auto=0",
            # Set fixed White Balance
            f"v4l2-ctl -d {device} -c white_balance_temperature={WB_TEMP}",
            # Disable Auto Exposure (1 = Manual for this camera)
            f"v4l2-ctl -d {device} -c exposure_auto=1",
            # Set fixed Exposure time
            f"v4l2-ctl -d {device} -c exposure_absolute={EXPOSURE_VAL}"
        ]
        
        for cmd in commands:
            try:
                # Run the Linux terminal command silently via Python
                subprocess.run(cmd, shell=True, stderr=subprocess.DEVNULL)
            except Exception:
                pass
    print("Camera hardware locked and ready for OpenCV!")

# This forces the function to run immediately as soon as the file is imported
init_cameras()

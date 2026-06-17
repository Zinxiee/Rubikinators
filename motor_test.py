import RPi.GPIO as GPIO
import time

# --- Configuration ---
DIR_PIN = 25   # Broadcom (BCM) pin 25 connected to A4988 DIR
STEP_PIN = 8  # Broadcom (BCM) pin 8 connected to A4988 STEP

# Motor characteristics
STEPS_PER_REV = 200              # 1.8 degrees per step
DEGREES_TO_TURN = 90             
STEPS_TO_TAKE = int((DEGREES_TO_TURN / 360.0) * STEPS_PER_REV) # Calculates to 50 steps

# Speed control (seconds between pulses)
# 0.005s is a reliable starting speed. Too low (e.g., 0.0001) will stall the motor.
STEP_DELAY = 0.005 

def setup():
    """Initializes the GPIO pins."""
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(DIR_PIN, GPIO.OUT)
    GPIO.setup(STEP_PIN, GPIO.OUT)
    
    # Initialize pins to low
    GPIO.output(DIR_PIN, GPIO.LOW)
    GPIO.output(STEP_PIN, GPIO.LOW)

def turn_motor(steps, direction_cw=True):
    """
    Sends pulse trains to the A4988 driver to step the motor.
    """
    # Set the direction (HIGH for Clockwise, LOW for Counter-Clockwise)
    GPIO.output(DIR_PIN, GPIO.HIGH if direction_cw else GPIO.LOW)

    print(f"Turning {steps} steps ({DEGREES_TO_TURN} degrees)...")
    
    for _ in range(steps):
        # Trigger one step
        GPIO.output(STEP_PIN, GPIO.HIGH)
        time.sleep(STEP_DELAY)
        
        # Reset step pin
        GPIO.output(STEP_PIN, GPIO.LOW)
        time.sleep(STEP_DELAY)

if __name__ == '__main__':
    try:
        setup()
        
        # Execute the 90-degree turn
        turn_motor(STEPS_TO_TAKE, direction_cw=True)
        print("Movement complete.")

    except KeyboardInterrupt:
        print("\nScript interrupted by user.")

    finally:
        # Always clean up GPIO pins on exit to free them up and prevent shorts
        GPIO.cleanup()
        print("GPIO cleaned up safely.")
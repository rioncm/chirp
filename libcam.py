import RPi.GPIO as GPIO
import time
import subprocess
from datetime import datetime

def setup_gpio(pir_pin):
    """Initialize GPIO pins for the PIR sensor."""
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(pir_pin, GPIO.IN)

def capture_image():
    """Capture an image using libcamera-still."""
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"images/captured/image_{timestamp}.jpg"
    command = f"libcamera-still -o {filename}"
    subprocess.run(command, shell=True, check=True)
    print(f"Image saved as {filename}")

def main():
    pir_pin = 17  # Adjust this according to your GPIO setup
    setup_gpio(pir_pin)
    print("Monitoring for motion...")

    try:
        while True:
            if GPIO.input(pir_pin):
                print("Motion detected!")
                capture_image()
                time.sleep(5)  # Delay to avoid multiple captures in quick succession
            time.sleep(0.1)  # Short delay to minimize CPU usage
    except KeyboardInterrupt:
        print("Program terminated")
    finally:
        GPIO.cleanup()

if __name__ == '__main__':
    main()

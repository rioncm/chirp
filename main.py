import RPi.GPIO as GPIO
import time
from datetime import datetime
import os
from picamera2 import Picamera2, Preview

# Setup GPIO pins
def setup_gpio(pir_pin):
    GPIO.setmode(GPIO.BCM)  # Use BCM GPIO numbering
    GPIO.setup(pir_pin, GPIO.IN)  # Set pin as GPIO input

# Initialize camera using picamera2
def initialize_camera():
    picam2 = Picamera2()
    picam2_config = picam2.create_still_configuration(main={"size": (640, 480)})
    picam2.configure(picam2_config)
    picam2.start()
    print("Camera opened")
    return picam2

# Capture image with picamera2
def capture_image(picam2, directory):
    # Ensure the directory exists
    if not os.path.exists(directory):
        os.makedirs(directory)
        print(f"Created directory {directory} for saving images.")
    
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"{directory}/image_{timestamp}.jpg"
    
    # Attempt to capture an image
    try:
        picam2.capture_file(filename)
        print(f"Image saved as {filename}")
    except Exception as e:
        print(f"An unexpected error occurred while saving image {filename}: {e}")

# Main function to monitor motion and capture images
def main():
    pir_pin = 17  # GPIO pin connected to the PIR sensor
    image_directory = "images/captured"  # Directory to store captured images

    setup_gpio(pir_pin)
    picam2 = initialize_camera()

    try:
        while True:
            if GPIO.input(pir_pin):
                print("Motion detected!")
                capture_image(picam2, image_directory)
                time.sleep(5)  # Wait for 5 seconds after capturing an image to avoid multiple captures for one motion
            time.sleep(0.1)  # Short delay to loop check
    except KeyboardInterrupt:
        print("Program terminated")
    finally:
        picam2.stop()  # Stop the camera
        GPIO.cleanup()  # Clean up GPIO on normal exit

# Uncomment the line below to run the program
main()

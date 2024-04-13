import RPi.GPIO as GPIO
import picamera
import time
from datetime import datetime

# Setup GPIO pins
def setup_gpio(pir_pin):
    GPIO.setmode(GPIO.BCM)  # Use BCM GPIO numbering
    GPIO.setup(pir_pin, GPIO.IN)  # Set pin as GPIO input

# Initialize camera
def initialize_camera():
    camera = picamera.PiCamera()
    camera.resolution = (1024, 768)
    return camera

# Capture image
def capture_image(camera, directory):
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"{directory}/image_{timestamp}.jpg"
    camera.capture(filename)
    print(f"Image saved as {filename}")

# Main function to monitor motion and capture images
def main():
    pir_pin = 17  # GPIO pin connected to the PIR sensor
    image_directory = "images/captured"  # Directory to store captured images

    setup_gpio(pir_pin)
    camera = initialize_camera()

    try:
        while True:
            if GPIO.input(pir_pin):
                print("Motion detected!")
                capture_image(camera, image_directory)
                time.sleep(5)  # Wait for 5 seconds after capturing an image to avoid multiple captures for one motion
            time.sleep(0.1)  # Short delay to loop check
    except KeyboardInterrupt:
        print("Program terminated")
    finally:
        GPIO.cleanup()  # Clean up GPIO on normal exit

# Uncomment the line below to run the program
# main()

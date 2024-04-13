import cv2
import RPi.GPIO as GPIO
import time
from datetime import datetime

# Setup GPIO pins
def setup_gpio(pir_pin):
    GPIO.setmode(GPIO.BCM)  # Use BCM GPIO numbering
    GPIO.setup(pir_pin, GPIO.IN)  # Set pin as GPIO input

# Initialize camera using OpenCV
def initialize_camera():
    cap = cv2.VideoCapture(0)  # 0 is usually the default value for the first camera
    if not cap.isOpened():
        print("Error: Camera could not be accessed.")
    return cap

# Capture image with OpenCV
def capture_image(cap, directory):
    ret, frame = cap.read()
    if ret:
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = f"{directory}/image_{timestamp}.jpg"
        cv2.imwrite(filename, frame)
        print(f"Image saved as {filename}")
    else:
        print("Error: No frame captured.")

# Main function to monitor motion and capture images
def main():
    pir_pin = 17  # GPIO pin connected to the PIR sensor
    image_directory = "/home/pi/captured_images"  # Directory to store captured images

    setup_gpio(pir_pin)
    cap = initialize_camera()

    try:
        while True:
            if GPIO.input(pir_pin):
                print("Motion detected!")
                capture_image(cap, image_directory)
                time.sleep(5)  # Wait for 5 seconds after capturing an image to avoid multiple captures for one motion
            time.sleep(0.1)  # Short delay to loop check
    except KeyboardInterrupt:
        print("Program terminated")
    finally:
        cap.release()  # Release the camera
        GPIO.cleanup()  # Clean up GPIO on normal exit

# Uncomment the line below to run the program
# main()

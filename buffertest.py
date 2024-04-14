import cv2
from datetime import datetime
import os
import RPi.GPIO as GPIO
import time

def setup_gpio(pir_pin):
    """Set up the GPIO pin for the PIR sensor."""
    GPIO.setmode(GPIO.BCM)  # BCM GPIO numbering
    GPIO.setup(pir_pin, GPIO.IN)  # Set pin as input

def setup_directory(directory):
    """Ensure the directory exists."""
    if not os.path.exists(directory):
        os.makedirs(directory)
        print(f"Created directory {directory} for saving images.")

def motion_detected(pir_pin):
    """Check if motion is detected by the PIR sensor."""
    return GPIO.input(pir_pin)

def capture_frames(cap, directory, pir_pin):
    """Continuously capture frames from the camera and check for motion."""
    while True:
        # Check for motion
        if motion_detected(pir_pin):
            ret, frame = cap.read()
            if not ret:
                print("Failed to capture frame from camera. Check camera settings and connection.")
                continue  # Skip the rest of the loop and try again

            print("Motion detected! Saving image...")
            save_frame(frame, directory)
            time.sleep(5)  # Wait for a few seconds to avoid capturing too many images quickly
        else:
            time.sleep(0.1)  # Short delay to reduce CPU usage when no motion is detected

def save_frame(frame, directory):
    """Save the captured frame with a timestamp."""
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"{directory}/image_{timestamp}.jpg"
    try:
        cv2.imwrite(filename, frame)
        print(f"Image saved as {filename}")
    except Exception as e:
        print(f"Failed to save image. Error: {e}")

def main():
    pir_pin = 17  # GPIO pin connected to the PIR sensor
    camera_index = 0  # Adjust this based on your camera setup
    image_directory = "images/captured"

    setup_gpio(pir_pin)
    cap = cv2.VideoCapture(camera_index)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    cap.set(cv2.CAP_PROP_FPS, 30)

    if not cap.isOpened():
        print("Cannot open camera")
        return

    setup_directory(image_directory)
    try:
        capture_frames(cap, image_directory, pir_pin)
    finally:
        cap.release()
        GPIO.cleanup()
        print("Camera and GPIO resources have been cleaned up")

if __name__ == '__main__':
    main()

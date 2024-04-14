import cv2
import RPi.GPIO as GPIO
import time
from datetime import datetime
import os


# Setup GPIO pins
def setup_gpio(pir_pin):
    GPIO.setmode(GPIO.BCM)  # Use BCM GPIO numbering
    GPIO.setup(pir_pin, GPIO.IN)  # Set pin as GPIO input

# Initialize camera using OpenCV
def initialize_camera():
      
    cap = cv2.VideoCapture(0)
    time.sleep(2)
    if cap.isOpened():
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        cap.set(cv2.CAP_PROP_FPS, 15)  # Adjust this based on your camera's specifications

        print(f"Camera opened")
        return cap
    cap.release()
    print("Error: No accessible camera found.")
    return None

# Capture image with OpenCV
def capture_image(cap, directory):
    # Ensure the directory exists
    if not os.path.exists(directory):
        os.makedirs(directory)
        print(f"Created directory {directory} for saving images.")
    
    # Attempt to capture a frame
    ret, frame = cap.read()
    
    if ret:
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = f"{directory}/image_{timestamp}.jpg"
        
        # Attempt to save the captured frame
        try:
            cv2.imwrite(filename, frame)
            print(f"Image saved as {filename}")
        except IOError as e:
            print(f"Failed to save image {filename}. IOError: {e}")
        except Exception as e:
            print(f"An unexpected error occurred while saving image {filename}: {e}")
    else:
        # Log details if frame capture failed
        print("Error: No frame captured. Checking camera connection and settings might help.")
        
        # Optionally, include additional diagnostics
        if not cap.isOpened():
            print("The camera capture device is not open. This could indicate a problem with camera initialization.")
        else:
            # Additional diagnostics could go here
            print("Camera is operational, but failed to capture a frame. This might indicate a temporary issue or incorrect settings.")

# Main function to monitor motion and capture images
def main():
    pir_pin = 17  # GPIO pin connected to the PIR sensor
    image_directory = "images/captured"  # Directory to store captured images

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
main()

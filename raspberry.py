# sudo apt-get update
# sudo apt-get upgrade
# pip3 install pyzbar
# pip3 install numpy
# pip3 install RPi.GPIO
# sudo apt-get install python3-opencv

import cv2
from pyzbar.pyzbar import decode
import csv
import numpy as np
import RPi.GPIO as GPIO
import time

# Set up GPIO pins
GPIO.setmode(GPIO.BCM)
GPIO.setup(20, GPIO.OUT) # Lock
GPIO.setup(21, GPIO.OUT) # Buzzer


while True:

    # Open the camera
    cap = cv2.VideoCapture(0)

    while True:
        # Capture a frame from the camera
        ret, frame = cap.read()

        # Decode the QR code in the frame
        decoded_objs = decode(frame)

        # Display the frame with QR code bounding boxes
        for obj in decoded_objs:
            # Extract the QR code data
            data = obj.data.decode('utf-8')
            print("QR code data:", data)

            # Draw a bounding box around the QR code
            rect = obj.rect
            cv2.rectangle(frame, (rect.left, rect.top), (rect.left + rect.width, rect.top + rect.height), (0, 255, 0), 3)

        # Display the frame
        cv2.imshow('frame', frame)

        # Exit the loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        # If a QR code is detected, stop capturing frames and exit the loop
        if len(decoded_objs) > 0:
            break

    # Release the camera
    cap.release()

    # Close all windows
    cv2.destroyAllWindows()

    # Import CSV file and compare the user data
    # opening the CSV file
    with open('Student_data.csv', mode ='r') as file:

        # reading the CSV file
        csvFile = csv.reader(file)

        arr = np.array([])

        # displaying the contents of the CSV file
        for lines in csvFile:
            arr = np.append(arr, lines)

        if data in arr:
            print('User is available...')
            GPIO.output(20, GPIO.HIGH) # High the relay
            time.sleep(3)
            GPIO.output(20, GPIO.LOW)
        else:
            print('Not Available')
            for i in range(0,10):
                GPIO.output(21, GPIO.HIGH) # Fire buzzer
                time.sleep(0.3)
                GPIO.output(21, GPIO.LOW)
                time.sleep(0.3)

    # Clean up GPIO pins
    GPIO.cleanup()
    
    # Exit the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
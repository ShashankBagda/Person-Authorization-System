import cv2
from pyzbar import pyzbar
import csv
import numpy as np

while True:
    # Open the camera
    cap = cv2.VideoCapture(0)

    while True:
        # Capture a frame from the camera
        ret, frame = cap.read()

        # Decode the barcode in the frame
        decoded_objs = pyzbar.decode(frame)

        # Display the frame with barcode bounding boxes
        for obj in decoded_objs:
            # Extract the barcode data
            data = obj.data.decode('utf-8')
            print("Barcode data:", data)

            # Draw a bounding box around the barcode
            rect = obj.rect
            cv2.rectangle(frame, (rect.left, rect.top), (rect.left + rect.width, rect.top + rect.height), (0, 255, 0), 3)

        # Display the frame
        cv2.imshow('frame', frame)

        # Exit the loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        # If a barcode is detected, stop capturing frames and exit the loop
        if len(decoded_objs) > 0:
            break

    # Release the camera
    cap.release()

    # Close all windows
    cv2.destroyAllWindows()

    # Import CSV file and compare the user data
    # Opening the CSV file
    with open('Student_data.csv', mode='r') as file:
        # Reading the CSV file
        csvFile = csv.reader(file)

        arr = np.array([])

        # Displaying the contents of the CSV file
        for lines in csvFile:
            arr = np.append(arr, lines)

        if data in arr:
            print('User is available...')
        else:
            print('Not Available')

    # Exit the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

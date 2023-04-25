import cv2
from pyzbar.pyzbar import decode

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


print(data)


import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Authenticate with the Google Sheets API using the credentials file
scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name("client_secret_261753424909-ffnhlq5kicq1p9tcimbkckuq3iiok35o.apps.googleusercontent.com.json", scope)
client = gspread.authorize(creds)

# Open the spreadsheet by its title
sheet = client.open('My Spreadsheet').sheet1

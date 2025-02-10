import requests
import csv
import re
import cv2
from pyzbar.pyzbar import decode
import os
import time

def find_matches_in_csv(csv_url, column_index, search_term):
    try:
        response = requests.get(csv_url)
        response.raise_for_status()
        csv_content = response.content.decode('utf-8')
        reader = csv.reader(csv_content.splitlines())
        matches = []
        row_num = 0
        for row in reader:
            row_num += 1
            if len(row) >= column_index:
                cell_value = row[column_index - 1].strip()
                if search_term.lower() == cell_value.lower():
                    matches.append(row_num)
        return matches

    except requests.exceptions.RequestException as e:
        print(f"Error accessing the CSV: {e}")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

def play_sound(sound_file):
    try:
        if os.name == 'nt':  # Windows
            import winsound
            winsound.PlaySound(sound_file, winsound.SND_FILENAME)
        elif os.name == 'posix':  # macOS/Linux
            # For macOS, you can use `afplay` (pre-installed) or `playsound`
            # For Linux, you might need to install `aplay` or `paplay`
            os.system(f"afplay {sound_file}") # Example using afplay (macOS)
            # os.system(f"aplay {sound_file}")  # Example using aplay (Linux)
            # or os.system(f"playsound {sound_file}") if you install playsound
        else:
            print("Sound not supported on this platform.")
    except Exception as e:
        print(f"Error playing sound: {e}")

# Example usage:
csv_url = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vQP4b1WF4f8S8Odfa_MsR1GgFlMcO7XtyzB9-6-Sn4xNUKMYFcY15dybWIb_2cZ5Q/pub?gid=1976201659&single=true&output=csv'
column_index = 4  # Column D

search_term = None

try:
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        raise IOError("Cannot open webcam")

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        decoded_data = decode(frame)

        for barcode in decoded_data:
            qr_data = barcode.data.decode("utf-8")
            match = re.search(r'\d+', qr_data)
            if match:
                search_term = match.group(0)
                print(f"Extracted search term from QR code: {search_term}")
                play_sound("beep.wav")
                break

        cv2.imshow('QR Code Scanner', frame)
        if cv2.waitKey(1) & 0xFF == ord('q') or search_term is not None:
            break

    cap.release()
    cv2.destroyAllWindows()

except Exception as e:
    print(f"Error reading QR code: {e}")

if search_term is not None:
    matches = find_matches_in_csv(csv_url, column_index, search_term)

    if matches is None:
        pass
    elif matches:
        print(f"Found '{search_term}' in rows: {matches}")
        play_sound("access-granted.wav")
    else:
        print(f"'{search_term}' not found.")
        play_sound("access-denied.wav")
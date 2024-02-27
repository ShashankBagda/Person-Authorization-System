import gspread
from oauth2client.service_account import ServiceAccountCredentials
import zbarlight
import RPi.GPIO as GPIO
import time

# GPIO pin numbers for LEDs
GREEN_LED_PIN = 18
RED_LED_PIN = 23

# Set up GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(GREEN_LED_PIN, GPIO.OUT)
GPIO.setup(RED_LED_PIN, GPIO.OUT)

# Google Sheets credentials
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)
client = gspread.authorize(creds)

# Google Sheets document and worksheet
spreadsheet = client.open('YourGoogleSheetName')
worksheet = spreadsheet.sheet1

def scan_qr_code():
    # Scan QR code
    with open('/dev/video0', 'rb') as f:
        qr_code = zbarlight.scan_codes('qrcode', f.read())
        if qr_code:
            return qr_code[0].decode('utf-8')
        else:
            return None

def check_enrollment(enrollment_number):
    # Check if enrollment number is in Google Sheets
    cell = worksheet.find(enrollment_number)
    return cell is not None

def blink_led(pin):
    GPIO.output(pin, GPIO.HIGH)
    time.sleep(1)
    GPIO.output(pin, GPIO.LOW)
    time.sleep(1)

try:
    while True:
        enrollment_number = scan_qr_code()
        if enrollment_number:
            if check_enrollment(enrollment_number):
                blink_led(GREEN_LED_PIN)  # Valid code, blink green LED
            else:
                blink_led(RED_LED_PIN)  # Invalid code, blink red LED
        else:
            print("No QR code found")

except KeyboardInterrupt:
    GPIO.cleanup()

import serial
import time
import csv
import os
import threading
from datetime import datetime
import pyautogui


SERIAL_PORT = '/dev/cu.usbmodem101'  # Update as needed for your system
BAUD_RATE = 9600
CSV_FILENAME = 'arduino_responses.csv'

header_needed = not os.path.exists(CSV_FILENAME)

def read_arduino_responses(arduino, csv_writer, csvfile):
    """
    Continuously read responses from Arduino and log them with a timestamp.
    """
    while True:
        if arduino.in_waiting > 0:
            try:
                response = arduino.readline().decode().strip()
            except Exception as e:
                print("Error reading from Arduino:", e)
                continue

            if response:
                current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
                csv_writer.writerow([current_time, response])
                csvfile.flush()
                print(f"Arduino Response: {response} at {current_time}")
        time.sleep(0.1)

try:
    # Open the CSV file in append mode
    csvfile = open(CSV_FILENAME, 'a', newline='')
    csv_writer = csv.writer(csvfile)
    if header_needed:
        csv_writer.writerow(["Datetime", "Arduino Response"])

    arduino = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
    time.sleep(2)

    response_thread = threading.Thread(target=read_arduino_responses, args=(arduino, csv_writer, csvfile), daemon=True)
    response_thread.start()

    print("Initialization complete. Waiting 1 minute before starting trials...")
    time.sleep(60)

    trial = 1
    while True:
        # -------------------------------
        # Step 1: Click the current mouse position.
        # -------------------------------
        pyautogui.click()
        print(f"Trial {trial}: Mouse clicked.")

        # -------------------------------
        # Step 2: Wait 2.5 seconds then send "s" to Arduino.
        # -------------------------------
        time.sleep(2.5)
        command = "s"
        arduino.write((command + "\n").encode())
        print(f"Trial {trial}: Sent command '{command}' to Arduino.")

        # -------------------------------
        # Step 3: Take a screenshot and save it.
        # -------------------------------
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        # The filename is in the format "Trial_<number>_<timestamp>.png"
        filename = f"Trial_{trial}_{timestamp}.png"
        screenshot = pyautogui.screenshot()
        screenshot.save(filename)
        print(f"Trial {trial}: Screenshot saved as {filename}.")

        trial += 1
        time.sleep(600)

except KeyboardInterrupt:
    print("Program terminated by user.")

except Exception as e:
    print("Error:", e)

finally:
    if 'arduino' in locals() and arduino.is_open:
        arduino.close()
    csvfile.close()
    print("Resources have been closed.")

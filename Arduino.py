import serial
import time
import csv
import os
import threading
from datetime import datetime

# Set the correct serial port for macOS (update as needed)
SERIAL_PORT = '/dev/cu.usbmodem101'
CSV_FILENAME = 'arduino_responses.csv'

# Check if CSV file exists; if not, a header is needed.
header_needed = not os.path.exists(CSV_FILENAME)

# p:100,10,2,5,5,100,100

def keyboard_input_thread(arduino):
    """
    Thread function that continuously reads user input from the keyboard and sends it
    to the Arduino. Commands like "START" and "RESET" can be entered.
    """
    print("Enter commands (e.g., START, RESET). Press Ctrl+C to exit.")
    while True:
        try:
            command = input()
            if command:
                # Append newline and send command over serial
                arduino.write((command.strip() + "\n").encode())
                print(f"Sent command: {command.strip()}")
        except Exception as e:
            print("Error reading input:", e)

try:
    # Open the CSV file in append mode and write header if needed.
    with open(CSV_FILENAME, 'a', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        if header_needed:
            csv_writer.writerow(["Datetime", "Arduino Response"])

        # Open the serial port.
        arduino = serial.Serial(SERIAL_PORT, 9600, timeout=1)
        time.sleep(2)  # Allow time for Arduino to initialize

        # Start a background thread to handle keyboard input.
        kb_thread = threading.Thread(target=keyboard_input_thread, args=(arduino,), daemon=True)
        kb_thread.start()

        print("Listening for Arduino response... (Press Ctrl+C to exit)")

        # Main loop: listen for responses from Arduino and log them.
        while True:
            if arduino.in_waiting > 0:
                response = arduino.readline().decode().strip()
                if response:
                    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    csv_writer.writerow([current_time, response])
                    csvfile.flush()
                    print(f"Arduino Response: {response} at {current_time}")
            time.sleep(0.1)  # Prevent busy waiting

except serial.SerialException as e:
    print(f"Serial Error: {e}")
except KeyboardInterrupt:
    print("\nStopped listening. Exiting...")
except Exception as e:
    print("Error:", e)
finally:
    if 'arduino' in locals() and arduino.is_open:
        arduino.close()

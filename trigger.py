import pyautogui
import time
import datetime

pyautogui.FAILSAFE = False  # Optional

try:
    while True:
        # Click the current mouse position
        pyautogui.click()
        
        # Take a screenshot and name it with a timestamp
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        screenshot = pyautogui.screenshot()
        screenshot.save(f"screenshot_{timestamp}.png")
        
        print(f"Clicked and saved screenshot at {timestamp}")
        
        # Wait 30 minutes
        time.sleep(1800)

except KeyboardInterrupt:
    print("Program terminated by user.")

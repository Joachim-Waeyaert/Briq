import os
import platform
import pyautogui
import time

def open_bluetooth_settings():
    system = platform.system()
    if system == "Windows":
        print("Opening Bluetooth settings on Windows...")
        os.system("start ms-settings:bluetooth")
    elif system == "Darwin":  # macOS
        print("Opening Bluetooth settings on macOS...")
        os.system("open /System/Library/PreferencePanes/Bluetooth.prefPane")
    elif system == "Linux":
        print("Please open Bluetooth settings manually on Linux.")
    else:
        print(f"Unsupported operating system: {system}")

def click_connect_button():
    time.sleep(3)  # Wait for settings to fully load
    print("Looking for Connect button on screen...")

    button_location = pyautogui.locateCenterOnScreen("button.png", confidence=0.95)
    button_location = (button_location[0] + 500, button_location[1])
    
    if button_location:
        print(f"Connect button found at: {button_location}")
        pyautogui.click(button_location)
    else:
        print("Connect button not found. Make sure the image is correct and the window is visible.")

if __name__ == "__main__":
    open_bluetooth_settings()
    click_connect_button()

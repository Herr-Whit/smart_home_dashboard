# query the dashboard server for the latest png to display on the screen
import json
import os
import time
from soldered_inkplate10 import Inkplate

DASHBOARD_URL = "192.168.178.42"
display = Inkplate(Inkplate.INKPLATE_2BIT)
# import socket

import network
import urequests as requests


def download_latest_png():
    """Query the dashboard server for the latest png to display on the screen"""

    response = requests.get(f"http://{DASHBOARD_URL}:8000/dashboard/")
    if response.status_code == 200:
        file_name = f"dashboard.png"
        file_path = os.path.join("sd", file_name)
        with open(file_name, "wb") as f:
            f.write(response.content)
        return file_path


def connect_to_wifi():
    with open("credentials.json", "r") as f:
        credentials = json.load(f)

    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        print("connecting to network...")
        sta_if.active(True)
        sta_if.connect(credentials["WIFI_SSID"], credentials["WIFI_PASSWORD"])
        while not sta_if.isconnected():
            pass


def main():
    # Initialize the display, needs to be called only once
    display.begin()

    # Clear the frame buffer
    display.clearDisplay()

    # This has to be called every time you want to update the screen
    # Drawing or printing text will have no effect on the display itself before you call this function
    display.display()

    # SD Card must be initialised with this function
    display.initSDCard()

    # Wait one second so we're totally sure it's initialized
    time.sleep(1)

    # Wake the SD (power ON)
    display.SDCardWake()

    # Draw image in grayscale and display it
    # Also print a message before and after
    print("Starting to draw image from file!")
    display.drawImageFile(0, 0, "sd/1.bmp", False)
    display.display()
    print("Finished drawing image from file!")

    # Put the SD card back to sleep to save power
    display.SDCardSleep()
    # To turn it back on, use:
    # display.SDCardWake()

    connect_to_wifi()
    # The URL of the dashboard server
    file_path = download_latest_png()
    print("file_path:", file_path)
    if file_path:
        print(f"Downloaded latest dashboard image to {file_path}")
        display.drawImageFile(0, 0, file_path)


if __name__ == "__main__":
    main()

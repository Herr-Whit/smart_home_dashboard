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
import machine

import ntptime
import utime


def get_current_time():
    try:
        ntptime.settime()  # Set the RTC using NTP
        # Fetch local time
        return utime.localtime()
    except:
        return None


def format_time():
    # Format the time as HH:MM:SS
    time_tuple = get_current_time()
    return "{:02}:{:02}:{:02}".format(time_tuple[3] + 2, time_tuple[4], time_tuple[5])


def download_latest_dashboard_image():
    """Query the dashboard server for the latest png to display on the screen"""
    print("Downloading latest dashboard image")
    response = requests.get(f"http://{DASHBOARD_URL}:8000/dashboard/")
    if response.status_code == 200:
        file_name = f"dashboard.bmp"
        # file_path = os.path.join("sd", file_name)
        file_path = file_name
        with open(file_name, "wb") as f:
            f.write(response.content)
        print(f"downloaded latest dashboard image: {file_path}")
        return file_path
    else:
        ValueError(f"Could not download latest dashboard image: {response.status_code}")


def get_timing_info():
    """returns the time and duration in ms, when the dashboard is going to be available. Tibber usually publishes the
    prices for the next day at 13:00."""
    print("Getting timing info")
    response = requests.get(f"http://{DASHBOARD_URL}:8000/timing/")
    if response.status_code == 200:
        return response.json()
    else:
        ValueError(f"Could not get timing info: {response.status_code}")


def connect_to_wifi():
    with open("tibber_credentials.json", "r") as f:
        credentials = json.load(f)

    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        print("connecting to network...")
        sta_if.active(True)
        sta_if.connect(credentials["WIFI_SSID"], credentials["WIFI_PASSWORD"])
        while not sta_if.isconnected():
            pass
        print("connected!")


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

    connect_to_wifi()

    time_str = format_time()
    try:
        file_path = download_latest_dashboard_image()

        print("file_path:", file_path)
        if file_path:
            print(f"Downloaded latest dashboard image to {file_path}")
            # Draw image in grayscale and display it
            # Also print a message before and after
            print("Starting to draw image from file!")
            display.drawImageFile(0, 0, file_path)
            print("Finished drawing image from file!")
            display.printText(0, 0, f"Last Update: {time_str}")

            display.display()
            print("Display updated")

        timing_info = get_timing_info()

        sleep_duration = int(timing_info["time_to_sleep"] * 1000)
        # rtc.alarm(rtc.ALARM0, )

        machine.sleep(sleep_duration)
        # put the device to sleep
        machine.deepsleep(sleep_duration)

    except Exception as e:
        print("Failed to download and display dashboard image")
        print(e)
        # Get the current time in seconds since the epoch
        debug_text = f"{time_str}: Failed to download and display dashboard image"
        print(f"Printing debug text: {debug_text}")
        display.printText(0, 0, debug_text)
        display.display()
        raise e
    # Put the SD card back to sleep to save power
    # display.SDCardSleep()
    # To turn it back on, use:
    # display.SDCardWake()
    print("unexected exit")


if __name__ == "__main__":
    try:
        main()
    except:
        pass

    # configure RTC.ALARM0 to be able to wake the device
    # rtc = machine.RTC()
    # rtc.irq(trigger=rtc.ALARM0, wake=machine.DEEPSLEEP)

    # set RTC.ALARM0 to fire after 10 seconds (waking the device)

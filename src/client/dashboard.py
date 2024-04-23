# query the dashboard server for the latest png to display on the screen
import json
import os
import time
from src.client.inkplate10 import Inkplate

DASHBOARD_URL = "192.168.178.42"
display = Inkplate(Inkplate.INKPLATE_2BIT)
# import socket

import network
import requests


def download_latest_png():
    """Query the dashboard server for the latest png to display on the screen"""
    # s = socket.socket()
    # ai = socket.getaddrinfo(DASHBOARD_URL, 8000)
    # addr = ai[0][-1]
    # print("Address infos:", ai)
    # print("Connect address:", addr)
    # s.connect(addr)
    #
    # if True:
    #     # MicroPython socket objects support stream (aka file) interface
    #     # directly, but the line below is needed for CPython.
    #     s = s.makefile("rwb", 0)
    #     s.write(b"GET /dashboard/ HTTP/1.0\r\n\r\n")
    #     print(s.read())
    # else:
    #     s.send(b"GET /dashboard HTTP/1.0\r\n\r\n")
    #     print(s.recv(4096))
    #
    # s.close()
    # client.request('GET', '/dashboard')
    # response = client.getresponse()
    # # response = requests.get(DASHBOARD_URL)
    # # check for 200
    # if response.status == 200:
    #     file_name = f"dashboard.png"
    #     file_path = os.path.join("sd", file_name)
    #     with open(file_name, "wb") as f:
    #         f.write(response.read())
    #     return file_path
    # else:
    #     return None
    response = requests.get(f"http://{DASHBOARD_URL}:8000/dashboard/")
    if response.status_code == 200:
        file_name = f"dashboard.png"
        file_path = os.path.join("sd", file_name)
        with open(file_name, "wb") as f:
            f.write(response.content)
        return file_path

def connect_to_wifi():
    with open('credentials.json', 'r') as f:
        credentials = json.load(f)

    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        print('connecting to network...')
        sta_if.active(True)
        sta_if.connect(credentials['WIFI_SSID'], credentials['WIFI_PASSWORD'])
        while not sta_if.isconnected():
            pass
def main():
    display.begin()

    display.initSDCard()
    time.sleep(5)
    connect_to_wifi()
    # The URL of the dashboard server
    file_path = download_latest_png()
    print('file_path:', file_path)
    if file_path:
        print(f"Downloaded latest dashboard image to {file_path}")
        display.drawImageFile(0, 0, file_path)

if __name__ == "__main__":
    main()
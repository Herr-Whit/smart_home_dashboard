# Smart Home Dashboard
![IMG_0795.jpg](res/IMG_0795.jpg)
This project involved building a smart home dashboard displaying dynamic energy prices, EV charge stage, as well as the 
next trash collection for various bins (that last one might not be that smart, but at least as  useful).

# Physical Setup
## Material
- Display: 
I used an [Inkplate 10](https://soldered.com/de/produkt/soldered-inkplate-10-platine-mitdem-9-7-e-paper/) E-Ink display,
with a ESP32 Microcontroller, to ensure the power consumption of the process is minimal. The controller runs a 
micropython script.
- Server:
A Raspberry PI 3, But any other version of PI or an Arduino should do the trick without a heavy power draw.
## Configuration
Both the server and display need to be in the same Wifi network. The Inkplate 10 can likely be run for a couple of weeks
on a battery, otherwise it can be plugged in.

# Installation
## Config
Add your credentials in the sample files
```
credentials/google_credentials.json.sample
credentials/tibber_credentials.json.sample
credentials/calendar_config.json.sample
```
## Server
Please enter your preferred python environment manager and just run
```
pip -r requirements.txt
```
## Display
Please refer to https://github.com/SolderedElectronics/Inkplate-micropython to set up micropython. Then push the 
contents of `src/client` to the internal storage.

# Running the setup
Run the FastAPI server on the pi:
```shell
python -m src.server.server
```
Just switch on the display, it will request the dashboard from the server after startup. If the server is not reachable 
the display will print a small error message and idle. Otherwise it will print the dashboad for ~5min and then sleep as 
instructed by the server.

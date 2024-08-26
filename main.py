import time
import json
import network
import requests
from pimoroni import Button
from picographics import PicoGraphics, DISPLAY_PICO_DISPLAY, PEN_P4
from pimoroni import RGBLED


# stored ssid and password
with open("config.json", "r") as f:
    config = json.load(f)

wifi_ssid = config["ssid"]
wifi_password = config["password"]

##################### Display setup ###########################################

# We're only using a few colours so we can use a 4 bit/16 colour palette and save RAM!
display = PicoGraphics(display=DISPLAY_PICO_DISPLAY, pen_type=PEN_P4, rotate=0)

display.set_backlight(0.5)
display.set_font("bitmap8")

button_a = Button(12)
button_b = Button(13)
button_x = Button(14)
button_y = Button(15)

# Set up the RGB LED For Display Pack and Display Pack 2.0":
led = RGBLED(6, 7, 8)

WHITE = display.create_pen(255, 255, 255)
BLACK = display.create_pen(0, 0, 0)
CYAN = display.create_pen(0, 255, 255)
MAGENTA = display.create_pen(255, 0, 255)
YELLOW = display.create_pen(255, 255, 0)
GREEN = display.create_pen(0, 100, 0)

# sets up a handy function we can call to clear the screen
def clear():
    display.set_pen(BLACK)
    led.set_rgb(0, 0, 0)
    display.clear()
    display.update()

##################### Wifi connection ###########################################

network.country('CH')

# Client-Betrieb
wlan = network.WLAN(network.STA_IF)

# WLAN-Interface aktivieren
wlan.active(True)

# WLAN-Verbindung herstellen
wlan.connect(wifi_ssid, wifi_password)

while not wlan.isconnected() and wlan.status() >= 0:
    # WLAN-Verbindungsstatus prüfen
    display.set_pen(GREEN)
    display.text('Connecting to Wifi in progress ...', 10, 10, 240,3)
    time.sleep(10)


display.clear()
display.set_pen(GREEN)
led.set_rgb(0, 100, 0)
INIT_MESSAGE_TIMEOUT = 5
display.text(f"Wifi connected, display will go off in {INIT_MESSAGE_TIMEOUT} seconds", 10, 20, 240, 3)
display.update()
time.sleep(INIT_MESSAGE_TIMEOUT)
clear()

##################### Check status ###########################################

AOD = "http://10.5.61.114:9200/nce-rest/arduino-status/aod-open-notifications"
CTD = "http://10.5.61.114:9200/nce-rest/arduino-status/ctd-open-notifications"
MSK = "http://10.5.61.114:9200/nce-rest/arduino-status/msk-open-notifications"
NR = "http://10.5.61.114:9200/nce-rest/arduino-status/nr-open-notifications"

def parse_response(url):
    response = requests.get(url).text
    parts = response.strip().split(";")
    status = int(parts[1])
    prio = parts[2]
    active = status == 1
    return active, prio



while True:
    print("checking aod ...")
    aod_active, aod_prio = parse_response(AOD)
    print(aod_active, aod_prio)
    sleep(10)
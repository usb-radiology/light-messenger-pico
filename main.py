import time
import json
import network
import requests
from machine import Timer
from picographics import PicoGraphics, DISPLAY_PICO_DISPLAY_2, PEN_P4
from pimoroni import RGBLED
import gc

DEPARTMENT = None
URL_TO_QUERY = None
URL_ALIVE = None

# stored ssid and password
with open("config.json", "r") as f:
    config = json.load(f)
    DEPARTMENT = config.get("department")
    rest_url = config.get("server_rest_url_prefix")
    URL_TO_QUERY = rest_url + f"{DEPARTMENT.lower()}-open-notifications"
    URL_ALIVE = rest_url + f"{DEPARTMENT.lower()}-status"

print(f"config.json loaded, settings are: {DEPARTMENT=},{URL_TO_QUERY=},{URL_ALIVE}")
##################### Display setup ###########################################
# We're only using a few colours so we can use a 4 bit/16 colour palette and save RAM!
display = PicoGraphics(display=DISPLAY_PICO_DISPLAY_2, pen_type=PEN_P4, rotate=0)
display.set_backlight(0.4)
display.set_font("bitmap8")
led = RGBLED(26, 27, 28)

WHITE = display.create_pen(255, 255, 255)
BLACK = display.create_pen(0, 0, 0)
RED = display.create_pen(255, 0, 0)
ORANGE = display.create_pen(255, 165, 0)
GREEN = display.create_pen(0, 220, 0)


# a handy function to clear the screen
def clear():
    display.set_pen(BLACK)
    led.set_rgb(0, 0, 0)
    display.clear()
    display.update()


def connect_to_wifi():
    network.country("CH")
    wlan = network.WLAN(network.STA_IF)  # Access WLAN interface
    wlan.active(True)  # Activate the interface
    mac = wlan.config("mac")  # Get MAC address
    mac_address = ":".join(["{:02x}".format(b) for b in mac])
    wifi_ssid = "USB-PSK"
    wifi_password = config.get(mac_address)
    wlan.connect(wifi_ssid, wifi_password)


def parse_response(url):
    response = requests.get(url).text
    parts = response.strip().split(";")
    status = int(parts[1])
    prio = parts[2]
    active = status == 1
    return active, prio


def prio_to_color(prio):
    background_pen = BLACK
    foreground_pen = WHITE
    if prio == "HIGH":
        background_pen = RED
        foreground_pen = WHITE
    elif prio == "MEDIUM":
        background_pen = ORANGE
        foreground_pen = WHITE
    elif prio == "LOW":
        background_pen = GREEN
        foreground_pen = WHITE
    return background_pen, foreground_pen


def show_message(prio):
    background_pen, foreground_pen = prio_to_color(prio)
    display.set_pen(background_pen)
    # sets the background to the actual pen color
    display.clear()
    display.update()
    display.set_pen(foreground_pen)
    display.text("Bitte visieren!", 10, 20, scale=3)
    display.text(f"Priorität {prio}", 10, 60, scale=3)
    display.text(f"Abteilung {DEPARTMENT.upper()}", 10, 100, scale=3)
    display.update()


connect_to_wifi()
display.set_pen(GREEN)
led.set_rgb(0, 100, 0)
INIT_MESSAGE_TIMEOUT = 5
display.set_pen(BLACK)
display.text("WiFi connected!", 10, 20, scale=3)
display.text("Display will go off in sec", 10, 50, scale=3)
display.text("3 sec", 10, 80, scale=3)
display.update()
time.sleep(3)
clear()


def check_and_display():
    print(f"Checking {DEPARTMENT} ...")
    active, prio = parse_response(URL_TO_QUERY)
    print(f"Got response: {active=},{prio=}")
    
    # alarm was not set locally but remote is on
    if active:
        show_message(prio)
    # alarm is active locally but remote is off
    if not active:
        clear()


def alive():
    print("sending alive signal")
    res = requests.get(URL_ALIVE)
    print(f"got response: {res.text=}")
    gc.collect()


# every 5 sec
keep_alive_timer = Timer(period=20000, mode=Timer.PERIODIC, callback=lambda t: alive())
# every 10 sec
check_and_display_timer = Timer(
    period=10000, mode=Timer.PERIODIC, callback=lambda t: check_and_display()
)

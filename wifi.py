import time
import json
import network
import requests

from picographics import PicoGraphics, DISPLAY_PICO_DISPLAY_2, PEN_P4
from pimoroni import RGBLED

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
display.set_backlight(0.5)
display.set_font("bitmap8")
led = RGBLED(26, 27, 28)
WHITE = display.create_pen(255, 255, 255)
BLACK = display.create_pen(0, 0, 0)
CYAN = display.create_pen(0, 255, 255)
MAGENTA = display.create_pen(255, 0, 255)
YELLOW = display.create_pen(255, 255, 0)
GREEN = display.create_pen(0, 100, 0)


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
    color = (0,0,0)
    if prio == "HIGH":
        color = (255, 0, 0)
    elif prio == "MEDIUM":
        color =  (255, 165, 0)
    elif prio == "LOW":
        color =  (0, 255, 0)
    active = status == 1
    return active, prio, color

connect_to_wifi()
display.set_pen(GREEN)
led.set_rgb(0, 100, 0)
INIT_MESSAGE_TIMEOUT = 5
display.set_pen(BLACK)
display.text("WiFi connected!",10,20,scale=3)
display.text("Display will go off in 10sec",10,50,scale=3)
display.update()
time.sleep(10)
res = requests.get("http://schreckhorn.dyn.uhbs.ch:8080/nce-rest/arduino-status/aod-open-notifications")
print(res.text)
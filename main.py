import time
import json
import network
import requests
from machine import Timer
from picographics import PicoGraphics, DISPLAY_PICO_DISPLAY, PEN_P4
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

##################### Display setup ###########################################

# We're only using a few colours so we can use a 4 bit/16 colour palette and save RAM!
display = PicoGraphics(display=DISPLAY_PICO_DISPLAY, pen_type=PEN_P4, rotate=0)

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
    wifi_ssid = config.get(mac_address)[0]
    wifi_password = config.get(mac_address)[1]
    wlan.connect(wifi_ssid, wifi_password)
    while not wlan.isconnected() and wlan.status() >= 0:
        display.set_pen(GREEN)
        display.text("Connecting to Wifi in progress ...", 10, 10, 240, 3)
        time.sleep(10)
        display.clear()
        display.set_pen(GREEN)
        led.set_rgb(0, 100, 0)
        INIT_MESSAGE_TIMEOUT = 5
        display.text(
            f"Wifi connected, display will go off in {INIT_MESSAGE_TIMEOUT} seconds",
            10,
            20,
            240,
            3,
        )
        display.update()
        time.sleep(INIT_MESSAGE_TIMEOUT)
        clear()


def parse_response(url):
    response = requests.get(url).text
    parts = response.strip().split(";")
    status = int(parts[1])
    prio = parts[2]
    if prio == "HIGH":
        color = (255, 0, 0)
    elif prio == "MEDIUM":
        color =  (255, 165, 0)
    elif prio == "LOW":
        color =  (0, 255, 0)
    active = status == 1
    return active, prio, color


def show_message(prio, color):
    display.set_pen(color)
    display.clear()
    display.update()
    display.set_pen(WHITE)
    display.text(f"{prio}", 10, 20, 240, 3)


connect_to_wifi()

ALARM = False
def check_and_display():
    global ALARM
    print(f"Checking {DEPARTMENT} ...")
    active, prio, color = parse_response(URL_TO_QUERY)
    # alarm was not set locally but remote is on
    if not ALARM and active:
        show_message(color)
        ALARM = True
    # alarm is active locally but remote is off
    if ALARM and not active:
        clear()
        ALARM = False

# every 5 sec
keep_alive_timer = Timer(
    period=5000, mode=Timer.PERIODIC, callback=lambda t: requests.get(URL_ALIVE)
)
# every 10 sec
check_and_display_timer = Timer(
    period=10000, mode=Timer.PERIODIC, callback=lambda t: check_and_display()
)


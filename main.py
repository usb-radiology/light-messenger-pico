import time
import json
import network
import requests
from picographics import PicoGraphics, DISPLAY_PICO_DISPLAY_2, PEN_P4
from pimoroni import RGBLED
import gc
import asyncio

from anim_display import AnimatedDisplay

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

print(
    f"config.json loaded, settings are: \n{DEPARTMENT=}\n{URL_TO_QUERY=}\n{URL_ALIVE=}"
)
##################### Display setup ###########################################
# We're only using a few colours so we can use a 4 bit/16 colour palette and save RAM!
display = PicoGraphics(display=DISPLAY_PICO_DISPLAY_2, pen_type=PEN_P4, rotate=0)
display.set_backlight(0.4)
display.set_font("bitmap8")
led = RGBLED(26, 27, 28)
led.set_rgb(0, 0, 0)

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
    led.set_rgb(255, 0, 0)
    wlan = network.WLAN(network.STA_IF)  # Access WLAN interface
    wlan.active(True)  # Activate the interface
    mac = wlan.config("mac")  # Get MAC address
    mac_address = ":".join(["{:02x}".format(b) for b in mac])
    wifi_ssid = "USB-PSK"
    wifi_password = config.get(mac_address)
    wlan.connect(wifi_ssid, wifi_password)

    while not wlan.isconnected():
        led.set_rgb(0, 0, 255)
        print("Waiting for connection...")
        time.sleep(1)

    led.set_rgb(0, 255, 0)
    ip_address = wlan.ifconfig()[0]
    print(f"MAC: {mac_address}")
    print(f"IP: {ip_address}")
    return mac_address, ip_address


def parse_response(url):
    response = requests.get(url).text
    parts = response.strip().split(";")
    status = int(parts[1])
    prio = parts[2]
    active = status == 1
    return active, prio


mac, ip_address = connect_to_wifi()
display.set_pen(GREEN)
led.set_rgb(0, 100, 0)
INIT_MESSAGE_TIMEOUT = 5
display.set_pen(BLACK)
display.text("WiFi connected!", 10, 20, scale=3)
display.text(f"MAC: {mac}", 10, 60, scale=3)
display.text(f"IP: {ip_address}", 10, 100, scale=3)
display.text("Display will go off in sec", 10, 140, scale=3)
display.text("3 sec", 10, 180, scale=3)
display.update()
time.sleep(3)
clear()


async def keep_alive():
    while True:
        print("sending alive signal")
        res = requests.get(URL_ALIVE)
        print(f"got response: {res.text=}")
        gc.collect()
        await asyncio.sleep(20)


async def run_animation(display):
    while True:
        if display.active:
            display.animate_circles()
        await asyncio.sleep(0.002)


async def check_and_display(display):
    while True:
        print(f"Checking {DEPARTMENT} ...")
        active, prio = parse_response(URL_TO_QUERY)
        print(f"Got response: {active=},{prio=}")
        display.active = active

        if active:
            display.set_prio(prio)
        else:
            # Clear the display if not active
            display.clear_display()

        await asyncio.sleep(10)


async def main(display, department):
    display = AnimatedDisplay(display, department)

    # Schedule check_and_display and keep_alive tasks
    await asyncio.gather(
        run_animation(display), check_and_display(display), keep_alive()
    )


# Start the asyncio event loop
asyncio.run(main(display, DEPARTMENT))

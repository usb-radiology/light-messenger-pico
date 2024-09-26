import os
import machine
import network
from picographics import PicoGraphics, DISPLAY_PICO_DISPLAY_2

# Initialize the display
display = PicoGraphics(display=DISPLAY_PICO_DISPLAY_2)
display.set_font('sans')

BLACK = display.create_pen(0, 0, 0)
WHITE = display.create_pen(255, 255, 255)
GREEN = display.create_pen(0, 100, 0)

# Function to get the MAC address of the Raspberry Pi Pico
def get_mac_address():
    wlan = network.WLAN(network.STA_IF)  # Access WLAN interface
    wlan.active(True)  # Activate the interface
    mac = wlan.config('mac')  # Get MAC address
    return ':'.join(['{:02x}'.format(b) for b in mac])

# Function to display the MAC address on the screen
def show_mac_on_display():
    display.set_backlight(0.5)  # Set backlight brightness
    display.set_pen(BLACK)  # White text
    display.clear()  # Clear display
    
    mac_address = get_mac_address()
    display.set_pen(GREEN)
    display.set_thickness(2)
    display.text(f"MAC Address:", 10, 30, scale=1)
    display.text(f"{mac_address}", 10, 60, scale=1)
    
    display.update()  # Update the display with new content

# Run the function to display the MAC address
show_mac_on_display()



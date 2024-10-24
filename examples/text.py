from picographics import PicoGraphics, DISPLAY_PICO_DISPLAY_2, PEN_P4
from pimoroni import RGBLED

##################### Display setup ###########################################
# We're only using a few colours so we can use a 4 bit/16 colour palette and save RAM!
display = PicoGraphics(display=DISPLAY_PICO_DISPLAY_2, pen_type=PEN_P4, rotate=0)
display.set_backlight(0.8)
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

display.clear()
display.set_pen(GREEN)
led.set_rgb(0, 100, 0)
INIT_MESSAGE_TIMEOUT = 5
display.set_pen(BLACK)
display.text("Hello World",10,20,scale=3)
display.update()

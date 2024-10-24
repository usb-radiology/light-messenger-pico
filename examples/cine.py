import math
import time
from picographics import PicoGraphics, DISPLAY_PICO_DISPLAY_2

# Set up the display
display = PicoGraphics(display=DISPLAY_PICO_DISPLAY_2)

# Get the width and height of the display
width, height = display.get_bounds()


BLACK = display.create_pen(0, 0, 0)
RED = display.create_pen(255, 0, 0)

diameter = height//3
angle = 0

while True:
    display.set_pen(BLACK)
    display.clear()

    d1 = 10 + (math.sin(angle) * diameter/2) + diameter/2;
    d2 = 10 + (math.sin(angle + math.pi/2) * diameter/2) + diameter/2;
    d3 = 10 + (math.sin(angle + math.pi) * diameter/2) + diameter/2;
    display.set_pen(RED)
    display.circle(0, height//2, int(d1));
    display.circle(width//2, height//2, int(d2));
    display.circle(width, height//2, int(d3));
    display.update()
    angle += 0.05;
    time.sleep(0.001)
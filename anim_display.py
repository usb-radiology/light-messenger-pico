import math
import time


class AnimatedDisplay:
    def __init__(self, display, department):
        # Set up the display
        self.display = display
        self.department = department

        # Get the width and height of the display
        self.width, self.height = self.display.get_bounds()

        # Define color pens
        self.WHITE = display.create_pen(255, 255, 255)
        self.BLACK = self.display.create_pen(0, 0, 0)
        self.BLACK = self.display.create_pen(0, 0, 0)
        self.RED = self.display.create_pen(255, 0, 0)
        self.ORANGE = self.display.create_pen(255, 165, 0)
        self.GREEN = self.display.create_pen(0, 220, 0)

        # Animation settings
        self.diameter = self.height // 3
        self.angle = 0
        self.active = False
        self.prio = ""
        self.color = None

    def set_prio(self, prio):
        self.prio = prio
        if prio == "HIGH":
            self.color = self.RED
        elif prio == "MEDIUM":
            self.color = self.ORANGE
        elif prio == "LOW":
            self.color = self.GREEN

    def clear_display(self):
        self.display.set_pen(self.BLACK)
        self.display.clear()
        self.display.update()

    def animate_circles(self):
        self.display.set_pen(self.BLACK)
        self.display.clear()

        # Calculate new circle diameters based on the current angle
        d1 = 10 + (math.sin(self.angle) * self.diameter / 2) + self.diameter / 2
        d2 = (
            10
            + (math.sin(self.angle + math.pi / 2) * self.diameter / 2)
            + self.diameter / 2
        )
        d3 = (
            10
            + (math.sin(self.angle + math.pi) * self.diameter / 2)
            + self.diameter / 2
        )

        # Draw the circles
        self.display.set_pen(self.color)
        self.display.circle(0, self.height // 2, int(d1))
        self.display.circle(self.width // 2, self.height // 2, int(d2))
        self.display.circle(self.width, self.height // 2, int(d3))
        self.display.set_pen(self.WHITE)
        self.display.text(self.department.upper(), self.width//2-10, self.height//2-10, scale=3)
        # Update the display
        self.display.update()

        # Increment the angle for the next frame
        self.angle += 0.04


import time
import random
import math
from pimoroni import Button
from picographics import PicoGraphics, DISPLAY_PICO_DISPLAY_2

# Initialize the display
display = PicoGraphics(display=DISPLAY_PICO_DISPLAY_2)

# Set the display backlight to full brightness
display.set_backlight(1.0)

# Set the display dimensions
WIDTH, HEIGHT = display.get_bounds()

# Configuration of colors for the confetti (you can change these)
confetti_colors = [
    display.create_pen(255, 0, 0),     # Red
    display.create_pen(0, 255, 0),     # Green
    display.create_pen(0, 0, 255),     # Blue
    display.create_pen(255, 255, 0),   # Yellow
    display.create_pen(255, 0, 255),   # Magenta
    display.create_pen(0, 255, 255),   # Cyan
    display.create_pen(255, 255, 255), # White
]



# Number of confetti pieces in the firework burst
NUM_CONFETTI = 60

# Confetti data (x, y positions, x, y velocities, size, color, life span)
confetti = []

# Function to reset the firework burst, initializing positions, velocities, and life spans
def reset_firework():
    global confetti
    confetti = []
    center_x = WIDTH // 2
    center_y = HEIGHT // 2
    for _ in range(NUM_CONFETTI):
        angle = random.uniform(0, 2 * math.pi)  # Random angle for radial motion
        speed = random.uniform(3, 6)  # Random initial speed
        velocity_x = math.cos(angle) * speed
        velocity_y = math.sin(angle) * speed
        size = random.randint(3, 6)  # Random size
        color = random.choice(confetti_colors)  # Random color
        life = random.uniform(1.0, 3.0)  # Random lifespan in seconds before fading
        confetti.append([center_x, center_y, velocity_x, velocity_y, size, color, life])

# Update and draw confetti for the firework burst
def update_firework():
    display.set_pen(display.create_pen(0,0,0)) # Set pen to black for clearing the screen
    display.clear()  # Clear the screen

    # Loop over all confetti particles
    for particle in confetti:
        x, y, vx, vy, size, color, life = particle
        
        # Update particle position
        particle[0] += vx  # Update x position
        particle[1] += vy  # Update y position
        
        # Apply deceleration to simulate gravity or air resistance (slows down the particle)
        particle[2] *= 0.98  # Slow down x velocity
        particle[3] *= 0.98  # Slow down y velocity

        # Decrease the lifespan of the confetti
        particle[6] -= 0.05

        # Set the pen to the particle's color and draw it (if it still has lifespan)
        if life > 0:
            display.set_pen(color)
            display.circle(int(x), int(y), size)  # Draw the particle

    display.update()  # Update the display with the new drawing

# Main loop
reset_firework()  # Initialize the firework burst

while True:
    update_firework()  # Update the confetti movement and drawing
    time.sleep(0.005)  # Small delay for smoother animation
    
    # If all confetti particles have "faded out" (i.e., life <= 0), reset the burst
    if all(p[6] <= 0 for p in confetti):
        reset_firework()  # Trigger a new firework burst
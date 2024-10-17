##################################################################
# Ball Fall Code
##################################################################
# Generate random configurations of balls by having them fall 
# under the influence of gravity
##################################################################
# INPUTS
#   - Environment
#   - Number of balls
#   - Fall spawn range
##################################################################
# OUTPUTS
#   - X/Y values for all balls
##################################################################
# IMPORTS
import random
import datetime
import pygame
import pymunk
from pymunk.vec2d import Vec2d
from numpy import *
import os

# Import necessary modules

def read_initial_positions(config_file='config.txt'):
    """Reads the initial positions from config.txt and returns them as tuples."""
    positions = []
    
    try:
        with open(config_file, 'r') as file:
            for line in file:
                x, y = map(int, line.strip().split(','))
                positions.append((x, y))
    except FileNotFoundError:
        print("Error: config.txt not found!")
        return [(0, 0), (1, 1)]  # Default positions if file is missing
    return positions

def main():
    # Load initial ball positions from config.txt
    initial_positions = read_initial_positions()
    
    # Assuming a function or class that generates balls
    balls = []  # List to hold ball objects or data
    
    # Initialize the first two balls with predefined positions
    balls.append({'id': 1, 'position': initial_positions[0]})
    balls.append({'id': 2, 'position': initial_positions[1]})

    # Log the initial positions for verification
    print(f"Ball 1 initial position: {balls[0]['position']}")
    print(f"Ball 2 initial position: {balls[1]['position']}")
    
    # Continue with other operations for the remaining balls...
    # You can generate other balls as needed here
    
if __name__ == "__main__":
    main()


# Configuration stuff
ball_r = 20
threshold_ratio = 1.02

# Initialize pygame
pygame.init()

# Set up the display
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()

# Set up the physics space
space = pymunk.Space()
space.gravity = (0, -500)  # Set the gravity in the correct direction
space.iterations = 120
space.collision_slop = 0.01
space.collision_persistence = 10

# Create the environment objects
static_lines = [
    pymunk.Segment(space.static_body, (200, height - 550), (600, height - 550), 5),
    pymunk.Segment(space.static_body, (50, height - 50), (200, height - 550), 5),
    pymunk.Segment(space.static_body, (750, height - 50), (600, height - 550), 5)
]
#static_lines = []
#with open('static_lines_config_1.txt', 'r') as file:
#    for line in file:
#        x1, y1, x2, y2 = map(int, line.strip().split(','))
#        segment = pymunk.Segment(space.static_body, (x1, y1), (x2, y2), 5)
#        segment.elasticity = 0.8
#        static_lines.append(segment)

space.add(*static_lines) # Unpack the static_lines list

# Create a ball group for collisions
ball_group = []

# Create a circle
def create_circle(position):
    body = pymunk.Body(1, 100)
    body.position = position
    shape = pymunk.Circle(body, ball_r)
    shape.elasticity = 0.8
    shape.friction = 0.5

    space.add(body, shape)
    ball_group.append(shape)
    
###############################################################################################################################################
###############################################################################################################################################
# Game loop
running = True
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Create a new circle at a random position when spacebar is pressed
    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE]:
        x = random.randint(50, width - 50)
        y = height-50
        create_circle((x, y))

    # Clear the screen
    screen.fill((255, 255, 255))

    # Update physics and draw objects
    dt = 1.0 / 60.0
    space.step(dt)

    for ball in ball_group:
        position = Vec2d(ball.body.position.x, height - ball.body.position.y)
        pygame.draw.circle(screen, (0, 0, 255), position, 20)

    for line in static_lines:
        body = line.body
        p1 = body.position + line.a.rotated(body.angle)
        p2 = body.position + line.b.rotated(body.angle)
        pygame.draw.lines(screen, (0, 0, 0), False, [(p1.x, height - p1.y), (p2.x, height - p2.y)])  # Adjust the y-coordinate

    # Update the display
    pygame.display.flip()
    clock.tick(60)


###############################################################################################################################################
###############################################################################################################################################
# Print output
# Get the current date and time
now = datetime.datetime.now()
# Format the date and time as yyyymmdd-hhmmss
filename = now.strftime("%Y%m%d-%H%M%S") + ".txt"

with open(filename, "a") as f:
    # Write some content to the file
    # Use python unique ids to differentiate balls
    print("-----------------------------------------------------",file=f)
    print("List of ball x/y positions",file=f)
    for ii in range(0,len(ball_group)):
        print(f"{ball_group[ii].body.position.x};{ball_group[ii].body.position.y}",file=f)
    
    print("-----------------------------------------------------",file=f)
    print("List of contacts",file=f)
    for ii in range(0,len(ball_group)-1):
        for jj in range(ii+1, len(ball_group)):
            ball1 = ball_group[ii]
            ball2 = ball_group[jj]
            dx = ball1.body.position.x - ball2.body.position.x
            dy = ball1.body.position.x - ball2.body.position.y
            dist = sqrt(dx*dx + dy*dy)
            if dist < (2*ball_r*threshold_ratio):
                print(f"{ii};{jj}",file=f)

# Another just for the connections
filename = "connections.txt"
if os.path.exists(filename):
    os.remove(filename)
    print(f"previous version of {filename} has been deleted.")

with open(filename, "a") as f:
    for ii in range(0, len(ball_group)-1):
        for jj in range(ii+1, len(ball_group)):
            ball1 = ball_group[ii]
            ball2 = ball_group[jj]
            dx = ball1.body.position.x - ball2.body.position.x
            dy = ball1.body.position.y - ball2.body.position.y
            dist = sqrt(dx*dx + dy*dy)
            #print(f"{dist}",file=f)
            if dist < (2*ball_r*threshold_ratio):
                print(f"{ii};{jj}",file=f)

# Quit the game
pygame.quit()
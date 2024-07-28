import pygame
from pygame.math import Vector3
from OpenGL.GL import *
from OpenGL.GLU import *
import math

# Initialize Pygame and OpenGL
pygame.init()
display = pygame.display.set_mode((0, 0), pygame.FULLSCREEN | pygame.DOUBLEBUF | pygame.OPENGL)
width, height = pygame.display.get_surface().get_size()

# Set up the camera
fov = 45
aspect = width / height
near = 0.1
far = 100.0

# Player position and rotation
position = Vector3(0, 1, 5)
rotation = Vector3(0, 0, 0)

# Simple cube vertices
vertices = (
    (1, -1, -1), (1, 1, -1), (-1, 1, -1), (-1, -1, -1),
    (1, -1, 1), (1, 1, 1), (-1, -1, 1), (-1, 1, 1)
)

# Simple cube edges
edges = (
    (0, 1), (0, 3), (0, 4), (2, 1), (2, 3), (2, 7),
    (6, 3), (6, 4), (6, 7), (5, 1), (5, 4), (5, 7)
)


def draw_cube():
    glBegin(GL_LINES)
    for edge in edges:
        for vertex in edge:
            glVertex3fv(vertices[vertex])
    glEnd()


def draw_floor():
    glBegin(GL_QUADS)
    for x in range(-10, 11, 2):
        for z in range(-10, 11, 2):
            glVertex3f(x, 0, z)
            glVertex3f(x + 2, 0, z)
            glVertex3f(x + 2, 0, z + 2)
            glVertex3f(x, 0, z + 2)
    glEnd()


clock = pygame.time.Clock()

pygame.mouse.set_visible(False)
pygame.event.set_grab(True)

# Main game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            pygame.quit()
            quit()

    # Handle key presses
    keys = pygame.key.get_pressed()
    move_speed = 0.1

    # Calculate movement vector
    move_vector = Vector3(0, 0, 0)
    if keys[pygame.K_w]:
        move_vector.z -= move_speed
    if keys[pygame.K_s]:
        move_vector.z += move_speed
    if keys[pygame.K_a]:
        move_vector.x -= move_speed
    if keys[pygame.K_d]:
        move_vector.x += move_speed
    if keys[pygame.K_SPACE]:
        move_vector.y += move_speed
    if keys[pygame.K_LSHIFT]:
        move_vector.y -= move_speed

    # Rotate movement vector
    yaw = math.radians(rotation.y)
    rotated_x = move_vector.x * math.cos(yaw) - move_vector.z * math.sin(yaw)
    rotated_z = move_vector.x * math.sin(yaw) + move_vector.z * math.cos(yaw)

    # Update position
    position.x += rotated_x
    position.y += move_vector.y
    position.z += rotated_z

    # Handle mouse movement for rotation
    mouse_change = pygame.mouse.get_rel()
    rotation.y += mouse_change[0] * 0.1
    rotation.x += mouse_change[1] * 0.1
    rotation.x = max(min(rotation.x, 90), -90)

    # Clear the screen and reset the model view matrix
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    # Set up perspective projection
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(fov, aspect, near, far)

    # Switch back to model view matrix
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    # Apply rotation
    glRotatef(rotation.x, 1, 0, 0)
    glRotatef(rotation.y, 0, 1, 0)

    # Move the world in the opposite direction of the player's movement
    glTranslatef(-position.x, -position.y, -position.z)

    # Enable depth testing
    glEnable(GL_DEPTH_TEST)

    # Draw the floor
    glColor3f(0.5, 0.5, 0.5)
    draw_floor()

    # Draw cubes
    glColor3f(1, 0, 0)
    draw_cube()

    glPushMatrix()
    glTranslatef(5, 1, -5)
    glColor3f(0, 1, 0)
    draw_cube()
    glPopMatrix()

    glPushMatrix()
    glTranslatef(-5, 1, 5)
    glColor3f(0, 0, 1)
    draw_cube()
    glPopMatrix()

    pygame.display.flip()
    clock.tick(60)
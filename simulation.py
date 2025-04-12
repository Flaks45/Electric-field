import math
import pygame
import random
import sys

from charge import Charge
from coordinates import Vector2D, Point2D
from particle import Electron, Proton, Neutron


class SimulationWindow:
    """
    Simulation window for the electric field.

    Attributes:
        width (int): The width of the window (default 800).
        height (int): The height of the window (default 800).
        screen (pygame.Surface): The pygame window surface where everything is drawn.
        objects (list): A list to store all objects (e.g., VisualVector2D) to be rendered.
        dynamic_objects (list): A list to store all dynamic objects to be rendered and updated.

    Methods:
        __init__(self, width=800, height=800):
            Initializes the pygame window with given dimensions.

        run(self):
            Starts and runs the main simulation loop, handling events and rendering.

        add_object(self, obj):
            Adds an object to the simulation (e.g., a visual representation).
    """

    def __init__(self, charges: list[Charge], width=800, height=800):
        pygame.init()
        self.width = width
        self.height = height

        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Electric field simulation")
        icon = pygame.image.load('./assets/black_logo.png')
        pygame.display.set_icon(icon)

        self.charges = charges
        self.objects = []
        self.dynamic_objects = []

        self.static_layer = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        self.static_layer_dirty = True  # Re-render static layer only when needed

    def run(self):
        """
        Runs the main simulation loop. This method continuously checks for events (like closing the window),
        updates the display, and keeps the window running until the user closes it.
        """
        clock = pygame.time.Clock()
        running = True
        while running:
            dt = clock.tick(60) / 1000  # Time since last frame in seconds

            # Event handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if event.type == pygame.KEYDOWN:
                    x, y = pygame.mouse.get_pos()
                    particle_event = False

                    # Electron (1)
                    if event.key == pygame.K_1:
                        particle_event = True
                        particles = [Electron(Point2D(x, y), Vector2D(0, 0), self.charges)]

                    # Proton (2)
                    elif event.key == pygame.K_2:
                        particle_event = True
                        particles = [Proton(Point2D(x, y), Vector2D(0, 0), self.charges)]

                    # Neutron (3)
                    elif event.key == pygame.K_3:
                        particle_event = True
                        particles = [Neutron(Point2D(x, y), Vector2D(0, 0), self.charges)]

                    # Electron spam (4)
                    elif event.key == pygame.K_4:
                        particle_event = True
                        particles = [Electron(Point2D(x, y), Vector2D(0, 0), self.charges)]
                        radius_increase = 0
                        for n in [8, 16, 24]:
                            radius_increase += 5
                            for i in range(n):
                                angle = i * (2 * math.pi / n)
                                pos_x = x + 3 * radius_increase * math.cos(angle)
                                pos_y = y + 3 * radius_increase * math.sin(angle)

                                particles.append(Electron(Point2D(pos_x, pos_y), Vector2D(0, 0), self.charges))

                    # Electron spam at random velocities (5)
                    elif event.key == pygame.K_5:
                        particle_event = True
                        particles = [Electron(Point2D(x, y), Vector2D(0, 0), self.charges)]
                        radius_increase = 0
                        for n in [8, 16, 24, 32]:
                            radius_increase += 5
                            for i in range(n):
                                angle = i * (2 * math.pi / n)
                                pos_x = x + 3 * radius_increase * math.cos(angle)
                                pos_y = y + 3 * radius_increase * math.sin(angle)
                                random_speed = Vector2D(random.randint(-1e7, 1e7), random.randint(-1e7, 1e7))

                                particles.append(Electron(Point2D(pos_x, pos_y), random_speed, self.charges))

                    # Right electron beam (6)
                    elif event.key == pygame.K_6:
                        particle_event = True
                        particles = []
                        for w in range(10):
                            for h in range(6):
                                pos_x = x + 10 * w
                                pos_y = y + 10 * (h - 1)
                                particles.append(Electron(Point2D(pos_x, pos_y), Vector2D(4e7, 0), self.charges))

                    # Proton spam at random velocities (7)
                    elif event.key == pygame.K_7:
                        particle_event = True
                        particles = [Proton(Point2D(x, y), Vector2D(0, 0), self.charges)]
                        radius_increase = 0
                        for n in [8, 16, 24]:
                            radius_increase += 5
                            for i in range(n):
                                angle = i * (2 * math.pi / n)
                                pos_x = x + 3 * radius_increase * math.cos(angle)
                                pos_y = y + 3 * radius_increase * math.sin(angle)
                                random_speed = Vector2D(random.randint(-1e7, 1e7), random.randint(-1e7, 1e7))

                                particles.append(Proton(Point2D(pos_x, pos_y), random_speed, self.charges))

                    # Reset dynamic particles
                    elif event.key == pygame.K_r:
                        self.clear_dynamic_objects()

                    # Avoid error when pressing another key
                    else:
                        continue

                    # Add action particles
                    if particle_event:
                        for particle in particles:
                            self.add_dynamic_object(particle)

            self.screen.fill((0, 0, 0))

            # Static objects
            if self.static_layer_dirty:
                self.static_layer.fill((0, 0, 0))  # Clear static surface
                for obj in self.objects:
                    obj.draw(self.static_layer)
                self.static_layer_dirty = False

            # Blit pre-rendered static layer
            self.screen.blit(self.static_layer, (0, 0))

            # Dynamic objects
            for obj in self.dynamic_objects:
                needs_render = obj.update(dt)
                if needs_render:
                    obj.draw(self.screen)

            pygame.display.flip()

        pygame.quit()
        sys.exit()

    def add_object(self, obj):
        """Adds an object to the simulation and marks the static layer for re-rendering."""
        self.objects.append(obj)
        self.static_layer_dirty = True

    def add_dynamic_object(self, obj):
        """Adds a dynamic object to the simulation."""
        self.dynamic_objects.append(obj)

    def clear_dynamic_objects(self):
        """Removes all dynamic objects from the simulation."""
        self.dynamic_objects.clear()


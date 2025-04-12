import math
import pygame
import sys


from coordinates import Point2D, Vector2D
from objects import Electron, Positron, Proton, Neutron


class SimulationWindow:
    """
    A window that visualizes a particle simulation, allowing user input to spawn
    different particles with assigned properties. Supports both static and dynamic objects.
    """

    def __init__(self, width=800, height=800, other_info: dict = None):
        """
        Initializes the simulation window and Pygame. Sets up display, layers, and state.

        :param width: Width of the window.
        :param height: Height of the window.
        :param other_info: Optional dictionary with simulation-wide parameters (e.g. slow_factor, external_charges).
        """
        pygame.init()
        self.width = width
        self.height = height

        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Electric field simulation")
        icon = pygame.image.load('./assets/black_logo.png')
        pygame.display.set_icon(icon)

        self.objects = []

        self.static_layer = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        self.static_layer_dirty = True  # Re-render static layer only when needed

        self.other_info = other_info

    def run(self):
        """
        Main loop of the simulation. Handles user input, spawns particles, updates dynamic objects,
        renders visuals, and manages redraws. Ends when the window is closed.
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
                    mouse_x, mouse_y = pygame.mouse.get_pos()

                    # Electron (1)
                    if event.key == pygame.K_1:
                        self.add_object(
                            Electron(
                                position=Point2D(mouse_x, mouse_y),
                                velocity=Vector2D(0, 0),
                                external_charges=self.other_info["external_charges"],
                                slow_factor=self.other_info["slow_factor"]
                            )
                        )

                    # Positron (2)
                    elif event.key == pygame.K_2:
                        self.add_object(
                            Positron(
                                position=Point2D(mouse_x, mouse_y),
                                velocity=Vector2D(0, 0),
                                external_charges=self.other_info["external_charges"],
                                slow_factor=self.other_info["slow_factor"]
                            )
                        )

                    # Proton (3)
                    elif event.key == pygame.K_3:
                        self.add_object(
                            Proton(
                                position=Point2D(mouse_x, mouse_y),
                                velocity=Vector2D(0, 0),
                                external_charges=self.other_info["external_charges"],
                                slow_factor=self.other_info["slow_factor"]
                            )
                        )

                    # Neutron (4)
                    elif event.key == pygame.K_4:
                        self.add_object(
                            Neutron(
                                position=Point2D(mouse_x, mouse_y),
                                velocity=Vector2D(0, 0),
                                external_charges=self.other_info["external_charges"],
                                slow_factor=self.other_info["slow_factor"]
                            )
                        )

                    # Electron ring (5)
                    elif event.key == pygame.K_5:
                        for n in [1, 8, 16, 24]:
                            offset = n * 2
                            for i in range(n):
                                angle = 2 * math.pi * i / n
                                x = mouse_x + offset * math.cos(angle)
                                y = mouse_y + offset * math.sin(angle)
                                self.add_object(
                                    Electron(
                                        position=Point2D(x, y),
                                        velocity=Vector2D(0, 0),
                                        external_charges=self.other_info["external_charges"],
                                        slow_factor=self.other_info["slow_factor"]
                                    )
                                )

                    # Positron ring (6)
                    elif event.key == pygame.K_6:
                        for n in [1, 8, 16, 24]:
                            offset = n * 2
                            for i in range(n):
                                angle = 2 * math.pi * i / n
                                x = mouse_x + offset * math.cos(angle)
                                y = mouse_y + offset * math.sin(angle)
                                self.add_object(
                                    Positron(
                                        position=Point2D(x, y),
                                        velocity=Vector2D(0, 0),
                                        external_charges=self.other_info["external_charges"],
                                        slow_factor=self.other_info["slow_factor"]
                                    )
                                )

                    # Reset dynamic particles
                    elif event.key == pygame.K_r:
                        self.clear_dynamic_objects()

                    # Avoid error when pressing another key
                    else:
                        continue

            # Clear static layer if it's dirty
            if self.static_layer_dirty:
                self.static_layer.fill((0, 0, 0))
                # Draw static objects
                for obj in self.objects:
                    if not obj.dynamic:
                        obj.visual(screen=self.static_layer)
                self.static_layer_dirty = False

            # Blit pre-rendered static layer
            self.screen.blit(self.static_layer, (0, 0))

            # Update dynamic objects
            dynamic_objects = [obj for obj in self.objects if obj.dynamic]
            for obj in dynamic_objects[:]:
                update_data = obj.update(dt=dt, screen=self.screen)
                if "destroy" in update_data:
                    dynamic_objects.remove(obj)

            # Refresh the display
            pygame.display.flip()

        pygame.quit()
        sys.exit()

    def add_object(self, obj):
        """
        Adds an object (static or dynamic) to the simulation.

        :param obj: An object.
        """
        self.objects.append(obj)

        if not obj.dynamic:
            self.static_layer_dirty = True

    def clear_dynamic_objects(self):
        """
        Removes all dynamic objects from the simulation (e.g., moving particles).
        Static objects are preserved.
        """
        self.objects = [obj for obj in self.objects if not obj.dynamic]

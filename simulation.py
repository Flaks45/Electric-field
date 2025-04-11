import pygame
import sys

from charge import Charge
from coordinates import Vector2D, Point2D
from electron import Electron


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
        pygame.init()  # Initialize pygame
        self.width = width
        self.height = height

        # Create the window with the given dimensions
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Electric field simulation")  # Set the window's title

        self.charges = charges
        self.objects = []
        self.dynamic_objects = []

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
                    running = False  # Exit the loop if the window is closed

                if event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = event.pos
                    electron = Electron(Point2D(x, y), Vector2D(0, 0), self.charges)
                    self.add_dynamic_object(electron)

            # Fill the screen with black (you can change this color)
            self.screen.fill((0, 0, 0))

            # Draw all objects in the simulation
            for obj in self.objects:
                obj.draw(self.screen)

            # Update and draw dynamic objects
            for obj in self.dynamic_objects:
                obj.update(dt)
                obj.draw(self.screen)

            # Update the display with changes
            pygame.display.flip()

        pygame.quit()  # Quit pygame once the loop ends
        sys.exit()  # Exit the program

    def add_object(self, obj):
        """Adds an object to the simulation."""
        self.objects.append(obj)

    def add_dynamic_object(self, obj):
        """Adds a dynamic object to the simulation."""
        self.dynamic_objects.append(obj)

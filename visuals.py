import math
import pygame

from coordinates import Vector2D, Point2D


class VisualVector2D:
    """
    A class to visually represent a 2D vector as an arrow with its magnitude determining the color.
    If the vector is (0, 0), a dot will be drawn instead.
    """

    def __init__(self, vector, start_point=(0, 0)):
        """
        Initializes a VisualVector2D to represent a vector as an arrow or a dot.

        Args:
            vector (Vector2D): The vector to be represented visually.
            start_point (Point2D): The starting point for the arrow (default is (0, 0)).
        """
        self.vector = vector
        self.start_point = start_point

    def draw(self, screen):
        """
        Draws the vector as an arrow on the given pygame surface.
        If the vector is (0, 0), it draws a dot.

        Args:
            screen (pygame.Surface): The surface on which to draw the vector.
        """
        # Calculate the magnitude of the vector
        magnitude = math.sqrt(self.vector.x ** 2 + self.vector.y ** 2)

        # Map magnitude to a color (red for strong, blue for weak) using the original magnitude
        color_strength = min(max(magnitude / 50, 0), 1)  # Normalize magnitude to range [0, 1]
        red = int(255 * color_strength)  # Red becomes stronger as magnitude increases
        blue = int(255 * (1 - color_strength) / 2)  # Blue becomes weaker as magnitude increases
        color = (red, 0, blue)  # RGB color tuple

        # Clamp the magnitude: maximum of 100 and minimum of 5 (unless the vector is (0, 0))
        if magnitude == 0:
            clamped_magnitude = 0
        else:
            clamped_magnitude = max(min(magnitude, 50), 5)

        dot_treshold = 0
        # Scale the vector to the clamped magnitude
        if magnitude > dot_treshold:
            scale_factor = clamped_magnitude / magnitude
            self.vector.x *= scale_factor
            self.vector.y *= scale_factor

        # If the vector is (0, 0), draw a dot instead of an arrow
        if clamped_magnitude == dot_treshold:
            pygame.draw.circle(screen, color, (int(self.start_point.x), int(self.start_point.y)), 5)
            return

        # Calculate the end point of the arrow based on the vector's direction and clamped magnitude
        end_x = self.start_point.x + self.vector.x
        end_y = self.start_point.y + self.vector.y

        # Draw the line representing the vector
        pygame.draw.line(screen, color, (self.start_point.x, self.start_point.y), (end_x, end_y), 3)

        # Arrowhead
        arrow_length = max(min(clamped_magnitude / 5, 10), 3)  # Length of the arrowhead
        angle = math.atan2(self.vector.y, self.vector.x)  # Angle of the vector in radians

        # Calculate the points of the arrowhead
        arrow_point1 = (
            end_x - arrow_length * math.cos(angle - math.pi / 6), end_y - arrow_length * math.sin(angle - math.pi / 6))
        arrow_point2 = (
            end_x - arrow_length * math.cos(angle + math.pi / 6), end_y - arrow_length * math.sin(angle + math.pi / 6))

        # Draw the arrowhead (a triangle)
        pygame.draw.polygon(screen, color, [(end_x, end_y), arrow_point1, arrow_point2])


class VisualPoint2D:
    """
    A class to visually represent a 2D point as a circle with a label (e.g., "+" or "-").
    """

    def __init__(self, point: Point2D, label="", color=(255, 255, 255), radius=10):
        """
        Initializes a visual point with a label.

        Args:
            point (Point2D): The position of the point.
            label (str): Text to display inside the point, typically "+" or "-".
            color (tuple): The RGB color of the circle. Default is white.
            radius (int): Radius of the circle. Default is 10.
        """
        self.point = point
        self.label = label
        self.color = color
        self.radius = radius
        self.font = pygame.font.SysFont(None, int(radius * 2.5))  # Scales text to fit circle

    def draw(self, screen: pygame.Surface):
        """
        Draws the labeled point on the screen.

        Args:
            screen (pygame.Surface): The surface to draw on.
        """
        # Draw the circle
        pygame.draw.circle(screen, (255, 255, 255), (int(self.point.x), int(self.point.y)), self.radius + 2)  # Outline
        pygame.draw.circle(screen, self.color, (int(self.point.x), int(self.point.y)), self.radius)

        # Render the label in white
        text_surface = self.font.render(self.label, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=(int(self.point.x), int(self.point.y - 2)))
        screen.blit(text_surface, text_rect)

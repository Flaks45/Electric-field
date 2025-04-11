import math
import pygame

from coordinates import Vector2D, Point2D


class VisualVector2D:
    """
    A class to visually represent a 2D vector as an arrow with its magnitude determining the color.
    If the vector is (0, 0), a dot will be drawn instead.
    """

    def __init__(self, vector: Vector2D, start_point: Point2D = (0, 0)):
        """
        Initializes a VisualVector2D to represent a vector as an arrow or a dot.

        Args:
            vector (Vector2D): The vector to be represented visually.
            start_point (Point2D): The starting point for the arrow (default is (0, 0)).
        """
        self.vector = vector
        self.start_point = start_point

    def draw(self, screen: pygame.Surface):
        """
        Draws the vector as an arrow on the given pygame surface.
        If the vector is (0, 0), it draws a dot.

        Args:
            screen (pygame.Surface): The surface on which to draw the vector.
        """
        magnitude = math.sqrt(self.vector.x ** 2 + self.vector.y ** 2)

        # Set color of the arrow
        color_strength = min(max(magnitude / 50, 0), 1)
        red = int(255 * color_strength)
        green = 0
        blue = int(255 * (1 - color_strength) / 2)
        color = (red, green, blue)

        # Clamp the magnitude
        if magnitude == 0:
            clamped_magnitude = 0
        else:
            clamped_magnitude = max(min(magnitude, 50), 10)

        dot_treshold = 0

        if magnitude > dot_treshold:
            scale_factor = clamped_magnitude / magnitude

        # If the vector is (0, 0), draw a dot instead of an arrow
        if clamped_magnitude == dot_treshold:
            pygame.draw.circle(screen, color, (int(self.start_point.x), int(self.start_point.y)), 5)
            return

        end_x = self.start_point.x + self.vector.x * scale_factor
        end_y = self.start_point.y + self.vector.y * scale_factor

        # Draw the line representing the vector
        pygame.draw.line(screen, color, (self.start_point.x, self.start_point.y), (end_x, end_y), 3)

        # Arrowhead
        arrow_length = max(min(clamped_magnitude / 5, 10), 4)  # Length of the arrowhead
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

    def __init__(self, point: Point2D,
                 label: str = " ", color: tuple[int, int, int] = (255, 255, 255), radius: int = 10):
        """
        Initializes a visual point with a label.

        Args:
            point (Point2D): The position of the point.
            label (str): Text to display inside the point, typically "+" or "-".
            color (tuple[int, int, int]): The RGB color of the circle. Default is white.
            radius (int): Radius of the circle. Default is 10.
        """
        self.point = point
        self.label = label
        self.color = color
        self.radius = radius
        self.font = pygame.font.SysFont(None, int(self.radius * 3))

    def update_font(self):
        """
        Adjusts the font size to ensure the label text fits within a circle defined by the radius.

        The font size is initially set based on the radius, and reduced if the text width exceeds
        the circle's diameter. The size is adjusted until the text fits or the font height reaches
        a minimum of 5 pixels.

        Attributes:
            self.font (pygame.font.Font): The font used to render the label.
            self.label (str): The text label.
            self.radius (int): The radius of the circle.

        Notes:
            The font size decreases iteratively by 1 pixel until the text fits or the font height reaches 5.
        """
        self.font = pygame.font.SysFont(None, int(self.radius * 3))
        text_width, _ = self.font.size(self.label)

        while text_width > self.radius * 2 and self.font.get_height() > 5:  # 5 is the minimum font height limit
            self.font = pygame.font.SysFont(None, self.font.get_height() - 1)
            text_width, _ = self.font.size(self.label)

    def draw(self, screen: pygame.Surface):
        """
        Draws the labeled point on the screen.

        Args:
            screen (pygame.Surface): The surface to draw on.
        """
        pygame.draw.circle(screen, (255, 255, 255), (int(self.point.x), int(self.point.y)), self.radius + 2)
        pygame.draw.circle(screen, self.color, (int(self.point.x), int(self.point.y)), self.radius)

        # Render label
        text_surface = self.font.render(self.label, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=(int(self.point.x), int(self.point.y - 2)))
        screen.blit(text_surface, text_rect)

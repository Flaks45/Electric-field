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

    def draw(self, screen: pygame.Surface, magnitude_clamps: tuple[int, int, int] = (10, 50, 1),
             arrowhead_clamps: tuple[int, int, int] = (4, 10, 5), line_width: int = 3,
             dot_size: int = 5, dot_treshold: float = 0.1):
        """
        Draws the vector as an arrow on the given Pygame surface. If the vector is zero-length
        (magnitude equals `dot_treshold`), a dot is drawn instead.

        The color of the vector is determined by its magnitude, ranging from blue (low magnitude)
        to red (high magnitude). The magnitude and arrowhead size are clamped and scaled
        according to the provided tuples.

        Args:
            screen (pygame.Surface): The Pygame surface to draw the vector on.
            magnitude_clamps (tuple[int, int, int], optional): A tuple specifying
                (minimum length, maximum length, magnitude scaling factor).
                Used to clamp and scale the vector's drawn length. Default is (10, 50, 1).
            arrowhead_clamps (tuple[int, int, int], optional): A tuple specifying
                (minimum arrowhead size, maximum arrowhead size, arrowhead scaling factor).
                Used to scale and clamp the arrowhead length. Default is (4, 10, 5).
            line_width (int, optional): The width of the vector's line. Default is 3.
            dot_size (int, optional): Radius of the dot to draw when the vector's magnitude
                equals `dot_treshold`. Default is 5.
            dot_treshold (float, optional): The magnitude at which the vector is considered
                zero and a dot is drawn instead of an arrow. Default is 0.0.
        """
        magnitude = math.sqrt(self.vector.x ** 2 + self.vector.y ** 2)

        # Set color of the arrow
        color_strength = min(max(magnitude / 50, 0), 1)
        red = int(255 * color_strength)
        green = 0
        blue = int(255 * (1 - color_strength) / 2)
        color = (red, green, blue)

        # If the vector is (0, 0), draw a dot instead of an arrow
        if magnitude <= dot_treshold:
            pygame.draw.circle(screen, color, (int(self.start_point.x), int(self.start_point.y)), dot_size)
            return

        minimum_magnitude, maximum_magnitude, multiplier_magnitude = magnitude_clamps
        clamped_magnitude = max(min(magnitude / multiplier_magnitude, maximum_magnitude), minimum_magnitude)
        scale_factor = clamped_magnitude / magnitude

        end_x = self.start_point.x + self.vector.x * scale_factor
        end_y = self.start_point.y + self.vector.y * scale_factor

        # Draw the line representing the vector
        pygame.draw.line(screen, color, (self.start_point.x, self.start_point.y), (end_x, end_y), line_width)

        # Arrowhead
        minimum_arrowhead, maximum_arrowhead, multiplier_arrowhead = arrowhead_clamps
        arrow_length = max(min(clamped_magnitude / multiplier_arrowhead, maximum_arrowhead), minimum_arrowhead)
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

    def update_font(self, base_multiplier: float = 3.0, min_font_height: int = 5, font_name: str = None):
        """
        Adjusts the font size to ensure the label text fits within a circle defined by the radius.

        The font size starts at (radius * base_multiplier) and is reduced until the text width fits
        within the circle's diameter or the font height reaches `min_font_height`.

        Args:
            base_multiplier (float, optional): Multiplier to determine initial font size from radius. Default is 3.0.
            min_font_height (int, optional): Minimum allowable font height in pixels. Default is 5.
            font_name (str, optional): Name of the font to use (uses system default if None). Default is None.

        Attributes:
            self.font (pygame.font.Font): The final font used to render the label.
            self.label (str): The text label.
            self.radius (int): The radius of the circle.

        Returns:
            None
        """
        font_size = int(self.radius * base_multiplier)
        self.font = pygame.font.SysFont(font_name, font_size)
        text_width, _ = self.font.size(self.label)

        while text_width > self.radius * 2 and self.font.get_height() > min_font_height:
            font_size -= 1
            self.font = pygame.font.SysFont(font_name, font_size)
            text_width, _ = self.font.size(self.label)

    def draw(self, screen: pygame.Surface, label_color: tuple[int, int, int] = (255, 255, 255),
             outline: bool = True, outline_radius: int = 2, outline_color: tuple[int, int, int] = (255, 255, 255)):
        """
        Draws a labeled point (a circle with optional outline and a text label) on the given Pygame surface.

        The label is centered slightly above the point. If `outline` is enabled, an additional
        circle is drawn beneath the main one to create an outline effect.

        Args:
            screen (pygame.Surface): The surface to draw the point and label on.
            label_color (tuple[int, int, int], optional): RGB color of the label text. Default is white (255, 255, 255).
            outline (bool, optional): Whether to draw an outline around the point. Default is True.
            outline_radius (int, optional): The extra radius for the outline circle. Default is 2.
            outline_color (tuple[int, int, int], optional): RGB color of the outline. Default is white (255, 255, 255).
        """
        if outline:
            pygame.draw.circle(screen, outline_color, (int(self.point.x), int(self.point.y)), self.radius + outline_radius)
        pygame.draw.circle(screen, self.color, (int(self.point.x), int(self.point.y)), self.radius)

        # Render label
        text_surface = self.font.render(self.label, True, label_color)
        text_rect = text_surface.get_rect(center=(int(self.point.x), int(self.point.y - 2)))
        screen.blit(text_surface, text_rect)

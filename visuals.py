import math
import pygame

from coordinates import Vector2D


class VisualVector2D:
    """
    A visual representation of a 2D vector.
    """

    def __init__(self, vector: Vector2D):
        """
        Initializes the VisualVector2D with a given vector.

        :param vector: An instance of Vector2D representing the direction and magnitude.
        """
        self.vector = vector

    def draw(self, **kwargs):
        """
        Draws the vector on a given surface. Arrow color, thickness, and appearance change
        based on magnitude. A dot is drawn instead if the vector is near-zero.

        Expected kwargs:
            - screen: pygame Surface to draw on.
            - position: Vector2D, starting position of the arrow.
            - magnitude_clamps: tuple of (min, max, multiplier) to scale visual length.
            - arrowhead_clamps: tuple of (min, max, multiplier) to scale arrowhead size.
            - line_width: integer width of the arrow line.
            - dot_size: integer radius of the fallback dot.
            - dot_treshold: float, below which a dot is drawn instead of an arrow.
        """
        screen = kwargs["screen"]
        position = kwargs["position"]

        if "magnitude_clamps" not in kwargs:
            magnitude_clamps = (10, 50, 1)
        else:
            magnitude_clamps = kwargs["magnitude_clamps"]

        if "arrowhead_clamps" not in kwargs:
            arrowhead_clamps = (4, 10, 5)
        else:
            arrowhead_clamps = kwargs["arrowhead_clamps"]

        if "line_width" not in kwargs:
            line_width = 3
        else:
            line_width = kwargs["line_width"]

        if "dot_size" not in kwargs:
            dot_size = 4
        else:
            dot_size = kwargs["dot_size"]

        if "dot_treshold" not in kwargs:
            dot_treshold = 0.1
        else:
            dot_treshold = kwargs["dot_treshold"]

        magnitude = math.sqrt(self.vector.x ** 2 + self.vector.y ** 2)

        # Set color of the arrow
        color_strength = min(max(magnitude / 50, 0), 1)
        red = int(255 * color_strength)
        green = 0
        blue = int(255 * (1 - color_strength) / 2)
        color = (red, green, blue)

        # If the vector is (0, 0), draw a dot instead of an arrow
        if magnitude <= dot_treshold:
            pygame.draw.circle(screen, color, (int(position.x), int(position.y)), dot_size)
            return

        minimum_magnitude, maximum_magnitude, multiplier_magnitude = magnitude_clamps
        clamped_magnitude = max(min(magnitude / multiplier_magnitude, maximum_magnitude), minimum_magnitude)
        scale_factor = clamped_magnitude / magnitude

        end_x = position.x + self.vector.x * scale_factor
        end_y = position.y + self.vector.y * scale_factor

        # Draw the line representing the vector
        pygame.draw.line(screen, color, (position.x, position.y), (end_x, end_y), line_width)

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
    A visual representation of a 2D point.
    """

    def __init__(self,
                 color: tuple[int, int, int] = (255, 255, 255), radius: int = 10,
                 outline: bool = True, outline_radius: int = 2, outline_color: tuple[int, int, int] = (255, 255, 255),
                 label: str = " ", label_color: tuple[int, int, int] = (255, 255, 255), font_name: str = None):
        """
        Initializes a VisualPoint2D with visual attributes and optional label.

        :param color: RGB tuple for the point fill.
        :param radius: Radius of the point circle.
        :param outline: Whether to draw an outline around the point.
        :param outline_radius: Width of the outline.
        :param outline_color: RGB tuple for the outline.
        :param label: Optional text to display at the point.
        :param label_color: RGB tuple for the label text.
        :param font_name: Optional font name for rendering the label.
        """
        # Drawing info
        self.color = color
        self.radius = radius
        self.outline = outline
        self.outline_radius = outline_radius
        self.outline_color = outline_color

        # Label info
        self.label = label
        self.label_color = label_color
        self.font_name = font_name
        self.font = self.get_font()

    def get_font(self, base_multiplier: float = 3.0, min_font_height: int = 5):
        """
        Returns a pygame Font object that fits the label inside the point radius.

        :param base_multiplier: Multiplier to determine initial font size.
        :param min_font_height: Minimum font height before stopping reduction.
        :return: pygame Font object.
        """
        font_size = int(self.radius * base_multiplier)
        font = pygame.font.SysFont(self.font_name, font_size)
        text_width, _ = font.size(self.label)

        while text_width > self.radius * 2 and font.get_height() > min_font_height:
            font_size -= 2
            font = pygame.font.SysFont(self.font_name, font_size)
            text_width, _ = font.size(self.label)

        return font

    def draw(self, **kwargs):
        """
        Draws the point, outline (optional), and label (optional) on the screen.

        Expected kwargs:
            - screen: pygame Surface to draw on.
            - position: Vector2D specifying point location on the screen.
        """
        if "screen" not in kwargs:
            return

        screen = kwargs["screen"]
        position = kwargs["position"]

        if self.outline:
            pygame.draw.circle(screen, self.outline_color, (int(position.x), int(position.y)),
                               self.radius + self.outline_radius)
        pygame.draw.circle(screen, self.color, (int(position.x), int(position.y)), self.radius)

        # Render label
        text_surface = self.font.render(self.label, True, self.label_color)
        text_rect = text_surface.get_rect(center=(int(position.x), int(position.y - 2)))
        screen.blit(text_surface, text_rect)

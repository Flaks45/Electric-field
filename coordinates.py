from dataclasses import dataclass
import math


@dataclass
class Point2D:
    """
    Represents a point in 2D space.

    Attributes:
        x (float): The x-coordinate.
        y (float): The y-coordinate.
    """
    x: float = 0
    y: float = 0


@dataclass
class Vector2D:
    """
    Represents a 2D vector used for direction, velocity, or acceleration.

    Attributes:
        x (float): The x component.
        y (float): The y component.
    """
    x: float
    y: float

    def normalize(self) -> "Vector2D":
        """Returns a unit vector pointing in the same direction."""
        magnitude = math.sqrt(self.x**2 + self.y**2)
        if magnitude > 0:
            return Vector2D(self.x / magnitude, self.y / magnitude)
        return Vector2D(0, 0)  # Return zero vector if already zero

    @staticmethod
    def from_points(p1: Point2D, p2: Point2D) -> "Vector2D":
        """Creates a vector going from p1 to p2."""
        return Vector2D(p2.x - p1.x, p2.y - p1.y)

    def __mul__(self, scalar: float) -> "Vector2D":
        """Scales the vector by a scalar."""
        return Vector2D(self.x * scalar, self.y * scalar)

    def __rmul__(self, scalar: float) -> "Vector2D":
        """Enables scalar * vector multiplication."""
        return self.__mul__(scalar)

    def __truediv__(self, scalar: float) -> "Vector2D":
        """Divides the vector by a scalar."""
        if scalar == 0:
            raise ZeroDivisionError("Cannot divide vector by zero.")
        return Vector2D(self.x / scalar, self.y / scalar)

    def __add__(self, other: "Vector2D") -> "Vector2D":
        """Adds two vectors component-wise."""
        return Vector2D(self.x + other.x, self.y + other.y)

    def __sub__(self, other: "Vector2D") -> "Vector2D":
        """Subtracts two vectors component-wise."""
        return Vector2D(self.x - other.x, self.y - other.y)


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
        x (float): The x component of the vector.
        y (float): The y component of the vector.
    """
    x: float = 0
    y: float = 0

    def normalize(self) -> "Vector2D":
        """
        Returns a unit vector pointing in the same direction.

        The unit vector is a vector of magnitude 1 that points in the same
        direction as the current vector.

        Returns:
            Vector2D: A new vector that is the unit vector in the same direction.

        Notes:
            If the vector is already a zero vector (magnitude = 0), it returns a zero vector.
        """
        magnitude = math.sqrt(self.x ** 2 + self.y ** 2)
        if magnitude > 0:
            return Vector2D(self.x / magnitude, self.y / magnitude)
        return Vector2D(0, 0)  # Return zero vector if already zero

    @staticmethod
    def from_points(p1: "Point2D", p2: "Point2D") -> "Vector2D":
        """
        Creates a vector going from point p1 to point p2.

        Args:
            p1 (Point2D): The starting point of the vector.
            p2 (Point2D): The ending point of the vector.

        Returns:
            Vector2D: A new vector representing the direction and magnitude
                      from p1 to p2.
        """
        return Vector2D(p2.x - p1.x, p2.y - p1.y)

    def __mul__(self, scalar: float) -> "Vector2D":
        """
        Scales the vector by a scalar.

        Args:
            scalar (float): The scalar value to multiply the vector by.

        Returns:
            Vector2D: A new vector that is scaled by the given scalar.
        """
        return Vector2D(self.x * scalar, self.y * scalar)

    def __rmul__(self, scalar: float) -> "Vector2D":
        """
        Enables scalar * vector multiplication.

        This method ensures that the scalar can be on the left-hand side
        of the multiplication operator.

        Args:
            scalar (float): The scalar value to multiply the vector by.

        Returns:
            Vector2D: A new vector that is scaled by the given scalar.
        """
        return self.__mul__(scalar)

    def __truediv__(self, scalar: float) -> "Vector2D":
        """
        Divides the vector by a scalar.

        Args:
            scalar (float): The scalar value to divide the vector by.

        Returns:
            Vector2D: A new vector that is the result of the division.

        Raises:
            ZeroDivisionError: If attempting to divide by zero.
        """
        if scalar == 0:
            raise ZeroDivisionError("Cannot divide vector by zero.")
        return Vector2D(self.x / scalar, self.y / scalar)

    def __add__(self, other: "Vector2D") -> "Vector2D":
        """
        Adds two vectors component-wise.

        Args:
            other (Vector2D): The vector to add to the current vector.

        Returns:
            Vector2D: A new vector that is the sum of the two vectors.
        """
        return Vector2D(self.x + other.x, self.y + other.y)

    def __sub__(self, other: "Vector2D") -> "Vector2D":
        """
        Subtracts two vectors component-wise.

        Args:
            other (Vector2D): The vector to subtract from the current vector.

        Returns:
            Vector2D: A new vector that is the difference of the two vectors.
        """
        return Vector2D(self.x - other.x, self.y - other.y)

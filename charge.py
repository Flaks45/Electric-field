import math

from coordinates import Point2D, Vector2D


class Charge:
    """
    Positive or negative charge in an electric field.

    Attributes:
        value (float): Charge value in [C].
        position (Point2D): Position of the charge in space.
        permittivity (float, optional): Electric field permittivity in [F/m]. Default is permittivity of free space.
    """

    def __init__(self, value: float, position: Point2D, permittivity: float = 8.8542e-12):
        """
        Initializes a charge object with the given value, position, and optional permittivity.

        Args:
            value (float): The value of the charge in Coulombs.
            position (Point2D): The position of the charge.
            permittivity (float, optional): The permittivity of the medium, default is the permittivity of free space.
        """
        self.value = value
        self.position = position

        # Constants
        self.permittivity = permittivity  # Vacuum permittivity [F/m]
        self.k = 1 / (4 * math.pi * self.permittivity)  # Coulomb's constant

    def calculate_field(self, other_position: Point2D) -> Vector2D:
        """
        Calculates the electric field vector at a given point caused by this charge.

        The electric field due to a point charge is given by:

            E = (k * Q) / r^2 * r̂

        Where:
            - E is the electric field vector,
            - k is Coulomb's constant: 1 / (4 * π * ε₀),
            - Q is the charge value,
            - r is the distance from the charge to the point where the field is being evaluated,
            - r̂ is the unit vector in the direction from the charge to the point.

        Args:
            other_position (Point2D): The point where the field is evaluated.

        Returns:
            Vector2D: The electric field vector at that point.
        """
        # Vector from charge to the other point
        direction = Vector2D.from_points(self.position, other_position)
        distance_squared = direction.x**2 + direction.y**2

        if distance_squared == 0:
            return Vector2D(0, 0)  # No field at the exact location of the charge

        unit_vector = direction.normalize()
        field_magnitude = self.k * self.value / distance_squared

        return field_magnitude * unit_vector

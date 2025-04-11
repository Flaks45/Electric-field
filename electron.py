from charge import Charge
from coordinates import Point2D, Vector2D
from visuals import VisualPoint2D


class Electron(VisualPoint2D):
    """
    Electron represented as a charged particle in 2D space.

    Attributes:
        position (Point2D): Current position of the electron.
        velocity (Vector2D): Current velocity of the electron.
        mass (float): Mass of the electron in [kg].
        charge (float): Charge of the electron in [C] (always negative).
        external_charges (list[Charge]): List of external charges exerting force.
    """

    def __init__(self, position: Point2D, velocity: Vector2D, external_charges: list[Charge]):
        super().__init__(position)
        self.position = position
        self.velocity = velocity
        self.mass = 9.109e-31  # kg
        self.charge = -1.602e-19  # C

        self.color = (0, 255, 0)
        self.label = "e-"

        self.external_charges = external_charges

    def calculate_force(self) -> Vector2D:
        """
        Calculates the electrostatic force exerted by an electric field on the electron.

        Returns:
            Vector2D: Force vector acting on the electron.
        """
        field = Vector2D(0, 0)
        for c in self.external_charges:
            field += c.calculate_field(Point2D(self.position.x, self.position.y))

        return self.charge * field  # F = qE

    def move(self, net_force: Vector2D, dt: float):
        """
        Updates the electron's position based on the net force and time step.

        Args:
            net_force (Vector2D): The net force acting on the electron.
            dt (float): Time step in seconds.
        """
        slow_factor = 10e4
        dt = dt / slow_factor

        # F = ma => a = F / m
        acceleration = net_force / self.mass

        # Update velocity and position
        self.velocity = self.velocity + acceleration * dt
        displacement = self.velocity * dt
        self.position = Point2D(
            self.position.x + displacement.x,
            self.position.y + displacement.y
        )

    def update(self, dt: float):
        self.move(self.calculate_force(), dt)
        self.point = self.position

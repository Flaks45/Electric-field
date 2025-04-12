from charge import Charge
from coordinates import Point2D, Vector2D
from visuals import VisualPoint2D


class Particle(VisualPoint2D):
    """
    Particle represented as a charged particle in 2D space.

    Attributes:
        position (Point2D): Current position of the particle.
        velocity (Vector2D): Current velocity of the particle.
        external_charges (list[Charge]): List of external charges exerting force on the particle.
        mass (float): Mass of the particle in [kg].
        charge (float): Charge of the particle in [C].
    """

    def __init__(self, position: Point2D, velocity: Vector2D, external_charges: list[Charge]):
        """
        Initializes a particle with the given position, velocity, and external charges.

        Args:
            position (Point2D): The initial position of the particle.
            velocity (Vector2D): The initial velocity of the particle.
            external_charges (list[Charge]): List of external charges affecting the particle.
        """
        super().__init__(position)
        self.position = position
        self.velocity = velocity
        self.external_charges = external_charges
        self.slow_factor = 10e4  # Factor to adjust the speed of movement

        # Default values to be overridden
        self.mass = 1  # kg
        self.charge = 0  # C
        self.color = (0, 0, 0)  # Default color (black)
        self.label = "NaN"  # Default label for the particle

    def calculate_force(self) -> Vector2D:
        """
        Calculates the electrostatic force exerted by an electric field on the particle.

        The force on a charged particle is given by:
            F = qE
        Where:
            - F is the force on the particle,
            - q is the charge of the particle,
            - E is the electric field at the particle's location.

        Returns:
            Vector2D: Force vector acting on the particle.
        """
        field = Vector2D(0, 0)
        for c in self.external_charges:
            field += c.calculate_field(Point2D(self.position.x, self.position.y))

        return self.charge * field  # Return the force F = qE

    def move(self, net_force: Vector2D, dt: float):
        """
        Updates the particle's position based on the net force and time step.

        The particle's motion is governed by Newton's second law:
            F = ma => a = F / m
        Where:
            - F is the net force on the particle,
            - m is the mass of the particle,
            - a is the acceleration.

        Args:
            net_force (Vector2D): The net force acting on the particle.
            dt (float): Time step in seconds.
        """
        dt = dt / self.slow_factor  # Apply slow factor to reduce speed

        # Calculate acceleration
        acceleration = net_force / self.mass

        # Update velocity and position
        self.velocity = self.velocity + acceleration * dt
        displacement = self.velocity * dt
        self.position = Point2D(
            self.position.x + displacement.x,
            self.position.y + displacement.y
        )

    def update(self, dt: float):
        """
        Updates the particle's state by calculating the force and moving it.

        Args:
            dt (float): Time step in seconds.
        """
        self.move(self.calculate_force(), dt)

        out_of_bounds_conditions = [
            self.position.x < 0 - self.radius,
            self.position.x > 800 + self.radius,
            self.position.y < 0 - self.radius,
            self.position.y > 800 + self.radius,
        ]
        if any(out_of_bounds_conditions):
            return False

        # Update the visual representation
        self.point = self.position
        return True


class Electron(Particle):
    """
    Represents an electron particle.

    Inherits from Particle and sets specific values for an electron:
        - Mass: 9.109e-31 kg
        - Charge: -1.602e-19 C (negative charge)
        - Color: Green
        - Label: "e-"
    """
    def __init__(self, position: Point2D, velocity: Vector2D, external_charges: list[Charge]):
        super().__init__(position, velocity, external_charges)

        self.mass = 9.109e-31  # kg (mass of electron)
        self.charge = -1.602e-19  # C (charge of electron)
        self.color = (0, 150, 0)  # Green color
        self.label = "e-"  # Electron label
        self.radius = 7

        self.update_font()


class Proton(Particle):
    """
    Represents a proton particle.

    Inherits from Particle and sets specific values for a proton:
        - Mass: 1.673e-27 kg
        - Charge: 1.602e-19 C (positive charge)
        - Color: Purple
        - Label: "p+"
    """
    def __init__(self, position: Point2D, velocity: Vector2D, external_charges: list[Charge]):
        super().__init__(position, velocity, external_charges)

        self.mass = 1.673e-27  # kg (mass of proton)
        self.charge = 1.602e-19  # C (charge of proton)
        self.color = (150, 0, 150)  # Purple color
        self.label = "p+"  # Proton label
        self.radius = 9

        self.update_font()


class Neutron(Particle):
    """
    Represents a neutron particle.

    Inherits from Particle and sets specific values for a neutron:
        - Mass: 1.675e-27 kg (mass of a neutron)
        - Charge: 0 C (no charge)
        - Color: Gray
        - Label: "n"
    """
    def __init__(self, position: Point2D, velocity: Vector2D, external_charges: list[Charge]):
        super().__init__(position, velocity, external_charges)

        self.mass = 1.675e-27  # kg (mass of neutron)
        self.charge = 0  # C (no charge)
        self.color = (150, 150, 150)  # Gray color
        self.label = "n"  # Neutron label
        self.radius = 9

        self.update_font()

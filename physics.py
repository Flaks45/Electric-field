import math

from coordinates import Point2D, Vector2D


class ChargeLogic:
    """
    Represents a point charge in the simulation, including its electric field computation.
    """

    def __init__(self, value: float, permittivity: float = 8.8542e-12):
        """
        Initializes the charge with its value and the physical constant for the vacuum permittivity.

        :param value: Charge value (Coulombs).
        :param permittivity: Vacuum permittivity constant (default is 8.8542e-12 [F/m]).
        """
        self.value = value

        # Constants
        self.permittivity = permittivity  # Vacuum permittivity [F/m]
        self.k = 1 / (4 * math.pi * self.permittivity)  # Coulomb's constant

    def calculate_field(self, position: Point2D, other_position: Point2D) -> Vector2D:
        """
        Calculates the electric field at a given point due to this charge.

        The electric field is calculated using Coulomb's law:
            E = (k * Q) / r^2 * r̂

        :param position: The position where the charge is.
        :param other_position: The position at which to evaluate the electric field.
        :return: The electric field vector at the specified position.
        """
        # Vector from charge to the other point
        direction = Vector2D.from_points(position, other_position)
        distance_squared = direction.x ** 2 + direction.y ** 2

        if distance_squared == 0:
            return Vector2D(0, 0)  # No field at the exact location of the charge

        unit_vector = direction.normalize()
        field_magnitude = self.k * self.value / distance_squared

        return field_magnitude * unit_vector

    def run(self, **kwargs):
        """
        Static method that does nothing when run. Placeholder for potential dynamic behavior.
        """
        position = kwargs["position"]
        if "other_position" in kwargs:
            other_position = kwargs["other_position"]
            field = self.calculate_field(position=position, other_position=other_position)
            return {"position": position, "field": field}

        return {"position": position}


class ParticleLogic:
    """
    Represents a particle subject to forces from external charges and its movement dynamics.
    """

    def __init__(self, velocity: Vector2D, external_charges: list, slow_factor: int,
                 mass: float, charge: float):
        """
        Initializes the particle with its velocity, external charge influences, and physical properties.

        :param velocity: The initial velocity vector of the particle.
        :param external_charges: A list of external charges affecting the particle.
        :param slow_factor: A factor to reduce the particle's speed.
        :param mass: The particle's mass.
        :param charge: The particle's charge.
        """
        self.velocity = velocity
        self.external_charges = external_charges
        self.slow_factor = slow_factor
        self.mass = mass
        self.charge = charge

    def calculate_force(self, position: Point2D) -> Vector2D:
        """
        Calculates the net force on the particle due to all external charges.

        The net force is determined by the sum of the forces from each charge:

            F = qE

        :param position: The position of the particle at which to evaluate the force.
        :return: The net force on the particle due to all external charges.
        """
        field = Vector2D(0, 0)
        for c in self.external_charges:
            update_data = c.update(other_position=Point2D(position.x, position.y))
            field += update_data["field"]

        return self.charge * field  # Return the force F = qE

    def move(self, position: Point2D, net_force: Vector2D, dt: float):
        """
        Moves the particle based on the computed net force and velocity, applying the slow factor.

        :param position: The current position of the particle.
        :param net_force: The net force acting on the particle.
        :param dt: The time step to calculate the particle's new position.
        :return: The new position of the particle after the move.
        """
        dt = dt / self.slow_factor  # Apply slow factor to reduce speed

        # Calculate acceleration
        acceleration = net_force / self.mass

        # Update velocity and position
        self.velocity = self.velocity + acceleration * dt
        displacement = self.velocity * dt
        position = Point2D(
            position.x + displacement.x,
            position.y + displacement.y
        )
        return {
            "position": position,
            "velocity": self.velocity,
            "acceleration": acceleration,
            "force": net_force
        }

    def run(self, **kwargs):
        """
        Updates the particle's position by calculating the force and applying the motion logic.

        :param kwargs: Keyword arguments containing 'dt' (time step) and 'position'.
        :return: A dictionary containing the updated position of the particle.
        """
        dt = kwargs["dt"]
        position = kwargs["position"]
        move_data = self.move(position, self.calculate_force(position), dt)

        what_is_other_position = "force"
        if what_is_other_position == "velocity":
            other_position = move_data["velocity"] * 2 * 10e-7
        elif what_is_other_position == "acceleration":
            other_position = move_data["acceleration"] * 5 * 10e-13
        else:
            other_position = move_data["force"] * 10e18

        return {
            "position": move_data["position"],
            "other_position": other_position,
            "width_clamps": (5, 10, 0.7),
            "arrowhead_clamps": (10, 25, 3),
            "magnitude_clamps": (25, 60, 1)
        }

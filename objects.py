from coordinates import Vector2D
from entity import Entity
from physics import ChargeLogic, ParticleLogic
from visuals import VisualPoint2D, VisualVector2D

SHOW_FORCES = False


class Charge(Entity):
    """
    Represents a charge in the simulation, either positive or negative.
    """

    def __init__(self, **kwargs):
        """
        Initializes the charge with its value, position, and visual representation.

        Expected kwargs:
            - position: Position of the charge in space.
            - value: Value of the charge (positive for positive charge, negative for negative charge).
        """

        # General data
        position = kwargs["position"]
        value = kwargs["value"]

        # Visual data
        radius = 15
        outline = True
        outline_radius = 2
        outline_color = (255, 255, 255)

        if value == 0:
            color = (150, 150, 150)
            label = " "
        elif value > 0:
            color = (255, 0, 0)
            label = "+"
        elif value < 0:
            color = (0, 0, 255)
            label = "-"
        else:
            raise ValueError(f"Value is not a number: {value}")

        # Get objects
        visual_point = VisualPoint2D(
            color,
            radius,
            outline,
            outline_radius,
            outline_color,
            label
        )

        charge_logic = ChargeLogic(
            value
        )

        super().__init__([visual_point], [charge_logic], False, position)
        self.charge_logic = charge_logic


class Field(Entity):
    """
    Represents the electric field at a specific position due to external charges.
    """

    def __init__(self, **kwargs):
        """
        Initializes the electric field with the given vector and position.

        Expected kwargs:
            - position: Position where the field is evaluated.
            - vector: The electric field vector at the given position.
        """
        # General data
        position = kwargs["position"]
        vector = kwargs["vector"]

        # Get objects
        visual_vector = VisualVector2D(
            vector
        )

        super().__init__([visual_vector], [], False, position)


class Electron(Entity):
    """
    Represents an electron in the simulation, including its charge, mass, and behavior under forces.
    """

    def __init__(self, **kwargs):
        """
        Initializes the electron with its position, velocity, mass, charge, and external influences.

       Expected kwargs:
            - position: The starting position of the electron.
            - velocity: The initial velocity vector of the electron.
            - external_charges: List of external charges influencing the electron's movement.
            - slow_factor: A factor to slow down the electron's movement.
        """
        # General data
        position = kwargs["position"]

        # Logic data
        velocity = kwargs["velocity"]
        external_charges = kwargs["external_charges"]
        slow_factor = kwargs["slow_factor"]
        mass = 9.109e-31
        charge = -1.602e-19

        # Visual data
        color = (0, 150, 0)
        radius = 7
        outline = True
        outline_radius = 2
        outline_color = (255, 255, 255)
        label = "e-"

        # Get objects
        visual_point = VisualPoint2D(
            color,
            radius,
            outline,
            outline_radius,
            outline_color,
            label
        )

        if SHOW_FORCES:
            visual_vector = VisualVector2D(
                vector=Vector2D(0, 0),
                color_scheme="cyan-green"
            )

            visuals = [visual_point, visual_vector]
        else:
            visuals = [visual_point]

        particle_logic = ParticleLogic(
            velocity,
            external_charges,
            slow_factor,
            mass,
            charge
        )

        super().__init__(visuals, [particle_logic], True, position)


class Positron(Entity):
    """
    Represents a positron in the simulation, including its charge, mass, and behavior under forces.
    """

    def __init__(self, **kwargs):
        """
        Initializes the positron with its position, velocity, mass, charge, and external influences.

        Expected kwargs:
            - position: The starting position of the positron.
            - velocity: The initial velocity vector of the positron.
            - external_charges: List of external charges influencing the positron's movement.
            - slow_factor: A factor to slow down the positron's movement.
        """
        # General data
        position = kwargs["position"]

        # Logic data
        velocity = kwargs["velocity"]
        external_charges = kwargs["external_charges"]
        slow_factor = kwargs["slow_factor"]
        mass = 9.109e-31
        charge = 1.602e-19

        # Visual data
        color = (150, 150, 0)
        radius = 7
        outline = True
        outline_radius = 2
        outline_color = (255, 255, 255)
        label = "e+"

        # Get objects
        visual_point = VisualPoint2D(
            color,
            radius,
            outline,
            outline_radius,
            outline_color,
            label
        )

        if SHOW_FORCES:
            visual_vector = VisualVector2D(
                vector=Vector2D(0, 0),
                color_scheme="cyan-green"
            )

            visuals = [visual_point, visual_vector]
        else:
            visuals = [visual_point]

        particle_logic = ParticleLogic(
            velocity,
            external_charges,
            slow_factor,
            mass,
            charge
        )

        super().__init__(visuals, [particle_logic], True, position)


class Proton(Entity):
    """
    Represents a proton in the simulation, including its charge, mass, and behavior under forces.
    """

    def __init__(self, **kwargs):
        """
        Initializes the proton with its position, velocity, mass, charge, and external influences.

        Expected kwargs:
            - position: The starting position of the proton.
            - velocity: The initial velocity vector of the proton.
            - external_charges: List of external charges influencing the proton's movement.
            - slow_factor: A factor to slow down the proton's movement.
        """
        # General data
        position = kwargs["position"]

        # Logic data
        velocity = kwargs["velocity"]
        external_charges = kwargs["external_charges"]
        slow_factor = kwargs["slow_factor"]
        mass = 1.673e-27
        charge = 1.602e-19

        # Visual data
        color = (150, 0, 150)
        radius = 7
        outline = True
        outline_radius = 2
        outline_color = (255, 255, 255)
        label = "p+"

        # Get objects
        visual_point = VisualPoint2D(
            color,
            radius,
            outline,
            outline_radius,
            outline_color,
            label
        )

        if SHOW_FORCES:
            visual_vector = VisualVector2D(
                vector=Vector2D(0, 0),
                color_scheme="cyan-green"
            )

            visuals = [visual_point, visual_vector]
        else:
            visuals = [visual_point]

        particle_logic = ParticleLogic(
            velocity,
            external_charges,
            slow_factor,
            mass,
            charge
        )

        super().__init__(visuals, [particle_logic], True, position)


class Neutron(Entity):
    """
    Represents a neutron in the simulation, including its charge, mass, and behavior under forces.
    """

    def __init__(self, **kwargs):
        """
        Initializes the neutron with its position, velocity, mass, charge, and external influences.

        Expected kwargs:
            - position: The starting position of the neutron.
            - velocity: The initial velocity vector of the neutron.
            - external_charges: List of external charges influencing the neutron's movement.
            - slow_factor: A factor to slow down the neutron's movement.
        """
        # General data
        position = kwargs["position"]

        # Logic data
        velocity = kwargs["velocity"]
        external_charges = kwargs["external_charges"]
        slow_factor = kwargs["slow_factor"]
        mass = 1.675e-27
        charge = 0

        # Visual data
        color = (150, 150, 150)
        radius = 7
        outline = True
        outline_radius = 2
        outline_color = (255, 255, 255)
        label = "n"

        # Get objects
        visual_point = VisualPoint2D(
            color,
            radius,
            outline,
            outline_radius,
            outline_color,
            label
        )

        if SHOW_FORCES:
            visual_vector = VisualVector2D(
                vector=Vector2D(0, 0),
                color_scheme="cyan-green"
            )

            visuals = [visual_point, visual_vector]
        else:
            visuals = [visual_point]

        particle_logic = ParticleLogic(
            velocity,
            external_charges,
            slow_factor,
            mass,
            charge
        )

        super().__init__(visuals, [particle_logic], True, position)

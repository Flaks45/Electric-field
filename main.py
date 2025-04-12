import math
import pygame

from coordinates import Point2D, Vector2D
from objects import Charge, Field
from simulation import SimulationWindow

if __name__ == "__main__":
    pygame.font.init()  # Needed for the fonts

    charges = [
        Charge(value=-2.0e-5, position=Point2D(200, 200)),
        Charge(value=2.0e-5, position=Point2D(600, 200)),
        Charge(value=1.0e-5, position=Point2D(200, 600)),
        Charge(value=-1.0e-5, position=Point2D(600, 600)),
    ]

    slow_factor = 10e4
    simulation_window = SimulationWindow(other_info={"external_charges": charges, "slow_factor": slow_factor})

    # Draw electric field
    density = 20
    for w in range(0, 800 + density, density):
        for h in range(0, 800 + density, density):
            resulting_field = Vector2D(0, 0)
            for c in charges:
                update_data = c.update(other_position=Point2D(w, h))
                resulting_field += update_data["field"]

            simulation_window.add_object(Field(vector=resulting_field, position=Point2D(w, h)))

    # Draw charges
    for c in charges:
        simulation_window.add_object(c)

    simulation_window.run()

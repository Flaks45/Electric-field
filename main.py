import math

from charge import Charge
from coordinates import Point2D, Vector2D
from simulation import SimulationWindow
from visuals import VisualVector2D, VisualPoint2D

if __name__ == "__main__":
    charges = []

    for h in range(33):
        charges.append(Charge(-5.0e-6, Point2D(800, h * 800 / 32)))
        charges.append(Charge(-5.0e-6, Point2D(0, h * 800 / 32)))

    for w in range(1, 32):
        charges.append(Charge(-5.0e-6, Point2D(w * 800 / 32, 800)))
        charges.append(Charge(-5.0e-6, Point2D(w * 800 / 32, 0)))

    simulation_window = SimulationWindow(charges)

    # Draw electric field
    density = 20
    for w in range(0, 800 + density, density):
        for h in range(0, 800 + density, density):
            resulting_field = Vector2D(0, 0)
            for c in charges:
                resulting_field += c.calculate_field(Point2D(w, h))
            simulation_window.add_object(VisualVector2D(resulting_field, Point2D(w, h)))

    # Draw charges
    for c in charges:
        if c.value > 0:
            label = "+"
            color = (255, 0, 0)
        else:
            label = "-"
            color = (0, 0, 255)
        simulation_window.add_object(VisualPoint2D(c.position, label, color, 15))

    simulation_window.run()

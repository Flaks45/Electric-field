import math

from charge import Charge
from coordinates import Point2D, Vector2D
from electron import Electron
from simulation import SimulationWindow
from visuals import VisualVector2D, VisualPoint2D

if __name__ == "__main__":
    charges = [
        Charge(2.0e-5, Point2D(300, 400)),
        Charge(-2.0e-5, Point2D(500, 400)),
    ]

    simulation_window = SimulationWindow(charges)

    density = 20
    for w in range(0, 800 + density, density):
        for h in range(0, 800 + density, density):
            resulting_field = Vector2D(0, 0)
            for c in charges:
                resulting_field += c.calculate_field(Point2D(w, h))
            simulation_window.add_object(VisualVector2D(resulting_field, Point2D(w, h)))

    for c in charges:
        if c.value > 0:
            label = "+"
            color = (255, 0, 0)
        else:
            label = "-"
            color = (0, 0, 255)
        simulation_window.add_object(VisualPoint2D(c.position, label, color, 10))

    simulation_window.run()

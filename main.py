from coordinates import Point2D, Vector2D
from objects import Field
from premade_charges import premade_charges
from simulation import SimulationWindow


if __name__ == "__main__":
    charges = premade_charges[13]

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

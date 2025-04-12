# Electric Field Simulator
[![Project Banner](assets/banner.png)](https://github.com/Flaks45/Electric-field)

A visual simulator for electric fields with interactive particle dynamics.

# Installation
**Python 3.9 or higher is required.**
To install the dependencies for this project run the following command:
```bash
# Linux/macOS
python3 -m pip install -r requirements.txt

# Windows
py -3 -m pip install -r requirements.txt
```

# Usage
Run the simulation with `main.py`.

<div>
  <img src="assets/field_example_1.png" width="50%">
</div>

This will launch the main window. Charges are hardcoded in main.py, so edit that file to customize, add, or remove them. 
You can use as many charges as you like.
> ⚠️ Charge values should be in the microcoulomb (µC) range for reasonable results.

# Field Examples
<div>
  <img src="assets/field_example_2.png" width="30%">
  <img src="assets/field_example_3.png" width="30%">
  <img src="assets/field_example_4.png" width="30%">
</div>

The canvas size is **800×800 meters**, so coordinate values and distances are treated as real-world scale.

# Physics
Force on a particle is calculated using the electric field equation:
```math
\vec{F} = q\vec{E}
```
Each individual field contribution follows:
```math
\vec{E}_n = \frac{1}{4\pi\varepsilon_0} \cdot \frac{q_n}{r_n^2} \hat{r}_n
```

# Particle Simulation
Particles can be added interactively during the simulation. **They will at your mouse position.**
> Controls (keyboard):
- `1` Electron.
- `2` Proton.
- `3` Neutron.
- `4` Electron ring.

Simulations with electrons:
<div>
  <img src="assets/field_demo_1.gif" width="30%">
  <img src="assets/field_demo_3.gif" width="30%">
  <img src="assets/field_demo_4.gif" width="30%">
</div>

Neutron and proton interaction example:
<div>
  <img src="assets/field_demo_2.gif" width="50%">
</div>

# Notes
- Neutrons have no charge and do not respond to the field but are included for reference.
- **Time has been slowed down in the simulation.** Search for `self.slow_factor` in `particle.py` if you wish to change it. Default value is at 1 second every 10000 steps (or 1 second every 10000 simulation seconds).

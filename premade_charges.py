import math
import pygame
import random

from coordinates import Point2D
from objects import Charge

pygame.font.init()  # Needed for the fonts

premade_charges = [
        # 0: Two opposite charges (negative and positive) horizontally aligned at (200, 400) and (600, 400)
        [
            Charge(value=-2.0e-5, position=Point2D(200, 400)),
            Charge(value=2.0e-5, position=Point2D(600, 400)),
        ],
        # 1: Four charges forming a square pattern at the corners of the 200x200 and 600x600 area
        [
            Charge(value=-1.0e-5, position=Point2D(200, 200)),
            Charge(value=1.0e-5, position=Point2D(600, 200)),
            Charge(value=1.0e-5, position=Point2D(200, 600)),
            Charge(value=-1.0e-5, position=Point2D(600, 600)),
        ],
        # 2: Four charges in a square pattern, but with alternating signs
        [
            Charge(value=-2.0e-5, position=Point2D(200, 200)),
            Charge(value=2.0e-5, position=Point2D(600, 200)),
            Charge(value=1.0e-5, position=Point2D(200, 600)),
            Charge(value=-1.0e-5, position=Point2D(600, 600)),
        ],
        # 3: 32 charges distributed in a circle with a radius of 300 pixels, centered at (400, 400)
        [
            Charge(value=-1.0e-5, position=Point2D(
                400 + 300 * math.cos(i * (2 * math.pi / 32)),
                400 + 300 * math.sin(i * (2 * math.pi / 32)))
                   ) for i in range(32)
        ],
        # 4: Charges placed along the borders of a square, negative values along the edges
        [
            Charge(value=-5.0e-6, position=Point2D(0, h * 800 / 32)) if i % 2 == 0 else
            Charge(value=-5.0e-6, position=Point2D(800, h * 800 / 32)) for h in range(33) for i in range(2)
        ] + [
            Charge(value=-5.0e-6, position=Point2D(w * 800 / 32, 0)) if i % 2 == 0 else
            Charge(value=-5.0e-6, position=Point2D(w * 800 / 32, 800)) for w in range(1, 32) for i in range(2)
        ],
        # 5: Charges along the edges of the square, alternating between negative and positive values
        [
            Charge(value=-5.0e-6, position=Point2D(0, h * 800 / 32)) if i % 2 == 0 else
            Charge(value=5.0e-6, position=Point2D(800, h * 800 / 32)) for h in range(33) for i in range(2)
        ] + [
            Charge(value=5.0e-6, position=Point2D(w * 800 / 32, 0)) if i % 2 == 0 else
            Charge(value=-5.0e-6, position=Point2D(w * 800 / 32, 800)) for w in range(1, 32) for i in range(2)
        ],
        # 6: Similar to index 4 but with the alternating charges being positive and negative
        [
            Charge(value=-5.0e-6, position=Point2D(0, h * 800 / 32)) if i % 2 == 0 else
            Charge(value=-5.0e-6, position=Point2D(800, h * 800 / 32)) for h in range(33) for i in range(2)
        ] + [
            Charge(value=5.0e-6, position=Point2D(w * 800 / 32, 0)) if i % 2 == 0 else
            Charge(value=5.0e-6, position=Point2D(w * 800 / 32, 800)) for w in range(1, 32) for i in range(2)
        ],
        # 7: A list of randomly generated charges with random positions and values
        [
            Charge(
                value=random.uniform(-2.0e-5, 2.0e-5),
                position=Point2D(random.randint(0, 800), random.randint(0, 800))
            ) for _ in range(random.randint(10, 15))
        ],
        # 8: A single charge at the center (400, 400) with a value of 0
        [
            Charge(value=0, position=Point2D(400, 400))
        ],
        # 9: A bigger list of randomly generated charges with random positions and values
        [
            Charge(
                value=random.uniform(-1.0e-5, 1.0e-5),
                position=Point2D(random.randint(0, 800), random.randint(0, 800))
            ) for _ in range(random.randint(60, 70))
        ],
        # 10: A bottle-like shape or negative charges
        [
            Charge(value=-2.0e-5, position=Point2D(x, y))
            for x in [300, 500]
            for y in [100, 700]
        ] + [
            Charge(value=-2.0e-5, position=Point2D(x, y))
            for x in [200, 600]
            for y in [200, 300, 400, 500, 600]
        ],
        # 11: A stream of negative charges in a vertical shape
        [
            Charge(value=-2.0e-5, position=Point2D(x, y))
            for x in [300, 500]
            for y in [100, 200, 300, 400, 500, 600, 700]
        ],
        # 12: Many neutral charges in a grid pattern
        [
            Charge(value=0, position=Point2D(x, y))
            for x in range(0, 900, 100)
            for y in range(0, 900, 100)
        ],
        # 13: Medium sized list of randomly generated charges with random positions and values
        [
            Charge(
                value=random.uniform(-1.0e-5, 1.0e-5),
                position=Point2D(random.randint(0, 800), random.randint(0, 800))
            ) for _ in range(random.randint(25, 35))
        ]
    ]
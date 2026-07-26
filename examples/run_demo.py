"""Kør ChromaPlex fuld potential-demo."""

import numpy as np
from chromaplex import CrystalSimulator
from chromaplex.utils import (
    exponent_remainder_to_number,
    luminance_to_ascii,
    number_to_exponent_remainder,
)

def run_full_demo():
    width, height = 10, 10
    sim = CrystalSimulator(size=50)

    # Opret testbillede
    original = np.zeros((height, width, 3), dtype=np.uint8)
    for y in range(height):
        for x in range(width):
            original[y, x] = [
                int(30 + 20 * np.sin(x / 2)),
                int(100 + 50 * np.cos(y / 2)),
                int(180 + 50 * np.sin((x + y) / 3))
            ]

    print("Skriver billede til krystal...")
    for y in range(height):
        for x in range(width):
            r, g, b = original[y, x]
            r_e, r_rest = number_to_exponent_remainder(int(r))
            g_e, g_rest = number_to_exponent_remainder(int(g))
            b_e, b_rest = number_to_exponent_remainder(int(b))
            sim.pack(x, y, 0, [("rød", r_e), ("grøn", g_e), ("blå", b_e)])
            vox = sim.grid[x][y][0]
            vox.channels["rød"]["rest"] = r_rest
            vox.channels["grøn"]["rest"] = g_rest
            vox.channels["blå"]["rest"] = b_rest

    print("Læser hologram tilbage...")
    reconstructed = np.zeros_like(original)
    for y in range(height):
        for x in range(width):
            r_e, r_rest = sim.read_voxel(x, y, 0, "rød")
            g_e, g_rest = sim.read_voxel(x, y, 0, "grøn")
            b_e, b_rest = sim.read_voxel(x, y, 0, "blå")
            reconstructed[y, x] = [
                exponent_remainder_to_number(r_e, r_rest),
                exponent_remainder_to_number(g_e, g_rest),
                exponent_remainder_to_number(b_e, b_rest),
            ]

    # Verificér
    assert np.array_equal(original, reconstructed), "FEJL: Rekonstruktion matcher ikke!"
    print("OK: Perfekt rekonstruktion!")

    # ASCII hologram
    print("\nHolografisk projektion (ASCII):")
    gray = np.mean(reconstructed, axis=2).astype(int)
    for y in range(height):
        line = ""
        for x in range(width):
            line += luminance_to_ascii(gray[y, x])
        print(line)

    # Gem billeder
    try:
        from PIL import Image
        Image.fromarray(original).save("earth_original.png")
        Image.fromarray(reconstructed).save("earth_reconstructed.png")
        print("\nBilleder gemt: earth_original.png, earth_reconstructed.png")
    except ImportError:
        print("\n(Pillow ikke installeret - billeder ikke gemt)")

    print("\nDemo gennemført!")


if __name__ == "__main__":
    run_full_demo()

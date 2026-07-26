"""Demonstrerer parallel optisk læsning/skrivning."""

import time

from chromaplex import CrystalSimulator
from chromaplex.utils import number_to_exponent_remainder

def demo_parallel():
    sim = CrystalSimulator(size=50)
    width, height = 20, 20

    print("Initialiserer krystal med testdata...")
    for y in range(height):
        for x in range(width):
            e, rest = number_to_exponent_remainder(x * y)
            sim.write_voxel(x, y, 0, "rød", e, rest)

    print("Sekventiel læsning...")
    start = time.time()
    for y in range(height):
        for x in range(width):
            sim.read_voxel(x, y, 0, "rød")
    seq_time = time.time() - start
    print(f"  Tid: {seq_time*1000:.2f} ms for {width*height} voxels")

    print("Planlæsning via simulatorens load_plane-API...")
    start = time.time()
    data = sim.load_plane(0, (0, width-1), (0, height-1), ["rød"])
    par_time = time.time() - start
    print(f"  Tid: {par_time*1000:.2f} ms for {width*height} voxels")

    speedup = seq_time / par_time if par_time > 0 else float("inf")
    print(f"\nForhold i denne Python-kørsel: {speedup:.1f}x")
    print("Bemærk: load_plane er et simulator-API, ikke en CPA-instruktion.")
    print("Resultatet er ikke en måling af optisk hardware eller SSD-hastighed.")

if __name__ == "__main__":
    demo_parallel()

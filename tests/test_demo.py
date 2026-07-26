"""Test suite for ChromaPlex Full Potential Demo - 20 tests."""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import unittest
import numpy as np
from chromaplex.utils import (
    exponent_remainder_to_number,
    luminance_to_ascii,
    number_to_exponent_remainder,
)
from chromaplex.crystal_simulator import CrystalSimulator, Voxel


class TestUtils(unittest.TestCase):
    def test_small_numbers(self):
        for n in range(0, 256):
            e, rest = number_to_exponent_remainder(n)
            self.assertGreaterEqual(rest, 0)
            self.assertEqual(exponent_remainder_to_number(e, rest), n)

    def test_large_numbers(self):
        for n in [10**6, 2**30, 10**12]:
            e, rest = number_to_exponent_remainder(n)
            self.assertEqual(exponent_remainder_to_number(e, rest), n)

    def test_powers_of_two(self):
        for e in range(1, 15):
            n = 2**e
            e_calc, rest = number_to_exponent_remainder(n)
            self.assertEqual(e_calc, e)
            self.assertEqual(rest, 0)

    def test_zero(self):
        e, rest = number_to_exponent_remainder(0)
        self.assertEqual((e, rest), (0, 0))
        self.assertEqual(exponent_remainder_to_number(e, rest), 0)

    def test_zero_and_one_are_distinct(self):
        self.assertEqual(number_to_exponent_remainder(0), (0, 0))
        self.assertEqual(number_to_exponent_remainder(1), (0, 1))

    def test_base_three_contract(self):
        e, rest = number_to_exponent_remainder(1_234_567, base=3)
        self.assertEqual((e, rest), (12, 703_126))
        self.assertEqual(exponent_remainder_to_number(e, rest, base=3), 1_234_567)


class TestVoxel(unittest.TestCase):
    def test_empty_voxel(self):
        v = Voxel()
        self.assertEqual(len(v.channels), 0)

    def test_write_read_channel(self):
        v = Voxel()
        v.write("rød", 7, 42)
        self.assertEqual(v.read("rød"), (7, 42))

    def test_multiple_channels_independent(self):
        v = Voxel()
        v.write("rød", 10, 100)
        v.write("grøn", 20, 200)
        self.assertEqual(v.read("rød"), (10, 100))
        self.assertEqual(v.read("grøn"), (20, 200))
        v.write("rød", 99, 0)
        self.assertEqual(v.read("rød"), (99, 0))
        self.assertEqual(v.read("grøn"), (20, 200))


class TestCrystalSimulator(unittest.TestCase):
    def setUp(self):
        self.sim = CrystalSimulator(size=30)

    def test_write_read_single_voxel(self):
        self.sim.write_voxel(5, 5, 5, "rød", 7, 42)
        self.assertEqual(self.sim.read_voxel(5, 5, 5, "rød"), (7, 42))

    def test_multiple_colors_same_voxel(self):
        self.sim.write_voxel(5, 5, 5, "rød", 8, 10)
        self.sim.write_voxel(5, 5, 5, "grøn", 9, 20)
        self.assertEqual(self.sim.read_voxel(5, 5, 5, "rød"), (8, 10))
        self.assertEqual(self.sim.read_voxel(5, 5, 5, "grøn"), (9, 20))

    def test_voxel_independence(self):
        self.sim.write_voxel(0, 0, 0, "rød", 1, 1)
        self.sim.write_voxel(1, 1, 1, "rød", 2, 2)
        self.assertEqual(self.sim.read_voxel(0, 0, 0, "rød"), (1, 1))
        self.assertEqual(self.sim.read_voxel(1, 1, 1, "rød"), (2, 2))

    def test_unwritten_voxel_returns_zero(self):
        self.assertEqual(self.sim.read_voxel(29, 29, 29, "rød"), (0, 0))

    def test_pack_method(self):
        self.sim.pack(10, 10, 10, [("rød", 5), ("grøn", 10)])
        self.assertEqual(self.sim.read_voxel(10, 10, 10, "rød"), (5, 0))
        self.assertEqual(self.sim.read_voxel(10, 10, 10, "grøn"), (10, 0))

    def test_overwrite_voxel(self):
        self.sim.write_voxel(0, 0, 0, "rød", 100, 200)
        self.sim.write_voxel(0, 0, 0, "rød", 999, 888)
        self.assertEqual(self.sim.read_voxel(0, 0, 0, "rød"), (999, 888))

    def test_load_plane(self):
        for y in range(3):
            for x in range(3):
                exponent, rest = number_to_exponent_remainder(x + y)
                self.sim.write_voxel(x, y, 0, "rød", exponent, rest)
        data = self.sim.load_plane(0, (0, 2), (0, 2), ["rød"])
        self.assertEqual(data.shape, (1, 3, 3))


class TestFullRoundtrip(unittest.TestCase):
    def setUp(self):
        self.sim = CrystalSimulator(size=40)

    def test_grayscale_roundtrip(self):
        w, h = 8, 8
        original = np.array([[(x * 32 + y * 8) % 256 for x in range(w)] for y in range(h)], dtype=int)
        for y in range(h):
            for x in range(w):
                v = int(original[y, x])
                e, r = number_to_exponent_remainder(v)
                self.sim.write_voxel(x, y, 0, "rød", e, r)
        reconstructed = np.zeros((h, w), dtype=int)
        for y in range(h):
            for x in range(w):
                e, r = self.sim.read_voxel(x, y, 0, "rød")
                reconstructed[y, x] = exponent_remainder_to_number(e, r)
        np.testing.assert_array_equal(original, reconstructed)

    def test_rgb_roundtrip(self):
        w, h = 5, 5
        original = np.zeros((h, w, 3), dtype=int)
        for y in range(h):
            for x in range(w):
                original[y, x] = [(x * 50) % 256, (y * 50) % 256, ((x + y) * 30) % 256]
        for y in range(h):
            for x in range(w):
                r, g, b = original[y, x]
                r_e, r_r = number_to_exponent_remainder(int(r))
                g_e, g_r = number_to_exponent_remainder(int(g))
                b_e, b_r = number_to_exponent_remainder(int(b))
                self.sim.pack(x, y, 0, [("rød", r_e), ("grøn", g_e), ("blå", b_e)])
                self.sim.grid[x][y][0].channels["rød"]["rest"] = r_r
                self.sim.grid[x][y][0].channels["grøn"]["rest"] = g_r
                self.sim.grid[x][y][0].channels["blå"]["rest"] = b_r
        reconstructed = np.zeros_like(original)
        for y in range(h):
            for x in range(w):
                for ci, col in enumerate(["rød", "grøn", "blå"]):
                    e, r = self.sim.read_voxel(x, y, 0, col)
                    reconstructed[y, x, ci] = exponent_remainder_to_number(e, r)
        np.testing.assert_array_equal(original, reconstructed)

    def test_edge_cases(self):
        for i, (r, g, b) in enumerate([(0, 0, 0), (255, 255, 255), (128, 128, 128),
                                         (255, 0, 0), (0, 255, 0), (0, 0, 255)]):
            r_e, r_r = number_to_exponent_remainder(r)
            g_e, g_r = number_to_exponent_remainder(g)
            b_e, b_r = number_to_exponent_remainder(b)
            self.sim.pack(i, 0, 0, [("rød", r_e), ("grøn", g_e), ("blå", b_e)])
            self.sim.grid[i][0][0].channels["rød"]["rest"] = r_r
            self.sim.grid[i][0][0].channels["grøn"]["rest"] = g_r
            self.sim.grid[i][0][0].channels["blå"]["rest"] = b_r
            r_e2, r_r2 = self.sim.read_voxel(i, 0, 0, "rød")
            g_e2, g_r2 = self.sim.read_voxel(i, 0, 0, "grøn")
            b_e2, b_r2 = self.sim.read_voxel(i, 0, 0, "blå")
            self.assertEqual(exponent_remainder_to_number(r_e2, r_r2), r)
            self.assertEqual(exponent_remainder_to_number(g_e2, g_r2), g)
            self.assertEqual(exponent_remainder_to_number(b_e2, b_r2), b)

    def test_large_image(self):
        w, h = 20, 20
        original = np.random.RandomState(42).randint(0, 256, (h, w, 3), dtype=np.uint8)
        for y in range(h):
            for x in range(w):
                r, g, b = original[y, x]
                r_e, r_r = number_to_exponent_remainder(int(r))
                g_e, g_r = number_to_exponent_remainder(int(g))
                b_e, b_r = number_to_exponent_remainder(int(b))
                self.sim.pack(x, y, 0, [("rød", r_e), ("grøn", g_e), ("blå", b_e)])
                self.sim.grid[x][y][0].channels["rød"]["rest"] = r_r
                self.sim.grid[x][y][0].channels["grøn"]["rest"] = g_r
                self.sim.grid[x][y][0].channels["blå"]["rest"] = b_r
        reconstructed = np.zeros_like(original)
        for y in range(h):
            for x in range(w):
                for ci, col in enumerate(["rød", "grøn", "blå"]):
                    e, r = self.sim.read_voxel(x, y, 0, col)
                    reconstructed[y, x, ci] = exponent_remainder_to_number(e, r)
        np.testing.assert_array_equal(original, reconstructed)


class TestHologramGeneration(unittest.TestCase):
    def test_ascii_hologram_output(self):
        self.assertEqual(
            [luminance_to_ascii(l) for l in [0, 50, 100, 150, 200, 255]],
            [" ", ".", "+", "#", "@", "@"],
        )
        self.assertEqual(luminance_to_ascii(np.int64(100)), "+")

    def test_hologram_dimensions(self):
        sim = CrystalSimulator(size=20)
        for y in range(3):
            for x in range(5):
                sim.write_voxel(x, y, 0, "rød", 7, 100)
        holo = np.zeros((3, 5), dtype=int)
        for y in range(3):
            for x in range(5):
                e, rest = sim.read_voxel(x, y, 0, "rød")
                holo[y, x] = exponent_remainder_to_number(e, rest)
        self.assertEqual(holo.shape, (3, 5))
        np.testing.assert_array_equal(holo, np.full((3, 5), 228))


class TestIntegrationWithDemo(unittest.TestCase):
    def test_demo_workflow(self):
        w, h = 4, 4
        sim = CrystalSimulator(size=20)
        original = np.zeros((h, w, 3), dtype=np.uint8)
        for y in range(h):
            for x in range(w):
                original[y, x] = [(x * 60) % 256, (y * 60) % 256, ((x + y) * 40) % 256]
        for y in range(h):
            for x in range(w):
                r, g, b = original[y, x]
                r_e, r_r = number_to_exponent_remainder(int(r))
                g_e, g_r = number_to_exponent_remainder(int(g))
                b_e, b_r = number_to_exponent_remainder(int(b))
                sim.pack(x, y, 0, [("rød", r_e), ("grøn", g_e), ("blå", b_e)])
                sim.grid[x][y][0].channels["rød"]["rest"] = r_r
                sim.grid[x][y][0].channels["grøn"]["rest"] = g_r
                sim.grid[x][y][0].channels["blå"]["rest"] = b_r
        reconstructed = np.zeros_like(original)
        for y in range(h):
            for x in range(w):
                for ci, col in enumerate(["rød", "grøn", "blå"]):
                    e, r = sim.read_voxel(x, y, 0, col)
                    reconstructed[y, x, ci] = exponent_remainder_to_number(e, r)
        np.testing.assert_array_equal(original, reconstructed)


if __name__ == "__main__":
    unittest.main(verbosity=2)

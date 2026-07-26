"""Integrationstests for den dokumenterede CPL → CPA → simulator-kontrakt."""

from pathlib import Path
import unittest

from chromaplex import CrystalSimulator, assemble, compile_cpl
from chromaplex.cpa_assembler import SUPPORTED_OPCODES
from chromaplex.utils import exponent_remainder_to_number


ROOT = Path(__file__).resolve().parents[1]


class TestCompactCPL(unittest.TestCase):
    def _run(self, source: str, *, size: int = 100) -> list[int]:
        instructions = assemble(compile_cpl(source))
        return CrystalSimulator(size=size).execute_program(instructions)

    def test_documented_store_load_print_roundtrip(self):
        source = """
        var data = 1234567;
        store data at (5, 5, 5) colour GREEN;
        load result from (5, 5, 5) colour GREEN;
        print result;
        """
        self.assertEqual(self._run(source), [1_234_567])

    def test_rgb_channels_are_independent(self):
        source = """
        var red_value = 255;
        var green_value = 128;
        var blue_value = 64;
        store red_value at (10, 20, 0) colour RED;
        store green_value at (10, 20, 0) colour GREEN;
        store blue_value at (10, 20, 0) colour BLUE;
        load r_value from (10, 20, 0) colour RED;
        load g_value from (10, 20, 0) colour GREEN;
        load b_value from (10, 20, 0) colour BLUE;
        print r_value;
        print g_value;
        print b_value;
        """
        self.assertEqual(self._run(source), [255, 128, 64])

    def test_unknown_statement_fails_instead_of_being_ignored(self):
        with self.assertRaises(SyntaxError):
            compile_cpl("teleport data to moon;")


class TestSpecificationCPL(unittest.TestCase):
    def test_hello_example_compiles_and_stores_losslessly(self):
        source = (ROOT / "examples" / "hello.cpl").read_text(encoding="utf-8")
        simulator = CrystalSimulator(size=20)
        simulator.execute_program(assemble(compile_cpl(source)))

        exponent, rest = simulator.read_voxel(0, 0, 0, "grøn")
        expected = int.from_bytes(b"Hello World", "big")
        self.assertEqual(exponent_remainder_to_number(exponent, rest), expected)

    def test_full_potential_example_compiles_and_executes(self):
        source = (ROOT / "examples" / "full_potential_demo.cpl").read_text(
            encoding="utf-8"
        )
        instructions = assemble(compile_cpl(source))
        simulator = CrystalSimulator(size=20)
        simulator.execute_program(instructions)

        values = []
        for color in ("rød", "grøn", "blå"):
            values.append(
                exponent_remainder_to_number(
                    *simulator.read_voxel(0, 0, 0, color)
                )
            )
        self.assertEqual(values, [0, 64, 128])


class TestCPAContract(unittest.TestCase):
    def test_pow2_add_uses_register_values(self):
        source = """
        LOAD.IMM rød, 20
        LOAD.IMM grøn, 185991
        POW2.ADD rød, grøn
        OUT rød
        HALT
        """
        simulator = CrystalSimulator()
        self.assertEqual(simulator.execute_program(assemble(source)), [1_234_567])

    def test_zero_and_one_remain_distinct_in_registers(self):
        source = """
        LOAD.IMM rød, 0
        OUT rød
        LOAD.IMM rød, 1
        OUT rød
        HALT
        """
        simulator = CrystalSimulator()
        self.assertEqual(simulator.execute_program(assemble(source)), [0, 1])

    def test_language_spec_lists_only_implemented_opcodes(self):
        specification = (ROOT / "docs" / "language_spec.md").read_text(
            encoding="utf-8"
        )
        for opcode in SUPPORTED_OPCODES:
            self.assertIn(f"`{opcode}`", specification)
        for unsupported in ("LOAD.PLANE", "STORE.ANGLES", "SCALE.XYZ"):
            self.assertNotIn(f"`{unsupported}`", specification)


if __name__ == "__main__":
    unittest.main(verbosity=2)

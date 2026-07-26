"""Brainfuck → CPA Turing-komplethedstest - 18 tests."""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import unittest
from chromaplex.bf_compiler import compile_bf_to_cpa
from chromaplex.cpa_assembler import assemble
from chromaplex.crystal_simulator import CrystalSimulator
from chromaplex.utils import exponent_remainder_to_number


class TestBFCompiler(unittest.TestCase):
    def test_simple_increment(self):
        cpa = compile_bf_to_cpa("+++")
        self.assertIn("LOAD.C R, (B,0,0)", cpa)
        self.assertIn("ADD.IMM R, R, 1", cpa)
        self.assertIn("HALT", cpa)

    def test_pointer_movement(self):
        cpa = compile_bf_to_cpa(">><<")
        self.assertIn("ADD.IMM B, B, 1", cpa)
        self.assertIn("SUB.IMM B, B, 1", cpa)

    def test_output(self):
        self.assertIn("OUT R", compile_bf_to_cpa("."))

    def test_input(self):
        self.assertIn("IN R", compile_bf_to_cpa(","))

    def test_simple_loop(self):
        cpa = compile_bf_to_cpa("+++[-]")
        self.assertIn("L0:", cpa)
        self.assertIn("JMP.IF EQ, L0_end", cpa)
        self.assertIn("JMP L0", cpa)

    def test_nested_loops(self):
        cpa = compile_bf_to_cpa("[++[--]++]")
        self.assertIn("L0:", cpa)
        self.assertIn("L1:", cpa)

    def test_hello_world_compiles(self):
        hw = "++++++++++[>+++++++>++++++++++>+++>+<<<<-]>++.>+."
        cpa = compile_bf_to_cpa(hw)
        self.assertIn("HALT", cpa)
        self.assertIn("LOAD.C", cpa)
        self.assertIn("OUT", cpa)

    def test_unbalanced_open(self):
        with self.assertRaises(SyntaxError):
            compile_bf_to_cpa("[+++")

    def test_unbalanced_close(self):
        with self.assertRaises(SyntaxError):
            compile_bf_to_cpa("+++]")

    def test_empty_program(self):
        self.assertIn("HALT", compile_bf_to_cpa(""))

    def test_comment_only(self):
        cpa = compile_bf_to_cpa("Dette er tekst +++ mere tekst")
        self.assertIn("ADD.IMM R, R, 1", cpa)

    def test_complex_program(self):
        cpa = compile_bf_to_cpa(",[>,]<[.<]")
        self.assertIn("IN R", cpa)
        self.assertIn("OUT R", cpa)

    def test_label_uniqueness(self):
        cpa = compile_bf_to_cpa("[+][+][+]")
        lines = cpa.split("\n")
        labels = [l.split(":")[0].strip() for l in lines if ":" in l and not l.strip().startswith(";") and l.strip().endswith(":")]
        self.assertEqual(len(labels), len(set(labels)))


class TestTuringCompleteness(unittest.TestCase):
    def test_known_loop_program_executes(self):
        simulator = CrystalSimulator()
        instructions = assemble(compile_bf_to_cpa("++[>+++<-]>."))
        self.assertEqual(simulator.execute_program(instructions), [6])

    def test_cpa_simulates_all_bf_instructions(self):
        source = ",[->+<]>."
        self.assertEqual(set(source), set("><+-.,[]"))
        simulator = CrystalSimulator()
        simulator.input_buffer = [4]
        self.assertEqual(
            simulator.execute_program(assemble(compile_bf_to_cpa(source))),
            [4],
        )

    def test_translation_overhead_is_finite(self):
        for instr in [">", "<", "+", "-", ".", ",", "[]"]:
            cpa = compile_bf_to_cpa(instr)
            lines = len(cpa.strip().split("\n"))
            self.assertLess(lines, 20, f"Overhead for '{instr}' = {lines}")

    def test_tape_cells_map_to_independent_voxels(self):
        simulator = CrystalSimulator()
        instructions = assemble(compile_bf_to_cpa("++>+++<."))
        self.assertEqual(simulator.execute_program(instructions), [2])
        self.assertEqual(
            exponent_remainder_to_number(
                *simulator.read_voxel(0, 0, 0, "rød")
            ),
            2,
        )
        self.assertEqual(
            exponent_remainder_to_number(
                *simulator.read_voxel(1, 0, 0, "rød")
            ),
            3,
        )

    def test_deterministic_compilation(self):
        hw = "+++[-]"
        self.assertEqual(compile_bf_to_cpa(hw), compile_bf_to_cpa(hw))


if __name__ == "__main__":
    unittest.main(verbosity=2)

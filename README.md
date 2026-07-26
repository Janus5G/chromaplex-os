> **English** | [Dansk](README.da.md)

# ChromaPlex OS v1.0.1

An experimental programming language, assembler, and 3D crystal-storage
simulator built around colour channels, voxels, and lossless
exponent–remainder number representation.

[![Tests](https://github.com/Janus5G/chromaplex-os/actions/workflows/tests.yml/badge.svg)](https://github.com/Janus5G/chromaplex-os/actions/workflows/tests.yml)
[![Demo](https://img.shields.io/badge/demo-GitHub%20Pages-0969da)](https://Janus5G.github.io/chromaplex-os/)
[![License: MIT](https://img.shields.io/badge/license-MIT-yellow.svg)](LICENSE)

## Explore

- [Open the ChromaPlex 3D browser demo](https://Janus5G.github.io/chromaplex-os/)
- [PRISME repository — spectral storage and optical routing](https://github.com/Janus5G/PRISME)
- [Open the live PRISME glass-plate demo](https://Janus5G.github.io/PRISME/demo/prisme.html)
- [Detailed CPL and CPA guide (Danish)](docs/programmeringssprog.md)
- [Compact implementation specification](docs/language_spec.md)
- [Press and technical FAQ](FAQ.md)

## What ChromaPlex OS contains

ChromaPlex OS has two programming layers:

| Layer | Name | Purpose |
|---|---|---|
| High level | CPL — ChromaPlex Language | Describes values, voxel coordinates, colour channels, storage, and output. |
| Low level | CPA — ChromaPlex Assembly | Defines the instructions assembled and executed by the crystal simulator. |

The repository includes:

- a CPL-to-CPA compiler;
- a validated CPA assembler;
- a sparse Python 3D crystal simulator;
- five logical colour channels: red, green, blue, violet, and UV;
- a Brainfuck-to-CPA compiler;
- browser and Python demonstrations;
- 49 unit and integration tests.

ChromaPlex OS is currently a software and simulation project. It does not claim
to be a finished physical storage product, and the repository does not contain
verified optical-hardware performance measurements.

## PRISME

[PRISME](https://github.com/Janus5G/PRISME) is the companion project for the
spectral and optical layer. It explores mapping bytes across red, green, blue,
violet, and UV channels, UV error control, an optical routing simulator, and a
browser-based glass-plate visualisation.

The relationship is:

```text
CPL source
   ↓
ChromaPlex compiler and CPA instruction set
   ↓
ChromaPlex crystal simulator
   ↓
PRISME spectral encoding and optical-routing model
```

Try the [live PRISME demo](https://Janus5G.github.io/PRISME/demo/prisme.html),
or inspect the [PRISME source and documentation](https://github.com/Janus5G/PRISME).

## Lossless number representation

For values from 2 upward, the default base-2 representation is:

```text
n = 2^e + remainder
```

`e` is the largest exponent for which `2^e <= n`. Zero and one use distinct
canonical pairs:

| Value | Pair |
|---:|---:|
| 0 | `(0, 0)` |
| 1 | `(0, 1)` |
| 1,234,567 | `(20, 185,991)` |

The representation is lossless when the complete remainder is retained. It is
not universal compression: whether it reduces storage depends on the data and
the concrete serialisation format.

The utilities also support other bases. The verified base-3 example is:

```text
1,234,567 = 3^12 + 703,126
```

## CPL example

```cpl
var data = 1234567;
store data at (5, 5, 5) colour GREEN;
load result from (5, 5, 5) colour GREEN;
print result;
```

Compile and run it directly:

```bash
cpl-run examples/store_green.cpl
```

Expected output:

```text
Output: [1234567]
```

Export textual CPA and run it separately:

```bash
cplc examples/store_green.cpl -o store_green.cpa
cpa-run store_green.cpa
```

## Installation

Requires Python 3.9 or newer.

```bash
git clone https://github.com/Janus5G/chromaplex-os.git
cd chromaplex-os
python -m pip install -e ".[test]"
python -m unittest discover -s tests -v
```

The verified suite contains 49 tests covering:

- zero/one distinction and base-2 roundtrips;
- the base-3 representation;
- compact and specification-oriented CPL;
- CPL → CPA → simulator integration;
- documented CPA opcode parity;
- Brainfuck loops, I/O, and voxel-backed tape cells.

## Command-line tools

| Command | Purpose |
|---|---|
| `cpl-run FILE.cpl` | Compile CPL and execute it in the simulator. |
| `cplc FILE.cpl -o FILE.cpa` | Compile CPL to textual CPA. |
| `cpa-run FILE.cpa` | Assemble and execute textual CPA. |
| `bf2cpa FILE.bf` | Translate Brainfuck to CPA. |
| `chromaplex-ai "prompt"` | Optional AI-assisted CPL generation. |

On Windows, if the commands are not found after installation, add Python's
`Scripts` directory to `PATH`.

## Browser demos

The repository root contains the static ChromaPlex demo:

- [ChromaPlex 3D crystal simulator](https://Janus5G.github.io/chromaplex-os/)

The connected PRISME project provides:

- [PRISME live glass-plate register](https://Janus5G.github.io/PRISME/demo/prisme.html)
- [PRISME repository](https://github.com/Janus5G/PRISME)

The ChromaPlex demo is deployed automatically through GitHub Pages when
`index.html`, `demo/`, or the Pages workflow changes.

## Repository structure

```text
chromaplex-os/
├── chromaplex/                 # Compiler, assembler, simulator, and utilities
├── examples/                   # CPL, CPA, Brainfuck, image, and plane demos
├── tests/                      # Unit and integration tests
├── docs/                       # Language and architecture documentation
├── demo/                       # Browser-demo files
├── index.html                  # GitHub Pages entry point
├── README.md                   # English documentation
└── README.da.md                # Danish documentation
```

## Scope and related documentation

- [Language specification](docs/language_spec.md)
- [Programming-language guide](docs/programmeringssprog.md)
- [Storage-capacity model and limitations](docs/storage_capacity_proof.md)
- [Brainfuck translation argument](docs/turing_completeness.md)
- [Security policy](SECURITY.md)
- [Security audit](SECURITY_AUDIT.md)

## Related projects

- [PRISME](https://github.com/Janus5G/PRISME) — spectral encoding and optical-routing model
- [Cplex](https://github.com/Janus5G/Cplex) — editor for ChromaPlex/CPL
- [ChromaPlex v2.0 Specification & Architecture](https://github.com/Janus5G/ChromaPlex-v2.0-Specification-Architecture-Documentation)

## License

MIT — see [LICENSE](LICENSE).

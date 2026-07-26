# Brainfuck-oversættelse til ChromaPlex Assembly

## Resultat

`chromaplex/bf_compiler.py` oversætter alle otte Brainfuck-operationer til CPA.
Integrationstests kører kendte loop-programmer, I/O og uafhængige tape-celler
gennem både assembleren og simulatoren.

| BF | CPA-oversættelse |
|---|---|
| `>` | `ADD.IMM b, b, 1` |
| `<` | `SUB.IMM b, b, 1` |
| `+` | `LOAD.C` + `ADD.IMM` + `STORE.C` |
| `-` | `LOAD.C` + `SUB.IMM` + `STORE.C` |
| `.` | `LOAD.C` + `OUT` |
| `,` | `IN` + `STORE.C` |
| `[` | `LOAD.C` + `CMP.IMM` + `JMP.IF` |
| `]` | `JMP` |

Brainfuck-tapen mappes til rød kanal langs krystallens x-akse, og pointeren
ligger i register `b`.

## Præcis afgrænsning

Oversættelsen bevarer Brainfuck-operationernes struktur med konstant
instruktionsoverhead. Det er det sædvanlige reduktionsargument for, at et
ubegrænset CPA-design kan udtrykke en kendt Turing-komplet model.

Den konkrete Python-simulator er med vilje begrænset af krystalstørrelse,
heltalsgrænser og et maksimum for antal instruktionstrin. En enkelt faktisk
kørsel er derfor endelig. Testene dokumenterer implementeret oversættelse og
eksekvering; de er ikke et fysisk hardwarebevis.

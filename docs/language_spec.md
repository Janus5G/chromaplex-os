# ChromaPlex Language Specification v1.0

## Status og scope

CPL (ChromaPlex Language) er et domænespecifikt sprog til den medfølgende
softwaremodel for farvekanaler og 3D-voxels. CPL kompileres til tekstbaseret CPA
(ChromaPlex Assembly), som assembleres til instruktionsobjekter og køres i
Python-simulatoren.

Denne fil er kontrakten for det implementerede v1.0-subset. Fysiske optiske
egenskaber og fremtidige parallelle hardwareinstruktioner er designidéer, ikke
en del af den nuværende assembler.

## Kanonisk talrepræsentation

For en base `b >= 2` kodes ikke-negative heltal sådan:

- `0 <= n < b`: `(eksponent, rest) = (0, n)`.
- `n >= b`: vælg største `e`, hvor `b^e <= n`, og gem `(e, n - b^e)`.

Det særlige første interval gør nul og én entydige. Ved base 2 er `(0, 0)` nul
og `(0, 1)` én. For `e >= 1` rekonstrueres tallet som `b^e + rest`.

Eksempel med base 2:

```text
1.234.567 = 2^20 + 185.991
```

Eksempel med base 3:

```text
1.234.567 = 3^12 + 703.126
```

## CPL-subset

Compileren accepterer to overfladesyntakser, som begge genererer samme CPA:

### Kompakt lagersyntaks

```ebnf
Program      ::= Statement*
Statement    ::= VarDecl | Store | Load | Print
VarDecl      ::= "var" IDENT "=" NumericExpression ";"
Store        ::= "store" (IDENT | INTEGER) "at" Coordinates
                 ("colour" | "color" | "farve") Color ";"
Load         ::= "load" IDENT "from" Coordinates
                 ("colour" | "color" | "farve") Color ";"
Print        ::= "print" (IDENT | INTEGER) ";"
Coordinates  ::= "(" INTEGER "," INTEGER "," INTEGER ")"
```

Farvenavne kan skrives som `RED`, `GREEN`, `BLUE`, `VIOLET`, `UV` eller de
danske `rød`, `grøn`, `blå`, `violet`, `uv`.

### Specifikationsorienteret syntaks

Det implementerede subset omfatter `streng`, `tal`, `potens`, `konstant`,
`skriv_voxel`, `kanal`, sikre compile-time `for`-loops samt de
demonstrationskonstruktioner, der bruges i `examples/full_potential_demo.cpl`.
Ukendte statements giver altid `SyntaxError`; de ignoreres ikke.

## CPA-instruktionssæt

| Mnemonic | Operander | Betydning |
|---|---|---|
| `LOAD.IMM` | register, værdi | Indlæs et ikke-negativt heltal. |
| `LOAD.PAIR` | register, eksponent, rest | Indlæs et eksplicit repræsentationspar. |
| `ADD.IMM` | dest, src, værdi | Læg en konstant til registerværdien. |
| `SUB.IMM` | dest, src, værdi | Træk en konstant fra; simulatoren mætter ved nul. |
| `STORE.C` | (x,y,z), farve, register | Skriv et registerpar til en voxelkanal. |
| `LOAD.C` | register, (x,y,z), farve | Læs en voxelkanal til et register. |
| `PACK` | (x,y,z), farver... | Skriv eksponentdelen fra flere farveregistre. |
| `UNPACK` | (x,y,z), registre... | Læs eksisterende kanaler til registre. |
| `MUL.P` | dest, src1, src2 | Heltalsmultiplikation. |
| `DIV.P` | dest, src1, src2 | Heltalsdivision. |
| `POW.P` | dest, src1, src2 | Heltalspotens. |
| `ADD.R` | dest, src1, src2 | Heltalsaddition. |
| `SUB.R` | dest, src1, src2 | Heltalssubtraktion, mættet ved nul. |
| `CMP.IMM` | register, værdi | Sammenlign med en konstant. |
| `CMP.P` | register1, register2 | Sammenlign to registerværdier. |
| `JMP` | label | Ubetinget hop. |
| `JMP.IF` | betingelse, label | Betinget hop (`EQ`, `NE`, `GT`, `LT`, `GE`, `LE`). |
| `OUT` | register | Tilføj registerværdien til outputbufferen. |
| `IN` | register | Læs næste værdi fra inputbufferen, hvis den findes. |
| `SHIFT.COLOR` | dest, src | Kopiér repræsentationsparret mellem registre. |
| `POW2.ADD` | eksponentregister, restregister | Beregn `2^e + rest` fra registrenes talværdier. |
| `HALT` | — | Stop programmet. |

`CrystalSimulator.load_plane(...)` er et Python-API til planlæsning. Det er ikke
en CPA-mnemonic i v1.0.

## Registre og kanaler

| Register | Kanal / rolle |
|---|---|
| `rød` | 650 nm-model / generelt register |
| `grøn` | 532 nm-model / generelt register |
| `blå` | 473 nm-model / generelt register |
| `violet` | 405 nm-model / generelt register |
| `uv` | 350 nm-model / generelt register |
| `r`, `b` | generelle hjælpe-/Brainfuck-registre |

Farveoperander accepterer kun `rød`, `grøn`, `blå`, `violet` og `uv`.

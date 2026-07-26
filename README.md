# ChromaPlex OS v1.0.1

**Krystalbaseret programmeringssprog med farvekodning og eksponentiel datarepræsentation.**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Tests](https://github.com/Janus5G/chromaplex-os/actions/workflows/tests.yml/badge.svg)](https://github.com/Janus5G/chromaplex-os/actions/workflows/tests.yml)

---

## Navigér hurtigt

- 🧰 **Compiler, assembler og simulator ligger samlet i dette repository**
- 🎮 **[Prøv browserdemoen](https://Janus5G.github.io/chromaplex-os/)**
- 📘 **[Læs programmeringssprogets dokumentation: CPL + CPA](docs/programmeringssprog.md)**
- 🧠 [Læs ChromaPlex v2.0 Specification & Architecture](https://github.com/Janus5G/ChromaPlex-v2.0-Specification-Architecture-Documentation)
- ℹ️ [Presse og tekniske spørgsmål: FAQ](FAQ.md)

---

## Om ChromaPlex OS

ChromaPlex OS bygger bro mellem anvendt fotonik og high-performance computerarkitektur. Projektet introducerer et domænespecifikt programmeringssprog, **CPL (ChromaPlex Language)**, og et lavniveau instruktionssæt, **CPA (ChromaPlex Assembly)**, designet til fremtidige optiske lagringsmedier.

I stedet for kun at tænke i traditionelle bits og bytes modellerer ChromaPlex data som:

- **Farver / bølgelængder:** Rød, Grøn, Blå, Violet og UV som uafhængige optiske kanaler.
- **Eksponent-rest-repræsentation:** For værdier fra 2 og op bruges `n = 2^e + rest`, hvor `e` er den største eksponent sådan at `2^e <= n`. Nul og én kodes særskilt som `(0,0)` og `(0,1)`, så repræsentationen er entydig og tabsfri.
- **3D voxels:** Data placeres i præcise `(x, y, z)` koordinater i en krystal.
- **Parallel optik:** Systemet er designet omkring idéen om simultan læsning og skrivning over mange optiske punkter.

> [!NOTE]
> Eksponent-rest-repræsentationen er ikke universel datakomprimering i sig selv. Den kan give kompakte beskrivelser, når data har struktur, fx små eller forudsigelige rester, men vilkårlige data bliver ikke automatisk mindre end almindelig binær lagring.

> [!NOTE]
> ChromaPlex OS er i dag et software- og simuleringsprojekt. Det demonstrerer sproget, assembleren, kompilatoren og krystalmodellen, men er ikke et færdigt fysisk hardware-produkt.

---

## Hvad er ChromaPlex?

ChromaPlex er et programmeringssprog og instruktionssæt til styring af krystalbaseret datalagring. I stedet for kun at spørge “hvilken byte ligger på denne adresse?”, spørger ChromaPlex:

1. Hvilket **voxel-koordinat** skal bruges?
2. Hvilken **farvekanal** skal data skrives i?
3. Skal tallet gemmes råt, eller som **eksponent + rest**?
4. Skal data læses sekventielt eller som et større optisk plan?

Det gør projektet velegnet til at eksperimentere med arkiver, holografiske billeddata, parallel læsning og langtidsholdbar datalagring.

---

## Programmeringssproget

ChromaPlex har to lag:

| Lag | Navn | Formål |
|-----|------|--------|
| Højniveau | **CPL** | Letlæseligt sprog til at beskrive data, voxels, farvekanaler og lagringsoperationer. |
| Lavniveau | **CPA** | Assembly-lignende instruktionssæt, som kompilatoren kan generere og simulatoren kan køre. |

Læs den fulde sprogdokumentation her:

## 📘 [ChromaPlex Programmeringssprog: CPL + CPA](docs/programmeringssprog.md)

---

## Eksempel: skriv og læs et tal i en krystal

```cpl
var data = 1234567;                       // Opretter variablen data med et stort heltal, som vi vil gemme optisk.
store data at (5, 5, 5) colour GREEN;     // Skriver værdien til voxel (5,5,5) i grøn kanal, fordi grøn bruges som standard stabil datakanal.
load result from (5, 5, 5) colour GREEN;  // Læser værdien tilbage fra samme koordinat og samme farvekanal.
print result;                             // Udskriver resultatet, så roundtrip kan verificeres i simulatoren.
```

Hvorfor grøn? Grøn kanal fungerer i dokumentationen som standardkanalen for simple eksempler, fordi den er let at aflæse visuelt og tydeligt adskilt fra UV/Violet-kanalerne, som ofte reserveres til metadata, indekser eller højpræcisionslag.

---

## Ydelsesstatus

Repositoryets målinger gælder kun Python-simulatoren. Der medfølger ingen
verificeret optisk hardwarebenchmark, SSD-sammenligning eller fysisk
retentionsmåling. Parallel optik er projektets arkitekturmål og skal testes på
relevant hardware, før konkrete hastighedstal kan angives.

---

## Komponenter

```text
chromaplex-os/
├── chromaplex/              # Hovedbibliotek med simulator, compiler og utilities
│   ├── cpa_assembler.py     # CPA assembler
│   ├── crystal_simulator.py # 3D krystalsimulator
│   ├── cpl_compiler.py      # CPL → CPA compiler
│   ├── ai_coder.py          # AI-assisteret CPL kodegenerering
│   ├── bf_compiler.py       # Brainfuck → CPA, brugt som Turing-komplethedsbevis
│   └── utils.py             # Hjælpefunktioner til potens/remainder-konvertering
├── examples/                # Demonstrationseksempler
│   ├── hello.cpl
│   ├── full_potential_demo.cpl
│   ├── store_green.cpl
│   ├── store_green.cpa
│   ├── run_demo.py
│   ├── parallel_demo.py
│   └── bf_hello.bf
├── tests/                   # Test-suite
│   ├── test_demo.py
│   ├── test_language_contract.py
│   └── test_turing.py
├── docs/                    # Dokumentation
│   ├── programmeringssprog.md
│   ├── language_spec.md
│   ├── storage_capacity_proof.md
│   └── turing_completeness.md
├── setup.py
└── LICENSE
```

---

## Hurtig start

```bash
git clone https://github.com/Janus5G/chromaplex-os.git          # Henter ChromaPlex OS kildekoden lokalt.
cd chromaplex-os                                                # Går ind i projektmappen.
pip install -e .                                                # Installerer pakken i editable mode til lokal udvikling.
cpl-run examples/store_green.cpl                                # Kompilerer CPL til CPA og kører resultatet; forventer Output: [1234567].
cplc examples/store_green.cpl -o store_green.cpa                # Eksporterer den genererede, tekstbaserede CPA.
cpa-run examples/store_green.cpa                                # Assemblerer og kører CPA direkte.
python examples/run_demo.py                                     # Kører hoveddemoen og tester roundtrip fra data til krystal og tilbage.
python examples/parallel_demo.py                                # Kører demoen for sekventiel vs. parallel læsning i simulatoren.
python -m unittest discover -s tests -v                         # Kører tests uden ekstra testdependency.
python -m pytest tests/ -v                                      # Alternativt: kør samme tests med pytest.
```

---

## Use cases

### Langtidsarkiv

ChromaPlex kan bruges som softwaremodel for arkivering af kulturarv, forskningsdata og offentlige dokumenter, hvor målet er databevaring uden kontinuerlig strøm i en fremtidig optisk lagringsarkitektur.

### Holografiske billeder

RGB-data kan fordeles over rød, grøn og blå kanal i samme voxelplan, så et billede kan rekonstrueres fra optiske lag.

### Videnskabelige datasæt

Store numeriske værdier kan beskrives som `n = 2^e + rest`, hvilket gør sproget interessant til datasæt med store tal, målinger eller indekser, især når værdierne har struktur eller små rester.

### Turing-komplet eksperiment

Brainfuck-kompilatoren oversætter de otte Brainfuck-operationer til CPA og
demonstrerer beregningsmodellens struktur. Den konkrete simulator har bevidste
grænser for krystalstørrelse og antal programtrin og er derfor endelig i en
enkelt kørsel.

---

## Arkitektur & Dokumentation

Den fulde tekniske specifikation og arkitektur-dokumentation for systemet er udskilt i sit eget repository for at holde koden ren. Her finder du ChromaPlex v2.0 og det spatiale tensor-instruktionssæt:

👉 [Læs ChromaPlex v2.0 Specification & Architecture](https://github.com/Janus5G/ChromaPlex-v2.0-Specification-Architecture-Documentation)

---

## Miljøvenlig datalagring

Efter skrivning kræver det antagede optiske lagringsmedie ingen kontinuerlig strøm for at fastholde data i den teoretiske lagringsmodel. Det gør ChromaPlex relevant som softwaremodel for fremtidige arkiver, hvor retention og energiforbrug er vigtigere end konstant omskrivning.

---

## Licens

MIT – se [LICENSE](LICENSE).

## Relaterede repositories

- [Cplex editor til ChromaPlex/CPL](https://github.com/Janus5G/Cplex)

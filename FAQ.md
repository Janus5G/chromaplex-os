# FAQ: presse og tekniske spørgsmål

## Hvad er ChromaPlex OS?

ChromaPlex OS er et eksperimentelt domænespecifikt programmeringssprog og en
softwaremodel for data i farvekanaler og 3D-voxels. Repositoryet indeholder:

- CPL-compiler (`chromaplex/cpl_compiler.py`)
- CPA-assembler (`chromaplex/cpa_assembler.py`)
- Python-baseret krystalsimulator (`chromaplex/crystal_simulator.py`)
- Brainfuck-til-CPA-compiler og browserdemo

## Er det et fysisk hardwareprodukt?

Nej. Denne version styrer ikke lasere eller fysisk fused-silica-hardware.
Farver, bølgelængder og voxels er softwareabstraktioner, som gør det muligt at
udvikle og teste sprog- og lageridéerne.

## Hvad betyder farvekanalerne?

Simulatoren modellerer fem logisk adskilte kanaler ved samme koordinat: rød,
grøn, blå, violet og UV. Det viser programmets adresseringsmodel. Det beviser
ikke i sig selv, at fem tilsvarende fysiske tilstande kan skrives og læses uden
crosstalk; det kræver laboratoriemålinger.

## Er eksponent/rest en komprimeringsalgoritme?

Ikke automatisk. ChromaPlex repræsenterer heltal med et kanonisk
eksponent/rest-par. Ved base 2 er `(0,0)` nul og `(0,1)` én; fra værdien 2 og op
bruges `n = 2^e + rest`.

Repræsentationen er tabsfri i simulatoren. Om den fylder mindre end almindelig
binær lagring afhænger af et konkret serialiseringsformat og dataenes struktur.
Dette repository definerer ikke et 32-bit fysisk pakkeformat.

## Hvad er idéen bag den optiske arkitektur?

Projektets hypotese er, at flere bølgelængder og parallelle skrive-/læsebaner kan
bruges som selvstændige datadimensioner. Softwaremodellen gør hypotesen
programmerbar. Varme, energifordeling, vinkelmultipleksing, skrivehastighed,
retention og fysisk kapacitet er ikke verificeret af koden.

## Hvordan tester jeg projektet?

```bash
git clone https://github.com/Janus5G/chromaplex-os.git
cd chromaplex-os
python -m pip install -e ".[test]"
python -m unittest discover -s tests -v
cpl-run examples/store_green.cpl
```

Det sidste program skal udskrive:

```text
Output: [1234567]
```

Browserdemoen kan åbnes via
[GitHub Pages](https://Janus5G.github.io/chromaplex-os/).

## Hvad skal valideres, før fysiske egenskaber kan hævdes?

Der kræves mindst en dokumenteret forsøgsopstilling, rå måledata, fejlrate,
crosstalk, kalibrering, energimåling, binært format og uafhængig reproduktion.
Se [kapacitetsmodellen](docs/storage_capacity_proof.md) for afgrænsningen.

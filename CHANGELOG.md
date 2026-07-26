# Changelog

## 1.0.1 — 2026-07-26

### Rettet

- Gjort heltalskodningen tabsfri: 0 kodes som `(0,0)`, og 1 som `(0,1)`.
- Verificeret base-3-eksemplet `1.234.567 = 3^12 + 703.126`.
- Tilføjet dokumenteret `var/store/load/print`-syntaks til den eksisterende
  CPL-compiler i stedet for at have en separat, modstridende compiler.
- Rettet `POW2.ADD`, så instruktionen bruger registrenes numeriske værdier.
- Samlet al compilerlogik i `chromaplex/cpl_compiler.py`; rodfilen er kun en
  bagudkompatibel wrapper.
- Gjort browserdemoens kodning identisk med Python-implementeringen.
- Flyttet CI-workflowet til `.github/workflows/tests.yml`, hvor GitHub kan køre
  det.
- Tilføjet `cpl-run` og outputfil til `cplc`.
- Rettet demos, ASCII-grænser, Brainfuck-tests og pakke-metadata.

### Dokumentation

- CPA-listen matcher nu præcist assemblerens implementerede opcodes.
- `load_plane` beskrives som Python-simulator-API, ikke CPA-instruktion.
- Udokumenterede hardware-, kapacitets- og hastighedstal er afgrænset som
  hypoteser i stedet for målte resultater.
- Fjernet gamle test- og rettelsesrapporter, som modsagde koden.

### Verifikation

- 49 unit- og integrationstests består.
- Ren wheel-installation består.
- `cpl-run`, `cplc`, `cpa-run`, hoveddemo og planlæsningsdemo er kørt fra den
  installerede pakke.

### Migrering

Den tidligere kode gav både 0 og 1 parret `(0,0)`, så de kunne ikke skelnes ved
dekodning. Data, hvor `(0,0)` var tiltænkt som værdien 1, skal migreres til
`(0,1)`. `(0,0)` betyder herefter altid 0.

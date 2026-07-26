# ChromaPlex Programmeringssprog

**Dokumentation for CPL (ChromaPlex Language) og CPA (ChromaPlex Assembly)**  
Version: 1.0.1  
Målgruppe: Øvet, med begynderforklaringer og tekniske detaljer til udviklere.

---

## Indholdsfortegnelse

1. [Hvad er ChromaPlex-sproget?](#hvad-er-chromaplex-sproget)
2. [Hvorfor findes CPL og CPA?](#hvorfor-findes-cpl-og-cpa)
3. [Mental model: krystal, voxel, kanal og potens](#mental-model-krystal-voxel-kanal-og-potens)
4. [CPL: højniveau-sproget](#cpl-højniveau-sproget)
5. [CPA: lavniveau-instruktionssættet](#cpa-lavniveau-instruktionssættet)
6. [Datakodning: `2^e + rest`](#datakodning-2e--rest)
7. [Eksekverbare eksempler](#eksekverbare-eksempler)
8. [Use cases](#use-cases)
9. [Fejlfinding](#fejlfinding)
10. [Sprog-reference](#sprog-reference)
11. [Videre læsning](#videre-læsning)

---

## Hvad er ChromaPlex-sproget?

ChromaPlex er et domænespecifikt programmeringssprog til at beskrive, hvordan data kan placeres, læses og manipuleres i en simuleret 3D-krystal. Sproget er bygget omkring tre ideer:

1. **Data har en fysisk position**: `(x, y, z)`.
2. **Data har en optisk kanal**: for eksempel `RED`, `GREEN`, `BLUE`, `VIOLET` eller `UV`.
3. **Data kan repræsenteres eksponentielt**: `værdi = 2^e + rest`.

Hvor et normalt program ofte skriver til en lineær hukommelsesadresse, skriver ChromaPlex til et voxel-koordinat og en farvekanal. Det gør sproget velegnet som eksperimentel model for 5D optisk datalagring.

> [!IMPORTANT]
> ChromaPlex OS er software, simulator og sprogarkitektur. Dokumentationen beskriver, hvordan man programmerer modellen. Den hævder ikke, at et færdigt fysisk krystaldrev allerede findes.

---

## Hvorfor findes CPL og CPA?

ChromaPlex bruger to lag, fordi forskellige læsere har forskellige behov.

| Lag | Navn | Målgruppe | Hvorfor det findes |
|-----|------|-----------|--------------------|
| Højniveau | CPL | Udviklere og eksperimenterende brugere | Gør det let at beskrive data, koordinater og farver uden at skrive assembly. |
| Lavniveau | CPA | Compiler-/VM-udviklere og forskere | Viser præcist hvilke operationer den virtuelle maskine udfører. |

**Hvorfor ikke kun ét sprog?**  
Fordi et højniveau-sprog er godt til læsbarhed, mens et assembly-lag er godt til kontrol. CPL er “hvad vil jeg opnå?”, CPA er “hvilke præcise instruktioner skal maskinen udføre?”.

---

## Mental model: krystal, voxel, kanal og potens

Forestil dig krystallen som et 3D-gitter:

```text
(x, y, z) = (5, 5, 5)
```

Ved denne position kan ChromaPlex gemme flere værdier, fordi hver farvekanal kan fungere som et separat lag:

| Kanal | Bølgelængde | Typisk rolle i eksempler |
|-------|-------------|--------------------------|
| `RED` / `rød` | 650 nm | Arkivdata, dybe lag eller rød billedkomponent |
| `GREEN` / `grøn` | 532 nm | Standard datakanal og grøn billedkomponent |
| `BLUE` / `blå` | 473 nm | Blå billedkomponent eller hjælpeværdi |
| `VIOLET` / `violet` | 405 nm | Metadata, præcision eller eksponent |
| `UV` / `uv` | 350 nm | Indeks, metadata eller højenergi-lag |

**Hvorfor farver?**  
Fordi hele ChromaPlex-idéen er at udnytte bølgelængder som uafhængige datakanaler. I simulatoren betyder det, at samme `(x, y, z)` kan indeholde flere værdier uden at overskrive hinanden, så længe de ligger i forskellige kanaler.

---

## CPL: højniveau-sproget

CPL beskriver intentionen: hvilke data du vil gemme, hvor de skal ligge, og hvilken kanal de skal bruge.

Den medfølgende compiler accepterer to overfladesyntakser:

1. **Toolchain-venlig CPL**, som bruger `var`, `store`, `load` og `print`.
2. **Specifikationsorienteret CPL**, som bruger danske nøgleord som `tal`, `potens`, `streng`, `skriv_voxel` og `kanal`.

Begge former kompileres af `chromaplex/cpl_compiler.py` til det samme
tekstbaserede CPA-instruktionssæt. Den kompakte form er nemmest til lager-I/O;
den danske form bruges af de større specifikations- og billeddemoer.

---

## CPA: lavniveau-instruktionssættet

CPA er ChromaPlex Assembly. Det er tættere på den virtuelle maskine og beskriver operationer som:

| Instruktion | Formål |
|------------|--------|
| `LOAD.IMM` | Indlæs en konstant i et register. |
| `STORE.C` | Skriv et register til et voxel og en farvekanal. |
| `LOAD.C` | Læs et voxel og en farvekanal ind i et register. |
| `PACK` | Pak flere farvekanaler i samme voxel. |
| `UNPACK` | Læs flere kanaler ud fra samme voxel. |
| `CMP.IMM` | Sammenlign et register med en konstant. |
| `JMP` | Hop til en label. |
| `JMP.IF` | Hop betinget ud fra statusflag. |
| `OUT` | Skriv registerværdi til outputbuffer. |
| `IN` | Læs inputværdi til register. |
| `HALT` | Stop programmet. |

**Hvorfor assembly?**  
Fordi CPA gør det tydeligt, at ChromaPlex ikke bare er en tekstsyntaks. Det er et instruktionssæt, hvor hukommelse, farver og optiske operationer kan modelleres på maskinnært niveau.

---

## Datakodning: `2^e + rest`

ChromaPlex bruger eksponentiel repræsentation:

```text
værdi = 2^e + rest
```

Nul og én er den nødvendige undtagelse: de kodes som henholdsvis `(0, 0)` og
`(0, 1)`. Dermed er de to værdier entydige. For alle værdier fra 2 og op gælder
formlen direkte.

Eksempel:

```text
1234567 = 2^20 + 185991
```

Her er:

- `e = 20`
- `rest = 185991`
- `2^20 = 1048576`
- `1048576 + 185991 = 1234567`

**Hvorfor gøre det?**  
Fordi store tal ofte kan beskrives effektivt ved at splitte “størrelsesorden” og “rest”. I en optisk lagringsmodel kan eksponenten tænkes som grov struktur og resten som finjustering. Det gør også sproget godt til at forklare, hvordan data kan pakkes over flere kanaler.

---

## Eksekverbare eksempler

### Eksempel 1: skriv og læs ét tal med CPL

Gem følgende som `examples/store_green.cpl`:

```cpl
var data = 1234567;                       // Opretter variablen data med værdien 1234567, fordi vi vil teste et stort tal.
store data at (5, 5, 5) colour GREEN;     // Skriver data til voxel (5,5,5) i GREEN, fordi grøn bruges som standardkanal.
load result from (5, 5, 5) colour GREEN;  // Læser værdien tilbage fra samme koordinat og kanal for at verificere roundtrip.
print result;                             // Udskriver resultatet, så du kan se at læsning matcher skrivning.
```

Kør med den compiler og simulator, der følger med dette repository:

```bash
cpl-run examples/store_green.cpl                 # Kompilerer CPL til CPA og kører programmet; forventer Output: [1234567].
cplc examples/store_green.cpl -o store_green.cpa # Gemmer den genererede CPA som tekst.
```

Forventet idé: Simulatoren skriver værdien til den grønne kanal og læser den tilbage fra samme voxel.

### Eksempel 2: samme idé i CPA

Gem følgende som `examples/store_green.cpa`:

```asm
LOAD.IMM grøn, 1234567              ; Indlæser tallet 1234567 i registeret grøn, fordi grøn kanal bruges som datakanal.
STORE.C (5,5,5), grøn, grøn         ; Skriver registeret grøn til voxel (5,5,5) i grøn kanal.
LOAD.C rød, (5,5,5), grøn           ; Læser samme grønne kanal tilbage i registeret rød, så vi kan bruge rød som outputregister.
OUT rød                             ; Sender den læste værdi til outputbufferen, så simulatoren kan vise resultatet.
HALT                                ; Stopper programmet, så VM'en ikke fortsætter efter demoen.
```

Kør med CPA-runneren:

```bash
cpa-run examples/store_green.cpa    # Assemblerer og kører CPA-programmet i krystalsimulatoren.
```

`cpa-run` kører tekstbaseret CPA. Dette repository definerer ikke et separat
binært CPA-filformat.

---

## Eksempel 3: RGB-billede i ét voxelplan

Dette eksempel viser idéen bag holografisk eller billedbaseret lagring. Hver pixel får tre kanaler: rød, grøn og blå.

```cpl
var red_value = 255;                       // Opretter rød intensitet for én pixel, fordi rød kanal repræsenterer pixelens R-komponent.
var green_value = 128;                     // Opretter grøn intensitet for samme pixel, fordi grøn kanal repræsenterer G-komponenten.
var blue_value = 64;                       // Opretter blå intensitet for samme pixel, fordi blå kanal repræsenterer B-komponenten.
store red_value at (10, 20, 0) colour RED; // Skriver rød komponent til voxel (10,20,0) i RED, så farven holdes separat.
store green_value at (10, 20, 0) colour GREEN; // Skriver grøn komponent til samme voxel i GREEN, fordi kanaler kan sameksistere.
store blue_value at (10, 20, 0) colour BLUE; // Skriver blå komponent til samme voxel i BLUE, så hele pixelens RGB-data ligger samlet.
load r from (10, 20, 0) colour RED;        // Læser rød komponent tilbage for rekonstruktion af pixelens farve.
load g from (10, 20, 0) colour GREEN;      // Læser grøn komponent tilbage for rekonstruktion af pixelens farve.
load b from (10, 20, 0) colour BLUE;       // Læser blå komponent tilbage for rekonstruktion af pixelens farve.
print r;                                   // Udskriver rød komponent, så vi kan kontrollere første del af roundtrip.
print g;                                   // Udskriver grøn komponent, så vi kan kontrollere anden del af roundtrip.
print b;                                   // Udskriver blå komponent, så vi kan kontrollere tredje del af roundtrip.
```

**Hvorfor samme voxel?**  
Fordi RGB-komponenterne tilhører samme logiske pixel. Ved at gemme dem i samme `(x, y, z)` men i tre forskellige farvekanaler bliver data nemmere at rekonstruere.

---

## Eksempel 4: specifikationsorienteret CPL med danske nøgleord

Denne form er nyttig i dokumentation og arkitekturtegninger:

```cpl
streng data = "Hello World";               // Definerer en tekststreng, fordi vi vil vise at tekst kan omsættes til taldata.
tal T = strengTilTal(data);                // Konverterer teksten til et tal, fordi krystallageret arbejder på numeriske værdier.
potens e = findEksponent(T);               // Finder eksponenten e, så tallet kan beskrives som 2^e + rest.
tal rest = T - (2^e);                      // Beregner restværdien, så den originale værdi kan rekonstrueres tabsfrit.
skriv_voxel(0, 0, 0) {                     // Vælger voxel (0,0,0), fordi demoen kun skal bruge én fysisk position.
    kanal grøn = e, rest = rest;           // Skriver e og rest i grøn kanal, fordi grøn bruges som letlæselig standardkanal.
}                                          // Afslutter voxelblokken, så compileren ved at skrivningen er komplet.
```

**Kan eksemplet køres?**  
Ja. Den viste `streng/tal/potens/skriv_voxel/kanal`-syntaks kompileres og
assembleres af pakken. De visuelle `hologram`-hjælpere i
`full_potential_demo.cpl` er demonstrationskonstruktioner; selve voxel-skrivning
og -læsning udføres i simulatoren.

---

## Eksempel 5: eksponentiel kodning i Python

Dette eksempel viser samme matematik, som sproget bygger på.

```python
def encode_value(value: int) -> tuple[int, int]:           # Definerer en funktion, der splitter et heltal i eksponent og rest.
    if value < 0:                                          # Tjekker negative værdier, fordi modellen kun koder ikke-negative tal.
        raise ValueError("Kun ikke-negative tal er tilladt") # Stopper programmet tydeligt, hvis input ikke kan kodes.
    if value == 0:                                         # Håndterer nul særskilt, fordi 2^e ellers altid er mindst 1.
        return 0, 0                                        # Returnerer e=0 og rest=0 som neutral repræsentation.
    exponent = value.bit_length() - 1                      # Finder største e, hvor 2^e er mindre end eller lig værdien.
    remainder = value - (1 << exponent)                    # Beregner resten ved at trække 2^e fra den oprindelige værdi.
    return exponent, remainder                             # Returnerer begge dele, så værdien kan rekonstrueres senere.

def decode_value(exponent: int, remainder: int) -> int:    # Definerer en funktion, der samler eksponent og rest til originalt tal.
    if exponent == 0:                                      # Genkender det kanoniske interval for nul og én.
        if remainder not in (0, 1):                        # Afviser ikke-kanoniske base-2-par, så datakorruption opdages.
            raise ValueError("Ugyldigt par ved exponent 0")
        return remainder                                   # Dekoder (0,0) som nul og (0,1) som én.
    return (1 << exponent) + remainder                     # Rekonstruerer alle værdier fra 2 og op som 2^e + rest.

e, rest = encode_value(1234567)                            # Koder testtallet, så vi kan se ChromaPlex-repræsentationen.
value = decode_value(e, rest)                              # Dekoder repræsentationen igen for at teste tabsfri roundtrip.
print(e, rest, value)                                      # Udskriver e, rest og rekonstrueret værdi til kontrol.
```

Kør lokalt:

```bash
python encode_demo.py                                      # Kører Python-demoen og viser eksponent, rest og rekonstrueret værdi.
```

---

## Use cases

### 1. Kulturarv og langtidsarkiv

Et nationalarkiv kan gemme dokumenter i en model, hvor retention efter skrivning ikke kræver aktiv strøm. ChromaPlex-sproget gør det muligt at beskrive, hvor dokumentindeks, metadata og selve payload-data placeres.

**Hvorfor er CPL relevant her?**  
Fordi arkivarer og udviklere kan tale om logiske datasæt, mens CPA kan bruges til at teste præcis placering og rekonstruktion.

### 2. Holografisk billedlagring

Billeddata kan fordeles over `RED`, `GREEN` og `BLUE` i samme voxelplan. Det gør det nemt at rekonstruere et billede, fordi alle tre farvekomponenter ligger fysisk samlet.

**Hvorfor bruge tre kanaler?**  
Fordi RGB-data naturligt består af tre komponenter. ChromaPlex-kanalerne matcher direkte denne struktur.

### 3. Videnskabelige måleserier

Store måletal, tidsserier eller indeksværdier kan beskrives som `2^e + rest`. Det gør sproget interessant til simulering af kompakte repræsentationer for store numeriske datasæt.

**Hvorfor eksponent + rest?**  
Fordi eksponenten beskriver størrelsesordenen, mens resten bevarer præcisionen.

### 4. Turing-komplethed og sprogdesign

CPA kan bruges som target for andre sprog. Projektets Brainfuck-til-CPA-kompilator viser, hvordan et kendt Turing-komplet sprog kan oversættes til voxel-baserede operationer.

**Hvorfor er det vigtigt?**  
Fordi det flytter CPA fra “lagerformat” til “beregningsmodel”. Det viser, at instruktionssættet kan bruges til mere end simple writes og reads.

---

## Fejlfinding

### Problem: `Ukendt mnemonic`

Årsag: CPA-instruktionen findes ikke i assemblerens nuværende subset.

Løsning:

```asm
HALT                                ; Test først at assembleren accepterer den simpleste instruktion.
```

Derefter tilføjes én instruktion ad gangen.

### Problem: Værdien læses som 0

Årsag: Du læser sandsynligvis fra forkert voxel eller forkert farvekanal.

Kontrollér:

```cpl
store data at (5, 5, 5) colour GREEN;     // Skriver til GREEN ved koordinat (5,5,5).
load result from (5, 5, 5) colour GREEN;  // Læser fra præcis samme kanal og koordinat.
```

### Problem: Voxel uden for område

Årsag: Koordinaterne ligger uden for simulatorens krystalstørrelse.

Løsning:

```cpl
store data at (0, 0, 0) colour GREEN;     // Brug laveste sikre koordinat for at teste at programmet virker.
```

---

## Sprog-reference

### CPL nøgleord

| Nøgleord | Betydning |
|----------|-----------|
| `var` | Opretter en variabel i den toolchain-venlige CPL-syntaks. |
| `store` | Skriver en værdi til et voxel. |
| `load` | Læser en værdi fra et voxel. |
| `print` | Udskriver en værdi fra et register eller en variabel. |
| `tal` | Deklarerer numerisk værdi i den specifikationsorienterede syntaks. |
| `potens` | Deklarerer en eksponentværdi. |
| `streng` | Deklarerer tekstdata. |
| `skriv_voxel` | Starter en voxel-skriveblok. |
| `kanal` | Angiver farvekanal i en voxelblok. |

### CPA registre og farver

| Register / kanal | Rolle |
|------------------|------|
| `rød` | Rød kanal eller generelt register i dansk CPA-syntaks. |
| `grøn` | Grøn kanal eller standard datakanal. |
| `blå` | Blå kanal eller hjælpeværdi. |
| `violet` | Violet kanal, ofte brugt til eksponenter eller metadata. |
| `uv` | UV-kanal, ofte brugt til indeks eller metadata. |
| `r`, `b` | Generelle hjælpe-/Brainfuck-registre i den nuværende CPA-simulator. |

### Farver

| Navn | Engelsk navn | Bølgelængde |
|------|--------------|-------------|
| `uv` | `UV` | 350 nm |
| `violet` | `VIOLET` | 405 nm |
| `blå` | `BLUE` | 473 nm |
| `grøn` | `GREEN` | 532 nm |
| `rød` | `RED` | 650 nm |

---

## Videre læsning

- [`README.md`](../README.md) — projektets GitHub-forside.
- [`FAQ.md`](../FAQ.md) — korte svar til presse, udviklere og tech-interesserede.
- [`docs/language_spec.md`](language_spec.md) — kompakt teknisk sprogspecifikation.
- [`docs/storage_capacity_proof.md`](storage_capacity_proof.md) — kapacitetsargument og fysisk motivation.
- [`docs/turing_completeness.md`](turing_completeness.md) — Turing-komplethedsargument via Brainfuck.
- [`chromaplex/cpl_compiler.py`](../chromaplex/cpl_compiler.py) — den autoritative CPL-compiler.
- [`chromaplex/cpa_assembler.py`](../chromaplex/cpa_assembler.py) — den autoritative CPA-assembler.
- [3D browserdemo](https://Janus5G.github.io/chromaplex-os/) — interaktiv softwaredemo.

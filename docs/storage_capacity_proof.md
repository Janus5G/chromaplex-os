# Kapacitetsmodel for farvekodede 3D-krystaller

## Status

Dette repository indeholder en softwaremodel, ikke et fysisk kapacitetsbevis.
Simulatoren viser, hvordan flere navngivne farvekanaler kan adresseres ved samme
`(x, y, z)`-koordinat. Den måler ikke voxelafstand, optisk crosstalk,
signal/støj-forhold, skriveenergi eller fysisk retention.

## Hvad koden faktisk demonstrerer

- Sparse 3D-voxeladressering i `CrystalSimulator`.
- Fem logisk adskilte kanaler: rød, grøn, blå, violet og UV.
- Tabsfri heltalsroundtrip med en kanonisk eksponent/rest-repræsentation.
- Planlæsning gennem simulatorens Python-API `load_plane`.

Eksponent/rest er en numerisk repræsentation, ikke automatisk komprimering.
Lagringsgevinsten afhænger af det konkrete serialiseringsformat og datasættet.
Denne version definerer ikke et fysisk eller binært pakkeformat.

## Hvad der kræves for et fysisk kapacitetsbevis

Et publicerbart fysisk resultat kræver mindst:

1. Målt voxelgeometri og antal reproducerbare tilstande pr. voxel.
2. Fejlrate før og efter fejlkorrigering.
3. Crosstalkmålinger mellem bølgelængder, vinkler og nabovoxels.
4. Et præcist binært format inklusive eksponent, rest og metadata.
5. Rådata, måleudstyr, kalibrering og reproducerbar forsøgsprotokol.

Indtil disse data findes, bør konkrete værdier for bits/cm³, GB/s, TB/s,
retention og energiforbrug omtales som hypoteser eller designmål — ikke som
verificerede egenskaber ved ChromaPlex OS.

# Security Policy

## Scope

Dette repository er en eksperimentel Python-prototype og browserdemo. Det må ikke behandles som produktionsklar hardwarestyring eller som sikker lagerinfrastruktur.

## Rapporter sårbarheder

Opret en privat security advisory på GitHub eller kontakt maintainer via en ikke-offentlig kanal. Del ikke secrets eller exploit-kode i offentlige issues.

## Baseline-krav

- Kør tests før merge: `python -m pytest tests/ -q`
- Kør statisk analyse i CI: `ruff`, `bandit`, `pip-audit` eller tilsvarende.
- Branch protection på `main`: kræv PR, review og grøn CI.
- Commit aldrig `.env`, API-nøgler, tokens, private nøgler eller genererede build-artifacts.
- Brug Dependabot eller tilsvarende dependency scanning.

## Kendte begrænsninger

- `index.html` og `demo/index.html` henter Three.js fra CDN. Før produktion bør dependency vendoreres lokalt eller låses med Subresource Integrity.
- AI-funktionen kræver `OPENAI_API_KEY`; nøglen må kun ligge i miljøvariabler/secrets manager.
- Browserdemoen er kun en lokal simulator og må ikke bruges til at behandle følsomme data.

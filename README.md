# Kandidatarbete

Detta repository innehåller kod och datafiler kopplade till kandidatarbetet *Generering av syntetiska data för virtuella simuleringar av trafikolyckor*. Projektet behandlar generering, utvärdering och konvertering av syntetiska trafikolycksdata till ett FHIR-kompatibelt format för vidare användning i en simulerings- och interoperabilitetskontext.

## Innehåll

Repositoryt innehåller implementationer för:

- preprocessing och strukturering av trafikolycksdata
- generering av syntetiska data med flera generativa modeller
- kvantitativ utvärdering av syntetisk datakvalitet
- visualisering av verklig och syntetisk data
- konvertering av syntetiska dataposter till FHIR-resurser
- export av en FHIR Bundle för testning mot Virtuality

## Modeller

Följande modeller har implementerats och utvärderats:

- Fristående CTGAN
- CTGANSynthesizer via SDV
- GaussianCopulaSynthesizer via SDV
- TVAESynthesizer via SDV

## Viktiga filer

| Fil | Beskrivning |
|---|---|
| `CTGAN.ipynb` | Implementation av fristående CTGAN-modell. |
| `CTGANMETA (1).ipynb` | Senaste rensade implementationen av CTGAN via SDV:s CTGANSynthesizer. |
| `Copy_of_GAUSSIANCOPULA (11)_clean.ipynb` | Senaste rensade implementationen av GaussianCopulaSynthesizer. |
| `TVAE (1)_clean.ipynb` | Senaste rensade implementationen av TVAESynthesizer. |
| `fhir_final_bundle.json` | Slutlig FHIR Bundle med syntetiska resurser för testning och validering. |

## FHIR-struktur

Det valda syntetiska datasetet har konverterats till en FHIR-baserad JSON-struktur. Varje syntetiskt trafikolycksfall representeras med resurser såsom:

- `Patient`
- `Encounter`
- `Observation`
- `Provenance`

Samtliga resurser samlas i en gemensam FHIR `Bundle` av typen `collection`.

## Syfte

Syftet med repositoryt är att möjliggöra granskning och reproducerbarhet av den tekniska implementationen bakom kandidatarbetet. Koden kompletterar metodbeskrivningen i rapporten och visar hur syntetisk trafikolycksdata har genererats, utvärderats och förberetts för interoperabel användning.

## Kommentar

Notebook-filerna är utvecklade inom ramen för ett proof-of-concept och är främst avsedda för metodgranskning, reproducerbarhet och fortsatt utveckling.

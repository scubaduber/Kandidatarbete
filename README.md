# Kandidatarbete

Detta repository innehåller kod och datafiler kopplade till kandidatarbetet *Generering av syntetiska data för virtuella simuleringar av trafikolyckor*. Projektet behandlar generering, utvärdering och konvertering av syntetiska trafikolycksdata till ett FHIR-kompatibelt format för vidare användning i en simulerings- och interoperabilitetskontext.

## Innehåll

Repositoryt innehåller implementationer för:

- preprocessing och strukturering av trafikolycksdata
- generering av syntetiska data med flera generativa modeller
- kvantitativ utvärdering av syntetisk datakvalitet
- visualisering av verklig och syntetisk data
- konvertering av syntetiska dataposter till FHIR-resurser
- export av olycksvisa FHIR-Bundles för testning mot Virtuality

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
| `virtualityvalidator` | Notebook för att skapa Virtuality-kompatibla FHIR-Bundles. |
| `manifest.json` | Manifestfil som listar genererade olycksvisa FHIR-Bundles, inklusive filnamn, olycks-ID, antal entries och filstorlek. |
| `synthetic_crash_accident_0.json` | Exempel på en syntetisk olycka representerad som en separat FHIR Bundle. |

## FHIR-struktur

Det valda syntetiska datasetet har konverterats till en FHIR-baserad JSON-struktur. Varje syntetiskt trafikolycksfall representeras som en separat FHIR `Bundle` av typen `collection`. Detta gjordes för att följa Virtualitys begränsningar för maximal filstorlek och maximalt antal entries per Bundle.

Varje olycks-Bundle innehåller resurser såsom:

- `Patient`
- `Encounter`
- `Observation`
- `Provenance`

De kvantitativa observationerna har kompletterats med UCUM-kompatibla enheter där det är tillämpligt. För olycksspecifika variabler används projektspecifika kodsystemreferenser direkt i FHIR-resurserna, eftersom flera av variablerna inte har entydiga motsvarigheter i exempelvis LOINC eller SNOMED CT.

## Virtuality-validering

Den ursprungliga exporten samlade samtliga syntetiska olyckor i en gemensam FHIR Bundle. Vid testning mot Virtualitys validator överskred denna både gränsen för maximal payload-storlek och maximalt antal entries. Exporten ändrades därför så att varje syntetisk olycka sparas som en egen Bundle.

I repositoryt inkluderas en manifestfil samt en exempel-Bundle för att visa strukturen. Den fullständiga exporten kan återskapas genom att köra `virtualityvalidator.ipynb`.

## Syfte

Syftet med repositoryt är att möjliggöra granskning och reproducerbarhet av den tekniska implementationen bakom kandidatarbetet. Koden kompletterar metodbeskrivningen i rapporten och visar hur syntetisk trafikolycksdata har genererats, utvärderats och förberetts för interoperabel användning.

## Kommentar

Notebook-filerna är utvecklade inom ramen för ett proof-of-concept och är främst avsedda för metodgranskning, reproducerbarhet och fortsatt utveckling.

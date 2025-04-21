# TipsMästaren - Datakatalog

Denna katalog innehåller data som används för att träna och testa TipsMästarens prediktionsmodeller.

## Datafiler

- `pl.csv`: Premier League-matcher med resultat och odds från olika bokmakers
- `cs.csv`: Championship-matcher med resultat och odds från olika bokmakers

## Dataformat

Datafilerna är i CSV-format och innehåller följande kolumner:

- `Div`: Division (liga)
- `Date`, `Time`: Datum och tid för matchen
- `HomeTeam`, `AwayTeam`: Hem- och bortalag
- `FTHG`, `FTAG`: Mål för hem- och bortalag vid full tid
- `FTR`: Resultat vid full tid (H=Hemmaseger, D=Oavgjort, A=Bortaseger)
- `HTHG`, `HTAG`, `HTR`: Mål och resultat vid halvtid
- `HS`, `AS`: Antal skott för hem- och bortalag
- `HST`, `AST`: Antal skott på mål för hem- och bortalag
- `HC`, `AC`: Antal hörnor för hem- och bortalag
- Diverse oddskolumner från olika bokmakers (B365, BW, PS, etc.)
- `AvgH`, `AvgD`, `AvgA`: Genomsnittliga odds för 1, X, 2

## Hantering av data

För att träna modellen på din egen maskin:

1. Placera datafiler i denna katalog
2. Kör skripten i `backend/train_model.py` för att bygga prediktionsmodellen

Observera att tränade modeller sparas i `models/`-katalogen.
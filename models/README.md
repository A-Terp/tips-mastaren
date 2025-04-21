# TipsMästaren - Modellkatalog

Denna katalog innehåller tränade maskininlärningsmodeller som används för prediktioner i TipsMästaren.

## Modellformat

Modellerna sparas vanligtvis i .joblib-format och innehåller:

- Tränad klassificeringsmodell (XGBoost eller annan)
- Skalning/normalisering (StandardScaler)
- Feature-information
- Metadata om träningen

## Generera modeller

För att träna nya modeller, kör:

```bash
python backend/train_model.py
```

Se till att du har data i data/-katalogen innan du tränar modellerna.
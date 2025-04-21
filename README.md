# TipsMästaren

En app för att prediktera och optimera spel på Stryktipset baserat på data och riskprofil.

## Beskrivning

TipsMästaren är ett verktyg som hjälper till att analysera matcher i Stryktipset och ger optimerade spelförslag baserat på data och användarens riskvilja. Applikationen använder historisk matchdata och odds för att prediktera sannolikheter för olika utfall (1, X, 2) och ger spelförslag anpassade efter användarens budget och riskprofil.

## Funktioner

- Prediktering av sannolikheter för utfall i Stryktipsetmatcher (1, X, 2)
- Justering av spelförslag baserat på användarens budget
- Tre olika risknivåer (låg, medium, hög) för anpassad spelstrategi
- Visualisering av prediktioner och värde jämfört med odds och streckfördelning

## Projektstruktur

- `/backend` - Python backend med prediktionsmodell och API
- `/frontend` - React frontend för användargränssnitt
- `/data` - Exempeldata och scripts för databehandling
- `/models` - Tränade modeller

## Installation

### Backend

```bash
cd backend
pip install -r requirements.txt
python app.py
```

### Frontend

```bash
cd frontend
npm install
npm start
```

## Användning

1. Starta backend-servern
2. Starta frontend-applikationen
3. Ange de aktuella matcherna i Stryktipset
4. Välj budget och risknivå
5. Få optimerade spelförslag

## Teknologier

- **Backend**: Python, Flask, scikit-learn, pandas
- **Frontend**: React, Tailwind CSS, Chart.js
- **Data**: Historiska matchresultat, odds och statistik
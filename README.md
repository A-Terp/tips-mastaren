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
cd tips-mastaren
pip install -r backend/requirements.txt
python3 backend/app.py
```

### Frontend

```bash
cd frontend
npm install
npm start
```

## Användning

1. **Förbered data**:
   Placera CSV-filerna (`pl.csv` och `cs.csv`) i `/data`-katalogen

2. **Träna modellen**:
   ```bash
   cd tips-mastaren
   python3 backend/train_model.py
   ```
   Detta skapar en modell i `/models`-katalogen

3. **Starta backend**:
   ```bash
   cd backend
   python3 app.py
   ```
   
4. **Starta frontend** (i ett nytt terminalfönster):
   ```bash
   cd frontend
   npm install
   npm start
   ```

5. **Använd appen**:
   - Öppna webbläsaren på `http://localhost:3000`
   - Ange matcher genom att fylla i lag och odds
   - Justera budget och risknivå
   - Klicka på "Generera prediktioner"

## Teknologier

- **Backend**: Python, Flask, scikit-learn, pandas
- **Frontend**: React, Tailwind CSS, Chart.js
- **Data**: Historiska matchresultat, odds och statistik
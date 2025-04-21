import React, { useState } from 'react';

function MatchForm({ onAddMatch }) {
  const [homeTeam, setHomeTeam] = useState('');
  const [awayTeam, setAwayTeam] = useState('');
  const [oddHome, setOddHome] = useState('');
  const [oddDraw, setOddDraw] = useState('');
  const [oddAway, setOddAway] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    
    // Validera fält
    if (!homeTeam || !awayTeam) {
      alert('Lagnamn måste anges');
      return;
    }
    
    // Skapa match-objekt
    const match = {
      home_team: homeTeam,
      away_team: awayTeam,
      AvgH: oddHome || undefined,
      AvgD: oddDraw || undefined,
      AvgA: oddAway || undefined
    };
    
    // Skicka till förälder
    onAddMatch(match);
    
    // Återställ formuläret
    setHomeTeam('');
    setAwayTeam('');
    setOddHome('');
    setOddDraw('');
    setOddAway('');
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div>
          <label className="block text-gray-700 mb-1">Hemmalag</label>
          <input 
            type="text" 
            value={homeTeam} 
            onChange={(e) => setHomeTeam(e.target.value)}
            className="w-full p-2 border rounded"
            placeholder="Hemmalag"
            required
          />
        </div>
        
        <div>
          <label className="block text-gray-700 mb-1">Bortalag</label>
          <input 
            type="text" 
            value={awayTeam} 
            onChange={(e) => setAwayTeam(e.target.value)}
            className="w-full p-2 border rounded"
            placeholder="Bortalag"
            required
          />
        </div>
      </div>
      
      <div className="grid grid-cols-3 gap-4">
        <div>
          <label className="block text-gray-700 mb-1">1 (odds)</label>
          <input 
            type="number" 
            value={oddHome} 
            onChange={(e) => setOddHome(e.target.value)}
            className="w-full p-2 border rounded"
            placeholder="1.50"
            step="0.01"
            min="1.01"
          />
        </div>
        
        <div>
          <label className="block text-gray-700 mb-1">X (odds)</label>
          <input 
            type="number" 
            value={oddDraw} 
            onChange={(e) => setOddDraw(e.target.value)}
            className="w-full p-2 border rounded"
            placeholder="3.25"
            step="0.01"
            min="1.01"
          />
        </div>
        
        <div>
          <label className="block text-gray-700 mb-1">2 (odds)</label>
          <input 
            type="number" 
            value={oddAway} 
            onChange={(e) => setOddAway(e.target.value)}
            className="w-full p-2 border rounded"
            placeholder="6.00"
            step="0.01"
            min="1.01"
          />
        </div>
      </div>
      
      <div>
        <button 
          type="submit" 
          className="bg-green-500 hover:bg-green-600 text-white py-2 px-4 rounded"
        >
          Lägg till match
        </button>
      </div>
    </form>
  );
}

export default MatchForm;
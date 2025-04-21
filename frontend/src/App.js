import React, { useState, useEffect } from 'react';
import axios from 'axios';
import MatchForm from './components/MatchForm';
import Results from './components/Results';
import './App.css';

const API_URL = 'http://localhost:5000/api';

function App() {
  const [matches, setMatches] = useState([]);
  const [budget, setBudget] = useState(100);
  const [riskLevel, setRiskLevel] = useState('medium');
  const [results, setResults] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  useEffect(() => {
    // Kolla om API:et är aktivt
    axios.get(`${API_URL}/health`)
      .catch(err => {
        setError('Kunde inte ansluta till API. Kontrollera att backend-servern körs.');
      });
  }, []);

  const handleAddMatch = (match) => {
    setMatches([...matches, { ...match, id: Date.now() }]);
  };

  const handleRemoveMatch = (id) => {
    setMatches(matches.filter(match => match.id !== id));
  };

  const handleUpdateMatch = (id, updatedMatch) => {
    setMatches(matches.map(match => match.id === id ? { ...updatedMatch, id } : match));
  };

  const handleBudgetChange = (e) => {
    setBudget(parseInt(e.target.value));
  };

  const handleRiskChange = (e) => {
    setRiskLevel(e.target.value);
  };

  const handlePredict = async () => {
    if (matches.length === 0) {
      setError('Lägg till minst en match först.');
      return;
    }

    setLoading(true);
    setError('');
    try {
      const response = await axios.post(`${API_URL}/predict`, {
        matches,
        budget,
        risk_level: riskLevel
      });
      setResults(response.data);
    } catch (err) {
      setError('Fel vid hämtning av prediktioner: ' + (err.response?.data?.error || err.message));
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-100">
      <header className="bg-blue-600 text-white p-4 shadow-md">
        <h1 className="text-3xl font-bold">TipsMästaren</h1>
        <p className="text-sm">Optimera dina Stryktipsspel med prediktioner baserade på data</p>
      </header>

      <main className="container mx-auto p-4">
        {error && (
          <div className="bg-red-100 border-l-4 border-red-500 text-red-700 p-4 mb-4" role="alert">
            <p>{error}</p>
          </div>
        )}

        <div className="bg-white p-6 rounded-lg shadow-md mb-6">
          <h2 className="text-xl font-semibold mb-4">Inställningar</h2>
          
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label className="block text-gray-700 mb-2">Budget (SEK)</label>
              <input 
                type="number" 
                value={budget} 
                onChange={handleBudgetChange}
                className="w-full p-2 border rounded"
                min="1"
              />
            </div>
            
            <div>
              <label className="block text-gray-700 mb-2">Risknivå</label>
              <select 
                value={riskLevel} 
                onChange={handleRiskChange}
                className="w-full p-2 border rounded"
              >
                <option value="low">Låg</option>
                <option value="medium">Medium</option>
                <option value="high">Hög</option>
              </select>
            </div>
          </div>
        </div>

        <div className="bg-white p-6 rounded-lg shadow-md mb-6">
          <h2 className="text-xl font-semibold mb-4">Matcher</h2>
          <MatchForm onAddMatch={handleAddMatch} />
          
          {matches.length > 0 && (
            <div className="mt-4">
              <h3 className="text-lg font-medium mb-2">Tillagda matcher</h3>
              <div className="space-y-3">
                {matches.map(match => (
                  <div key={match.id} className="flex items-center justify-between p-2 border rounded bg-gray-50">
                    <span>
                      {match.home_team} vs {match.away_team}
                    </span>
                    <div>
                      <button 
                        onClick={() => handleRemoveMatch(match.id)}
                        className="text-red-500 hover:text-red-700 ml-2"
                      >
                        Ta bort
                      </button>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}
          
          <div className="mt-6">
            <button 
              onClick={handlePredict}
              disabled={loading || matches.length === 0}
              className="bg-blue-500 hover:bg-blue-600 text-white py-2 px-4 rounded disabled:opacity-50"
            >
              {loading ? 'Bearbetar...' : 'Generera prediktioner'}
            </button>
          </div>
        </div>

        {results && <Results results={results} />}
      </main>
      
      <footer className="bg-gray-800 text-white text-center p-4 mt-8">
        <p>© {new Date().getFullYear()} TipsMästaren - En app för optimerade Stryktipsspel</p>
      </footer>
    </div>
  );
}

export default App;
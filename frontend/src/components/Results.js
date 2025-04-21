import React from 'react';
import { Bar } from 'react-chartjs-2';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
} from 'chart.js';

ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend
);

function Results({ results }) {
  const { predictions, system, expected_value, win_probability } = results;

  // Förbereda data för diagram
  const chartData = {
    labels: predictions.map((p, i) => `Match ${i+1}`),
    datasets: [
      {
        label: 'Hemmaseger (1)',
        data: predictions.map(p => p.probabilities['1'] * 100),
        backgroundColor: 'rgba(54, 162, 235, 0.6)',
      },
      {
        label: 'Oavgjort (X)',
        data: predictions.map(p => p.probabilities['X'] * 100),
        backgroundColor: 'rgba(255, 206, 86, 0.6)',
      },
      {
        label: 'Bortaseger (2)',
        data: predictions.map(p => p.probabilities['2'] * 100),
        backgroundColor: 'rgba(255, 99, 132, 0.6)',
      },
    ],
  };

  const chartOptions = {
    responsive: true,
    plugins: {
      legend: {
        position: 'top',
      },
      title: {
        display: true,
        text: 'Predikterade sannolikheter per match',
      },
    },
    scales: {
      y: {
        beginAtZero: true,
        max: 100,
        title: {
          display: true,
          text: 'Sannolikhet (%)',
        },
      },
    },
  };

  return (
    <div className="bg-white p-6 rounded-lg shadow-md">
      <h2 className="text-xl font-semibold mb-4">Resultat</h2>
      
      <div className="mb-6">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
          <div className="bg-blue-50 p-4 rounded-md">
            <h3 className="font-medium text-blue-800">Förväntat värde</h3>
            <p className="text-2xl font-bold">{expected_value.toFixed(2)} SEK</p>
          </div>
          
          <div className="bg-green-50 p-4 rounded-md">
            <h3 className="font-medium text-green-800">Vinstchans</h3>
            <p className="text-2xl font-bold">{(win_probability * 100).toFixed(2)}%</p>
          </div>
        </div>
      </div>
      
      <div className="mb-6">
        <h3 className="text-lg font-medium mb-3">Rekommenderat spelsystem</h3>
        <div className="overflow-x-auto">
          <table className="min-w-full bg-white border">
            <thead>
              <tr className="bg-gray-100">
                <th className="py-2 px-4 border">Match</th>
                <th className="py-2 px-4 border">Hemmalag</th>
                <th className="py-2 px-4 border">Bortalag</th>
                <th className="py-2 px-4 border">Val</th>
                <th className="py-2 px-4 border">1</th>
                <th className="py-2 px-4 border">X</th>
                <th className="py-2 px-4 border">2</th>
              </tr>
            </thead>
            <tbody>
              {system.map((match, index) => (
                <tr key={index} className={index % 2 === 0 ? 'bg-gray-50' : 'bg-white'}>
                  <td className="py-2 px-4 border text-center">{match.match_index}</td>
                  <td className="py-2 px-4 border">{match.home_team}</td>
                  <td className="py-2 px-4 border">{match.away_team}</td>
                  <td className="py-2 px-4 border font-bold">{match.selection.join(', ')}</td>
                  <td className="py-2 px-4 border text-center">
                    {(match.probabilities['1'] * 100).toFixed(1)}%
                  </td>
                  <td className="py-2 px-4 border text-center">
                    {(match.probabilities['X'] * 100).toFixed(1)}%
                  </td>
                  <td className="py-2 px-4 border text-center">
                    {(match.probabilities['2'] * 100).toFixed(1)}%
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
      
      <div className="mt-6">
        <h3 className="text-lg font-medium mb-3">Sannolikheter per match</h3>
        <div style={{ height: '400px' }}>
          <Bar data={chartData} options={chartOptions} />
        </div>
      </div>
    </div>
  );
}

export default Results;
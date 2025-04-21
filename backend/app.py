from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import numpy as np
import json
import os
from predictor import MatchPredictor
from optimizer import StryktipsetOptimizer

app = Flask(__name__)
CORS(app)

# Ladda modellen vid uppstart
predictor = MatchPredictor()

@app.route('/api/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()
        matches = data.get('matches', [])
        budget = data.get('budget', 100)
        risk_level = data.get('risk_level', 'medium')
        
        # Anropa prediktorn för att få sannolikheter
        predictions = predictor.predict(matches)
        
        # Optimera system baserat på budget och risknivå
        optimizer = StryktipsetOptimizer(predictions, budget, risk_level)
        result = optimizer.optimize()
        
        return jsonify({
            'predictions': predictions,
            'system': result['system'],
            'expected_value': result['expected_value'],
            'win_probability': result['win_probability']
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'ok'})

if __name__ == '__main__':
    app.run(debug=True)
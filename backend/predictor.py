#!/usr/bin/env python3

import pandas as pd
import numpy as np
import joblib
import os
from sklearn.preprocessing import StandardScaler
from xgboost import XGBClassifier

class MatchPredictor:
    def __init__(self, model_path=None):
        self.model = None
        self.scaler = None
        self.feature_columns = [
            'AvgH', 'AvgD', 'AvgA',        # Genomsnittliga odds
            'MaxH', 'MaxD', 'MaxA',        # Maximala odds
            'AHh',                         # Asian Handicap
            'Avg>2.5', 'Avg<2.5'          # Över/under 2.5 mål
        ]
        
        # Om ingen modell laddas, träna en ny
        if model_path and os.path.exists(model_path):
            self.load_model(model_path)
        else:
            self.train_model()
    
    def load_model(self, model_path):
        """Ladda förtränad modell"""
        model_data = joblib.load(model_path)
        self.model = model_data['model']
        self.scaler = model_data['scaler']
        self.feature_columns = model_data.get('features', self.feature_columns)
    
    def train_model(self):
        """Träna en ny modell på historisk data"""
        # I en riktig implementation skulle vi ladda historisk data
        # och träna modellen här. För enkelhetens skull används en
        # dummy-modell tills vidare.
        
        self.model = XGBClassifier(random_state=42)
        self.scaler = StandardScaler()
        
        # Här skulle träning ske...
        # För demo, gör en dummy-modell
        print("Dummy-modell skapad - i verklig implementation skulle träning ske")
    
    def extract_features(self, match_data):
        """Extrahera relevanta features från matchdata"""
        features = []
        
        for match in match_data:
            # Extrahera önskade features från matchdata
            match_features = [match.get(feat, 0) for feat in self.feature_columns]
            features.append(match_features)
            
        return np.array(features)
    
    def predict(self, matches):
        """Prediktera sannolikheter för matcher"""
        # För demo - returnera simulerade sannolikheter
        # I verkligheten skulle vi använda vår tränade modell
        
        predictions = []
        
        for match in matches:
            home_team = match.get('home_team', 'Unknown')
            away_team = match.get('away_team', 'Unknown')
            
            # Simulera sannolikheter baserat på odds om de finns, annars slumpa
            home_odds = match.get('AvgH', None)
            draw_odds = match.get('AvgD', None)
            away_odds = match.get('AvgA', None)
            
            if home_odds and draw_odds and away_odds:
                # Konvertera odds till sannolikheter
                total = 1/float(home_odds) + 1/float(draw_odds) + 1/float(away_odds)
                home_prob = (1/float(home_odds)) / total
                draw_prob = (1/float(draw_odds)) / total
                away_prob = (1/float(away_odds)) / total
            else:
                # Slumpa sannolikheter om odds saknas
                probs = np.random.dirichlet(np.ones(3))
                home_prob, draw_prob, away_prob = probs
            
            predictions.append({
                'home_team': home_team,
                'away_team': away_team,
                'probabilities': {
                    '1': float(home_prob),
                    'X': float(draw_prob),
                    '2': float(away_prob)
                }
            })
        
        return predictions

    def save_model(self, path):
        """Spara tränad modell till fil"""
        model_data = {
            'model': self.model,
            'scaler': self.scaler,
            'features': self.feature_columns
        }
        joblib.dump(model_data, path)
#!/usr/bin/env python3

import pandas as pd
import numpy as np
import os
import joblib
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from xgboost import XGBClassifier
from sklearn.metrics import accuracy_score, log_loss, confusion_matrix
from data_processor import DataProcessor

def train_and_save_model(output_path='../models/match_predictor.joblib'):
    """Träna prediktionsmodell och spara till disk"""
    print("Förbereder data för träning...")
    
    # Ladda och förbered data
    processor = DataProcessor(data_path='../data')
    processor.load_data(['pl.csv', 'cs.csv'])  # Anpassa filnamn efter behov
    X, y = processor.prepare_training_data()
    
    if X is None or y is None:
        print("Kunde inte förbereda träningsdata. Avslutar.")
        return False
    
    # Dela upp i tränings- och testdata
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Skala features
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    print(f"Tränar modell på {X_train.shape[0]} matcher...")
    
    # Träna XGBoost-modell
    model = XGBClassifier(
        n_estimators=100,
        max_depth=5,
        learning_rate=0.1,
        random_state=42,
        objective='multi:softprob',
        num_class=3
    )
    
    model.fit(X_train_scaled, y_train)
    
    # Utvärdera modellen
    y_pred = model.predict(X_test_scaled)
    y_pred_proba = model.predict_proba(X_test_scaled)
    
    accuracy = accuracy_score(y_test, y_pred)
    loss = log_loss(y_test, y_pred_proba)
    conf_matrix = confusion_matrix(y_test, y_pred)
    
    print(f"Modellprestanda:")
    print(f"Accuracy: {accuracy:.4f}")
    print(f"Log Loss: {loss:.4f}")
    print(f"Confusion Matrix:\n{conf_matrix}")
    
    # Spara modellen
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    model_data = {
        'model': model,
        'scaler': scaler,
        'features': X.columns.tolist(),
        'metadata': {
            'accuracy': accuracy,
            'log_loss': loss,
            'training_samples': X_train.shape[0],
            'feature_importance': dict(zip(X.columns, model.feature_importances_))
        }
    }
    
    joblib.dump(model_data, output_path)
    print(f"Modell sparad till {output_path}")
    
    return True

if __name__ == "__main__":
    train_and_save_model()
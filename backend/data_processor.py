import pandas as pd
import numpy as np
import os

class DataProcessor:
    def __init__(self, data_path='../data'):
        self.data_path = data_path
        self.processed_data = None
    
    def load_data(self, files):
        """Ladda data från CSV-filer"""
        data_frames = []
        
        for file in files:
            file_path = os.path.join(self.data_path, file)
            if os.path.exists(file_path):
                df = pd.read_csv(file_path)
                data_frames.append(df)
        
        if data_frames:
            self.processed_data = pd.concat(data_frames, ignore_index=True)
            print(f"Laddade {len(self.processed_data)} matcher från {len(data_frames)} filer")
        else:
            print("Inga datafiler hittades")
    
    def preprocess(self):
        """Förbehandla data för modelträning"""
        if self.processed_data is None:
            print("Ingen data att förbehandla")
            return None
        
        # Rensa data och hantera saknade värden
        df = self.processed_data.copy()
        
        # Ersätt saknade odds med genomsnitt
        numeric_columns = df.select_dtypes(include=['float64', 'int64']).columns
        df[numeric_columns] = df[numeric_columns].fillna(df[numeric_columns].mean())
        
        # Konvertera kategoriska variabler
        df['FTR'] = df['FTR'].map({'H': 0, 'D': 1, 'A': 2})
        
        # Skapa nya features baserat på oddsskillnader
        if 'AvgH' in df.columns and 'AvgA' in df.columns:
            df['OddsRatio'] = df['AvgH'] / df['AvgA']
        
        return df
    
    def prepare_training_data(self):
        """Förbered data för träning"""
        if self.processed_data is None:
            print("Ingen data att förbereda")
            return None, None
        
        df = self.preprocess()
        
        # Välj features och target
        features = [
            'AvgH', 'AvgD', 'AvgA',        # Genomsnittliga odds
            'MaxH', 'MaxD', 'MaxA',        # Maximala odds
            'AHh',                         # Asian Handicap
            'Avg>2.5', 'Avg<2.5'          # Över/under 2.5 mål
        ]
        
        # Filtrera kolumner som faktiskt finns i data
        available_features = [f for f in features if f in df.columns]
        
        if not available_features:
            print("Inga tillgängliga features hittades")
            return None, None
        
        if 'FTR' not in df.columns:
            print("Målvariabel (FTR) saknas")
            return None, None
        
        X = df[available_features]
        y = df['FTR']
        
        print(f"Träningsdata förberedd med {len(available_features)} features och {len(y)} rader")
        return X, y
    
    def get_recent_matches(self, n=100):
        """Hämta de senaste matcherna för test/validering"""
        if self.processed_data is None:
            print("Ingen data att hämta")
            return None
        
        # Sortera efter datum om möjligt
        if 'Date' in self.processed_data.columns:
            sorted_data = self.processed_data.sort_values('Date', ascending=False)
            return sorted_data.head(n)
        else:
            # Om inget datum finns, ta de sista n raderna
            return self.processed_data.tail(n)
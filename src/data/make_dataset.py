import pandas as pd
import os
from pathlib import Path

def load_raw_data():
    """Charge les données brutes depuis data/raw"""
    raw_dir = Path(__file__).resolve().parents[2] / 'data' / 'raw'
    # Adapter selon vos fichiers bruts
    df = pd.read_csv(raw_dir / 'your_raw_file.csv')
    return df

def load_clean_data():
    """Charge les données nettoyées depuis data/processed"""
    processed_dir = Path(__file__).resolve().parents[2] / 'data' / 'processed'
    return pd.read_csv(processed_dir / 'df_clean.csv')

def save_clean_data(df):
    """Sauvegarde les données nettoyées"""
    processed_dir = Path(__file__).resolve().parents[2] / 'data' / 'processed'
    df.to_csv(processed_dir / 'df_clean.csv', index=False)
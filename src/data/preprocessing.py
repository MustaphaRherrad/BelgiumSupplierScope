import pandas as pd

def clean_data(df):
    """Effectue le nettoyage des données"""
    # Je copie ici toutes mes étapes de nettoyage que j'ai fait dans le notebook
    
    # Exemple basique :
    df_clean = df.copy()
    
    # 1. Suppression des colonnes vides
    df_clean = df_clean.dropna(axis=1, how='all')
    
    # 2. Conversion des colonnes booléennes
    bool_cols = ['bid_iswinning', 'bid_issubcontracted', 'bid_isconsortium']
    for col in bool_cols:
        if col in df_clean.columns:
            df_clean[col] = df_clean[col].astype(bool)
    
    # 3. Autres transformations...
    
    return df_clean
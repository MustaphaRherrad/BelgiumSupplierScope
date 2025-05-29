import pandas as pd
import numpy as np
from pathlib import Path
import matplotlib.pyplot as plt
import seaborn as sns

def calculate_expense_metrics(df):
    """
    Calcule les métriques principales des dépenses
    """
    # Conversion des prix en euros si nécessaire
    if 'currency' in df.columns:
        df = convert_currency_to_eur(df)
    
    # Agrégations par année - 
    yearly_expense = df.groupby('tender_year')['tender_finalprice'].agg(
        ['sum', 'mean', 'median', 'count']
    ).reset_index()
    yearly_expense.columns = ['tender_year', 'total', 'mean', 'median', 'count']
    
    # Autres métriques à calculer... peut-être!!!
    
    return {
        'yearly_expense': yearly_expense,
        # autres résultats...
    }

def convert_currency_to_eur(df):
    """
    Convertit tous les prix en euros en utilisant des taux de change
    """
    # Implémentation à compléter je n'aurais pas besoin ici!
    return df


def calculate_market_metrics(df):
    """
    Calcule les métriques clés par année :
    - Nombre de marchés
    - Dépense moyenne
    - Dépense médiane
    """
    # Conversion en numérique et filtrage
    df = df[df['tender_finalprice'].notna()].copy()
    df['tender_finalprice'] = pd.to_numeric(df['tender_finalprice'], errors='coerce')
    
    # Agrégation par année
    metrics = df.groupby('tender_year')['tender_finalprice'].agg(
        n_markets=('size'),  # Nombre de marchés
        mean_spending=('mean'),  # Dépense moyenne
        median_spending=('median')  # Dépense médiane
    ).reset_index()
    
    return metrics

def calculate_all_expense_metrics(df):
    """Calcule toutes les métriques de dépenses"""
    market_metrics = calculate_market_metrics(df)
    
    return {
        'market_metrics': market_metrics,
        # Ajouter d'autres métriques ici...
    }

def calculate_buyer_metrics(df):
    """
    Calcule les métriques par type d'acheteur :
    - Dépenses par buyer_buyertype
    - Dépenses par buyer_mainactivities
    """
    # Nettoyage préalable
    df = df[df['tender_finalprice'].notna()].copy()
    df['tender_finalprice'] = pd.to_numeric(df['tender_finalprice'])
    
    # Métriques par type d'acheteur
    by_buyertype = (df.groupby('buyer_buyertype')['tender_finalprice']
                    .agg(total=('sum'),
                        mean=('mean'),
                        count=('count'))
                    .reset_index()
                    .sort_values('total', ascending=False))
    
    # Métriques par activité principale
    by_activity = (df.groupby('buyer_mainactivities')['tender_finalprice']
                   .agg(total=('sum'),
                       mean=('mean'),
                       count=('count'))
                   .reset_index()
                   .sort_values('total', ascending=False))
    
    return {
        'by_buyertype': by_buyertype,
        'by_activity': by_activity
    }


def calculate_price_differences(df):
    """
    Calcule les différences et ratios entre prix estimés et finaux
    """
    # Filtrer les données valides
    df = df[(df['tender_estimatedprice'] > 0) & 
            (df['tender_finalprice'] > 0)].copy()
    
    # Calculer les métriques
    df['price_difference'] = df['tender_finalprice'] - df['tender_estimatedprice']
    df['price_ratio'] = df['tender_finalprice'] / df['tender_estimatedprice']
    df['price_difference_pct'] = (df['price_difference'] / df['tender_estimatedprice']) * 100
    
    return df

def analyze_by_procedure_type(df):
    """
    Analyse les différences de prix par type de procédure
    """
    price_stats = df.groupby('tender_proceduretype').agg({
        'price_difference': ['mean', 'median', 'std'],
        'price_ratio': ['mean', 'median', 'std'],
        'price_difference_pct': ['mean', 'median'],
        'tender_id': 'count'
    }).reset_index()
    
    # Renommer les colonnes
    price_stats.columns = ['_'.join(col).strip() if col[1] else col[0] 
                          for col in price_stats.columns]
    
    return price_stats.rename(columns={'tender_id_count': 'n_observations'})
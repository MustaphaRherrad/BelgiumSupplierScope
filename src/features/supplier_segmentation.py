import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import MinMaxScaler

def create_kraljic_matrix(df):
    """Crée la matrice de Kraljic avec gestion des modalités"""
    # Calcul des métriques pour Kraljic
    supplier_stats = df.groupby('bidder_masterid').agg({
        'bid_price': ['sum', 'count', 'std'],
        'tender_proceduretype': lambda x: (x == 'OPEN').mean(),
        'corr_proc': 'mean',
        'tender_maincpv': lambda x: x.mode()[0] if not x.mode().empty else None,
        'bidder_country': lambda x: x.mode()[0] if not x.mode().empty else 'Unknown'
    }).reset_index()
    
    # Aplatir les colonnes multi-niveaux
    supplier_stats.columns = ['bidder_masterid', 'total_spend', 'bid_count', 
                            'price_std', 'open_procedure_rate', 
                            'avg_corr_risk', 'main_cpv', 'main_country']
    
    # Nettoyage des pays (prendre le premier si c'est une liste)
    supplier_stats['main_country'] = supplier_stats['main_country'].apply(
        lambda x: x[0] if isinstance(x, (list, np.ndarray)) else x)
    
    # Calcul des dimensions Kraljic
    supplier_stats['impact'] = supplier_stats['total_spend'] * supplier_stats['bid_count']
    supplier_stats['risk'] = supplier_stats['price_std'].fillna(0) * \
                           (1 - supplier_stats['open_procedure_rate'].fillna(0)) * \
                           supplier_stats['avg_corr_risk'].fillna(0)
    
    # Normalisation
    scaler = MinMaxScaler()
    supplier_stats[['impact_norm', 'risk_norm']] = scaler.fit_transform(
        supplier_stats[['impact', 'risk']])
    
    # Segmentation
    impact_segment = pd.cut(supplier_stats['impact_norm'], 
                          bins=[0, 0.5, 1], 
                          labels=['Low', 'High']).astype(str)
    risk_segment = pd.cut(supplier_stats['risk_norm'], 
                        bins=[0, 0.5, 1], 
                        labels=['Low', 'High']).astype(str)
    
    supplier_stats['kraljic_segment'] = impact_segment + '_' + risk_segment
    
    return supplier_stats
'''
def plot_kraljic_matrix(supplier_stats, save_path='reports/figures/kraljic_matrix.png'):
    plt.figure(figsize=(12, 10))
    
    # Simplifier les pays pour éviter trop de catégories
    supplier_stats['country_group'] = supplier_stats['main_country'].apply(
        lambda x: x if x in supplier_stats['main_country'].value_counts().head(5).index else 'Autres')
    
    sns.scatterplot(
        data=supplier_stats,
        x='risk_norm',
        y='impact_norm',
        hue='kraljic_segment',
        style='country_group',  # Utiliser le groupe de pays simplifié
        size='total_spend',
        sizes=(20, 200),
        palette='viridis',
        alpha=0.7
    )
    
    plt.axhline(0.5, color='gray', linestyle='--')
    plt.axvline(0.5, color='gray', linestyle='--')
    plt.title("Matrice de Kraljic des Fournisseurs")
    plt.xlabel("Risque (normalisé)")
    plt.ylabel("Impact (normalisé)")
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    plt.close()
'''
import os
from pathlib import Path

def plot_kraljic_matrix(supplier_stats, save_path=None):
    """
    Visualise et sauvegarde la matrice de Kraljic
    Args:
        supplier_stats: DataFrame contenant les données
        save_path: Chemin complet ou None pour dossier par défaut
    """
    # Chemin par défaut relatif au projet
    if save_path is None:
        project_root = Path(__file__).resolve().parents[2]  # Remonte jusqu'au dossier racine
        save_path = project_root / 'reports' / 'figures' / 'kraljic_matrix.png'
    
    # Conversion en Path object si nécessaire
    save_path = Path(save_path)
    
    # Création des dossiers avec vérification
    save_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Création du graphique
    plt.figure(figsize=(12, 10))
    
    supplier_stats['country_group'] = supplier_stats['main_country'].apply(
        lambda x: x if x in supplier_stats['main_country'].value_counts().head(5).index else 'Autres')
    
    sns.scatterplot(
        data=supplier_stats,
        x='risk_norm',
        y='impact_norm',
        hue='kraljic_segment',
        style='country_group',
        size='total_spend',
        sizes=(20, 200),
        palette='viridis',
        alpha=0.7
    )
    
    plt.axhline(0.5, color='gray', linestyle='--')
    plt.axvline(0.5, color='gray', linestyle='--')
    plt.title("Matrice de Kraljic des Fournisseurs")
    plt.xlabel("Risque (normalisé)")
    plt.ylabel("Impact (normalisé)")
    plt.text(0.25, 0.25, 'Articles Simples', ha='center', fontsize=10)
    plt.text(0.75, 0.25, 'Articles Leviers', ha='center', fontsize=10)
    plt.text(0.25, 0.75, 'Articles Critiques', ha='center', fontsize=10)
    plt.text(0.75, 0.75, 'Articles Stratégiques', ha='center', fontsize=10)
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    
    # Sauvegarde avec vérification
    try:
        plt.savefig(str(save_path), dpi=300, bbox_inches='tight')  # str() pour compatibilité
        print(f"Graphique sauvegardé avec succès dans : {save_path}")
    except Exception as e:
        print(f"Échec de la sauvegarde : {e}")
        print(f"Vérifiez les permissions sur : {save_path.parent}")
    
    plt.close()
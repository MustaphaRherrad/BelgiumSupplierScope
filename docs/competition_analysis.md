Voici comment organiser proprement l'analyse de concurrence dans la structure existante :

### 1. Organisation des fichiers

```
belgiumsupplierscope/
├── notebooks/
│   └── competition_analysis.ipynb      # Notebook principal d'exécution
├── src/
│   ├── features/
│   │   └── competition_analysis.py    # Nouvelles métriques de concurrence
│   ├── visualizations/
│   │   └── competition_visuals.py     # Visualisations spécifiques
│   └── data/
│       └── competition_processing.py  # Prétraitement des données compétition
├── reports/
│   ├── figures/
│   │   └── competition/               # Nouveau dossier pour les visuels
│   ├── tables/
│   │   └── competition/               # Nouveau dossier pour les tables
│   └── competition_report.md          # Rapport synthétique
```

### 2. Contenu des fichiers

**src/features/competition_analysis.py**
```python
import pandas as pd

def calculate_competition_metrics(df):
    """Calcule les métriques de base de concurrence"""
    metrics = {
        'avg_bids_per_tender': df['tender_recordedbidscount'].mean(),
        'single_bidding_rate': (df.groupby('tender_id')['bid_id']
                               .transform('count') == 1).mean(),
        'unique_suppliers_count': df['bidder_id'].nunique()
    }
    return metrics

def calculate_hhi(df, group_col='tender_maincpv'):
    """Calcule l'indice Herfindahl-Hirschman par groupe"""
    def hhi(group):
        market_shares = group['bid_price'] / group['bid_price'].sum()
        return (market_shares**2).sum() * 10000
    
    return df.groupby(group_col).apply(hhi).reset_index(name='hhi_index')

def calculate_pareto(df):
    """Analyse Pareto des fournisseurs"""
    supplier_share = df.groupby('bidder_name')['bid_price'].sum().sort_values(ascending=False)
    supplier_share = supplier_share.reset_index()
    supplier_share['cum_pct'] = (supplier_share['bid_price'].cumsum() / 
                                supplier_share['bid_price'].sum()) * 100
    return supplier_share
```

**src/visualizations/competition_visuals.py**
```python
import matplotlib.pyplot as plt
import seaborn as sns

def plot_competition_heatmap(competition_stats, save_path=None):
    """Heatmap des métriques de concurrence"""
    plt.figure(figsize=(12, 8))
    sns.heatmap(competition_stats.set_index('tender_proceduretype'),
                annot=True, cmap='YlGnBu', fmt='.1f')
    plt.title('Métriques de Concurrence par Type de Procédure')
    if save_path:
        plt.savefig(save_path, bbox_inches='tight', dpi=300)
    plt.close()

def plot_pareto_curve(pareto_df, save_path=None):
    """Courbe de Pareto des fournisseurs"""
    plt.figure(figsize=(10, 6))
    plt.plot(pareto_df['cum_pct'], 'b-')
    plt.axhline(80, color='r', linestyle='--')
    plt.title('Analyse Pareto des Fournisseurs')
    plt.xlabel('Nombre de Fournisseurs (triés)')
    plt.ylabel('Part Cumulative du Montant Total (%)')
    if save_path:
        plt.savefig(save_path, bbox_inches='tight', dpi=300)
    plt.close()
```

**src/data/competition_processing.py**
```python
from pathlib import Path
from ..features import competition_analysis
from ..visualizations import competition_visuals

def process_competition_data(df, output_dir):
    """Pipeline complet d'analyse de concurrence"""
    # Création des dossiers
    Path(f"{output_dir}/figures/competition").mkdir(parents=True, exist_ok=True)
    Path(f"{output_dir}/tables/competition").mkdir(parents=True, exist_ok=True)
    
    # Calcul des métriques
    hhi_results = competition_analysis.calculate_hhi(df)
    pareto_results = competition_analysis.calculate_pareto(df)
    
    # Sauvegarde
    hhi_results.to_csv(f"{output_dir}/tables/competition/hhi_results.csv", index=False)
    pareto_results.to_csv(f"{output_dir}/tables/competition/pareto_results.csv", index=False)
    
    # Visualisations
    competition_visuals.plot_pareto_curve(
        pareto_results,
        save_path=f"{output_dir}/figures/competition/pareto_curve.png"
    )
    
    return hhi_results, pareto_results
```

### 3. Notebook d'exécution (notebooks/competition_analysis.ipynb)

```python
# %% Imports
from src.data.competition_processing import process_competition_data
import pandas as pd

# %% Chargement des données
df = pd.read_csv("data/processed/df_clean.csv")  # Adaptez le chemin

# %% Exécution de l'analyse
output_dir = "reports"
hhi_results, pareto_results = process_competition_data(df, output_dir)

# %% Affichage des résultats
display(hhi_results.head())
display(pareto_results.head())

# %% Analyse complémentaire
top_suppliers = pareto_results[pareto_results['cum_pct'] <= 80]
print(f"Nombre de fournisseurs réalisant 80% du CA: {len(top_suppliers)}")
```

### 4. Rapport (reports/competition_report.md)

```markdown
# Analyse de Concurrence - BelgiumSupplierScope

## Métriques Clés
- Taux d'attribution unique: {single_bidding_rate}%
- Nombre moyen d'offres par appel: {avg_bids_per_tender}
- Indice HHI moyen: {mean_hhi}

## Principaux Résultats
![Courbe Pareto](figures/competition/pareto_curve.png)

## Recommandations
1. Surveiller les procédures à faible concurrence
2. Analyser les secteurs avec HHI > 2500
3. Diversifier les fournisseurs stratégiques
```

### 5. Exécution ordonnée

1. Exécuter le notebook `competition_analysis.ipynb`
2. Les résultats seront sauvegardés dans :
   - `reports/tables/competition/` pour les données brutes
   - `reports/figures/competition/` pour les visualisations
3. Le rapport se génère automatiquement dans `reports/competition_report.md`

Cette structure maintient une séparation claire entre :
- Le code de traitement (src/data)
- Les calculs métiers (src/features)
- La visualisation (src/visualizations)
- L'exécution et exploration (notebooks)
- Le reporting final (reports)
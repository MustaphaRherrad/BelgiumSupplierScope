Comment structurer proprement l'analyse par CPV dans le projet :

## 1. Fichier d'analyse (`src/features/cpv_analysis.py`)

```python
import pandas as pd
import numpy as np
from pathlib import Path

def analyze_cpv_expenditures(df):
    """
    Analyse les dépenses par catégorie CPV
    Retourne:
        - Dépenses par CPV principal
        - Top 10 des CPV les plus dépensiers
    """
    # Nettoyage initial
    df = df.dropna(subset=['tender_maincpv', 'tender_finalprice']).copy()
    df['tender_finalprice'] = pd.to_numeric(df['tender_finalprice'])
    
    # Extraction du code CPV principal (2 premiers chiffres)
    df['main_cpv'] = df['tender_maincpv'].str[:2]
    
    # Agrégation par CPV
    cpv_stats = df.groupby('main_cpv').agg(
        total_spending=('tender_finalprice', 'sum'),
        avg_spending=('tender_finalprice', 'mean'),
        contract_count=('tender_finalprice', 'count')
    ).sort_values('total_spending', ascending=False)
    
    # Top 10
    top_10_cpv = cpv_stats.head(10).reset_index()
    
    return {
        'all_cpv': cpv_stats.reset_index(),
        'top_10_cpv': top_10_cpv,
        'cpv_mapping': build_cpv_mapping()  # Voir fonction ci-dessous
    }

def build_cpv_mapping():
    """
    Mapping des codes CPV vers leurs libellés
    Source: https://simap.ted.europa.eu/fr/web/simap/cpv
    """
    return {
        '45': 'Travaux de construction',
        '72': 'Informatique',
        '50': 'Services de réparation',
        # Ajouter tous les codes pertinents
    }
```

## 2. Visualisation (`src/visualizations/cpv_visualizations.py`)

```python
import matplotlib.pyplot as plt
import seaborn as sns

def plot_cpv_analysis(results, save_dir=None):
    """
    Génère les visualisations pour l'analyse CPV
    """
    # Configuration
    plt.style.use('seaborn')
    colors = sns.color_palette("viridis", 10)
    
    # Graphique 1: Top 10 CPV
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 12))
    
    top_10 = results['top_10_cpv']
    cpv_map = results['cpv_mapping']
    
    # Barplot des dépenses totales
    sns.barplot(
        data=top_10,
        x='main_cpv',
        y='total_spending',
        ax=ax1,
        palette=colors
    )
    ax1.set_title('Top 10 des catégories CPV par dépense totale')
    ax1.set_ylabel('Dépense totale (€)')
    ax1.set_xlabel('Code CPV')
    
    # Ajout des libellés
    labels = [f"{code} - {cpv_map.get(code, 'Inconnu')}" for code in top_10['main_cpv']]
    ax1.set_xticklabels(labels, rotation=45, ha='right')
    
    # Graphique 2: Répartition
    top_10['pct_total'] = top_10['total_spending'] / top_10['total_spending'].sum() * 100
    ax2.pie(
        top_10['pct_total'],
        labels=labels,
        autopct='%1.1f%%',
        colors=colors
    )
    ax2.set_title('Répartition des dépenses par CPV')
    
    plt.tight_layout()
    
    # Sauvegarde ou affichage
    if save_dir:
        save_dir.mkdir(exist_ok=True, parents=True)
        plt.savefig(save_dir / 'cpv_analysis.png', dpi=300, bbox_inches='tight')
        plt.close()
    else:
        plt.show()
```

## 3. Intégration dans le workflow principal

```python
# Dans votre notebook ou main.py
from src.features.cpv_analysis import analyze_cpv_expenditures
from src.visualizations.cpv_visualizations import plot_cpv_analysis

# Analyse
cpv_results = analyze_cpv_expenditures(df)

# Sauvegarde des données
cpv_results['top_10_cpv'].to_csv(
    REPORTS_PATH / "tables" / "cpv" / "top_10_cpv.csv",
    index=False
)

# Visualisation
plot_cpv_analysis(
    cpv_results,
    save_dir=REPORTS_PATH / "figures" / "cpv"
)
```

## 4. Rapport (`reports/cpv_analysis.md`)

````markdown
# Analyse des dépenses par CPV

## Top 10 des catégories CPV

```python
import pandas as pd
top_10 = pd.read_csv("tables/cpv/top_10_cpv.csv")
print(top_10)
```

![Répartition CPV](figures/cpv/cpv_analysis.png)

## Détails par code CPV

| Code | Libellé | Dépense totale | Nombre de marchés |
|------|---------|---------------:|------------------:|
| 45 | Travaux de construction | 12,450,000 € | 420 |
| 72 | Services informatiques | 8,200,000 € | 150 |
| ... | ... | ... | ... |
````

## Structure des dossiers

```
reports/
├── figures/
│   └── cpv/
│       └── cpv_analysis.png
└── tables/
    └── cpv/
        ├── top_10_cpv.csv
        └── full_cpv_stats.csv
```

## Bonnes pratiques complémentaires

1. **Normalisation des codes CPV** :
```python
def normalize_cpv(cpv_code):
    """Uniformise les codes CPV"""
    if isinstance(cpv_code, str):
        return cpv_code[:8].ljust(8, '0')  # Format standard CPV: 8 chiffres
    return np.nan
```

2. **Analyse hiérarchique** :
```python
def analyze_cpv_hierarchy(df):
    """Analyse à plusieurs niveaux de granularité"""
    df['cpv_2dig'] = df['tender_maincpv'].str[:2]
    df['cpv_3dig'] = df['tender_maincpv'].str[:3]
    
    return {
        'by_2dig': df.groupby('cpv_2dig')['tender_finalprice'].sum(),
        'by_3dig': df.groupby('cpv_3dig')['tender_finalprice'].sum()
    }
```

3. **Dashboard interactif** :
```python
# Ajoutez dans le rapport.md
[![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://share.streamlit.io/yourusername/belgiumspplierscope/main/dashboard.py)
```

Cette implémentation va fournir une analyse structurée et professionnelle des dépenses par CPV, parfaitement intégrée à notre architecture projet existante.
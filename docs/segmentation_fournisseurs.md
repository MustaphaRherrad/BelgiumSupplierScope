# Segmentation et Cartographie des Fournisseurs pour BelgiumSupplierScope

Voici une approche structurée pour réaliser ces analyses , en organisant les résultats dans l'arborescence de ce projet.

## 1. Matrice de Kraljic

Pour cartographier les fournisseurs selon le risque et l'impact:

```python
# Dans src/features/supplier_segmentation.py

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import MinMaxScaler

def create_kraljic_matrix(df):
    # Calcul des métriques pour Kraljic
    supplier_stats = df.groupby('bidder_masterid').agg({
        'bid_price': ['sum', 'count', 'std'],
        'tender_proceduretype': lambda x: (x == 'OPEN').mean(),
        'corr_proc': 'mean',
        'tender_maincpv': pd.Series.mode,
        'bidder_country': pd.Series.mode
    }).reset_index()
    
    supplier_stats.columns = ['bidder_masterid', 'total_spend', 'bid_count', 
                            'price_std', 'open_procedure_rate', 
                            'avg_corr_risk', 'main_cpv', 'main_country']
    
    # Calcul des dimensions Kraljic
    supplier_stats['impact'] = supplier_stats['total_spend'] * supplier_stats['bid_count']
    supplier_stats['risk'] = supplier_stats['price_std'] * (1 - supplier_stats['open_procedure_rate']) * supplier_stats['avg_corr_risk']
    
    # Normalisation
    scaler = MinMaxScaler()
    supplier_stats[['impact_norm', 'risk_norm']] = scaler.fit_transform(
        supplier_stats[['impact', 'risk']])
    
    # Segmentation
    supplier_stats['kraljic_segment'] = pd.cut(
        supplier_stats['impact_norm'], bins=[0, 0.5, 1], labels=['Low', 'High']) + '_' + \
        pd.cut(supplier_stats['risk_norm'], bins=[0, 0.5, 1], labels=['Low', 'High'])
    
    return supplier_stats

def plot_kraljic_matrix(supplier_stats, save_path='reports/figures/kraljic_matrix.png'):
    plt.figure(figsize=(10, 8))
    sns.scatterplot(data=supplier_stats, x='risk_norm', y='impact_norm', 
                    hue='kraljic_segment', style='main_country', size='total_spend')
    plt.axhline(0.5, color='gray', linestyle='--')
    plt.axvline(0.5, color='gray', linestyle='--')
    plt.title("Matrice de Kraljic des Fournisseurs")
    plt.xlabel("Risque (normalisé)")
    plt.ylabel("Impact (normalisé)")
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    plt.savefig(save_path)
    plt.close()
```

## 2. Segmentation Géographique

```python
# Dans src/visualization/geo_visualization.py

import geopandas as gpd
import contextily as ctx

def plot_supplier_buyer_geo(df, belgium_shapefile='data/external/belgium_nuts.shp', 
                           save_dir='reports/figures/geo_analysis/'):
    # Charger les données géographiques
    belgium = gpd.read_file(belgium_shapefile)
    
    # Préparation des données
    suppliers = df.dropna(subset=['bidder_nuts', 'bidder_masterid']).groupby(
        ['bidder_nuts', 'bidder_masterid']).size().reset_index(name='counts')
    buyers = df.dropna(subset=['buyer_nuts']).groupby(
        ['buyer_nuts']).size().reset_index(name='counts')
    
    # Fusion avec les données géo
    suppliers_geo = belgium.merge(suppliers, left_on='NUTS_ID', right_on='bidder_nuts')
    buyers_geo = belgium.merge(buyers, left_on='NUTS_ID', right_on='buyer_nuts')
    
    # Visualisation
    fig, ax = plt.subplots(1, 2, figsize=(20, 10))
    
    suppliers_geo.plot(column='counts', ax=ax[0], legend=True, 
                      cmap='Reds', scheme='quantiles')
    ax[0].set_title("Répartition Géographique des Fournisseurs")
    
    buyers_geo.plot(column='counts', ax=ax[1], legend=True, 
                   cmap='Blues', scheme='quantiles')
    ax[1].set_title("Répartition Géographique des Acheteurs")
    
    for a in ax:
        ctx.add_basemap(a, crs=belgium.crs.to_string(), source=ctx.providers.CartoDB.Positron)
    
    plt.savefig(f'{save_dir}supplier_buyer_geo_distribution.png')
    plt.close()
```

## 3. Analyse par CPV

```python
# Dans src/features/cpv_analysis.py

def analyze_cpv_dominance(df, top_n=10, save_dir='reports/tables/'):
    # Analyse des fournisseurs dominants par CPV
    cpv_suppliers = df.groupby(['tender_maincpv', 'bidder_masterid']).agg({
        'bid_price': 'sum',
        'bid_id': 'count'
    }).reset_index()
    
    # Classement par CPV
    cpv_rank = cpv_suppliers.sort_values(['tender_maincpv', 'bid_price'], 
                                        ascending=[True, False])
    top_suppliers_per_cpv = cpv_rank.groupby('tender_maincpv').head(top_n)
    
    # Sauvegarde
    top_suppliers_per_cpv.to_csv(f'{save_dir}top_suppliers_by_cpv.csv', index=False)
    
    # Visualisation
    top_cpvs = df['tender_maincpv'].value_counts().head(top_n).index
    plt.figure(figsize=(12, 8))
    for cpv in top_cpvs:
        subset = top_suppliers_per_cpv[top_suppliers_per_cpv['tender_maincpv'] == cpv].head(5)
        plt.barh(subset['bidder_masterid'], subset['bid_price'], label=cpv)
    
    plt.title(f"Top {top_n} Fournisseurs par CPV Principal")
    plt.xlabel("Montant Total des Contrats")
    plt.ylabel("Fournisseur")
    plt.legend()
    plt.tight_layout()
    plt.savefig(f'reports/figures/top_suppliers_by_cpv.png')
    plt.close()
```

## Workflow d'Exécution

Dans un notebook Jupyter (`notebooks/Supplier_Segmentation_Analysis.ipynb`):

```python
# Chargement des données
from src.data.make_dataset import load_clean_data
df = load_clean_data()

# 1. Matrice de Kraljic
from src.features.supplier_segmentation import create_kraljic_matrix, plot_kraljic_matrix
supplier_stats = create_kraljic_matrix(df)
plot_kraljic_matrix(supplier_stats)

# 2. Analyse Géographique
from src.visualization.geo_visualization import plot_supplier_buyer_geo
plot_supplier_buyer_geo(df)

# 3. Analyse par CPV
from src.features.cpv_analysis import analyze_cpv_dominance
analyze_cpv_dominance(df)
```

## Structure des Résultats

Les résultats seront organisés comme suit:

```
reports/
├── figures/
│   ├── kraljic_matrix.png
│   ├── supplier_buyer_geo_distribution.png
│   ├── top_suppliers_by_cpv.png
│   └── geo_analysis/
│       └── [autres cartes géographiques]
└── tables/
    └── top_suppliers_by_cpv.csv
```

## Recommandations Supplémentaires

1. Pour la matrice de Kraljic, je peux affiner les métriques de risque et d'impact en:
   - Ajoutant des données externes sur la stabilité financière des fournisseurs
   - Considérant la criticité des CPV (services essentiels vs. non-essentiels)

2. Pour l'analyse géographique:
   - Utiliser des données de densité économique par région NUTS
   - Croiser avec des indicateurs socio-économiques

3. Pour l'analyse CPV:
   - Normaliser par la taille du marché total par CPV
   - Calculer des indices de concentration (HHI) par segment CPV

Ces analyses fourniront une vue complète du paysage des fournisseurs en Belgique, permettant d'identifier les fournisseurs stratégiques, les risques géographiques et les domaines de spécialisation.

---

Voici comment intégrer notre matrice de Kraljic avec les autres analyses dans un dashboard interactif Plotly, tout en conservant la version actuelle du graphique :

### 1. Version Interactive de la Matrice Kraljic (Plotly)

```python
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

def create_interactive_kraljic(supplier_stats):
    # Création du scatter plot interactif
    fig = px.scatter(
        supplier_stats,
        x='risk_norm',
        y='impact_norm',
        color='kraljic_segment',
        hover_name='bidder_masterid',
        hover_data=['main_cpv', 'main_country', 'total_spend'],
        labels={
            'risk_norm': 'Risque d\'Approvisionnement',
            'impact_norm': 'Impact Stratégique',
            'kraljic_segment': 'Segment Kraljic'
        },
        title='Matrice de Kraljic Interactive'
    )
    
    # Ajout des lignes de quadrant
    fig.add_hline(y=0.5, line_dash="dash", line_color="grey")
    fig.add_vline(x=0.5, line_dash="dash", line_color="grey")
    
    # Annotation des quadrants
    annotations = [
        dict(x=0.25, y=0.25, text="Articles Simples", showarrow=False, font=dict(size=14)),
        dict(x=0.75, y=0.25, text="Articles Leviers", showarrow=False, font=dict(size=14)),
        dict(x=0.25, y=0.75, text="Articles Critiques", showarrow=False, font=dict(size=14)),
        dict(x=0.75, y=0.75, text="Articles Stratégiques", showarrow=False, font=dict(size=14))
    ]
    
    fig.update_layout(annotations=annotations)
    return fig
```

### 2. Dashboard Complet avec Plotly Dash

Créer un fichier `dashboard.py` dans le dossier `dashboards/` :

```python
import dash
from dash import dcc, html
import plotly.express as px
from src.features.supplier_segmentation import create_kraljic_matrix
from src.visualization.geo_visualization import create_geo_plot
from src.features.cpv_analysis import create_cpv_chart

app = dash.Dash(__name__)

# Chargement des données
df = load_clean_data()  # Utiliser la fonction de chargement
supplier_stats = create_kraljic_matrix(df)

app.layout = html.Div([
    html.H1("Analyse des Fournisseurs - BelgiumSupplierScope"),
    
    dcc.Tabs([
        dcc.Tab(label='Matrice Kraljic', children=[
            dcc.Graph(figure=create_interactive_kraljic(supplier_stats))
        ]),
        
        dcc.Tab(label='Analyse Géographique', children=[
            dcc.Graph(figure=create_geo_plot(df))
        ]),
        
        dcc.Tab(label='Analyse par CPV', children=[
            dcc.Graph(figure=create_cpv_chart(df))
        ])
    ])
])

if __name__ == '__main__':
    app.run_server(debug=True)
```

### 3. Fonctions Supplémentaires Nécessaires

Dans `src/visualization/geo_visualization.py` :

```python
def create_geo_plot(df):
    # Adaptez votre fonction existante pour retourner un plotly figure
    fig = px.scatter_geo(df.dropna(subset=['bidder_nuts']),
                        lat='latitude', 
                        lon='longitude',
                        hover_name='bidder_name',
                        scope='europe',
                        center={'lat': 50.5, 'lon': 4.5},
                        title='Localisation des Fournisseurs')
    return fig
```

Dans `src/features/cpv_analysis.py` :

```python
def create_cpv_chart(df):
    top_cpvs = df['tender_maincpv'].value_counts().nlargest(10).index
    fig = px.sunburst(
        df[df['tender_maincpv'].isin(top_cpvs)],
        path=['tender_maincpv', 'bidder_name'],
        values='bid_price',
        title='Répartition des Marchés par CPV et Fournisseur'
    )
    return fig
```

### 4. Structure Finale Recommandée

```
belgium-supplier-scope/
├── dashboards/
│   ├── dashboard.py          # Fichier principal du dashboard
│   └── assets/               # CSS/JS personnalisés
├── src/
│   ├── visualization/
│   │   ├── geo_visualization.py  # Fonctions géo modifiées
│   │   └── kraljic_visual.py     # Version plotly de Kraljic
│   └── ... 
└── ...
```

### 5. Exécution

Lancer le dashboard avec :
```bash
python dashboards/dashboard.py
```

### Points Clés :

1. **Conservation** de la version matplotlib existante
2. **Interactivité** : tooltips sur les points, zoom, filtrage
3. **Navigation** par onglets entre les analyses
4. **Responsive** : s'adapte à différents écrans

Ce dashboard permettra de :
- Visualiser la concentration dans les "articles simples"
- Identifier les rares fournisseurs "leviers"
- Croiser avec la localisation géographique
- Analyser la répartition par CPV

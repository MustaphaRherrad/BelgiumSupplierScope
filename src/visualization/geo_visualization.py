import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
import contextily as ctx
from pathlib import Path
import os

def plot_supplier_buyer_geo(df, save_dir='reports/figures/geo_analysis/'):
    """Version corrigée avec gestion des colonnes variables"""
    # 1. Chemin absolu vers les fichiers
    project_root = Path(__file__).resolve().parents[2]
    nuts_dir = project_root / 'data' / 'external' / 'NUTS_BN_01M_2021_4326'
    shapefile = nuts_dir / 'belgium_nuts.shp'
    
    # 2. Vérification des fichiers
    required_files = ['belgium_nuts.shp', 'belgium_nuts.dbf', 'belgium_nuts.shx']
    missing_files = [f for f in required_files if not (nuts_dir / f).exists()]
    
    if missing_files:
        raise FileNotFoundError(
            f"Fichiers manquants dans {nuts_dir}:\n"
            f"{', '.join(missing_files)}\n"
            "Vérifiez les noms et extensions des fichiers"
        )

    # 3. Chargement avec détection automatique du code pays
    '''
    try:
        belgium = gpd.read_file(str(shapefile))
        
        # Détection de la colonne de code pays
        country_code_col = None
        for col in ['CNTR_CODE', 'cntr_code', 'ISO2', 'country']:
            if col in belgium.columns:
                country_code_col = col
                break
                
        if country_code_col:
            belgium = belgium[belgium[country_code_col] == 'BE']
        else:
            print("Avertissement : Colonne de code pays non trouvée - utilisation de toutes les données")
            
    except Exception as e:
        raise RuntimeError(f"Erreur de lecture : {str(e)}")'''
        
    belgium = gpd.read_file(str(shapefile))
    print("Avertissement : Pas de colonne de code pays, toutes les entités du shapefile seront utilisées.")
    belgium['NUTS_BN_ID'] = belgium['NUTS_BN_ID'].astype(str)  # Conversion en string
    
    # Préparation des données (inchangé)
    suppliers = df.dropna(subset=['bidder_nuts', 'bidder_masterid']).groupby(
        ['bidder_nuts', 'bidder_masterid']).size().reset_index(name='counts')
    buyers = df.dropna(subset=['buyer_nuts']).groupby(
        ['buyer_nuts']).size().reset_index(name='counts')
    suppliers['bidder_nuts'] = suppliers['bidder_nuts'].astype(str)  # Conversion
    buyers['buyer_nuts'] = buyers['buyer_nuts'].astype(str)          # Conversion
    
    # Fusion sur la bonne colonne
    suppliers_geo = belgium.merge(suppliers, left_on='NUTS_BN_ID', right_on='bidder_nuts')
    buyers_geo = belgium.merge(buyers, left_on='NUTS_BN_ID', right_on='buyer_nuts')


    # Nettoyage des données
    suppliers_geo = suppliers_geo[
        ~suppliers_geo.geometry.isna() & 
        suppliers_geo.geometry.is_valid
    ]
    suppliers_geo['counts'] = pd.to_numeric(suppliers_geo['counts'], errors='coerce')
    suppliers_geo = suppliers_geo.dropna(subset=['counts'])
    
    buyers_geo = buyers_geo[
        ~buyers_geo.geometry.isna() & 
        buyers_geo.geometry.is_valid
    ]
    buyers_geo['counts'] = pd.to_numeric(buyers_geo['counts'], errors='coerce')
    buyers_geo = buyers_geo.dropna(subset=['counts'])
    
    # Vérification finale
    if suppliers_geo.empty or buyers_geo.empty:
        raise ValueError("Données insuffisantes pour le tracé après nettoyage")
    
    # 6. Création du dossier de sortie
    save_dir = project_root / save_dir
    save_dir.mkdir(parents=True, exist_ok=True)

    # 7. Visualisation
    fig, ax = plt.subplots(1, 2, figsize=(20, 10))
    
    suppliers_geo.plot(column='counts', ax=ax[0], legend=True,
                      cmap='Reds', scheme='quantiles')
    ax[0].set_title("Fournisseurs (Belgique)")
    
    buyers_geo.plot(column='counts', ax=ax[1], legend=True,
                   cmap='Blues', scheme='quantiles')
    ax[1].set_title("Acheteurs (Belgique)")
    
    for a in ax:
        ctx.add_basemap(a, crs=belgium.crs.to_string(), 
                       source=ctx.providers.CartoDB.Positron)
    
    # 8. Sauvegarde
    output_path = save_dir / 'supplier_buyer_geo_distribution.png'
    plt.savefig(str(output_path), dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"Carte générée avec succès : {output_path}")
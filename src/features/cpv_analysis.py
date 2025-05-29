import pandas as pd
from pathlib import Path

def load_cpv_reference(filepath):
    """Charge et structure le référentiel CPV"""
    cpv_df  = pd.read_excel(filepath, dtype={'CODE': str})
    
    # Nettoyage des codes
    cpv_df['code_8dig'] = cpv_df['CODE'].str.split('-').str[0]
    cpv_df['code_2dig'] = cpv_df['code_8dig'].str[:2]
    cpv_df['code_3dig'] = cpv_df['code_8dig'].str[:3]
    
    # Identification des catégories principales (première occurrence de chaque code 2dig)
    main_categories = cpv_df.drop_duplicates('code_2dig').set_index('code_2dig')['FR'].to_dict()
    
    return cpv_df, main_categories

def map_cpv_codes(df, cpv_ref):
    """Mappe les codes CPV avec leur libellé complet"""
    # Jointure avec le référentiel
    df_mapped = pd.merge(
        df,
        cpv_ref[['code_8dig', 'FR']],
        left_on='tender_cpvs',
        right_on='code_8dig',
        how='left'
    )
    
    # Remplissage des valeurs manquantes
    df_mapped['FR'] = df_mapped['FR'].fillna('CPV Inconnu')
    
    return df_mapped

def analyze_cpv_with_reference(df, cpv_ref_path):
    """Analyse complète avec le référentiel officiel"""
    # Chargement du référentiel
    cpv_ref, main_categories = load_cpv_reference(cpv_ref_path)
    
    # Prétraitement des données
    df_expanded = (
        df[['tender_cpvs', 'tender_finalprice']]
        .dropna(subset=['tender_cpvs', 'tender_finalprice'])
        .assign(tender_cpvs=lambda x: x['tender_cpvs'].str.split(','))
        .explode('tender_cpvs')
        .assign(tender_cpvs=lambda x: x['tender_cpvs'].str.strip())
        .query("tender_cpvs != ''")
    )
    
    # Mapping des codes
    df_mapped = map_cpv_codes(df_expanded, cpv_ref)
    
    # Extraction des niveaux hiérarchiques
    df_mapped['cpv_2dig'] = df_mapped['tender_cpvs'].str[:2]
    df_mapped['cpv_3dig'] = df_mapped['tender_cpvs'].str[:3]
    
    # Calcul des poids pour éviter les doubles comptages
    tender_prices = df_mapped.groupby('tender_cpvs')['tender_finalprice'].first()
    df_mapped['weighted_price'] = df_mapped['tender_cpvs'].map(tender_prices) / \
                                 df_mapped.groupby('tender_cpvs')['tender_cpvs'].transform('count')
    
    # Agrégation par niveau CPV
    def aggregate_by_level(level):
        return df_mapped.groupby(level).agg(
            total_spending=('weighted_price', 'sum'),
            avg_spending=('weighted_price', 'mean'),
            tender_count=('tender_cpvs', 'nunique'),
            label=('FR', 'first')
        ).sort_values('total_spending', ascending=False)
    
    return {
        'by_2dig': aggregate_by_level('cpv_2dig'),
        'by_3dig': aggregate_by_level('cpv_3dig'),
        'by_8dig': aggregate_by_level('tender_cpvs'),
        'main_categories': main_categories,
        'full_data': df_mapped
    }
import numpy as np

def preprocess_expense_data(df):
    """
    Prétraitement spécifique pour l'analyse des dépenses
    """
    # Filtrage des données pertinentes
    expense_df = df[df['tender_finalprice'].notna()].copy()
    
    # Conversion des types si nécessaire
    expense_df['tender_finalprice'] = expense_df['tender_finalprice'].astype(float)
    
    # Nettoyage supplémentaire...
    
    return expense_df



from src.features.expense_analysis import calculate_price_differences, analyze_by_procedure_type
from src.visualization.expense_visualizations import plot_price_comparison

def process_price_comparison(df_clean, output_dir):
    """
    Pipeline complet pour l'analyse de comparaison des prix
    """
    # Calcul des différences
    df_prices = calculate_price_differences(df_clean)
    
    # Analyse par type de procédure
    price_stats = analyze_by_procedure_type(df_prices)
    
    # Sauvegarde des résultats
    price_stats.to_csv(f"{output_dir}/tables/expense/price_comparison_stats.csv", index=False)
    
    # Visualisations
    plot_price_comparison(
        df_prices,
        save_path=f"{output_dir}/figures/expense/price_comparison.png"
    )
    
    return df_prices, price_stats
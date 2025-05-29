import matplotlib.pyplot as plt
import seaborn as sns
from textwrap import wrap
from pathlib import Path

def plot_hierarchical_cpv(results, save_dir=None):
    """Visualisation hiérarchique des CPV"""
    sns.set_theme(style="whitegrid")
    plt.figure(figsize=(16, 12))
    
    by_2dig = results['by_2dig'].head(10)
    main_cats = results['main_categories']
    
    # Création des labels
    labels = [
        f"{idx} - {main_cats.get(idx, 'Autre')}\n"
        f"Total: {row['total_spending']/1e6:.1f}M €\n"
        f"{row['tender_count']} marchés"
        for idx, row in by_2dig.iterrows()
    ]
    
    # Graphique avec correction du warning
    ax = sns.barplot(
        x=range(len(by_2dig)),
        y=by_2dig['total_spending']/1e6,
        hue=by_2dig.index,
        dodge=False,
        palette='viridis'
    )
    
    # Configuration des ticks
    ax.set_xticks(range(len(by_2dig)))
    ax.set_xticklabels(["\n".join(wrap(l, 30)) for l in labels], 
                      rotation=45, 
                      ha='right')
    ax.set_title('Top 10 des catégories CPV (niveau 2 digits)', pad=20, fontsize=14)
    ax.set_ylabel('Dépenses totales (Millions €)', fontsize=12)
    ax.set_xlabel('')
    
    # Ajout des annotations
    for i, p in enumerate(ax.patches):
        ax.annotate(f"{p.get_height():.1f}M", 
                   (p.get_x() + p.get_width() / 2., p.get_height()),
                   ha='center', va='center', 
                   xytext=(0, 10), 
                   textcoords='offset points')
    
    plt.tight_layout()
    
    # Sauvegarde
    if save_dir:
        save_dir.mkdir(exist_ok=True, parents=True)
        plt.savefig(save_dir / 'cpv_hierarchical.png', dpi=300, bbox_inches='tight')
        plt.close()
    else:
        plt.show()

def plot_sunburst_cpv(results, save_path=None):
    """Diagramme sunburst interactif"""
    import plotly.express as px
    
    # Préparation rigoureuse des données
    try:
        df = results['full_data'].copy()
        df_agg = df.groupby(['cpv_2dig', 'cpv_3dig'], dropna=True)['weighted_price'].sum().reset_index()
        
        # Mapping robuste avec valeurs par défaut
        df_agg['2dig_label'] = df_agg['cpv_2dig'].map(results['main_categories']).fillna('Inconnu')
        df_agg['3dig_label'] = df_agg['cpv_3dig'].map(
            results['by_3dig']['label'].to_dict()
        ).fillna('Sous-catégorie')
        
        # Filtrage des NaN et vérification
        df_agg = df_agg.dropna(subset=['2dig_label', '3dig_label', 'weighted_price'])
        df_agg = df_agg[df_agg['weighted_price'] > 0]
        
        if df_agg.empty:
            raise ValueError("Données insuffisantes pour le sunburst")
        
        # Création du sunburst
        fig = px.sunburst(
            df_agg,
            path=['2dig_label', '3dig_label'],
            values='weighted_price',
            title='Répartition hiérarchique des dépenses par CPV'
        )
        
        if save_path:
            save_path.parent.mkdir(exist_ok=True, parents=True)
            fig.write_html(str(save_path))
            return True
        else:
            fig.show()
            return True
            
    except Exception as e:
        print(f"Erreur lors de la génération du sunburst: {str(e)}")
        return False

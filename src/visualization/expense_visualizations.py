import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from pathlib import Path

def plot_yearly_expense(data, save_path=None):
    """
    Génère un graphique des dépenses annuelles
    """
    plt.figure(figsize=(12, 6))
    sns.barplot(x='tender_year', y='total', data=data)
    plt.title('Dépenses totales par année')
    plt.xlabel('Année')
    plt.ylabel('Dépense totale (€)')
    
    if save_path:
        Path(save_path).parent.mkdir(exist_ok=True, parents=True)
        plt.savefig(save_path, bbox_inches='tight', dpi=300)
        plt.close()
    else:
        plt.show()

# Autres fonctions de visualisation...

def plot_market_metrics(metrics, save_path=None):
    """
    Visualise les métriques des marchés par année
    """
    fig, axes = plt.subplots(3, 1, figsize=(12, 12))
    
    # Nombre de marchés
    sns.barplot(data=metrics, x='tender_year', y='n_markets', ax=axes[0])
    axes[0].set_title('Nombre de marchés par année')
    axes[0].set_ylabel('Nombre')
    
    # Dépense moyenne
    sns.barplot(data=metrics, x='tender_year', y='mean_spending', ax=axes[1])
    axes[1].set_title('Dépense moyenne par marché')
    axes[1].set_ylabel('€')
    
    # Dépense médiane
    sns.barplot(data=metrics, x='tender_year', y='median_spending', ax=axes[2])
    axes[2].set_title('Dépense médiane par marché')
    axes[2].set_ylabel('€')
    
    plt.tight_layout()
    
    if save_path:
        Path(save_path).parent.mkdir(parents=True, exist_ok=True)
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.close()
    else:
        plt.show()

def plot_buyer_metrics(metrics, save_dir=None):
    """
    Visualise les dépenses par type d'acheteur
    """
    # Dépenses par type d'acheteur
    plt.figure(figsize=(12, 6))
    sns.barplot(data=metrics['by_buyertype'].head(10),
                x='total', y='buyer_buyertype')
    plt.title('Top 10 des dépenses par type d\'acheteur')
    plt.xlabel('Dépense totale (€)')
    plt.ylabel('Type d\'acheteur')
    
    if save_dir:
        plt.savefig(save_dir / 'expense_by_buyertype.png', 
                   bbox_inches='tight', dpi=300)
        plt.close()
    else:
        plt.show()
    
    # Dépenses par activité principale
    plt.figure(figsize=(12, 6))
    sns.barplot(data=metrics['by_activity'].head(10),
                x='total', y='buyer_mainactivities')
    plt.title('Top 10 des dépenses par activité principale')
    plt.xlabel('Dépense totale (€)')
    plt.ylabel('Activité principale')
    
    if save_dir:
        plt.savefig(save_dir / 'expense_by_activity.png',
                   bbox_inches='tight', dpi=300)
        plt.close()
    else:
        plt.show()

def plot_price_comparison(df, save_path=None):
    """
    Crée des visualisations pour la comparaison prix estimé/final
    """
    plt.figure(figsize=(15, 10))
    
    # Distribution des ratios
    plt.subplot(2, 2, 1)
    sns.histplot(np.log10(df['price_ratio']), bins=50, kde=True)
    plt.title('Distribution des ratios prix final/estimé (log10)')
    plt.xlabel('log10(Ratio prix final/estimé)')
    
    # Ratio par type de procédure
    plt.subplot(2, 2, 2)
    sns.boxplot(data=df, y='tender_proceduretype', x='price_ratio', 
                showfliers=False)
    plt.title('Ratio prix final/estimé par type de procédure')
    plt.xscale('log')
    plt.xlabel('Ratio (échelle log)')
    
    # Différence absolue par type de procédure
    plt.subplot(2, 2, 3)
    sns.boxplot(data=df, y='tender_proceduretype', x='price_difference_pct',
                showfliers=False)
    plt.title('Différence % prix final vs estimé')
    plt.xlabel('Différence en %')
    
    # Relation prix estimé vs final
    plt.subplot(2, 2, 4)
    sample = df.sample(min(1000, len(df)))
    sns.scatterplot(data=sample, x='tender_estimatedprice', y='tender_finalprice',
                    alpha=0.5)
    plt.plot([sample['tender_estimatedprice'].min(), sample['tender_estimatedprice'].max()],
             [sample['tender_estimatedprice'].min(), sample['tender_estimatedprice'].max()],
             'r--')
    plt.xscale('log')
    plt.yscale('log')
    plt.title('Relation prix estimé vs final')
    plt.xlabel('Prix estimé (log)')
    plt.ylabel('Prix final (log)')
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
    else:
        plt.show()
    plt.close()
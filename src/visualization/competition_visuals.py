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
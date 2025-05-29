from pathlib import Path
from ..features import competition_analysis
from ..visualization import competition_visuals

def process_competition_data(df, output_dir):
    """Pipeline complet d'analyse de concurrence"""
    # Convertir en Path et résoudre le chemin absolu
    output_path = Path(output_dir).resolve()
    
    # Création des dossiers de manière robuste
    (output_path / "figures/competition").mkdir(parents=True, exist_ok=True)
    (output_path / "tables/competition").mkdir(parents=True, exist_ok=True)
    
    # Calcul des métriques
    hhi_results = competition_analysis.calculate_hhi(df)
    pareto_results = competition_analysis.calculate_pareto(df)

    # Sauvegarde avec chemins absolus
    hhi_results.to_csv(str(output_path / "tables/competition/hhi_results.csv"), index=False)
    pareto_results.to_csv(str(output_path / "tables/competition/pareto_results.csv"), index=False)
    
    competition_visuals.plot_pareto_curve(
        pareto_results,
        save_path=str(output_path / "figures/competition/pareto_curve.png")
    )
    
    
    return hhi_results, pareto_results
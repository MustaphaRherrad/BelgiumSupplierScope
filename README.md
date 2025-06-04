# BelgiumSupplierScope

Projet d'analyse des marchés publics en Belgique.

## Structure du projet
- data/: données brutes, transformées, externes, intermédiaires
- notebooks/: notebooks Jupyter pour exploration et modélisation
- src/: code source organisé (modèles, features, visualisation, utils, data)
- config/: fichiers de configuration
- tests/: tests unitaires
- docs/: documentation
- reports/: résultats et figures
- dashboards/: exemples de dashboards interactifs

## Installation

### Installation de l'environnement

#### Avec conda
``````
conda create -n supplierscope python=3.11
conda activate supplierscope
pip install -r requirements.txt
``````

## Usage
Développer et exécuter les notebooks dans le dossier notebooks/

## Données
![Ensemble de données sur les marchés publics mondiaux (GPPD)](https://data.mendeley.com/datasets/fwzpywbhgw/2)

## Rapports
* ![Analyse_par_CPV](docs/analyse_par_cpv.md)
* ![analyse de la Concurrence](docs/competition_analysis.md)



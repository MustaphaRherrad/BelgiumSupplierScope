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
- dashboards/: exemples de dashboards interactifs (les graphiques plotly -html- ne sont pas encore exploitables à ce stade de réalisation, j'essairai de trouver une alternative pour mettre cette visualisation à disposition)

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
Les graphiques et les reporting dans reports/

---

## Données
[Ensemble de données sur les marchés publics mondiaux (GPPD)](https://data.mendeley.com/datasets/fwzpywbhgw/2)

* **Institution**: Central European University
* Ces données sont mis à disposition sous **CC BY NC 3.0 licence description**.
* Contributeurs: Fazekas, Mihaly; Toth, Bence; Alshaibani , Ahmed; Abdou, Aly (2024), “GTI Global Public Procurement Dataset (GPPD) 1/2”, Mendeley Data, V2, doi: 10.17632/fwzpywbhgw.2
  
Il s'agit d'une base de données mondiale sur les procédures de marchés publics. Grâce à diverses méthodes de web scraping, les contributeurs ont collecté et harmonisé les procédures de marchés publics de 42 pays entre 2006 et 2021. Les plages d'années varient selon les pays, en fonction de la disponibilité des données provenant des sources collectées. Compte tenu de la diversité des formats de publication des données dans chaque pays, ils ont standardisé les informations publiées afin de les adapter à une norme de données commune. Pour chaque pays, les informations clés concernant les principaux acheteurs et fournisseurs, la géolocalisation de l'organisation (telles que les codes NUTS, le cas échéant), les informations sur les produits (codes CPV 2008, le cas échéant), les prix (en devises locales et également ajustés en fonction de la parité de pouvoir d'achat), ainsi que les détails du processus de passation des marchés (par exemple, la date d'attribution du marché ou la procédure suivie).

---

## Rapports
* [Analyse_par_CPV](reports/cpv_analysis_report.md)
* [Analyse de la Concurrence](reports/competition_report.md)
* [Analyse de la Dépense](reports/expense_analysis_report.md)



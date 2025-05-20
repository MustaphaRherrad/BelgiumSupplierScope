# Architecture du projet

SupplierScope/
│
├── data/                    # Toutes les données du projet
│   ├── raw/                 # Données brutes (ne jamais modifier)
│   ├── processed/           # Données nettoyées/transformées
│   ├── external/            # Données externes (météo, indices, etc.)
│   ├── interim/             # Données intermédiaires (étapes de prétraitement)
│   └── samples/             # Jeux de données exemples ou réduits
│
├── notebooks/               # Jupyter notebooks pour l'analyse et la modélisation
│   ├── 01_exploration.ipynb
│   ├── 02_modelisation.ipynb
│   ├── 03_clustering.ipynb
│   ├── 04_deep_learning.ipynb
│   └── README.md
│
├── src/                     # Code source principal du projet
│   ├── __init__.py
│   ├── models/              # Modèles de scoring, ML, etc.
│   │   ├── __init__.py
│   │   ├── baseline.py
│   │   └── supplier_scoring.py
│   ├── features/            # Feature engineering
│   │   ├── __init__.py
│   │   └── build_features.py
│   ├── visualization/       # Fonctions de visualisation
│   │   ├── __init__.py
│   │   └── plot_utils.py
│   ├── data/                # Scripts de chargement et prétraitement des données
│   │   ├── __init__.py
│   │   ├── load_data.py
│   │   └── preprocessing.py
│   └── utils/               # Fonctions utilitaires
│       ├── __init__.py
│       └── helpers.py
│
├── config/                  # Fichiers de configuration
│   ├── parameters.yml
│   └── logging.yml
│
├── tests/                   # Tests unitaires
│   ├── __init__.py
│   ├── test_models.py
│   └── test_features.py
│
├── docs/                    # Documentation du projet
│   ├── architecture.md
│   └── usage.md
│
├── reports/                 # Rapports, résultats, figures
│   ├── figures/
│   ├── tables/
│   └── README.md
│
├── dashboards/              # Exemples de dashboards interactifs
│   └── README.md
│
├── .gitignore               # Fichiers et dossiers à ignorer par git
├── requirements.txt         # Dépendances Python du projet
├── README.md                # Présentation générale du projet
└── LICENSE                  # Licence d'utilisation

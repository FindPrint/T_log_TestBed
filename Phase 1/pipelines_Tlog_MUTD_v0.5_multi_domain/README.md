# T_log & MUTD v0.5 – Multi-domain Pipelines

This folder groups four **reproducible pipelines** that apply the T_log (v0.5) and MUTD (v0.5.5) equations to different real-world datasets.

Each pipeline is designed to be **self-contained** and executable directly from its main Jupyter notebook.

## Pipelines included

- `Pipeline_Tlog_V0.1_Sunspots_En/`  
  Sunspots time series (solar activity).

- `T_log_Tsunami_V_0_1En/`  
  Earthquake–Tsunami dataset.

- `T_log_Pipeline_PM2.5_Global_vs_Local_(New_York)EN/`  
  Global vs local PM2.5 air quality (New York focus).

- `T_log_UrbanClimate/`  
  Urban climate dataset (MUTD with effective dimension estimation).

There is also an overview PDF:

- `Tlog_MUTD_v0.5_sunspots_tsunami_pm25_urbanclimate_overview.pdf`  
  Summary document covering all four pipelines.

## Common structure of each pipeline

Inside each pipeline folder you will typically find:

- **Main notebook**  
  The core `.ipynb` file (e.g. `Pipeline_Tlog_V0.1_Sunspots_En.ipynb`, `T_log_Tsunami_V_0_1En.ipynb`, etc.).  
  Running this notebook end-to-end reproduces the analysis.

- **`THEORY/`**  
  Local copy of the relevant theoretical text(s) for the pipeline (T_log / MUTD).

- **`data/`**  
  Input datasets used by the pipeline. Some datasets may be downloaded automatically if they are too large to include directly.

- **`logs/`**  
  CSV and markdown logs produced during execution (e.g. run metadata, key metrics).

- **`results/`**  
  Figures, tables and other exported results.

- **`requirements.txt`**  
  Python dependencies required to run the notebook.

- **`kaggle.json`** (when present)  
  Kaggle API configuration file used to download data.  
  **Do not publish real credentials** in a public repository. Replace this file with your own credentials locally or configure Kaggle via environment variables.

  **Kaggle API key options:**

  1. Edit the placeholders in the provided `kaggle.json` files (`"username"`, `"key"`) with your own Kaggle credentials.
  2. Replace the placeholder file with the official `kaggle.json` downloaded from Kaggle: create a free account, go to **My Account → API → Create New Token**, then copy the downloaded file into the pipeline folder.

- **`convert_ipynb_to_pdf.py`**  
  Utility script to export the notebook as PDF.

## How to run any pipeline (example: Sunspots)

1. Install Python 3 and a virtual environment tool (e.g. `venv` or `conda`).
2. Open a terminal in the pipeline folder, for example:
   - `Pipeline_Tlog_V0.1_Sunspots_En/`
3. (Optional but recommended) Create and activate a virtual environment.
4. Install dependencies:
   - `pip install -r requirements.txt`
5. If the pipeline uses Kaggle:
   - Place a valid `kaggle.json` in the expected location (or configure the Kaggle CLI according to the official documentation).
6. Open the main notebook in Jupyter, JupyterLab or VS Code:
   - `Pipeline_Tlog_V0.1_Sunspots_En.ipynb`
7. Run all cells in order.  
   Logs and results will be written automatically into the `logs/` and `results/` folders.

For other pipelines, follow the same steps inside their respective folders.

---

## T_log & MUTD v0.5 – Pipelines multi-domaines (FR)

Ce dossier regroupe quatre **pipelines reproductibles** qui appliquent les équations T_log (v0.5) et MUTD (v0.5.5) à différents jeux de données réels.

Chaque pipeline est conçu pour être **autonome** et exécutable directement à partir de son notebook Jupyter principal.

### Pipelines inclus

- `Pipeline_Tlog_V0.1_Sunspots_En/`  
  Série temporelle des taches solaires (Sunspots).

- `T_log_Tsunami_V_0_1En/`  
  Jeu de données Séisme–Tsunami.

- `T_log_Pipeline_PM2.5_Global_vs_Local_(New_York)EN/`  
  Qualité de l’air PM2.5 globale vs locale (focus New York).

- `T_log_UrbanClimate/`  
  Données de climat urbain (MUTD avec estimation de dimension effective).

Un PDF de synthèse est également présent :

- `Tlog_MUTD_v0.5_sunspots_tsunami_pm25_urbanclimate_overview.pdf`  
  Document de synthèse couvrant les quatre pipelines.

### Structure commune de chaque pipeline

À l’intérieur de chaque dossier de pipeline, on retrouve généralement :

- **Notebook principal**  
  Le fichier `.ipynb` central (par ex. `Pipeline_Tlog_V0.1_Sunspots_En.ipynb`, `T_log_Tsunami_V_0_1En.ipynb`, etc.).  
  L’exécution complète de ce notebook permet de reproduire l’analyse.

- **`THEORY/`**  
  Copie locale du ou des textes théoriques utilisés par le pipeline (T_log / MUTD).

- **`data/`**  
  Jeux de données d’entrée. Certains jeux peuvent être téléchargés automatiquement s’ils sont trop volumineux pour être inclus directement.

- **`logs/`**  
  Journaux CSV et markdown produits lors de l’exécution (métadonnées de run, métriques clés, etc.).

- **`results/`**  
  Figures, tableaux et autres résultats exportés.

- **`requirements.txt`**  
  Liste des dépendances Python nécessaires à l’exécution du notebook.

- **`kaggle.json`** (lorsqu’il est présent)  
  Fichier de configuration de l’API Kaggle utilisé pour télécharger des données.  
  **Ne publiez pas de véritables identifiants** dans un dépôt public. Remplacez ce fichier par vos propres identifiants en local ou configurez Kaggle via des variables d’environnement.
  
  **Options pour la clé API Kaggle :**
  
  1. Modifier les placeholders dans les fichiers `kaggle.json` fournis (`"username"`, `"key"`) avec vos propres identifiants Kaggle.
  2. Remplacer le fichier de placeholder par le `kaggle.json` officiel téléchargé depuis Kaggle (compte gratuit, menu **My Account → API → Create New Token**), puis copier ce fichier dans le dossier du pipeline.

- **`convert_ipynb_to_pdf.py`**  
  Script utilitaire pour exporter le notebook en PDF.

### Comment exécuter un pipeline (exemple : Sunspots)

1. Installer Python 3 et un outil d’environnement virtuel (par ex. `venv` ou `conda`).
2. Ouvrir un terminal dans le dossier du pipeline, par exemple :
   - `Pipeline_Tlog_V0.1_Sunspots_En/`
3. (Optionnel mais recommandé) Créer et activer un environnement virtuel.
4. Installer les dépendances :
   - `pip install -r requirements.txt`
5. Si le pipeline utilise Kaggle :
   - Placer un `kaggle.json` valide à l’emplacement attendu (ou configurer l’interface en ligne de commande Kaggle selon la documentation officielle).
6. Ouvrir le notebook principal dans Jupyter, JupyterLab ou VS Code :
   - `Pipeline_Tlog_V0.1_Sunspots_En.ipynb`
7. Exécuter toutes les cellules dans l’ordre.  
   Les journaux et résultats seront écrits automatiquement dans les dossiers `logs/` et `results/`.

Pour les autres pipelines, suivre les mêmes étapes dans leurs dossiers respectifs.

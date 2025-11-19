# PM2.5 Global vs Local (New York) – Partie 1 (cellules 0–9) : Préparation, acquisition Kaggle et inspection initiale

## 1. Périmètre de la partie

Cette première partie correspond aux cellules **0–9** du notebook splitté `PM25_part01.ipynb`, dérivé de :

`T_log_Pipeline_PM2.5_Global_vs_Local_(New_York)EN.ipynb`

Elle couvre :

- l’**installation des dépendances** via `requirements.txt` ;
- la **préparation de l’environnement** (dossiers, seeds, logger, fichiers de log et résumé) ;
- l’**acquisition des données Kaggle** pour l’Urban Air Quality & Climate Dataset (1958–2025) ;
- une **inspection détaillée** du fichier `air_quality_global.csv` (PM2.5/NO₂, 20 villes) ;
- la définition du plan pour le futur calcul de `T_log` global et par ville.

Aucun calcul de T_log n’est encore effectué ici, mais tous les prérequis de données et de logging sont mis en place.

---

## 2. Installation des dépendances (requirements.txt)

La première cellule exécutable installe les dépendances listées dans `requirements.txt` via `pip` :

- fonction `install_requirements(file_path="requirements.txt")` qui lance :

  - `python -m pip install -r requirements.txt`

- la cellule affiche :
  - un message de succès si l’installation se passe bien ;
  - une recommandation de **redémarrer le kernel** lors de la première exécution.

Cette étape garantit que toutes les librairies utilisées dans le pipeline (pandas, numpy, matplotlib, kaggle, etc.) sont présentes. Elle est pensée pour être exécutée une fois au début.

---

## 3. Bloc 1 – Préparation de l’environnement, logger et fichiers de log

### 3.1 Imports, seeds et dossiers

La cellule "Bloc 1 — Préparation" :

- importe les modules standards : `os`, `csv`, `shutil`, `random`, `logging`, `datetime` ;
- importe les modules scientifiques : `numpy`, `pandas`, `matplotlib` (avec backend `Agg`) ;
- fixe les **seeds** :
  - `SEED = 42`, `random.seed(42)`, `np.random.seed(42)` ;
- crée les dossiers (si inexistants) :
  - `data/`, `results/`, `logs/` ;
- supprime `/content/sample_data` si présent (cas Colab).

### 3.2 Timestamps et fichiers de log

La fonction `utc_timestamp()` fournit des timestamps :

- timezone-aware via `datetime.now(timezone.utc).isoformat()` ;
- au format ISO 8601.

Fichiers gérés :

- `logs/logs.csv` : journal tabulaire (timestamp, level, message) ;
- `logs/summary.md` : résumé textuel des événements.

Si `logs.csv` n’existe pas, il est initialisé avec les en-têtes `['timestamp', 'level', 'message']`.

### 3.3 Logger Python et fonctions de journalisation

Configuration d’un logger nommé `TlogV01` :

- niveau `INFO` ;
- handler console (format `'%(asctime)s [%(levelname)s] %(message)s'`) ;
- handler fichier `logs/app.log` avec le même format.

Fonctions utilitaires :

- `log_event(level, message)` :
  - envoie le message au logger (console + fichier) selon le niveau (`INFO`, `WARNING`, `ERROR`) ;
  - append en parallèle à `logs/logs.csv` avec timestamp UTC ;
- `append_summary_md(text)` :
  - ajoute du texte à `logs/summary.md` (Markdown), par exemple des résumés de blocs.

### 3.4 Banner de session et plot de vérification

Au démarrage :

- un header de session est construit :

  - `# Session Log T_log V0.1` ;
  - date/heure de début ;
  - conventions (`bias=0`, seeds 42, outputs dans `results/`).

- ce header est écrit dans `summary.md` si le fichier est nouveau.

Un **plot de vérification** est généré :

- sinusoïde simple, figure `(4,3)` ;
- sauvegardée en `results/env_check_plot.png` ;
- loggée via `log_event('INFO', ...)` et résumée dans `summary.md`.

La cellule se termine par :

- logs INFO indiquant que le bloc 1 est prêt ;
- impression d’un résumé minimal (dossiers créés, chemins de log).

Conclusion : le pipeline PM2.5 dispose d’un environnement de travail reproductible avec logging structuré, similaire à celui du pipeline Sunspots.

---

## 4. Bloc 2 – Acquisition des données Kaggle (Urban Air Quality & Climate Dataset)

### 4.1 Installation et configuration Kaggle

La cellule "Bloc 2 — Data Acquisition" :

- installe silencieusement la librairie `kaggle` si nécessaire (`!pip install kaggle --quiet`) ;
- importe l’API `kaggle.api` (alias `kaggle_api`).

Elle prépare :

- `KAGGLE_DATASET_ID = "krishd123/urban-air-quality-and-climate-dataset-1958-2025"` ;
- `TARGET_FILE_NAME = "urban_climate.csv"` ;
- dossiers : `DATA_DIR = 'data'`, `LOGS_DIR = 'logs'`, `RESULTS_DIR = 'results'` ;
- chemins :
  - `LOCAL_COPY = data/urban_climate.csv` ;
  - `RESULT_PREVIEW = results/urban_climate_preview.csv`.

Une fonction `append_log(level, message)` :

- ajoute une ligne dans `logs/logs.csv` (avec `datetime.utcnow().isoformat() + 'Z'` – note : warning de dépréciation, mais fonctionnement OK) ;
- ajoute une entrée Markdown dans `logs/summary.md` (timestamp + niveau + message).

`log_event` est redéfini comme alias vers `append_log`, de sorte que les appels ultérieurs utilisent ce canal.

### 4.2 Authentification Kaggle

La fonction `find_and_auth_kaggle()` :

- tente d’abord d’utiliser les variables d’environnement `KAGGLE_USERNAME` et `KAGGLE_KEY` ;
- sinon, cherche un `kaggle.json` :
  - dans `~/.kaggle/kaggle.json` ;
  - ou dans le répertoire courant (`./kaggle.json`) ;
- lit le fichier JSON pour récupérer `username` et `key`, les place dans les variables d’environnement ;
- appelle `kaggle_api.authenticate()`.

Elle logge :

- succès ou échec de la recherche de clés ;
- succès ou échec de l’authentification.

En cas d’échec, une exception est levée avec un message explicite (clé API non configurée).

### 4.3 Téléchargement et lecture de `urban_climate.csv`

Une fois authentifié :

- téléchargement du dataset avec :

  - `kaggle_api.dataset_download_files(KAGGLE_DATASET_ID, path=DATA_DIR, unzip=True, force=True, quiet=True)` ;

- vérification que `data/urban_climate.csv` existe ;
- log d’un succès `SUCCESS` dans `logs/logs.csv` et `summary.md`.

**Lecture robuste du CSV** :

- plusieurs tentatives :
  1. `pd.read_csv(LOCAL_COPY)` ;
  2. `pd.read_csv(..., encoding='utf-8', sep=';')` ;
  3. `pd.read_csv(..., encoding='latin1')` ;
- en cas d’échec total, une `RuntimeError` regroupe les messages d’erreurs.

Sur l’exécution observée :

- lecture réussie en mode standard ;
- `n_rows = 11040`, `n_cols = 12` ;
- colonnes :

  - `['city', 'country', 'latitude', 'longitude', 'year', 'month', 'temperature_celsius', 'humidity_percent', 'precipitation_mm', 'wind_speed_ms', 'urban_heat_island_intensity', 'data_source']` ;

- aucune valeur manquante (`missing_counts` = 0 pour toutes les colonnes) ;
- un aperçu des 200 premières lignes est sauvegardé dans `results/urban_climate_preview.csv`.

La cellule imprime un résumé détaillé (nombre de lignes/colonnes, colonnes, counts de NA) et logge ces informations.

Ce `urban_climate.csv` sera utilisé plus tard pour croiser PM2.5 et climat urbain.

---

## 5. Bloc 3a – Inspection de `air_quality_global.csv` (PM2.5/NO₂, 20 villes)

Avant de calculer T_log, le pipeline inspecte spécifiquement le fichier `data/air_quality_global.csv`, qui contient les mesures PM2.5 et NO₂ pour 20 villes dans 10 pays.

### 5.1 Structure et qualité des données

La cellule "Bloc 3a — Inspection et validation" :

- charge `air_quality_global.csv` dans `df_aq` ;
- affiche :
  - les 10 premières lignes ;
  - la liste des colonnes ;
  - le nombre total de lignes ;
  - `df.info()` (types et non‑null counts) ;
  - le nombre de valeurs manquantes par colonne ;
  - le nombre de doublons ;
  - des statistiques descriptives (`describe(include='all')`).

Résultats observés :

- `n = 6480` lignes ;
- 11 colonnes :

  - `['city', 'country', 'latitude', 'longitude', 'year', 'month', 'pm25_ugm3', 'no2_ugm3', 'data_quality', 'measurement_method', 'data_source']` ;

- aucune valeur manquante ;
- `nb_duplicates = 0` ;
- 20 villes et 10 pays ;
- pour PM2.5 :
  - moyenne globale ≈ **40.97 µg/m³** ;
  - distribution large (min ≈ 5.1, max ≈ 274.18) ;
- pour NO₂ :
  - moyenne ≈ **39.62 µg/m³** ;
  - min ≈ 10.25, max ≈ 110.27.

Les champs qualitatifs (`data_quality`, `measurement_method`, `data_source`) décrivent la qualité et la méthode de mesure (par ex. "Federal Reference Method", "EPA_AQS").

### 5.2 Logging et résumé

La cellule :

- appelle `log_event("INFO", ...)` et `append_summary_md(...)` pour noter dans `logs/logs.csv` et `logs/summary.md` :

  - le fait que l’inspection de `air_quality_global.csv` a été réalisée ;
  - le nombre de lignes et de doublons.

Conclusion de Bloc 3a :

- `air_quality_global.csv` est **propre** (0 NA, 0 doublon) ;
- la structure (ville, année, mois, PM2.5, NO₂, qualité, source) est adaptée à un calcul T_log sur des sous-séries temporelles (par ville, par pays, ou globalement).

---

## 6. Préparation du calcul de T_log pour PM2.5 global et local (New York)

Les cellules Markdown de fin de partie esquissent le plan pour les blocs suivants :

- **T_log global PM2.5** :
  - série constituée de l’ensemble des 6480 observations PM2.5 ;
  - choix initial proposé : `d = 1` (série temporelle scalaire) ;
  - on s’attend à un T_log global fortement **négatif** (n grand, d < 4).

- **T_log local New York** :
  - sous-série pour la ville "New York" (n ≈ 324, 27 ans × 12 mois) ;
  - même choix initial `d = 1` ;
  - comparaison T_log(New York) vs T_log(global) pour analyser l’écart local/global.

Ces calculs effectifs (bloc 3b et suivants) ne sont pas encore dans cette partie ; ici, tout est mis en place pour que le calcul de T_log soit **bien posé**, sur des données contrôlées.

---

## 7. Rôle de la Partie 1 dans le pipeline PM2.5 Global vs Local

Cette première partie :

- installe proprement les **dépendances** du projet (avec rappel de redémarrer le kernel) ;
- prépare un **environnement loggé** (dossiers, logger Python, CSV de logs, résumé Markdown, plot de check) ;
- télécharge et lit de manière **robuste** le dataset Kaggle "Urban Air Quality & Climate 1958–2025" ;
- vérifie que `urban_climate.csv` est complet (aucune valeur manquante) ;
- inspecte en détail `air_quality_global.csv` et valide sa structure (n=6480, 0 NA, 0 doublons) ;
- définit un **plan clair** pour le calcul de T_log sur PM2.5, en mode global et par ville (notamment New York).

En résumé, la Partie 1 prépare l’intégralité du socle technique (données et logs) pour que les blocs suivants puissent se concentrer sur :

- le calcul de T_log(n,d) pour PM2.5 ;
- l’analyse comparative Global vs Local (New York) ;
- et, ultérieurement, l’extension à d’autres dimensionnements (graphes multi-villes, dimension spectrale, etc.).

# UrbanClimate V0.1 – Partie 5 (cellules 40–49) : Diagnostics des fenêtres temporelles atypiques et packaging

## 1. Périmètre

Cette partie correspond aux cellules 40–49 de `UrbanClimate_part05.ipynb`.

Elle intervient **après** la cross‑validation temporelle (Partie 4) et se concentre sur les **fenêtres « atypiques »** identifiées dans `results/temporal_cv_atypical_windows/temporal_cv_atypical_periods_windows_index_enriched.csv` (par ex. périodes où T_log est extrême, changement de signe, outliers marqués, etc.).

Objectifs :

- produire des **diagnostics détaillés** par fenêtre (par feature et par ville) ;
- générer des **heatmaps ville × feature** pour visualiser les anomalies ;
- construire un **résumé compact** par fenêtre ;
- empaqueter les fichiers clés dans un **ZIP unique** pour revue externe.

---

## 2. Diagnostics détaillés par fenêtre atypique

### 2.1 Lecture de l’index enrichi

La cellule principale lit :

- `results/temporal_cv_atypical_windows/temporal_cv_atypical_periods_windows_index_enriched.csv`.

Chaque ligne de cet index décrit une fenêtre atypique :

- `window_type` (annual, 3yr, etc.) ;
- `window_center` (année centrale) ;
- `pipeline` (A/B/C) ;
- chemin d’un CSV brut `raw_csv` contenant les observations sur cette fenêtre ;
- métriques d’atypicité (proportion d’outliers, médiane des scores de Mahalanobis, etc.).

### 2.2 Diagnostics par feature

Pour chaque entrée de l’index :

1. On lit le CSV brut `raw_csv` (si présent).
2. On construit une clé `city_key` (si nécessaire) à partir de `city,country,latitude,longitude`.
3. On identifie les **features numériques** pertinentes :
   - priorité aux colonnes climatiques :
     - `temperature_celsius`, `humidity_percent`, `precipitation_mm`, `wind_speed_ms`, `urban_heat_island_intensity` ;
   - sinon, fallback sur les colonnes numériques à plus forte variance.
4. On calcule, pour chaque feature :
   - `n`, `n_nan`, `frac_nan` ;
   - moyenne, médiane, écart‑type, skewness ;
   - top‑3 valeurs extrêmes (indices + valeurs) par écart absolu à la médiane ;
   - bottom‑3 valeurs (plus petites).

Toutes ces informations sont enregistrées dans :

- `results/temporal_cv_atypical_windows/diagnostics/<tag>/diagnostics_features_<tag>.csv`.

Le tag `<tag>` code `(window_type, window_center, pipeline)` (par ex. `3yr_1984.0_A`).

### 2.3 Résumé par ville et heatmaps

Pour chaque fenêtre :

- agrégation par `city_key` :
  - `n_obs` (nombre d’observations dans la fenêtre) ;
  - médianes, moyennes et fractions de NaN pour chaque feature ;
- sauvegarde dans :
  - `diagnostics_by_city_<tag>.csv` ;
- construction d’une matrice pour heatmap :
  - lignes = villes ;
  - colonnes = `median_<feature>` ;
  - normalisation par **z‑score** par feature si possible (std>0), sinon min‑max ;
- génération d’une **heatmap ville × feature** (`seaborn.heatmap`) avec colormap `vlag` centrée ;
- sauvegarde dans :
  - `heatmap_cities_features_<tag>.png`.

Cette étape permet de visualiser, pour chaque fenêtre atypique, quelles villes et quelles variables sont responsables des anomalies (valeurs extrêmes, patterns structurés).

### 2.4 Résumé Markdown par fenêtre

Pour chaque tag `<tag>`, la cellule crée :

- `summary_<tag>.md` contenant :
  - date de génération ;
  - chemins vers `raw_csv`, `diagnostics_features`, `by_city`, heatmap ;
  - une liste d’observations rapides par feature (n, frac_NaN, médiane, moyenne, skewness).

Les événements sont ajoutés à `logs/summary.md` via `append_log`.

---

## 3. Résumé compact et packaging ZIP

La cellule suivante crée une vue synthétique de toutes les fenêtres atypiques :

- lecture de l’index enrichi `temporal_cv_atypical_periods_windows_index_enriched.csv` ;
- pour chaque fenêtre (`window_type, window_center, pipeline`) :
  - recensement des artefacts produits dans `diagnostics/<tag>/` :
    - `summary_<tag>.md` ;
    - `diagnostics_by_city_<tag>.csv` ;
    - éventuelle heatmap `heatmap_cities_features_<tag>.png` ;
  - extraction des **features utilisées** (depuis `diagnostics_features_<tag>.csv`) ;
  - identification des top‑3 villes les plus suspectes :
    - en priorité, colonnes avec "outlier" ou "frac" dans leur nom ;
    - sinon, rang par `n_obs`.

Un CSV résumé est produit :

- `results/temporal_cv_atypical_windows/temporal_cv_atypical_periods_summary.csv`.

Chaque ligne contient notamment :

- `window_type`, `window_center`, `pipeline` ;
- `n_rows` (taille du CSV brut), `prop_obs_outlier`, `median_md`, `prop_cities_with_gt10pct_outliers`, `max_city_outlier_frac` ;
- `flag_for_review` (booléen importé de l’index) ;
- `top3_cities_by_outlier_or_nobs` (ville:score) ;
- `features_used` ;
- chemins vers le summary markdown, la heatmap et le CSV par ville.

En parallèle, un **package ZIP** est créé :

- `results/temporal_cv_atypical_windows/temporal_cv_atypical_periods_summary_package.zip` ;
- il contient, sous `atypical_windows_files/`, pour chaque fenêtre :
  - `summary_<tag>.md` ;
  - `diagnostics_by_city_<tag>.csv` ;
  - `heatmap_cities_features_<tag>.png` (si présent) ;
  - le `raw_csv` de la fenêtre (ex. `temporal_cv_atypical_period_window_3yr_1984.00_A_raw.csv`).

Ce ZIP permet de transmettre **en un seul fichier** toutes les pièces nécessaires à une revue humaine détaillée des périodes problématiques.

---

## 4. Check-list de validation pour le pipeline A

Les cellules de texte en fin de partie définissent une **liste de vérifications prioritaires** pour le pipeline A (baseline StandardScaler), couvrant :

- existence et non‑vacuité des fichiers clés :
  - `results/pipeline_details/A_baseline_StandardScaler_d_estimate.csv` ;
  - `A_baseline_StandardScaler_loo.csv`, `_loo_summary.csv` ;
  - `results/tlog_pipelines_overview.csv` ;
- cohérence des paramètres : `d_part, d_pca90, d_est, n_cities` ;
- robustesse LOO :
  - `mean(T_log_loo)`, `std`, `rel_std_pct` ≈ valeurs attendues (ex. 24.36 % pour rel_std_pct, −0.353 pour la moyenne) dans une tolérance fixée ;
- tests statistiques : p‑value du t‑test << 1 (rejet H0 `mean(T_log_loo)=0`) ;
- sanitation : absence de NaN/Inf dans les fichiers `*_sanitized.csv` ;
- cohérence du sweep (sous‑échantillonnage) et des exports de fenêtres atypiques ;
- présence et cohérence de `results/params.json` et `results/README_method.md` (reproductibilité) ;
- utilisation du flag `flag_for_review` dans l’index enrichi pour prioriser les fenêtres à vérifier.

Ce bloc sert de **guide d’audit** pour vérifier que tous les artefacts UrbanClimate V0.1 sont présents, sains et cohérents.

---

## 5. Rôle de la Partie 5 dans UrbanClimate V0.1

La Partie 5 complète la validation UrbanClimate V0.1 en :

- creusant les **fenêtres temporelles atypiques** détectées par la cross‑validation ;
- fournissant pour chacune d’elles des diagnostics détaillés (par feature et par ville) et une visualisation structurée (heatmaps) ;
- construisant un **résumé compact** et un **package ZIP** prêts à être transmis pour revue externe ou archivage ;
- définissant une check‑list claire pour vérifier la cohérence de l’ensemble du pipeline (en particulier le pipeline A baseline).

En combinant cela avec les Parties 1–4, on dispose non seulement d’un diagnostic global (Divergence) et robuste dans le temps, mais aussi d’un **outillage complet pour investiguer en détail** les périodes où le comportement de T_log ou des features climatiques sort de la norme.

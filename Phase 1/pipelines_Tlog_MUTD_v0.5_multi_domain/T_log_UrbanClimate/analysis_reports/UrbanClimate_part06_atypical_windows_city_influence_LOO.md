# UrbanClimate V0.1 – Partie 6 (cellules 50–59) : Fenêtres atypiques, influence des villes et LOO ciblé

## 1. Périmètre

Cette sixième partie correspond aux cellules 50–59 de `UrbanClimate_part06.ipynb`.

Elle se place **après** l’identification et les diagnostics détaillés des fenêtres temporelles atypiques (Partie 5) et se concentre sur :

- la synthèse des fenêtres les plus sensibles (par influence d’une ville top‑offender) ;
- la quantification de l’impact de **Beijing** sur T_log ;
- la mise en place d’une procédure LOO étendue par ville dans chaque fenêtre atypique.

---

## 2. Résumé prioritaire des fenêtres atypiques

Une cellule de texte résume les fenêtres jugées prioritaires :

- **Fenêtres signalées** (pipelines A/B/C) :
  - `3yr_1984.0_{A,B,C}`
  - `3yr_2014.0_{A,B,C}`
  - `annual_2003.0_{A,C}`
  - `annual_2008.0_{A,B,C}`
  - `annual_2012.0_{A,B,C}`
  - `annual_2014.0_{A,C}`
  - `annual_2016.0_{A,B,C}`
- **Pattern commun** :
  - mêmes 5 features utilisées :
    - `temperature_celsius`, `humidity_percent`, `precipitation_mm`, `wind_speed_ms`, `urban_heat_island_intensity` ;
  - même ville "top offender" pour toutes ces fenêtres :
    - `Beijing_China_39.9042_116.4074`.
- **Chiffres typiques** (d’après l’index enrichi et `tests_priority_summary.csv`) :
  - `prop_obs_outlier ≈ 0.0257` (≈2.6 % d’observations marquées outliers) ;
  - `median_md ≈ 3.0` (médiane des scores de Mahalanobis) ;
  - `prop_cities_with_gt10pct_outliers = 0.05` ;
  - `max_city_outlier_frac` compris entre ~0.49 et 0.54 (une ville concentre près de la moitié des outliers) ;
  - exemples de T_log positifs sur ces sous‑périodes :
    - `3yr_1984.0_A` : T_log ≈ 0.069 ;
    - `3yr_2014.0_A` : T_log ≈ 0.051 ;
    - `annual_2008.0_A` : T_log ≈ 0.146 ;
  - rappel : T_log global verrouillé ≈ **−0.298824** (régime Divergence).

Conclusion de ce résumé : certaines fenêtres temporelles montrent des T_log positifs ou faiblement positifs **portés en grande partie par Beijing**.

---

## 3. Vérifications immédiates recommandées

Une section textuelle propose des check‑lists rapides :

1. **Contribution de Beijing** :
   - ouvrir `diagnostics_by_city_<tag>.csv` pour une fenêtre représentative (ex. `3yr_1984.0_A`) ;
   - lire `n_obs`, moyennes et compte d’outliers par feature pour Beijing.
2. **Recalcul de T_log sans Beijing** :
   - pour une fenêtre donnée, filtrer `city_key != Beijing_...` ;
   - ré‑agréger par ville, standardiser, recalculer `d_part`, `d_pca90`, `d_est` et `T_log` ;
   - comparer `T_log_excl` au T_log complet, mesurer `delta_T_log_exclude_topcity` ;
   - si |delta| > 0.02, marquer la fenêtre comme **hautement sensible**.
3. **Transformation des précipitations** :
   - comparer `winsor_precip_T_log` vs `log1p_precip_T_log` dans `tests_priority_summary.csv` ;
   - prioriser les fenêtres où ces transformations changent fortement T_log.
4. **Features générant le plus d’outliers** :
   - inspecter les `summary_<tag>.md` pour voir quelles features (souvent `precipitation_mm` et `urban_heat_island_intensity`) concentrent les outliers.

Ces vérifications servent de **triage** pour décider quelles fenêtres et quelles features méritent une inspection manuelle approfondie.

---

## 4. Classement des fenêtres par sensibilité à la ville top‑offender

Une courte cellule Python illustre comment lister les fenêtres les plus sensibles :

- lecture de `results/temporal_cv_atypical_windows/diagnostics/tests_priority_summary.csv` ;
- calcul de `delta_abs = |delta_T_log_exclude_topcity|` ;
- tri décroissant pour obtenir les top 10 fenêtres par sensibilité.

Extraits de `tests_priority_summary.csv` :

- `annual_2012.0_{A,B,C}` :
  - T_log ≈ 0.0526 → T_log_excl ≈ −0.1477 → delta ≈ **−0.20** ;
- `annual_2008.0_{A,B,C}` :
  - T_log ≈ 0.1455 → T_log_excl ≈ 0.0528 → delta ≈ **−0.093** ;
- `3yr_1984.0_{A,B,C}` :
  - delta ≈ **−0.079** ;
- `annual_2016.0_A` :
  - delta ≈ **−0.053**.

Toutes ces deltas sont **négatives** : retirer Beijing rend systématiquement T_log plus négatif.

---

## 5. Batch : recalcul de T_log sans la ville top‑offender

Une cellule Python automatisée effectue ce recalcul en batch pour les fenêtres prioritaires :

- paramètres :
  - fichier prioritaire : `results/temporal_cv_atypical_windows/diagnostics/tests_priority_summary.csv` ;
  - index enrichi : `results/temporal_cv_atypical_windows/temporal_cv_atypical_periods_windows_index_enriched.csv` ;
  - dossier de sortie : `results/temporal_cv_atypical_windows/diagnostics/tlog_exclude_city_results` ;
  - `TOPN = 10` fenêtres les plus sensibles (par |delta|) ;
  - features par défaut : mêmes 5 features climatiques.

Pour chaque fenêtre sélectionnée :

1. localise le `raw_csv` correspondant (via l’index enrichi ou un pattern glob) ;
2. reconstruit `city_key` si nécessaire ;
3. choisit les features numériques utilisables (priorité aux 5 features climatiques) ;
4. agrège par ville (moyenne), élimine les villes avec NaN ;
5. standardise, calcule `d_part`, `d_pca90`, `d_est` et `T_log_orig` ;
6. identifie la `top_city` (Beijing) ;
7. recalcule `d_est_ex`, `T_log_exclude_topcity` en retirant cette ville ;
8. enregistre toutes les métriques dans un CSV résumé.

Sorties :

- `results/temporal_cv_atypical_windows/diagnostics/tlog_exclude_city_results/tlog_exclude_topcity_comparison.csv` ;
- pour chaque fenêtre, des plots dans `.../tlog_exclude_city_results/<tag>/` :
  - heatmap ville × feature (médianes normalisées) ;
  - séries temporelles de `precipitation_mm` pour la top city (si disponible).

Le CSV contient, par fenêtre :

- `tag`, `window_type`, `window_center`, `pipeline`, `raw_csv`, `n_cities`, `features` ;
- `top_city` ;
- `T_log_orig`, `T_log_exclude_topcity`, `delta_T_log_exclude_topcity` ;
- `d_part`, `d_pca90`, `d_est`, et les valeurs correspondantes **après exclusion** ;
- `status` (ok / erreurs de données).

---

## 6. Résumé rapide des résultats batch

Les commentaires récapitulent les principaux constats :

- **Top city** : Beijing est identifiée comme top‑offender pour toutes les fenêtres traitées.
- **Effet d’exclusion** : 
  - `delta_T_log_exclude_topcity < 0` pour toutes les fenêtres → retirer Beijing rend T_log **plus négatif** ;
  - les deltas vont d’environ −0.05 à −0.20, avec les effets les plus forts sur `annual_2012.0_{A,B,C}`.
- **Effet sur d_est** :
  - `d_est` diminue légèrement après exclusion (baisse typique de ~0.03–0.07) ;
  - Beijing contribue à augmenter légèrement la dimension effective perçue.

Interprétation :

- la présence de Beijing dans ces fenêtres **pousse T_log vers le haut**, rapprochant certains sous‑ensembles d’un régime proche de l’équilibre ou faiblement saturant ;
- son exclusion renforce au contraire le diagnostic global de Divergence ;
- l’influence n’est pas assez extrême pour inverser massivement le signe partout, mais elle est suffisamment forte (jusqu’à Δ≈−0.2) pour justifier des tests LOO plus complets.

Résumé en une phrase :

> Beijing est un contributeur structurant du signal dans les fenêtres atypiques ; son retrait rend systématiquement T_log plus négatif et réduit légèrement d_est.

---

## 7. Plan LOO étendu par ville

Les dernières cellules décrivent (et préparent) un **objectif LOO étendu** :

- pour chaque fenêtre flaggée : 
  - recalculer T_log en retirant **chaque ville** à tour de rôle ;
  - produire un CSV de classement des villes par :
    - delta moyen `T_log_without_city − T_log_full` ;
    - delta absolu ;
    - nombre de fois où le retrait change le régime (D → E / S, etc.) ;
  - sauvegarder, par fenêtre, un plot montrant la distribution LOO de T_log et la position du T_log complet.

Objectif pratique :

- obtenir une **short‑list de villes très influentes** à down‑weight, exclure, ou soumettre à corrections (par ex. corrections de features ou re‑pondération) ;
- compléter le diagnostic : Beijing n’est peut‑être pas la seule ville structurante ; d’autres métropoles peuvent aussi avoir un impact significatif sur T_log.

---

## 8. Rôle de la Partie 6 dans UrbanClimate V0.1

Cette partie :

- passe de la simple détection de fenêtres atypiques (Partie 5) à une **analyse d’influence par ville** ;
- montre que certaines **villes spécifiques** (notamment Beijing) jouent un rôle structurant sur T_log dans des périodes où le régime semble s’écarter du schéma global ;
- fournit une base concrète pour des **analyses LOO ville‑par‑ville** dans chaque fenêtre, permettant d’identifier précisément quelles villes soutiennent ou affaiblissent le diagnostic ;
- renforce l’idée que, même si certaines fenêtres montrent T_log>0, ces signaux peuvent être fortement portés par un petit nombre de villes, et qu’il est donc nécessaire de distinguer :
  - le régime **structurel** (global, robuste aux LOO) ;
  - des **effets localisés** liés à des villes particulières.

En résumé, la Partie 6 fait le lien entre la robustesse globale T_log UrbanClimate et la granularité spatiale (villes) dans les fenêtres temporelles les plus critiques.

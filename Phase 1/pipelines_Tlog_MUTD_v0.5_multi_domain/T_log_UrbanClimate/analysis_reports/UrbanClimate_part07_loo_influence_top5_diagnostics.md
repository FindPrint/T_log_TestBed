# UrbanClimate V0.1 – Partie 7 (cellules 60–69) : LOO étendue, classement d’influence et diagnostics top‑5 villes

## 1. Périmètre

Cette partie correspond aux cellules 60–69 de `UrbanClimate_part07.ipynb`.

Elle prolonge la Partie 6 en :

- généralisant la **LOO par ville** pour toutes les fenêtres atypiques prioritaires ;
- construisant un **classement global des villes influentes** sur T_log ;
- produisant des **diagnostics bruts détaillés** pour les 5 villes les plus influentes.

---

## 2. LOO étendue par fenêtre : classement d’influence des villes

### 2.1 Script LOO par ville et par fenêtre

La cellule principale :

- lit :
  - `results/temporal_cv_atypical_windows/diagnostics/tests_priority_summary.csv` ;
  - `results/temporal_cv_atypical_windows/temporal_cv_atypical_periods_windows_index_enriched.csv` ;
- boucle sur chaque fenêtre atypique `tag` (ou un sous‑ensemble via `TOPN_WINDOWS`) ;
- pour chaque fenêtre :
  1. localise le `raw_csv` correspondant (via l’index enrichi ou un `glob *tag*raw.csv`) ;
  2. reconstruit `city_key` si nécessaire à partir de `city,country,lat,lon` ;
  3. sélectionne les features numériques, avec priorité aux 5 colonnes climatiques (`temperature`, `humidity`, `precipitation`, `wind_speed`, `UHI`) ;
  4. agrège par ville (moyenne), supprime les villes avec NaN ;
  5. standardise (StandardScaler), calcule `d_part`, `d_pca90`, `d_est` et `T_full` ;
  6. effectue un **LOO par ville** :
     - pour chaque ville i, retire la ville, recalcule d et T_log (`T_loo`), puis `delta = T_loo − T_full` ;
  7. construit un DataFrame `loo_df` pour la fenêtre, avec :
     - `city`, `T_loo`, `delta`, `delta_abs`, `d_part_loo`, `d_pca90_loo`, `d_est_loo` ;
  8. trie les villes par `delta_abs` décroissant → villes les plus influentes (en valeur absolue) ;
  9. enregistre **les 5 villes les plus influentes** dans une table globale `influence_rows`.

Les sorties par fenêtre sont enregistrées dans :

- `results/temporal_cv_atypical_windows/diagnostics/loo_influence/<tag>/<tag>_loo_by_city.csv` ;
- plus deux plots :
  - `.../<tag>_loo_hist.png` : histogramme de `T_loo` avec une ligne verticale pour `T_full` ;
  - `.../<tag>_top_influence.png` : bar chart des 10 plus grands `delta` (impact par ville).

### 2.2 Classement global des villes influentes

Après avoir parcouru toutes les fenêtres, la cellule :

- concatène `influence_rows` en un DataFrame global ;
- sauvegarde :

`results/temporal_cv_atypical_windows/diagnostics/loo_influence/loo_influence_top5_per_window.csv`

Chaque ligne contient :

- `tag`, `window_type`, `window_center`, `pipeline`, `raw_csv`, `n_cities` ;
- `feature_list` (features utilisées) ;
- `influencer_rank` (1 à 5) ;
- `city` ;
- `delta_T_log`, `delta_abs`, `T_full`, `T_without_city` ;
- `d_est_full`, `d_est_without_city`.

Interprétation :

- pour chaque fenêtre atypique, on dispose du **top‑5 des villes** qui provoquent le plus grand changement de T_log lorsqu’on les retire.

---

## 3. Synthèse des villes les plus influentes (top5_loo_summary.csv)

### 3.1 Construction du résumé global

Une cellule suivante lit `loo_influence_top5_per_window.csv` et construit un résumé global de l’influence, agrégé par ville :

- groupement par `city` ;
- calcul :
  - `n_windows` = nombre de fenêtres où la ville apparaît dans le top‑5 ;
  - `mean_delta_abs`, `median_delta_abs`, `max_delta_abs` ;
  - `mean_delta_signed` ;
  - `prop_windows_pct` = proportion de fenêtres couvertes.

Les résultats sont triés par `mean_delta_abs` décroissant ; les 5 villes les plus influentes sont sauvegardées dans :

- `results/top5_loo_summary.csv`.

Exemple de top‑5 (d’après la sortie affichée) :

- New York_USA_40.7128_-74.006
- Tokyo_Japan_35.6762_139.6503
- Delhi_India_28.7041_77.1025
- Dallas_USA_32.7767_-96.797
- Chicago_USA_41.8781_-87.6298

Avec notamment :

- `mean_delta_abs` ≈ 0.35 (New York), 0.31 (Tokyo), 0.28 (Delhi), 0.24 (Dallas), 0.23 (Chicago) ;
- `mean_delta_signed` **négative** pour toutes ces villes (leur retrait diminue T_log) ;
- Delhi et Chicago apparaissent dans de nombreuses fenêtres (`n_windows` élevés), New York dans toutes les fenêtres considérées ici (`prop_windows_pct`=100 %).

### 3.2 Interprétation rapide

- un petit groupe de villes (New York, Tokyo, Delhi, Dallas, Chicago, etc.) concentre une part importante de la **sensibilité** de T_log ;
- ces villes tirent T_log vers le **haut** (delta_signed<0 → leur retrait le baisse) ;
- l’effet est **répété** sur plusieurs fenêtres, donc non purement ponctuel.

---

## 4. Diagnostics bruts pour le top‑5 (villes les plus influentes)

Une dernière cellule `diagnostics_top5` produit des diagnostics détaillés pour les 5 villes du top5 global :

- lit :
  - `results/top5_loo_summary.csv` ;
  - `data/urban_climate.csv` ;
- construit `city_key` si nécessaire ;
- pour chaque ville du top‑5 :
  1. filtre toutes les observations brutes sur l’ensemble de la période ;
  2. sauvegarde les signaux bruts dans :

     - `results/diagnostics_top5/<city_key>/signals_<city_key>.csv` ;

  3. calcule des statistiques descriptives par feature (count, mean, std, median, min, max, skew) ;
  4. calcule des **distances de Mahalanobis robustes** (MinCovDet) si possible, stockées dans :

     - `robust_mahalanobis_<city_key>.csv` ;

  5. calcule des **Z‑scores robustes** (median/MAD) par feature, stockés dans :

     - `zscores_<city_key>.csv` ;

  6. assemble un `summary_<city_key>.csv` combinant :
     - une ligne meta rappelant les métriques LOO (mean_delta_abs, max_delta_abs, n_windows, etc.) ;
     - les stats descriptives par feature ;
  7. génère un **plot de séries temporelles** des 5 features climatiques pour la ville :

     - `timeseries_<city_key>.png` ;

  8. crée un petit `README.txt` résumant les fichiers générés et la disponibilité du modèle de Mahalanobis.

Tous ces diagnostics sont regroupés dans :

- `results/diagnostics_top5/` (un sous‑dossier par ville).

---

## 5. Utilisation recommandée des diagnostics top‑5

Les diagnostics bruts pour les 5 villes les plus influentes permettent :

- d’inspecter **visuellement** les comportements temporels des features (séries, pics, dérives) ;
- de repérer les features **systématiquement décalées** (via Z‑scores robustes) et les observations très éloignées (Mahalanobis) ;
- de documenter précisément si l’influence d’une ville provient :
  - de quelques points extrêmes ;
  - ou d’un **niveau structurel différent** (par ex. précipitations systématiquement plus fortes, UHI élevé, etc.).

Ces diagnostics nourrissent les stratégies évoquées en Partie 6 :

- prétraitement localisé par ville (winsorisation, log‑transform, clipping) ;
- règles de flag‑and‑review pour les fenêtres où l’impact est trop élevé ;
- et, en dernier recours, exclusion conditionnelle de certaines villes.

---

## 6. Rôle de la Partie 7 dans UrbanClimate V0.1

Cette partie :

- passe d’une analyse LOO centrée sur une seule ville (Beijing) à un **classement global des villes influentes** sur T_log ;
- identifie un **noyau de villes structurantes** (New York, Tokyo, Delhi, Dallas, Chicago, etc.) dont l’influence est forte et répétée sur les fenêtres atypiques ;
- fournit des diagnostics bruts complets pour ces villes, consolidant la base de décision pour :
  - interpréter correctement les résultats T_log ;
  - choisir d’éventuelles corrections locales ou politiques de downweight/exclusion.

Combinée aux Parties 1–6, cette étape boucle l’analyse **ville × temps** pour UrbanClimate V0.1 :

- le régime global reste Divergence (T_log<0) ;
- certaines fenêtres et villes tirent ponctuellement le système vers des T_log plus élevés ;
- ces cas sont maintenant documentés et quantifiables, plutôt que laissés comme artefacts non analysés.

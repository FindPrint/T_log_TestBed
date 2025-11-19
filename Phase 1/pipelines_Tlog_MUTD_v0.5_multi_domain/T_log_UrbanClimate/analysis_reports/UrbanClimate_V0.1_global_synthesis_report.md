# UrbanClimate V0.1 – Rapport global de synthèse du pipeline T_log

## 1. Objet du rapport

Ce rapport synthétise l’ensemble du pipeline **T_log UrbanClimate V0.1**, dérivé du notebook `T_log_UrbanClimate.ipynb` et détaillé dans les rapports partiels :

- `UrbanClimate_part01` à `UrbanClimate_part07` ;
- les artefacts produits dans `results/` et `logs/`.

L’objectif est de résumer, de manière compacte mais rigoureuse, ce que montre la loi

\[
T_{\log}(n,d) = (d-4)\,\ln(n) + \text{bias}
\]

appliquée au dataset **Urban Air Quality and Climate (1958–2025)**, et en particulier :

- la valeur et le rôle de la **dimension effective d** ;
- le **régime global** (Divergence / Équilibre / Saturation) du système urbain ;
- la **robustesse** de ce diagnostic aux choix de prétraitement, au temps, et à la composition en villes ;
- l’influence de villes particulières (Beijing, Delhi, New York, etc.).

---

## 2. Données et cadre expérimental

### 2.1 Dataset UrbanClimate

- Source : Kaggle, `krishd123/urban-air-quality-and-climate-dataset-1958-2025`.
- Fichier utilisé : `data/urban_climate.csv` téléchargé et vérifié dans le pipeline.
- Taille : **11040 enregistrements**, **12 colonnes**.
- Colonnes principales :
  - clés géographiques : `city`, `country`, `latitude`, `longitude` ;
  - temps : `year`, `month` ;
  - variables climatiques :
    - `temperature_celsius` ;
    - `humidity_percent` ;
    - `precipitation_mm` ;
    - `wind_speed_ms` ;
    - `urban_heat_island_intensity` ;
  - `data_source`.
- Qualité :
  - aucun NA détecté sur les colonnes principales dans l’analyse initiale ;
  - les distributions sont bien définies et utilisables pour l’estimation de `d`.

### 2.2 Construction des entités et prétraitements

L’unité structurante pour T_log n’est pas l’observation brute, mais la **ville**.

- clé de ville :
  - `city_key = city + country + latitude + longitude` ;
- nombre de villes : `n_cities = 20` ;
- agrégation :
  - pour les estimations globales, on agrège les variables climatiques **par ville** sur toute la période (moyenne temporelle) ;
- features utilisées pour l’estimation de `d` :
  - `temperature_celsius`, `humidity_percent`, `precipitation_mm`, `wind_speed_ms`, `urban_heat_island_intensity`.

Prétraitement de base :

- standardisation **StandardScaler** (z‑score) sur la matrice `villes × features` ;
- version verrouillée documentée dans `results/params.json` et `results/README_method.md`.

---

## 3. Loi T_log, dimension et régimes

Dans UrbanClimate V0.1, la loi testée est essentiellement :

\[
T_{\log}(n,d) = (d-4)\,\ln(n)\quad (\text{biais nul}).
\]

Régimes associés :

- **Divergence** si \(T_{\log} < 0\) ;
- **Équilibre** si \(T_{\log} = 0\) ;
- **Saturation** si \(T_{\log} > 0\).

La **dimension effective d** n’est pas imposée a priori mais **estimée** à partir des features climatiques :

- estimateur 1 – **Participation ratio** :
  - spectre de la covariance de `Xs` (villes × features standardisées) ;
  - \(d_{part} = (\sum_i \lambda_i)^2 / \sum_i \lambda_i^2\) ;
- estimateur 2 – **PCA90** :
  - plus petit `k` tel que la variance expliquée cumulée ≥ 90 % ;
- dimension retenue :

\[
 d_{estimate} = \frac{d_{part} + d_{pca90}}{2}.
\]

Cette dimension, couplée à `n = n_cities`, sert à calculer T_log et à analyser le régime global et localement (par fenêtres temporelles, sous‑ensembles de villes, etc.).

---

## 4. Phase I – Estimation de d et diagnostic global (Parties 1–2)

### 4.1 Estimation initiale de d et T_log (Partie 1)

En utilisant les 20 villes, agrégées par moyenne temporelle des 5 features climatiques :

- `d_participation ≈ 3.8005` ;
- `d_pca90 = 4` ;
- `d_estimate ≈ 3.90025` ;
- `n_eff = n_cities = 20` ;

ce qui donne :

\[
T_{\log} \approx (3.90025-4) \ln(20) \approx -0.2988.
\]

Le régime global UrbanClimate est donc **en Divergence** (T_log < 0).

Robustesse initiale :

- Leave‑One‑Out (LOO) sur les villes :
  - moyenne T_log_LOO ≈ −0.353 ;
  - écart type ≈ 0.086 ;
  - rel_std_pct ≈ 24.4 % ;
  - p‑value du test t (H0 : mean T_log = 0) ≈ 0 → rejet de l’équilibre.
- Balayage n/d (fractions de villes 0.5/0.75/1.0 et perturbations de d) :
  - la majorité des tirages reste en **Divergence**, en particulier pour les sous‑échantillons à 50 % de villes ;
  - les perturbations de d autour de 4 modulent T_log dans le sens attendu (plus négatif si d plus petit).

### 4.2 Nettoyage, rapport final et verrouillage de la méthode (Partie 2)

- nettoyage NaN/Inf des CSVs (`tlog_d_estimates`, LOO, sweep) :
  - remplacement des Inf par NaN, imputation médiane ;
  - clipping de `d_estimate` dans `[0.1, 100]` ;
- rapport final `results/final_report.md` :
  - confirmant `d ≈ 3.9003`, `T_log ≈ −0.2988`, régime Divergence ;
- verrouillage de la méthode :
  - `results/params.json` et `results/README_method.md` décrivent précisément :
    - agrégation par ville ;
    - features utilisées ;
    - StandardScaler ;
    - participation ratio + PCA90 ;
    - T_log = (d−4) ln(n_eff).

Sensibilité aux features (drop‑one) :

- retirer `temperature_celsius` ou `precipitation_mm` : effet modéré sur d et T_log ;
- retirer `humidity_percent`, `wind_speed_ms` ou `urban_heat_island_intensity` :
  - d_est tombe ≈ 3 ;
  - T_log ≈ −3 → Divergence fortement accentuée ;
- ces trois variables portent l’essentiel du signal structurale.

---

## 5. Phase II – Qualité des features et prétraitements robustes (Parties 3–4)

### 5.1 Qualité des trois features clés (Partie 3)

Une analyse détaillée (`feature_quality_report.md`) montre :

- distributions globales par feature (histos, boxplots winsorisés, QQ‑plots) ;
- calcul des outliers univariés (règle IQR) et multivariés (Mahalanobis robuste, MinCovDet) ;
- corrélations de Spearman entre features (par ville) ;
- VIF (colinéarité modérée mais non extrême).

Certaines villes (par ex. Dallas, San Antonio, Delhi, Houston...) apparaissent régulièrement comme **outliers multivariés** dans l’espace (humidity, wind, UHI), ce qui explique en partie la sensibilité de d et T_log.

### 5.2 Prétraitements robustes et impact sur d/T_log (Partie 3)

Plusieurs variantes de prétraitement sont comparées :

1. **baseline_StandardScaler** (méthode verrouillée) ;
2. **winsor_1-99_StandardScaler** (winsorisation 1%/99% + StandardScaler) ;
3. **winsor_1-99_RobustScaler** ;
4. **RobustScaler_only** ;
5. **MinCovDet_proj** (projection sur vecteurs propres de la covariance robuste).

Résultats :

- baseline & MinCovDet : `d ≈ 3.90`, `T_log ≈ −0.30` ;
- winsor+StandardScaler : `d ≈ 3.89`, `T_log ≈ −0.32` ;
- variantes RobustScaler : `d ≈ 2.8–2.9`, `T_log ≈ −3.5` (Divergence très forte, considérée comme **effet de sur‑correction**).

Choix opérationnel recommandé :

- conserver la méthode verrouillée StandardScaler ;
- présenter en contraste winsorisation 1–99% + StandardScaler et la projection MinCovDet, qui restent proches du baseline ;
- éviter les prétraitements trop agressifs (RobustScaler) qui écrasent la structure multivariée.

### 5.3 Cross‑validation temporelle (Partie 4)

Une cross‑validation par **fenêtres glissantes** est menée pour pipelines A/B/C :

- fenêtres **annuelles** (1 an, pas 12 mois) ;
- fenêtres **3 ans** (3 ans, pas 6 mois) ;
- pour chaque fenêtre : agrégation par ville, calcul de d et T_log pour chaque pipeline.

Sorties :

- `temporal_cv_annual.csv`, `temporal_cv_3yr.csv` ;
- séries temporelles T_log (T_log vs centre de fenêtre) ;
- heatmaps T_log (fenêtre × pipeline) ;
- métriques de stabilité du signe (fraction de fenêtres où T_log garde le même signe que la médiane du pipeline).

Résultat global :

- pour la plupart des fenêtres, T_log reste **négatif** (Divergence) pour tous les pipelines ;
- certaines fenêtres **atypiques** (années 2003, 2008, 2012, 2014, 2016 et périodes 3 ans centrées 1984, 2014) montrent des T_log proches de 0 ou légèrement positifs, et sont marquées pour revue.

---

## 6. Phase III – Fenêtres atypiques et influence des villes (Parties 5–7)

### 6.1 Diagnostics détaillés par fenêtre atypique (Partie 5)

Les fenêtres atypiques identifiées sont décrites dans :

- `results/temporal_cv_atypical_windows/temporal_cv_atypical_periods_windows_index_enriched.csv`.

Pour chacune, le pipeline génère :

- diagnostics par feature (`diagnostics_features_<tag>.csv`) ;
- diagnostics par ville (`diagnostics_by_city_<tag>.csv`) ;
- heatmap villes × features (`heatmap_cities_features_<tag>.png`) ;
- résumé `summary_<tag>.md` ;
- un résumé global & un ZIP :
  - `temporal_cv_atypical_periods_summary.csv` ;
  - `temporal_cv_atypical_periods_summary_package.zip`.

Ces artefacts permettent une revue humaine complète des périodes où T_log se comporte différemment.

### 6.2 Influence de Beijing et T_log exclu (Partie 6)

Une première analyse cible la ville la plus souvent identifiée comme top‑offender : **Beijing**.

- Fenêtres sensibles :
  - `3yr_1984.0_{A,B,C}`, `3yr_2014.0_{A,B,C}` ;
  - `annual_2003.0_{A,C}`, `annual_2008.0_{A,B,C}`, `annual_2012.0_{A,B,C}`, `annual_2014.0_{A,C}`, `annual_2016.0_{A,B,C}`.
- Effet de l’exclusion de Beijing :
  - T_log diminue systématiquement (`delta_T_log_exclude_topcity < 0`) ;
  - amplitude typique des deltas : **−0.05** à **−0.20**, avec un exemple fort sur `annual_2012` (Δ≈−0.20) ;
  - `d_est` baisse légèrement (~0.03–0.07) ;
- Interprétation :
  - Beijing tire T_log **vers le haut** dans ces fenêtres ;
  - son retrait renforce la Divergence ;
  - l’influence est suffisante pour justifier des analyses LOO plus complètes.

### 6.3 LOO étendue et top‑5 villes influentes (Partie 7)

La LOO est ensuite généralisée à toutes les **villes** et tous les **tags prioritaires** :

- pour chaque fenêtre atypique :
  - LOO par ville, calcul de `delta_T_log = T_without_city − T_full` ;
  - top‑5 villes les plus influentes (par |delta|) ;
- les résultats sont regroupés dans :

  - `loo_influence_top5_per_window.csv`.

Un résumé global par ville (`top5_loo_summary.csv`) montre que :

- les villes les plus influentes sur T_log (en moyenne |delta|) sont :
  - New York, Tokyo, Delhi, Dallas, Chicago (Beijing figure aussi en bonne place dans les diagnostics détaillés) ;
- `mean_delta_signed` est **négatif** pour toutes ces villes → leur suppression rend T_log plus négatif ;
- ces villes apparaissent dans de nombreuses fenêtres, signe d’un effet **structurel** et non ponctuel.

### 6.4 Diagnostics bruts pour les 5 villes les plus influentes

Pour les 5 villes de `top5_loo_summary.csv`, le pipeline génère :

- `results/diagnostics_top5/<city_key>/signals_<city>.csv` : toutes les observations brutes (sur tout l’horizon temporel) ;
- `summary_<city>.csv` : stats descriptives par feature + méta informations LOO ;
- `robust_mahalanobis_<city>.csv` : distances de Mahalanobis robustes par observation ;
- `zscores_<city>.csv` : Z‑scores robustes (median/MAD) ;
- `timeseries_<city>.png` : séries temporelles des 5 features climatiques ;
- `README.txt` : mini résumé des fichiers.

Ces diagnostics permettent de comprendre **pourquoi** ces villes ont un impact fort :

- distributions décalées d’une feature (par ex. précipitations ou UHI) ;
- présence de segments temporels cohérents avec des extrêmes climatiques ou des biais de mesure.

---

## 7. Synthèse globale : régime UrbanClimate V0.1

En combinant toutes les phases, on obtient l’image suivante :

1. **Dimension effective** :
   - d’estimée ≈ **3.90**, légèrement inférieure à 4 ;
   - estimation stable sous plusieurs estimators (participation ratio, PCA90) et prétraitements raisonnables (StandardScaler, MinCovDet).

2. **Régime global T_log** :
   - à `n_cities = 20`, `T_log ≈ −0.30` → **régime Divergence** ;
   - LOO sur les 20 villes confirme une moyenne T_log significativement < 0.

3. **Robustesse** :
   - nettoyage NaN/Inf, clipping de d : pas de changement qualitatif du diagnostic ;
   - prétraitements robustes modérés (winsor 1–99) : T_log légèrement plus négatif mais cohérent ;
   - cross‑validation temporelle : la plupart des fenêtres (1 an ou 3 ans) restent en Divergence ;
   - quelques fenêtres atypiques montrent T_log>0, mais sont **fortement corrélées à un petit groupe de villes** (Beijing, Delhi, New York, etc.).

4. **Influence des villes** :
   - un noyau de grandes métropoles (New York, Tokyo, Delhi, Dallas, Chicago, Beijing, etc.) exerce un levier important sur T_log dans les fenêtres priorisées ;
   - leur suppression rend T_log plus négatif, **renforçant** le diagnostic de Divergence ;
   - leur comportement climatique (features) est non trivial et parfois très extrême ou décalé.

En résumé :

- UrbanClimate V0.1 se trouve globalement dans un régime de **Divergence** (d<4, T_log<0) ;
- ce diagnostic est robuste à des variantes raisonnables de prétraitement, à la cross‑validation temporelle, et à une analyse LOO par ville ;
- des signaux locaux (fenêtres temporelles + villes spécifiques) peuvent temporairement tirer T_log vers le haut, mais ils sont **identifiés, quantifiés et traçables**.

---

## 8. Limites et pistes pour V1/V2

Limites explicites :

- dimension effective `d` estimée à partir de seules variables climatiques scalaires (5 features) ;
- hypothèse de biais nul dans T_log pour ce pipeline ;
- absence de modélisation explicite des mécanismes physiques urbains (sources anthropiques, morphologie urbaine, politiques climatiques) ;
- dépendance aux villes influentes : même si leur impact est tracé, la décision de les traiter (downweight/exclure) reste au niveau méthodologique.

Pistes proposées :

- **T_log V1** :
  - introduire un biais calibré pour contrôler la dérive systématique de T_log autour de 0 ;
  - explorer des estimateurs de dimension plus riches (non‑linéaires, manifold learning) ;
- **T_log V2** :
  - intégrer explicitement des modèles temps‑série sur les features par ville (mémoire, régimes saisonniers) ;
  - modéliser la dimension **spatio‑temporelle** (temps + réseau de villes) ;
  - étendre la validation à d’autres datasets urbains (autres régions, autres variables).

---

## 9. Rôle pratique de ce rapport

`UrbanClimate_V0.1_global_synthesis_report.md` peut servir de :

- **résumé de haut niveau** du pipeline UrbanClimate ;
- **point d’entrée** vers les rapports `UrbanClimate_part01–07` et les artefacts `results/` ;
- base textuelle pour un article ou un rapport technique, en complétant avec les rapports détaillés et les figures.

La combinaison des analyses globales (d & T_log) et locales (fenêtres atypiques, influence de villes) fait de UrbanClimate V0.1 un cas d’étude complet pour la loi T_log appliquée à des données climatiques urbaines multi‑villes et multi‑décennales.

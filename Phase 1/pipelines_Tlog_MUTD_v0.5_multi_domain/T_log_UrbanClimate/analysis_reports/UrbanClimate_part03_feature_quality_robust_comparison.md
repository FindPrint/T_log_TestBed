# UrbanClimate V0.1 – Partie 3 (cellules 20–29) : Qualité des features clés et ré‑estimation robuste de d et T_log

## 1. Périmètre

Cette troisième partie correspond aux cellules 20–29 de `UrbanClimate_part03.ipynb`.

Elle ajoute une couche de validation autour des trois features qui dominaient déjà la sensibilité T_log en Partie 2 :

- `humidity_percent`
- `wind_speed_ms`
- `urban_heat_island_intensity`

Objectifs :

- vérifier la **qualité statistique** de ces variables (distribution, outliers, corrélations, VIF) ;
- tester des **prétraitements robustes** (winsorisation, RobustScaler, MinCovDet) et voir leur impact sur la dimension effective `d` et T_log ;
- préparer des pipelines A/B/C pour comparaisons plus complètes (LOO, sweep) en fin de notebook.

---

## 2. Contrôle de qualité des features

Une cellule "Feature quality checks" :

- charge `data/urban_climate.csv` ;
- construit une clé de ville `city_key = city,country,latitude,longitude` et agrège par ville ;
- calcule des **statistiques robustes globales** pour chaque feature : min, Q1, médiane, Q3, max, moyenne, écart‑type, IQR, MAD, skewness, kurtosis, proportion de NaN ;
- sauvegarde ces stats dans `results/feature_quality_stats.csv` ;
- génère, pour chaque feature :
  - histogramme (`hist_*.png`) ;
  - boxplot winsorisé 1%/99% (`box_win_*.png`) ;
  - QQ‑plot vs loi normale (`qq_*.png`) ;
- produit des **séries temporelles** pour un petit nombre de villes les plus documentées (top 6), en traçant l’évolution des trois features par `year_month` ;
- calcule :
  - la matrice de corrélation de Spearman par ville (`feature_spearman_corr.csv`) ;
  - des **scores de Mahalanobis** robustes sur l’espace (humidity, wind, UHI) (`feature_mahalanobis_scores.csv`) ;
  - des **VIF** (variance inflation factor) pour détecter la colinéarité (`feature_vif.csv`) ;
- détecte des outliers :
  - par règle IQR sur les valeurs brutes de chaque feature ;
  - par Mahalanobis sur l’espace multivarié (villes avec distance > quantile 97.5%) ;
  - résume dans `feature_outliers_detected.csv` ;
- assemble le tout dans un rapport `results/feature_quality_report.md` listant stats, matrices, outliers et chemins des plots.

En pratique, cette étape confirme que :

- les trois variables portent bien un signal structurés (corrélations non triviales) ;
- certaines villes (par exemple grandes métropoles) apparaissent comme **outliers multivariés** dans l’espace (humidity, wind, UHI), ce qui explique en partie la forte sensibilité observée sur d et T_log.

---

## 3. Ré‑estimation robuste de d et T_log

Une cellule "robust comparison" met en place plusieurs variantes de prétraitement sur la matrice per‑city des features :

- baseline : StandardScaler (méthode verrouillée) ;
- winsorisation 1%/99% + StandardScaler ;
- winsorisation 1%/99% + RobustScaler ;
- RobustScaler seul ;
- projection MinCovDet (covariance robuste) à partir des données standardisées.

Pour chaque variante, la cellule :

- calcule `d_part` (participation ratio), `d_pca90`, `d_est = (d_part + d_pca90)/2` (avec clipping éventuel) ;
- calcule `T_log = (d_est - 4)*ln(n_eff)` avec `n_eff = max(2, n_cities)` ;
- sauvegarde le tableau comparatif dans `results/tlog_robust_comparison.csv` ;
- trace un barplot comparant T_log pour chaque prétraitement (`tlog_robust_comparison.png`).

Résultats affichés :

- **baseline_StandardScaler** : `d ≈ 3.90`, `T_log ≈ −0.2988` (Divergence modérée, cohérent avec Parties 1–2) ;
- **winsor_1-99_StandardScaler** : `d ≈ 3.89`, `T_log ≈ −0.318` (très proche du baseline, légère accentuation de la divergence) ;
- **winsor_1-99_RobustScaler** et **RobustScaler_only** : `d ≈ 2.8–2.9`, `T_log ≈ −3.5 à −3.6` → Divergence beaucoup plus forte (perte de structure multivariée informative, dimension effective abaissée) ;
- **MinCovDet_proj** : `d ≈ 3.90`, `T_log ≈ −0.2988`, quasiment identique à la baseline.

Interprétation :

- la méthode verrouillée StandardScaler et la variante MinCovDet (projection robuste) convergent vers la même estimation `d ≈ 3.90`, T_log ≈ −0.30 ;
- les prétraitements centrés fortement robustes (RobustScaler) ont tendance à écraser les contrastes multivariés et à abaisser d vers ≈3, produisant un T_log très négatif qui ne reflète plus la structure d’origine mais plutôt une sur‑correction ;
- le compromis raisonnable pour une preuve empirique **honnête et reproductible** est donc :
  - de conserver la méthode verrouillée StandardScaler (documentée dans `params.json`/`README_method.md`) ;
  - de présenter, à titre de contrôle, les résultats sous winsorisation 1%/99% + StandardScaler et sous projection MinCovDet, qui sont transparents et ne modifient pas qualitativement la conclusion.

---

## 4. Pipelines A/B/C (préparation)

La fin de ce bloc prépare une cellule (non détaillée ici) qui définit trois pipelines pour des validations comparatives plus lourdes :

- **Pipeline A** : méthode verrouillée StandardScaler (baseline V0.1) ;
- **Pipeline B** : winsorisation 1%/99% + StandardScaler ;
- **Pipeline C** : projection MinCovDet.

L’idée est de ré‑exécuter pour chacun :

- l’estimation de d et T_log ;
- le LOO sur les villes + test t ;
- le balayage n/d (fractions 0.5/0.75/1.0, variations ±20% sur d) ;
- puis de comparer les métriques de robustesse et les cartes de régimes.

Cette préparation s’appuie directement sur les diagnostics de qualité et la comparaison de prétraitements réalisés dans cette Partie 3.

---

## 5. Message global de la Partie 3

- Les trois features `humidity_percent`, `wind_speed_ms` et `urban_heat_island_intensity` sont confirmées comme **portant le signal structurel** pour UrbanClimate (corrélations et outliers multivariés non triviaux).
- La méthode verrouillée StandardScaler donne `d ≈ 3.90`, `T_log ≈ −0.30` ; cette estimation est **reproduite** par la projection robuste MinCovDet.
- Les approches trop agressivement robustes (RobustScaler fort) produisent des `d` nettement plus faibles et des T_log très négatifs, qui traduisent davantage une perte d’information qu’un meilleur ajustement.
- La suite du notebook exploitera ces pipelines A/B/C pour démontrer que, même sous ces variantes raisonnables, UrbanClimate reste globalement en **régime Divergence** et que la conclusion V0.1 est robuste aux choix de prétraitement documentés.

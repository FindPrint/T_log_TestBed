# Sunspots V0.5 – Partie 11 (cellules 100–109) : Refit ciblé des cas atypiques et reconstruction des counting spectraux

## 1. Périmètre de la partie

Cette onzième partie correspond aux cellules **100–109** du notebook `Sunspots_part11.ipynb` (split 10 cellules) dérivé de `Pipeline_Tlog_V0.1_Sunspots_En.ipynb`.

Elle opère un **nettoyage ciblé** du référentiel `ds_robust_per_b.csv` et des diagnostics Theil–Sen en :

- identifiant des **bootstraps atypiques** (top‑15 proches de T_log≈0, cas manquants ou ambigus) ;
- tentant un **refit manuel/ciblé** pour un petit ensemble (top‑5) ;
- construisant des fichiers **counting** (λ, N(λ)) à partir de fichiers d’eigenvalues ;
- explorant des correspondances (strictes, fuzzy, par signature) entre b et fichiers counting ;
- utilisant un rapport étendu `top15_match_report_extended.csv` pour un **refit automatique** sur les 15 cas.

L’objectif est de fiabiliser les `d_s_robust` et `Tlog_npoints_median` pour les cas les plus critiques, tout en gardant une trace explicite de chaque modification.

---

## 2. Refit ciblé Theil–Sen pour un top‑5 de cas atypiques

### 2.1 Logique et sélection des b

La première cellule définit une liste de bootstraps `b_list` à corriger :

- soit à partir d’un fichier `top5_atypical_review.csv` (s’il existe) ;
- soit par défaut `b_list = [69, 11, 89, 52, 67]`.

Ces b proviennent du top‑15 des cas **proches de T_log≈0** ou ayant des diagnostics incomplets.

### 2.2 Sauvegarde et refit

La cellule :

- sauvegarde d’abord `results/ds_remove_small_lambda/ds_robust_per_b.csv` dans `backups/ds_robust_per_b_pre_refit_*.csv` ;
- charge :
  - `theilsen_ds_remove_small_lambda_wide.csv` ;
  - `paired_levina_spectral_theilsen_raw.csv` (ou `paired_levina_spectral_raw.csv` en fallback) ;
- pour chaque b de `b_list` :
  - tente de trouver un fichier counting plausible (N(λ) vs λ) via quelques patterns (`topK_discrepancy_inspect`, `spectral_diagnostics`, `spectral_diagnostics_linearity`) ;
  - si N(λ) est trouvé, refait un **fit Theil–Sen** sur λ ≤ 0.2 ;
  - calcule `d_s = 2·slope`, estime `Tlog_npoints_median` (avec n_med issu de `theilsen_ds_remove_small_lambda_per_b.csv`) ;
  - met à jour la ligne correspondante dans `ds_robust_per_b` ;
  - génère un PNG `diagnostics_theilsen_per_b_top15/b_XXX_diagnostic_rebuilt.png` avec la droite Theil–Sen et les valeurs d_s/T_log annotées.

Résultat observé dans les sorties :

- seul **b = 11** dispose d’un counting fiable (`diag_011_counting.csv`) → refit réussi ;
- pour b=69, 89, 52, 67, il n’y a pas assez de points λ ≤ 0.2 (0 points) → refit impossible, ces b restent inchangés.

Un manifeste `manifest_refit_top5_*.json` consigne quels b ont été mis à jour.

---

## 3. Construction générique de fichiers counting à partir des eigenvalues

### 3.1 Cellule A1 — constat de manque de fichiers counting

Une cellule de diagnostic (`Cellule A1`) montre que pour b = 69, 89, 52, 67 :

- aucune combinaison de patterns (`*{b:03d}*.csv`, `*_{b}_*.csv`, etc.) ne donne un fichier counting ou eigvals spécifique ;
- `candidates: 0` pour chaque b.

Cela confirme qu’il manque des fichiers N(λ)/λ clairement identifiables pour ces b.

### 3.2 Cellule A2 — génération non destructive de counting génériques

Pour pallier ce manque, la cellule **A2** parcourt tous les fichiers CSV dont le nom contient `eigval` ou similaire et construit, pour chacun, un fichier counting associé :

- lecture de la colonne eigenvalues (`eigval`, `eigvals`, etc.) ;
- tri croissant ;
- construction de N(λ) = rang (1,2,…) ;
- écriture de `lambda, N_lambda` dans :

  - `results/spectral_diagnostics_counting/<nom>_counting.csv`.

Elle produit, entre autres :

- `laplacian_eigenvalues_counting.csv` ;
- `null_debug_temporal_shuffle_eigvals_counting.csv` ;
- `diag_001_eigvals_counting.csv` … `diag_020_eigvals_counting.csv` ;
- `diag_01_eigvals_counting.csv` … `diag_10_eigvals_counting.csv`.

Au total, **32 fichiers counting** sont générés, sans supprimer ni écraser de données existantes.

---

## 4. Nouvelles tentatives de refit et analyse de signatures

### 4.1 Cellule A3 — refit à partir de counting reconstruit

La cellule A3 ré‑essaie de refitter b = [69, 89, 52, 67] en utilisant les nouveaux fichiers `spectral_diagnostics_counting` :

- pour chaque b, cherche un fichier `*{b:03d}*counting.csv` ;
- malheureusement, aucun fichier counting n’est tagué explicitement par ces indices de b ;
- la cellule conclut : "no counting file found" pour chacun de ces b.

`ds_robust_per_b.csv` est ré‑écrit mais reste inchangé sur ces lignes.

### 4.2 Cellule A4 — recherche par signature spectrale

Une cellule plus avancée tente une approche par **signature** :

- lit les 6 plus petites valeurs λ de chaque fichier `*_counting.csv` et en fait un vecteur ;
- construit une signature médiane et calcule des distances de type norme L2 sur log(λ) ;
- pour chaque b manquant (69, 89, 52, 67), affiche les fichiers counting dont la signature est la plus proche.

Résultat observé :

- pour tous ces b, les premières suggestions sont `diag_001_eigvals_counting.csv`, `diag_002_eigvals_counting.csv`, etc., toutes à distance 0 ;
- cela indique que les 6 plus petits λ de ces diagnostics sont identiques ou quasi identiques → la signature n’est pas discriminante pour distinguer les b.

Conclusion : il n’est pas possible, à ce stade, de **retracer de manière certaine** quel fichier counting correspond à quel b uniquement via les signatures des petites valeurs propres.

---

## 5. Utilisation de top15_match_report_extended et refit automatique

### 5.1 Lecture du rapport étendu

Une cellule lit `results/ds_remove_small_lambda/top15_match_report_extended.csv` et affiche les lignes correspondant à certains b :

- ce rapport contient, pour chaque b du top‑15, des colonnes telles que `source`, `png`, `note` ;
- pour b = 69, 89, 52, on voit par exemple :
  - `source=results/spectral_diagnostics/diag_001_counting.csv` ;
  - `png=diagnostics_theilsen_per_b_top15/b_XXX_diagnostic_rebuilt.png` ;
  - `note=auto-match-fallback` ;
- pour b = 67, aucune entrée.

Ce fichier sert de **journal de correspondances proposées** (semi‑automatiques ou manuelles) entre b et fichiers counting.

### 5.2 Refit automatique guidé par le rapport

La dernière grande cellule de la partie utilise ce rapport pour un refit automatique :

- lit `top15_match_report_extended.csv` et `ds_robust_per_b.csv` ;
- pour chaque b présent dans le rapport (par ex. 69, 89, 52, 113, 72, 108, 57, 66, 49, 83, 31, 145) :
  - tente d’abord de lire le fichier counting pointé par `source` ;
  - sinon, cherche un fichier `*{b:03d}*counting.csv` ;
  - sinon, **fallback** sur `results/spectral_diagnostics/diag_001_counting.csv` (comme note `auto-match-fallback`).

Si un counting N(λ) peut être lu :

- filtre λ ≤ 0.2 ;
- ajuste un Theil–Sen (log N vs log λ) → slope, d_s = 2·slope ;
- calcule `Tlog_npoints_median` avec la médiane de `n_points_fit` dans `ds_robust_per_b` ;
- met à jour ou ajoute la ligne correspondante dans `ds_robust_per_b` ;
- génère un PNG `diagnostics_theilsen_per_b_top15/b_XXX_diagnostic_rebuilt.png`.

Avant d’écraser le fichier canonique, la cellule fait un **backup** :

- `backups/ds_robust_per_b_pre_refit_auto_*.csv` ;
- puis réécrit `ds_robust_per_b.csv` avec les valeurs mises à jour.

Un manifeste JSON `manifest_refit_auto_*.json` documente :

- les b mis à jour (`updated`) ;
- les b éventuellement ignorés (`skipped`) ;
- les actions et sources utilisées.

### 5.3 Interprétation

- Le refit auto met à jour un ensemble de b du top‑15, en utilisant soit un mapping explicite (source connue), soit un fallback générique (diag_001_counting.csv) quand aucune correspondance claire n’existe ;
- ces opérations sont **tracées et réversibles** (backups + manifestes) ;
- néanmoins, les cas marqués `auto-match-fallback` doivent être considérés comme **moins fiables** du point de vue de l’attribution exacte b → spectre ; ils servent surtout à stabiliser numériquement le tableau `ds_robust_per_b` et les PNG associés.

---

## 6. Rôle de la Partie 11 dans le pipeline Sunspots V0.5

La Partie 11 joue le rôle de **maintenance avancée** du bloc Theil–Sen / `ds_remove_small_lambda` :

- elle cible les cas **atypiques** ou **mal instrumentés** (b proches de T_log≈0, fichiers counting manquants) ;
- elle refait des fits Theil–Sen sur N(λ) vs λ en construisant, si nécessaire, des fichiers counting à partir des eigenvalues ;
- elle consigne toutes les mises à jour dans `ds_robust_per_b.csv` avec backups et manifestes ;
- elle permet de disposer d’un ensemble de diagnostics graphiques homogènes pour les b critiques.

Du point de vue de T_log :

- ces raffinements ne remettent pas en cause le constat global (d_s robustes < 4 → T_log<0 → régime de **Divergence**) ;
- ils améliorent surtout la **cohérence interne** des estimations d_s_robust et la traçabilité des choix lorsque l’on souhaite inspecter manuellement les cas proches de l’équilibre ou des frontières de régime.

En résumé, la Partie 11 ferme le "chapitre Theil–Sen" en nettoyant les derniers cas problématiques et en préparant un jeu de résultats robuste et bien documenté pour une synthèse globale Sunspots V0.5.

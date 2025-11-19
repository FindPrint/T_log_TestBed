# Sunspots V0.5 – Partie 10 (cellules 90–99) : Pipeline ds_remove_small_lambda et reconstruction robuste par Theil–Sen

## 1. Périmètre de la partie

Cette dixième partie correspond aux cellules **90–99** du notebook `Sunspots_part10.ipynb` (split 10 cellules) dérivé de `Pipeline_Tlog_V0.1_Sunspots_En.ipynb`.

Elle se concentre sur un **pipeline auxiliaire** appelé `ds_remove_small_lambda` qui vise à :

- exploiter les résultats Theil–Sen précédemment calculés (pentes spectrales robustes) ;
- reconstruire un tableau propre par bootstrap **ds_robust_per_b** ;
- calculer un T_log associé (via une convention spécifique sur `n_points_fit`) ;
- identifier les **bootstraps les plus proches de T_log ≈ 0** ;
- générer des diagnostics graphiques pour ces cas.

Tous les traitements de cette partie sont **non destructifs** ou soigneusement journalisés (backups, manifestes).

---

## 2. Préflight non‑destructif des fichiers ds_remove_small_lambda

La première cellule est un **preflight** qui ne modifie rien :

- construit les chemins :
  - `results/ds_remove_small_lambda/theilsen_ds_remove_small_lambda_wide.csv` ;
  - `results/ds_remove_small_lambda/theilsen_ds_remove_small_lambda_per_b.csv` ;
  - dossier `diagnostics_theilsen_per_b/` ;
- affiche :
  - la date/heure UTC ;
  - le répertoire de travail courant ;
  - l’existence (FOUND/MISSING) des deux CSV ;
  - le contenu du dossier de diagnostics (PNG déjà présents) ;
  - les manifests JSON éventuels (`manifest_from_inspect.json`) ;
  - la taille et le SHA1 des deux CSV ;
  - un **aperçu (5 lignes)** de chaque CSV existant.

Sortie observée :

- les deux fichiers `theilsen_ds_remove_small_lambda_*.csv` existent (wide + per_b) ;
- un dossier `diagnostics_theilsen_per_b` contient déjà 5 PNG (b_101, b_140, b_17, b_56, b_81) ;
- un manifeste `manifest_from_inspect.json` trace des infos sur une inspection précédente ;
- les entêtes des CSV montrent notamment que `theilsen_ds_remove_small_lambda_wide.csv` contient des colonnes :
  - `b, d_s_k0, d_s_k1, d_s_k2, d_s_k3, levina_mle` ;
  - avec d_s_k0..k3 correspondant à des d_s(Theil–Sen) calculés en excluant 0,1,2,3 plus petites valeurs propres.

Cette cellule sert à **vérifier l’état du disque** avant toute réécriture, en mode 100 % lecture.

---

## 3. Reconstruction non‑destructive de ds_robust_per_b à partir des fichiers paired

La seconde cellule reconstruit un tableau **cohérent** des dimensions spectrales robustes par bootstrap :

- elle lit, si possible :
  - `results/paired_levina_spectral_theilsen/paired_levina_spectral_theilsen_raw.csv` (prioritaire) ;
  - sinon `results/paired_levina_spectral/paired_levina_spectral_raw.csv` ;
- filtre les lignes pour **λ_max ≈ 0.2** (le λ_max utilisé auparavant) :
  - si une colonne `lambda_max` existe, sélectionne `lambda_max == 0.2` ;
  - sinon, prend la meilleure approximation (λ_max ≤ 0.2, n_points_fit, etc.).

À partir de ces lignes, elle reconstruit :

- `b` (indice de bootstrap) ;
- `n_points_fit` ;
- `lambda_max_used` ;
- `slope_used` (Theil–Sen) ;
- `d_s_robust` (soit lu directement, soit = 2·slope) ;
- `fit_ok`.

Ce tableau est sauvegardé dans `results/ds_remove_small_lambda/ds_robust_per_b_rebuilt.csv`. Elle calcule ensuite un T_log basé sur une convention `n_points_median` :

- lit `theilsen_ds_remove_small_lambda_per_b.csv` si disponible pour prendre la médiane de `n_points_fit` ;
- sinon, utilise la médiane de `n_points_fit` dans `df_rebuilt` ;
- définit :

\[
 T_{\log}^{(npoints\_median)} = (d_s^{robust} - 4) \ln(n_{points\_median}).
\]

Ce T_log local n’est pas le T_log global du système, mais une **tension effective** calculée pour un n calibré par le nombre de points de fit, utile pour classer les bootstraps.

Un fichier wide augmentée `theilsen_ds_remove_small_lambda_wide_augmented_rebuilt.csv` est également écrit, ajoutant `d_s_robust` aux colonnes d_s_k0..k3.

---

## 4. Remplacement contrôlé de ds_robust_per_b.csv par la version reconstruite

La troisième cellule effectue le remplacement **avec sauvegarde** :

1. **Backup** :
   - si `results/ds_remove_small_lambda/ds_robust_per_b.csv` existe, il est déplacé dans `backups/ds_robust_per_b_YYYYMMDDThhmmssZ.csv` ;
2. **Remplacement** :
   - `ds_robust_per_b_rebuilt.csv` est renommé en `ds_robust_per_b.csv` ;
3. **Résumé** :
   - lecture du fichier canonique ;
   - affichage de la distribution de `d_s_robust` (moyenne ≈ 1.56, min ≈ 1.38, max ≈ 1.75) ;
   - résumé de `Tlog_npoints_median` (moyenne ≈ −6.61, min ≈ −7.09, max ≈ −6.10).

Ensuite, la cellule identifie les **15 bootstraps dont |T_log| est le plus proche de 0** :

- ajoute une colonne `abs_Tlog = |Tlog_npoints_median|` ;
- trie par `abs_Tlog` ;
- affine `top15_Tlog_closest_to_zero.csv` dans `results/ds_remove_small_lambda/` ;
- affiche ce top‑15 (b, d_s_robust, Tlog, fit_ok, λ_max_used).

Enfin, elle écrit un petit manifeste JSON (`manifest_replace_*.json`) dans `results/ds_remove_small_lambda/` décrivant l’action :

- `action`, `timestamp_utc`, chemin du canonique, nombre de lignes, etc.

Cette étape fige un **référentiel propre** `ds_robust_per_b.csv` pour la suite des diagnostics Theil–Sen.

---

## 5. Diagnostics graphiques pour les 15 bootstraps proches de T_log ≈ 0

### 5.1 Première tentative (diagnostics_theilsen_per_b_top15)

Une cellule tente de générer, pour chaque b du top‑15 :

- un diagnostic log‑log N(λ) vs λ avec la droite Theil–Sen correspondante ;
- annotation de d_s et T_log dans un encart ;
- sauvegarde des PNG dans `diagnostics_theilsen_per_b_top15/b_XXX_diagnostic_rebuilt.png`.

Pour cela, elle cherche des fichiers `*_counting.csv` (λ, N(λ) ou eigenvalues) selon plusieurs patterns (topK_discrepancy_inspect, spectral_diagnostics_linearity, spectral_diagnostics) puis récupère les plus adaptés.

Résultat :

- seuls quelques b (ex. 8, 11, 19) disposent de fichiers counting utilisables ;
- des warnings sont affichés pour les autres b (fichiers introuvables).

### 5.2 Deuxième tentative (reconstruction par similarité de contenu)

Une cellule plus avancée :

- scanne récursivement les CSV du projet pour repérer ceux qui ressemblent à des fichiers eigenvalues/counting (columns `eigval`, `lambda`, `N_lambda`) ;
- construit une **signature** des petites valeurs (les 6 plus petits λ ou eigenvalues) pour chaque fichier candidat ;
- pour chaque b manquant, liste les fichiers dont la signature est la plus proche (distance sur log λ) ;
- affiche pour chaque b une liste de candidates avec un score de distance.

Ces suggestions permettent à l’utilisateur de :

- identifier manuellement les fichiers counting les plus plausibles pour les b manquants ;
- compléter au besoin les diagnostics et les PNG à la main.

---

## 6. Rôle de la Partie 10 dans le pipeline Sunspots V0.5

Cette Partie 10 :

- consolide un **référentiel robuste** `ds_robust_per_b.csv` basé sur les résultats Theil–Sen précédemment calculés, avec backups et manifestes ;
- fournit un **T_log effectif par bootstrap** (`Tlog_npoints_median`) et un classement des bootstraps par proximité de T_log ≈ 0 ;
- tente de construire des **diagnostics graphiques** pour ces cas « proches de l’équilibre », en retrouvant les fichiers N(λ) ou eigenvalues correspondants ;
- sans toucher ni aux embeddings ni aux calculs principaux, mais en réorganisant proprement les résultats pour permettre une exploration plus fine.

En pratique, cette partie marque la fin du "bloc Theil–Sen" : elle fige les d_s robustes par bootstrap, identifie des cas particuliers à inspecter visuellement, et prépare un éventuel travail ultérieur sur la sélection/pondération des λ (via `ds_remove_small_lambda`) dans le calcul de la dimension spectrale et du T_log associé.

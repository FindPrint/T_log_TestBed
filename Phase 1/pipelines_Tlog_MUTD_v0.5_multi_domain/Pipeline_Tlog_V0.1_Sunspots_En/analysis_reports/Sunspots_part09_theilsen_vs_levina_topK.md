# Sunspots V0.5 – Partie 9 (cellules 80–89) : Theil–Sen spectral vs Levina–Bickel et inspection des cas extrêmes

## 1. Périmètre de la partie

Cette neuvième partie correspond aux cellules **80–89** du notebook `Sunspots_part09.ipynb` (split 10 cellules) dérivé de `Pipeline_Tlog_V0.1_Sunspots_En.ipynb`.

Elle poursuit l’analyse avancée de la dimension, en particulier :

- le recalcul systématique d’une **dimension spectrale d_s** via Theil–Sen pour chaque bootstrap ;
- la comparaison **appariée** Levina–Bickel vs d_s(Theil–Sen) (tests statistiques, scatter plots, boxplots) ;
- l’inspection détaillée des **bootstraps les plus discordants** (top‑K) ;
- l’étude de l’effet d’exclure les plus petites valeurs propres sur la pente spectrale.

L’objectif est de comprendre finement **pourquoi** les dimensions estimées par Levina–Bickel (~8) et par pente spectrale (d_s ≪ 4) restent numériquement incompatibles.

---

## 2. Recalcul de d_s (Theil–Sen) pour chaque bootstrap et comparaison avec Levina

### 2.1 Méthodologie

Une cellule majeure **recalcule d_s spectrale avec Theil–Sen** pour chaque bootstrap `b` déjà utilisé dans le bootstrap Levina–Bickel :

- fichiers d’entrée :
  - `results/levina_bickel_boot_samples.csv` (colonnes `b`, `levina_mle`) ;
- paramètres :
  - `embedding_dim = 10`, `tau = 1`, `k_neighbors = 10`, `n_eig = 400` ;
  - `subsample_frac = 0.6` ;
  - `lambda_max_list = [0.1, 0.2, 0.4]` ;
  - `min_points_for_fit = 4`.

Pour chaque bootstrap `b` :

1. on ré‑utilise les **mêmes sous‑échantillons** que pour Levina (même `rng_seed` et `subsample_frac`) ;
2. on calcule le spectre du Laplacien (400 plus petites valeurs propres) ;
3. pour chaque `lambda_max` de la liste :
   - on sélectionne N(λ) pour λ ≤ `lambda_max` ;
   - on ajuste une pente log‑log via **Theil–Sen** (robuste) sur `log N` vs `log λ` ;
   - on en déduit \( d_s^{TS} = 2 · \text{slope} \). 

Les résultats sont stockés dans :

- `results/paired_levina_spectral_theilsen/paired_levina_spectral_theilsen_raw.csv`.

On calcule ensuite, pour chaque λ_max :

- médianes Levina et d_s(Theil–Sen) ;
- moyenne et écart‑type des différences Levina − d_s(Theil–Sen) ;
- tests Wilcoxon appariés, t‑test apparié, corrélation de Spearman.

Résumé : `paired_levina_spectral_theilsen_tests_summary.csv`.

### 2.2 Résultats principaux

La cellule d’analyse indique :

- Levina m_hat médiane ≈ **7.94** (sur ~150 bootstraps) ;
- d_s(Theil–Sen) médiane :
  - ≈ **0.83** pour λ_max=0.1 ;
  - ≈ **1.56** pour λ_max=0.2 ;
  - ≈ **3.19** pour λ_max=0.4 ;
- les différences Levina − d_s(Theil–Sen) sont massives (≈ 6.5–7.1) et très structurées ;
- Wilcoxon et t‑tests appariés donnent p ≪ 0.001 pour toutes les λ_max ;
- Spearman rho reste très faible (→ pas de corrélation forte). 

Interprétation immédiate :

- même avec un estimateur **robuste** Theil–Sen, les estimations spectrales de d_s restent **bien en deçà** de Levina (~8) ;
- la divergence entre méthodes n’est pas due à une instabilité aléatoire, mais à une **incompatibilité de définition** (intrinsic dim locale vs pente spectrale small‑λ, choix de λ_max, etc.).

---

## 3. Inspection des K bootstraps les plus discordants (top‑K)

### 3.1 Sélection des cas extrêmes

Une cellule (`topK_discrepancy_inspect`) :

- lit `paired_levina_spectral_theilsen_raw.csv` ;
- calcule l’écart absolu `|levina_mle − theilsen_d_s|` ;
- pour un λ_max donné (par défaut 0.2), sélectionne les **top‑K = 10** bootstraps avec l’écart le plus grand ;
- sauvegarde un résumé dans :
  - `results/topK_discrepancy_inspect/top_10_discrepancy_summary_lambda_0.2.csv` ;
  - `.../top_10_discrepancy_inspection_lambda_0.2.csv`.

Pour chaque b de ce top‑K, si possible, elle :

- régénère `X_sub`, calcule le spectre de Laplacien ;
- reconstruit N(λ) ;
- refait un fit Theil–Sen sur λ ≤ 0.2 ;
- calcule Cook’s distance approximative pour le fit OLS associé (diagnostic) ;
- produit :
  - `b_XXX_lambda_0.2_counting.csv` ;
  - `b_XXX_lambda_0.2_spectral_diagnostic.png` (N(λ) + droite TS + annotation des points influents).

### 3.2 Observations dégagées

La cellule de synthèse note :

- pour ces 10 bootstraps, Theil–Sen donne des pentes ≈ 0.69–0.76 → d_s ≈ 1.38–1.52 ;
- Levina m_hat ≈ 8.0 pour les mêmes b ;
- la différence Levina − d_s ≈ 6.5 est quasi constante ;
- les graphes log‑log N(λ) montrent :
  - une plage globalement linéaire sur λ ≤ 0.2 ;
  - la droite Theil–Sen suit bien la tendance centrale ;
  - un point très à gauche (λ min) souvent marqué comme très influent dans les diagnostics OLS.

Conclusion : 

- ce n’est pas un "bug" sur quelques cas isolés, mais un **pattern structurel** ;
- l’écart entre Levina et d_s(Theil–Sen) persiste même pour les cas extrêmes analysés individuellement.

---

## 4. Effet d’exclure les plus petits λ sur d_s(Theil–Sen)

Les dernières cellules (partiellement tronquées dans l’aperçu) visent à explorer l’effet de :

- exclure les k plus petites valeurs propres (k = 0..3) de la plage de fit ;
- recalculer d_s(Theil–Sen) pour chaque bootstrap ;
- voir si l’on peut rapprocher les estimations spectrales de l’estimation Levina ou, au moins, stabiliser d_s autour d’une valeur choisie.

Même si les détails numériques ne sont pas intégralement visibles, l’intention est claire :

- tester si les **très petites valeurs propres** (λ extrêmes) sont responsables d’une sous‑estimation systématique de la pente ;
- vérifier le compromis entre **robustesse** (exclure des points) et **fidélité** à la structure small‑λ.

---

## 5. Rôle de la Partie 9 dans le pipeline Sunspots V0.5

La Partie 9 :

- montre que, même avec un estimateur robuste Theil–Sen et des diagnostics raffinés, les dimensions spectrales et Levina–Bickel restent **profondément différentes** en échelle ;
- confirme que cette différence n’est pas due à quelques outliers, mais à la **définition même** de ce que mesure la pente log‑log N(λ) sur small‑λ ;
- propose une inspection fine des cas les plus extrêmes et de l’effet d’exclure des λ très petits ;
- renforce l’idée que, dans ce pipeline :
  - **le signe** de T_log(n,d_est) (Divergence) est fiable, car toutes les définitions raisonnables de d_est restent < 4 ;
  - mais la **valeur numérique précise** de d_est et de T_log doit être lue comme **dépendante de la convention** (Levina vs spectral, OLS vs Theil–Sen, plage λ, gestion des influents).

En ce sens, la Partie 9 sert de **"zoom méthodologique"** : elle explicite, avec des chiffres, des tests et des figures, les limites de comparabilité entre différents estimateurs de dimension appliqués au même signal Sunspots, plutôt que de trancher en faveur d’un seul. Cela prépare un rapport global Sunspots V0.5 où l’on pourra choisir et justifier la définition de dimension à retenir pour l’interprétation physique de T_log.

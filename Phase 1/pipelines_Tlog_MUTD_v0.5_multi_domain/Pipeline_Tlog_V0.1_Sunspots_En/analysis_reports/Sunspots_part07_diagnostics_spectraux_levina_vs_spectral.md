# Sunspots V0.5 – Partie 7 (cellules 60–69) : Diagnostics spectraux avancés et comparaison Levina–Bickel vs pente spectrale

## 1. Périmètre de la partie

Cette septième partie correspond aux cellules **60–69** du notebook `Sunspots_part07.ipynb` (split 10 cellules) dérivé de `Pipeline_Tlog_V0.1_Sunspots_En.ipynb`.

Elle approfondit la question de la **cohérence et de la robustesse** des estimateurs de dimension utilisés pour Sunspots :

- diagnostics spectraux détaillés sur des sous‑échantillons (log‑log N(λ) avec plusieurs λ_max) ;
- étude de la sensibilité de la pente spectrale à la plage de fit λ_max ;
- comparaison **appariée** entre la dimension intrinsèque Levina–Bickel (MLE) et la dimension spectrale d_s ;
- conclusion sur ce que ces divergences signifient pour T_log.

---

## 2. Diagnostics spectraux sur sous‑échantillons (20 diagnostics)

### 2.1 Méthode

Une première cellule construit un ensemble de **diagnostics spectraux** :

- paramètres :
  - `embedding_dim = 10`, `tau = 1` ;
  - `k_neighbors = 10` ;
  - `n_eig = 200` (petites valeurs propres du Laplacien normalisé) ;
  - `subsample_frac = 0.6` ;
  - `n_diagnostics = 20` (20 sous‑échantillons bootstrap) ;
  - liste de λ max pour visualisation : `lambda_max_list = [0.1, 0.2, 0.4]` ;
  - `lambda_max_fit = 0.2` utilisé pour le fit numérique rapporté ;
  - `min_points_for_fit = 6`.

Pour chaque diagnostic i=1..20 :

1. tirage déterministe d’un sous‑ensemble de nœuds (`rng_seed = 42`) ;
2. construction d’un graphe k‑NN et calcul des 200 plus petites valeurs propres du Laplacien ;
3. **spectral counting** : N(λ) = # {eig ≤ λ} ;
4. sauvegarde des eigenvalues (`diag_i_eigvals.csv`) et de N(λ) (`diag_i_counting.csv`) ;
5. fit log‑log sur λ ≤ 0.2 pour estimer la pente et d_s = 2·slope ;
6. en plus, visualisation log‑log de N(λ) avec des fits de pente séparés pour les trois λ_max de la liste, et sauvegarde de `diag_i_loglog.png`.

Un résumé global est écrit dans :

- `results/spectral_diagnostics/spectral_diagnostics_summary.csv`.

### 2.2 Résultats

Les logs indiquent que, pour les 20 diagnostics :

- nombre d’eigenvalues calculés = 200 pour chaque sous‑échantillon ;
- nombre de points de fit (λ ≤ 0.2) ≈ 16–18 ;
- `fit_ok=True` pour tous les diagnostics.

Une cellule de texte résume :

- les slopes small‑λ sont **stables** sur les 20 sous‑échantillons :
  - `slope ≈ 0.14–0.15` ⇒ `d_s ≈ 0.28–0.31` ;
- ce résultat est cohérent avec les estimations initiales (d_s ~ 0.22–0.30) ;
- le fit se fait sur une plage de λ assez courte (≈ 16–18 points), mais les pentes restent remarquablement proches d’un diagnostic à l’autre.

Parallèlement, l’estimateur **Levina–Bickel MLE** (vu en Partie 6) donnait une dimension intrinsèque locale ≈ **7.9** (IC [7.84, 8.03]) sur les mêmes embeddings.

## 3. Sensibilité de la pente spectrale à la plage λ_max

### 3.1 Sweep λ_max

Une cellule suivante balaye plusieurs valeurs de `lambda_max` pour voir comment la pente spectrale (et donc d_s=2·slope) varie avec la plage de fit :

- `lambda_max_grid = [0.05, 0.1, 0.2, 0.4, 0.8]` ;
- `min_points_for_fit = 4` (pour pouvoir estimer la pente même avec peu de points).

Pour chaque diagnostic (les mêmes 20 sous‑échantillons que précédemment) et chaque λ_max de la grille :

1. on calcule N(λ) ;
2. on retient les points λ ≤ λ_max ;
3. si le nombre de points ≥ 4, on ajuste une pente log‑log ;
4. on stocke slope et d_s = 2·slope dans `lambda_max_sweep_summary.csv` ;
5. on agrège ensuite par λ_max pour obtenir médiane, IQR, etc., dans `lambda_max_sweep_aggregate.csv` ;
6. une figure `lambda_max_sensitivity_plot.png` représente médiane d_s vs λ_max (avec un ruban d’IQR).

### 3.2 Constats

Une cellule d’analyse résume en 5 lignes :

- Pour **λ_max croissant**, la pente augmente :
  - λ_max=0.05 → médiane d_s ≈ 0.16 ;
  - λ_max=0.1 → ≈ 0.21 ;
  - λ_max=0.2 → ≈ 0.30 ;
  - λ_max=0.4 → ≈ 0.51 ;
  - λ_max=0.8 → ≈ 0.87.

- Sur la plage **small‑λ (λ≤0.2)**, les pentes sur les diagnostics sont stables, avec d_s ≈ 0.28–0.32.

- Levina–Bickel continue de donner une intrinsic dim ≈ 7.9 sur les mêmes embeddings.

Interprétation :

- la **dimension spectrale** est très sensible au choix de λ_max (plus on élargit la plage, plus la pente augmente) ;
- sur small‑λ, le spectre a une **pente très faible** (quasi plate) → d_s spectrale ≪ dimension intrinsèque locale ;
- les deux estimateurs (spectral vs Levina–Bickel) se focalisent sur des propriétés différentes du graphe/signal.

---

## 4. Comparaison appariée Levina–Bickel vs pente spectrale

### 4.1 Set‑up

Une cellule "Paired comparison" cherche à comparer, **pour les mêmes sous‑échantillons bootstrap**, l’estimation de dimension :

- côté **Levina–Bickel** : `levina_bickel_boot_samples.csv` (colonnes `b`, `levina_mle`, `n_nodes_sub`) ;
- côté **spectral** : on re‑calcule les valeurs propres et N(λ) sur les mêmes indices de bootstrap et on ajuste une pente pour plusieurs λ_max (`[0.1, 0.2, 0.4]`).

Pour chaque bootstrap `b` et chaque λ_max :

- on stocke `levina_mle` et `d_s_spectral` ;
- on produit :
  - `paired_levina_spectral_raw.csv` (détails par b, λ_max) ;
  - `paired_levina_spectral_summary.csv` (médianes et différences) ;
  - des scatter plots Levina vs d_s (`paired_scatter_lambda_*.png`) ;
  - un boxplot des différences Levina−d_s (`paired_diff_boxplot.png`).

### 4.2 Résultats principaux

Les logs montrent que :

- Levina–Bickel MLE :
  - médiane ≈ 7.94 (CI ~[7.84, 8.03]) ;
- d_s spectrale (medians) :
  - λ_max=0.1 → d_s ≈ 0.21 ;
  - λ_max=0.2 → d_s ≈ 0.30 ;
  - λ_max=0.4 → d_s ≈ 0.52.

Les médianes des différences (Levina − spectral) sont typiquement :

- ≈ 7.7 (pour λ_max=0.1) ;
- ≈ 7.6 (pour λ_max=0.2) ;
- ≈ 7.4 (pour λ_max=0.4).

Les scatter plots montrent un nuage de points plutôt "droite‑bas" :

- Levina élevé (~8) ;
- spectral d_s très bas (<1) ;
- très peu de points proches de la diagonale (identité).

### 4.3 Interprétation

Une cellule de texte conclut :

- les estimations *appairées* confirment que **Levina–Bickel et la pente spectrale ne mesurent pas la même chose** :
  - LB capte une dimension de voisinage local dans un embedding de dimension 10, d’où m_hat ≈ 8 ;
  - la pente spectrale small‑λ capture un comportement de type scaling très local dans la queue du spectre (quasi plat), donnant d_s ≪ 1.

- la différence d’échelle est largement due à :
  - la **sensibilité à λ_max** (valeure plus grandes de λ → pentes plus élevées) ;
  - le fait que les petites valeurs propres choisies pour le fit sont très proches, conduisant à une pente quasi nulle.

Conséquence pratique :

- le **signe** de T_log (négatif) reste robuste, car même avec d_s modestement augmentée (via λ_max) on a d_s < 4 → T_log < 0 ;
- la **valeur absolue** de d_s et de T_log dépend fortement de la définition de la dimension (spectrale vs Levina–Bickel) et du choix de λ_max ;
- il faut donc **documenter explicitement** la convention adoptée quand on rapporte d_s/T_log.

---

## 5. Rôle de la Partie 7 dans le pipeline Sunspots V0.5

Cette septième partie :

- vérifie de manière détaillée que l’estimation de d_s par spectral counting est **cohérente** à travers des sous‑échantillons bootstrap et des λ_max small‑λ, tout en montrant sa dépendance à la plage de fit ;
- démontre la **discordance systématique** entre d_s spectral (≪1) et la dimension intrinsèque Levina–Bickel (~8), via des comparaisons appariées ;
- clarifie que ces deux estimateurs s’intéressent à des propriétés différentes du signal / graphe ;
- renforce l’idée que, pour Sunspots V0.5, **le régime T_log<0 (Divergence) est stable**, mais que **l’échelle numérique précise** de d_s et T_log doit être interprétée avec prudence et en fonction de la définition choisie.

En pratique, cette partie ferme le bloc "diagnostics de dimension" et prépare une phase plus narrative/synthétique (ou comparative avec d’autres pipelines) où l’on pourra expliquer clairement quelles conventions de dimension et de T_log sont retenues pour le cas des taches solaires.

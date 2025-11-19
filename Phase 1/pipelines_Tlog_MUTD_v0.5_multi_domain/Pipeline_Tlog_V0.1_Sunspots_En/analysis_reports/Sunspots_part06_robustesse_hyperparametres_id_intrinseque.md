# Sunspots V0.5 – Partie 6 (cellules 50–59) : Robustesse aux hyperparamètres et dimension intrinsèque Levina–Bickel

## 1. Périmètre de la partie

Cette sixième partie correspond aux cellules **50–59** du notebook `Sunspots_part06.ipynb` (split 10 cellules) dérivé de `Pipeline_Tlog_V0.1_Sunspots_En.ipynb`.

Elle traite de la **robustesse** de l’estimation de dimension (et donc de T_log) par rapport à :

- les hyperparamètres de construction du graphe (embedding_dim, k_neighbors) ;
- le choix de la méthode d’estimation (dimension spectrale d_s vs dimension intrinsèque Levina–Bickel).

Elle contient trois volets :

1. un **sweep de sensibilité** embedding_dim × k_neighbors (diagnostic rapide, sans bootstrap complet) ;
2. un **bootstrap sur 4 configurations représentatives** (A–D) pour d_s et T_log ;
3. un **bootstrap Levina–Bickel** (MLE dimension intrinsèque) et un overlay avec d_s spectral.

---

## 2. Sensibilité de d_s à (embedding_dim, k_neighbors)

### 2.1 Méthode (sensitivity sweep)

Une première cellule (`todo_sensitivity_sweep.txt` + code) explore une grille d’hyperparamètres :

- `embedding_dims = [4, 6, 8, 10, 12]` ;
- `k_list = [4, 6, 8, 10, 12]` ;
- `tau = 1`, `n_eig = 150`, `lambda_max = 0.2`, `min_points_for_fit = 6`.

Pour chaque couple (`emb`, `k`) :

1. on construit un **embedding de Takens** dim `emb` (si la série est assez longue) ;
2. on construit un graphe **k‑NN** sur les premiers `min(1500, n_nodes)` points de l’embedding ;
3. on calcule le Laplacien normalisé et les `n_eig` plus petites valeurs propres ;
4. on estime d_s par **spectral counting** sur λ ≤ 0.2 (comme dans les parties précédentes).

Les résultats sont sauvegardés dans :

- `results/sensitivity_embedding_k.csv` (colonnes `embedding_dim, k, d_s, note`) ;
- `results/sensitivity_embedding_k_heatmap.png` (heatmap d_s en fonction de emb et k).

### 2.2 Résultats principaux (exemples)

Parmi les d_s imprimés :

- emb=4 :
  - k=4 → d_s ≈ 2.16 ; k=6 → 1.94 ; k=8 → 1.74 ; k=10 → 0.40 ; k=12 → 1.51 ;
- emb=6 :
  - k=4 → 2.05 ; k=6 → 1.65 ; k=8 → 1.44 ; k=10 → 0.30 ; k=12 → 0.23 ;
- emb=8 :
  - k=4 → 1.87 ; k=6 → 1.45 ; k=8 → 1.32 ; k=10 → 0.28 ; k=12 → 1.21 ;
- emb=10 :
  - k=4 → 1.66 ; k=6 → 1.38 ; k=8 → 1.32 ; k=10 → 0.27 ; k=12 → 1.25 ;
- emb=12 :
  - k=4 → 1.54 ; k=6 → 1.40 ; k=8 → 1.36 ; k=10 → 0.28 ; k=12 → 1.32.

### 2.3 Interprétation rapide

Une cellule d’analyse textuelle souligne :

- la **forte dépendance** de d_s aux hyperparamètres :
  - certaines combinaisons (notamment `k=10` pour plusieurs embedding_dim) produisent des d_s très faibles (~0.25–0.4) ;
  - d’autres (par ex. emb ∈ {6,8,10,12}, k ∈ {4,6,8}) donnent des d_s plus stables (≈ 1.3–1.6).

Objectif : choisir quelques configurations représentatives pour un **bootstrap contrôlé**, afin de voir comment d_s et T_log se comportent réellement (distribution, IC) au-delà de ce diagnostic ponctuel.

---

## 3. Bootstrap sur 4 configurations représentatives (A–D)

### 3.1 Choix des configurations

Une cellule (`todo_robust_grid` + code) définit 4 configurations :

- **Config A (référence)** : `A_ref_10_10` → `embedding_dim=10`, `k=10` ;
- **Config B** : `B_10_8` → `embedding_dim=10`, `k=8` ;
- **Config C** : `C_8_6` → `embedding_dim=8`, `k=6` ;
- **Config D** : `D_6_4` → `embedding_dim=6`, `k=4`.

La logique :

- A_ref reproduit la configuration initiale qui donnait d_s très bas (~0.22–0.30) ;
- B–D explorent la “zone plus stable” identifiée par la heatmap (d_s ≈ 1.3–2.0).

### 3.2 Paramètres bootstrap

- `n_boot = 120` itérations par configuration ;
- `subsample_frac = 0.6` (60 % des nœuds par bootstrap) ;
- `n_eig = 150`, `lambda_max = 0.2`, `min_points_for_fit = 6` ;
- même série Sunspots, même embedding de Takens (dim selon config), même graphe k‑NN, même méthode d_s.

Pour chaque config :

1. construire l’embedding complet `X_full` ;
2. pour b=1..n_boot :
   - sous‑échantillonner des nœuds pour obtenir `X_sub` ;
   - calculer Laplacien, valeurs propres, d_s ;
3. stocker les échantillons `d_s` ;
4. propager vers T_log :

\[
T_{\log}(n,d_s) = (d_s - 4) \ln(n), \quad n = 3265.
\]

Les fichiers produits par config :

- `results/robust_grid_{name}_samples.csv` (colonnes `d_s`, `T_log`) ;
- `results/robust_grid_{name}_ds_hist.png` ;
- `results/robust_grid_{name}_Tlog_hist.png` ;
- résumé global : `results/robust_grid_summary.csv`.

### 3.3 Résultats principaux

La cellule d’interprétation résume (médianes) :

- **Config A_ref_10_10**
  - d_s_median ≈ 0.297 ;
  - T_log_median ≈ −29.96.

- **Config B_10_8**
  - d_s_median ≈ 1.475 ;
  - T_log_median ≈ −20.43.

- **Config C_8_6**
  - d_s_median ≈ 1.662 ;
  - T_log_median ≈ −18.92.

- **Config D_6_4**
  - d_s_median ≈ 2.252 ;
  - T_log_median ≈ −14.14.

On retrouve la même relation analytique que précédemment : l’augmentation de d_s rapproche (d_s−4) de 0, donc T_log devient **moins négatif** (mais reste < 0).

### 3.4 Interprétation

- Pour les 4 configurations, **T_log reste négatif** : le **signe** (régime Divergence) est **robuste** sur cette grille ;
- En revanche, l’**amplitude** de T_log varie fortement (de ≈ −30 à ≈ −14) en fonction de (`embedding_dim`, `k`) :
  - la config A_ref (10,10) reproduit le résultat initial (d_s bas, T_log ≈ −30) ;
  - les configs B–D déplacent d_s vers 1.5–2.25 et atténuent la divergence (T_log ≈ −20 → −14).

Conclusion :

- la conclusion qualitative « régime Divergence » est **stable** ;
- la valeur numérique exacte de d_s et de T_log est **sensible aux hyperparamètres** d’embedding et de graphe.

---

## 4. Dimension intrinsèque Levina–Bickel (MLE) et comparaison avec d_s spectral

### 4.1 Objectif

La cellule `todo_levina_bickel_boot` propose d’introduire un second estimateur de dimension intrinsèque, **Levina–Bickel (MLE)**, pour :

- estimer la dimension intrinsèque sur des sous‑échantillons bootstrap de l’embedding de Takens ;
- comparer la distribution obtenue à la distribution de d_s spectral (`spectral_dimension_bootstrap.csv`).

### 4.2 Méthode Levina–Bickel

Paramètres :

- `embedding_dim = 10`, `tau = 1` (embedding de Takens comme pour d_s spectral) ;
- `k_neighbors_id = 20` (taille des voisinages locaux pour la MLE) ;
- `n_boot = 150` itérations ;
- `subsample_frac = 0.6` (fraction de nœuds conservés par bootstrap).

Pour chaque bootstrap :

1. on construit un sous‑ensemble `X_sub` de l’embedding ;
2. on construit un graphe k‑NN (k=20) sur `X_sub` ;
3. pour chaque point, on récupère les distances à ses k plus proches voisins (hors soi) ;
4. on applique la formule Levina–Bickel sur ces distances :

\[
 m_i = \left[ \frac{1}{k-1} \sum_{j=1}^{k-1} \log\frac{R_k}{R_j} \right]^{-1},
\]

   où `R_j` sont les distances aux voisins d’ordre j ;
5. on agrège les `m_i` (par exemple par la **médiane**) pour obtenir une estimation globale `m_hat` sur `X_sub` ;
6. on répète pour tous les bootstraps.

Les résultats sont sauvegardés dans :

- `results/levina_bickel_boot_samples.csv` (colonnes `b`, `n_nodes_sub`, `levina_mle`) ;
- `results/levina_bickel_boot_summary.csv` (médiane, moyenne, IC 95 %) ;
- `results/levina_bickel_boot_hist.png` (histogramme des m_hat).

### 4.3 Overlay Levina–Bickel vs d_s spectral

La cellule tente également de charger `results/spectral_dimension_bootstrap.csv` pour :

- superposer sur un même plot les distributions **Levina–Bickel** (intrinsic dim) et **spectral d_s** ;
- fichier overlay : `results/levina_bickel_boot_overlay_spectral.png` ;
- un CSV `levina_bickel_boot_overlay_samples.csv` permet d’analyser en détail les deux échantillons.

Les valeurs numériques exactes (médians, IC) ne sont pas visibles dans la sortie tronquée, mais la structure du code montre que l’objectif est de **valider ou nuancer** les estimations d_s obtenues par spectral counting en les confrontant à un estimateur statistique différent.

---

## 5. Rôle de la Partie 6 dans le pipeline Sunspots V0.5

Cette sixième partie :

- montre que la **classification qualitative** du régime (T_log<0 → Divergence) est **robuste** face à un ensemble raisonnable d’hyperparamètres (embedding_dim, k_neighbors) ;
- met en évidence que l’**amplitude de T_log** et la valeur précise de la dimension estimée **dépendent des choix de construction du graphe** ;
- introduit un **second estimateur** de dimension intrinsèque (Levina–Bickel) pour croiser les diagnostics 
  - d_s spectral vs d_id MLE ;
- prépare un travail plus systématique de **calibration d’hyperparamètres** et de **comparaison d’estimateurs** (spectral, Levina–Bickel, autres) pour ancrer solidement l’interprétation de T_log dans le cas Sunspots.

En résumé, la Partie 6 n’ajoute pas un nouveau verdict sur le régime (qui reste Divergence), mais elle documente la **sensibilité méthodologique** de d_s et T_log, et ouvre la voie à une étude plus fine de la dimension intrinsèque du signal.

# Sunspots V0.5 – Partie 4 (cellules 30–39) : Dimension spectrale, T_log effectif et probabilités de régime

## 1. Périmètre de la partie

Cette quatrième partie correspond aux cellules **30–39** du notebook `Sunspots_part04.ipynb` (split 10 cellules) dérivé de `Pipeline_Tlog_V0.1_Sunspots_En.ipynb`.

Elle intervient **après** :

- la construction du graphe temporel Sunspots (embedding de Takens + graphe k‑NN) ;
- le calcul du **Laplacien normalisé** et de ses premières valeurs propres (Partie 3).

Elle couvre :

- l’estimation d’une **dimension spectrale d_s** à partir du spectre de Laplacien (spectral counting) ;
- un **bootstrap de d_s** par sous‑échantillonnage de nœuds du graphe ;
- la propagation de la distribution de d_s vers une distribution de **T_log(n, d_est)** ;
- le calcul de **probabilités de régime** (Saturation / Équilibre / Divergence) basées sur cette dimension effective ;
- un constat final sur la nécessité de tester des null‑models.

---

## 2. Estimation initiale de la dimension spectrale d_s (spectral counting)

### 2.1 Méthode

À partir de `results/laplacian_eigenvalues.csv` (produit dans la Partie 3) :

- on lit les valeurs propres \(\lambda_i\) du Laplacien normalisé ;
- on trie les valeurs \(\lambda\) par ordre croissant et on filtre les **valeurs > eps** (pour éviter les zéros numériques) ;
- on construit le **compteur spectral** :

\[
N(\lambda) = \#\{\lambda_i \le \lambda\}.
\]

- on se restreint aux petites valeurs propres \(\lambda \le \lambda_{\max}\) avec `lambda_max = 0.1` ;
- on exige au moins `min_points_for_fit = 10` points dans cette plage pour ajuster un modèle ;
- on ajuste la loi de puissance en log‑log :

\[
\log N(\lambda) \approx \log C + (d_s/2) \log \lambda ;
\]

- une régression linéaire `stats.linregress(log_lambda, log_N)` donne :
  - la pente `slope ≈ d_s/2` ;
  - l’intercept, R, p‑value, etc.

Les résultats sont sauvegardés dans :

- `results/spectral_dimension_counting.csv` (table \(\lambda, N(\lambda), \log \lambda, \log N\)) ;
- `results/spectral_dimension_summary.csv` (slope, d_s_est, erreurs…) ;
- `results/spectral_dimension_fit.png` (plot log‑log avec la droite de fit).

### 2.2 Résultat obtenu

Résumé affiché :

- `lambda_max_for_fit = 0.1` ;
- `n_points_fit = 10` ;
- `slope ≈ 0.1184` ;
- `d_s_est = 2 * slope ≈ 0.2368` ;
- `stderr_slope ≈ 0.0263` → `d_s_se ≈ 0.0527` ;
- `R ≈ 0.846`, `p_value ≈ 0.0020`.

La **dimension spectrale initiale** est donc :

\[
 d_s \approx 0.24 \quad \text{avec erreur standard} \approx \pm 0.05.
\]

C’est une valeur très faible (bien < 1), plausible dans le cadre d’un graphe de similarité très comprimé, mais qui nécessite un test de **robustesse**.

---

## 3. Bootstrap de la dimension spectrale d_s par sous‑échantillonnage de nœuds

### 3.1 Objectif

La cellule `todo_cell_bootstrap_ds` pose l’objectif : obtenir une **distribution empirique** de d_s par bootstrap pour :

- estimer médiane, moyenne, écart‑type ;
- calculer un intervalle de confiance 95 % ;
- tester la robustesse de l’estimation par rapport au choix des nœuds utilisés dans le graphe.

### 3.2 Méthode

Paramètres principaux :

- `embedding_dim = 10`, `tau = 1`, `k_neighbors = 10`, `n_eig = 100` ;
- **bootstrap** :
  - `n_boot = 150` itérations ;
  - `subsample_frac = 0.8` : à chaque itération on retient 80 % des nœuds (sans remise) ;
  - `lambda_max = 0.1`, `min_points_for_fit = 8`.

Pour chaque bootstrap :

1. On sous‑échantillonne des nœuds du nuage `X_full` (embedding complet) ;
2. On reconstruit un graphe k‑NN sur ces points ;
3. On calcule le Laplacien normalisé local ;
4. On récupère jusqu’à `n_eig` plus petites valeurs propres ;
5. On applique la même procédure de **spectral counting** que plus haut (avec `lambda_max` et un minimum de points) ;
6. Si le fit est possible, on stocke `d_s`, la pente, R, le nombre de points, etc.

Les résultats sont enregistrés dans `results/spectral_dimension_bootstrap.csv` et visualisés via `results/spectral_dimension_bootstrap_hist.png`.

### 3.3 Résultats

- Nombre de réalisations valides : **150/150** ;
- statistiques sur d_s :
  - **médiane** ≈ 0.2223 ;
  - moyenne ≈ 0.2206 ;
  - écart‑type ≈ 0.0088 ;
  - **IC 95 %** ≈ [0.2007, 0.2325].

La distribution est donc :

- très **concentrée autour de ~0.22** ;
- avec une incertitude statistique faible (ordre 0.01–0.02 en largeur de bande).

Conclusion : la dimension spectrale estimée d_s ≈ 0.22 est **robuste** par rapport au sous‑échantillonnage des nœuds.

---

## 4. Propagation de d_s vers une distribution de T_log(n, d_est)

### 4.1 Objectif

La cellule `todo_Tlog_from_ds.txt` propose de **propager** la distribution bootstrap de d_s vers une distribution de T_log, en considérant que la dimension effective n’est plus 1 (choix naïf), mais ≈ d_s.

Paramètres :

- `n_value = 3265` (taille observée du dataset) ;
- `ds_boot_csv = 'results/spectral_dimension_bootstrap.csv'` ;
- `bias = 0.0` (aucun biais ajouté).

### 4.2 Calcul

On lit les échantillons `d_s` valides et on calcule pour chacun :

\[
T_{\log}(n,d_s) = (d_s - 4) \ln(n) + \text{bias}.
\]

On obtient une distribution de T_log (un échantillon par bootstrap) :

- les paires `(d_s, T_log)` sont sauvegardées dans `results/Tlog_from_ds_bootstrap.csv` ;
- un résumé statistique est sauvegardé dans `results/Tlog_from_ds_bootstrap_summary.csv` ;
- un histogramme `results/Tlog_from_ds_bootstrap_hist.png` illustre la distribution.

### 4.3 Résultats

Statistiques sur T_log :

- `Tlog_median ≈ -30.565` ;
- `Tlog_mean ≈ -30.579` ;
- `Tlog_std ≈ 0.071` ;
- IC 95 % ≈ **[-30.740, -30.483]** ;
- min ≈ -30.854, max ≈ -30.431.

La distribution est donc :

- **nettement décalée vers les valeurs négatives** ;
- avec une **faible dispersion** (~0.07) autour de ~−30.56.

Interprétation (cellule d’analyse textuelle) :

- d_s médiane ≈ 0.222 (IC 95 % ≈ [0.201, 0.233]) ;
- pour n=3265, cela donne une distribution de T_log concentrée autour de ≈ −30.56 ;
- T_log est très nettement < 0 pour tous les échantillons → **régime Divergence** quasi certain pour cette définition "dynamique" de la dimension (d_est ≈ 0.22).

---

## 5. Probabilités de régime (Saturation / Équilibre / Divergence)

### 5.1 Méthode

La cellule `todo_Tlog_regime_probabilities.txt` définit une procédure pour convertir les échantillons T_log en **probabilités de régime** :

- **Saturation** si `T_log > +tol_equilibrium` ;
- **Équilibre** si `|T_log| ≤ tol_equilibrium` ;
- **Divergence** si `T_log < −tol_equilibrium`.

Paramètres :

- `tlog_csv = 'results/Tlog_from_ds_bootstrap.csv'` ;
- `tol_equilibrium = 0.01` (tolérance étroite autour de 0) ;
- on calcule aussi la masse |T_log| ≤ 0.1 (`tol2`), à titre complémentaire.

Les résultats sont sauvegardés dans `results/Tlog_regime_probabilities.csv`.

### 5.2 Résultats

À partir de 150 échantillons T_log :

- `p_saturation = 0.0` ;
- `p_equilibrium = 0.0` ;
- `p_divergence = 1.0` (pour tolérance 0.01) ;
- `p_equilibrium_tol2 = 0.0` (aucun échantillon dans |T_log| ≤ 0.1) ;
- `Tlog_median ≈ -30.565`, `Tlog_mean ≈ -30.579`.

Constat :

- quelle que soit la tolérance raisonnable autour de 0 (0.01, 0.1), **100 %** des échantillons T_log se trouvent du côté négatif → régime **Divergence** avec probabilité ≈ 1.

---

## 6. Conclusion et lien vers les null‑models

La dernière cellule textuelle résume :

- `p(T_log < 0) = 1` pour la définition actuelle (d_est ≈ 0.22, n = 3265) ;
- la classification en régime Divergence est **sans ambiguïté** dans ce cadre ;
- prochaine étape naturelle : tester cette conclusion contre des **null‑models** (séries shuffle temporellement, surrogates de phase) pour voir si :
  - la dimension spectrale très faible ;
  - et la valeur très négative de T_log

sont de véritables signatures dynamiques, ou bien des conséquences triviales du prétraitement (embedding, kNN) ou de propriétés statistiques simples du signal.

Une cellule suivante (hors de cette partie) proposera justement un pipeline de null‑models (temporal shuffle, phase‑randomized) avec estimation de d_s et T_log pour chacun.

---

## 7. Rôle de la Partie 4 dans le pipeline Sunspots V0.5

Cette quatrième partie :

- fournit une **estimation robuste** de la **dimension spectrale d_s** du graphe Sunspots (d_s ≈ 0.22, IC 95 % ≈ [0.20, 0.23]) ;
- montre comment cette dimension effective peut être **propagée vers T_log** pour obtenir une distribution réaliste de T_log(n,d_est) ;
- établit que, pour la taille observée n=3265, le système Sunspots se situe avec probabilité ≈ 1 en régime de **Divergence** selon la métrique T_log ;
- prépare le terrain pour une comparaison avec des **null‑models**, essentielle pour interpréter physiquement (ou structurellement) cette divergence :
  - est‑elle liée à la dynamique propre des taches solaires ;
  - ou peut‑on retrouver des signatures similaires en détruisant partiellement les corrélations temporelles (shuffle) ou les phases (phase‑randomized) ?

En résumé, la Partie 4 connecte pour la première fois la **dimension effective d_s** issue du graphe à la tension combinatoire T_log, et fournit un diagnostic probabiliste de régime basé sur cette dimension estimée, plutôt que sur un choix ad hoc de d.

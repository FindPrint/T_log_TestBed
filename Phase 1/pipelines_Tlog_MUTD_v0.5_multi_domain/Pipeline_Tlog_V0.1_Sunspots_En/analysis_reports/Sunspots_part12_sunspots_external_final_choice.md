# Sunspots V0.5 – Partie 12 (cellules 110–fin) : Pipeline autonome `sunspots_external`, diagnostics et choix final de configuration

## 1. Périmètre de la partie

Cette douzième partie correspond aux cellules **110–fin** du notebook `Sunspots_part12.ipynb` (split 10 cellules) dérivé de `Pipeline_Tlog_V0.1_Sunspots_En.ipynb`.

Elle met en place un **pipeline autonome compact** qui :

- télécharge les données Sunspots directement depuis Kaggle (optionnel) ;
- applique l’embedding de Takens, construit le graphe k-NN, le Laplacien normalisé et son spectre ;
- estime une **dimension spectrale d_s via Theil–Sen** sur N(λ) vs λ ≤ λ_max ;
- effectue un **bootstrap d_s** à partir du spectre de Laplacien ;
- propage vers **T_log(n, d_s)** pour n = 3265 (taille de la série) ;
- effectue un **null-model rapide** (temporal shuffle) pour comparer ;
- produit des **diagnostics détaillés** (figures, CSV) sur la distribution de d_s et T_log ;
- explore une petite **grille de paramètres** (λ_max, exclusion des plus petits λ) ;
- fixe une **configuration finale** (lambda_max, exclude_k) et consigne cette décision dans un fichier prêt pour commit.

---

## 2. Pipeline autonome `sunspots_external` : Kaggle → Laplacien → d_s → T_log

### 2.1 Chargement des données depuis Kaggle

La cellule principale commence par configurer :

- `use_kaggle = True` ;
- `kaggle_dataset = "robervalt/sunspots"` ;
- `download_path = data/sunspots_kaggle`, `extract_dir = data/sunspots_kaggle/extracted` ;
- `results_dir = results/sunspots_external` (créé si besoin).

Elle inclut un helper `kaggle_download` qui :

- lit `kaggle.json` (dans `~/.kaggle/` ou le répertoire courant) ;
- authentifie via `kaggle.api` ;
- télécharge l’archive ZIP Sunspots, puis l’extrait dans `extract_dir` ;
- sélectionne un CSV contenant "sun" dans le nom, typiquement `Sunspots.csv`.

Le script charge ensuite la série temporelle :

- détecte une colonne candidate contenant "sun" (ici `Monthly Mean Total Sunspot Number`) ;
- convertit en numérique, `dropna()` ;
- obtient `series` de taille `n_system = 3265`.

### 2.2 Embedding de Takens et graphe k-NN

Paramètres d’embedding et de graphe :

- `embedding_dim = 10`, `tau = 1` ;
- `k_neighbors = 10`.

Fonction `takens_embed` :

- construit Y ∈ R^{L×m} avec

\[
L = N - (m-1)τ
\]

- ici `X` a la forme `(3256, 10)`.

Construction du graphe :

- `kneighbors_graph(X, n_neighbors=k_neighbors, mode="connectivity", include_self=False)` ;
- symétrisation `A = 0.5 (A + A^T)` puis binarisation ;
- `A` est un graphe k-NN symétrique non pondéré, sparse CSR.

### 2.3 Laplacien normalisé et spectre

- calcul du degré `deg = A.sum(axis=1)` (avec correction pour les nœuds isolés) ;
- matrice de normalisation `D_inv_sqrt = diag(1/√deg)` ;
- Laplacien normalisé :

\[
L = I - D^{-1/2} A D^{-1/2}
\]

- calcul des `k_eig = min(n_eig, N-2)` plus petites valeurs propres (ici `n_eig = 200`, donc 200 petites λ) via `eigsh` ;
- tri des λ (réels, positifs) et sauvegarde dans :

  - `results/sunspots_external/laplacian_eigenvalues.csv`.

### 2.4 Estimation ponctuelle de d_s par Theil–Sen

À partir des valeurs propres positives `lam` et du comptage cumulé `Nlam = 1..len(lam)` :

- sélection des points avec `lambda <= lambda_max` (ici `lambda_max = 0.2`, `n_points = 19`) ;
- fit Theil–Sen sur `log N` vs `log λ` :

\[
\log N(λ) \approx a + s \log λ, \quad d_s = 2s.
\]

Résultat :

- `d_s_point ≈ 1.9995` (avec 19 points small‑λ).

### 2.5 Bootstrap de d_s à partir du spectre

La cellule ne rebâtit pas le graphe à chaque bootstrap, mais **resample les eigenvalues** :

- `n_boot = 200` ;
- à chaque itération, tirage avec remise sur les indices des λ (taille ~80 % des λ), tri, recalcul d_s avec la même méthode (Theil–Sen sur `λ <= λ_max`) ;
- d_s valides (au moins 3 points small‑λ) sont conservés.

Résultats :

- 200 échantillons d_s retenus (aucun rejet) ;
- médiane d_s_boot ≈ **2.05** ;
- intervalle 95 % ≈ [**1.07**, **4.42**].

### 2.6 Propagation vers T_log et fichiers générés

Pour chaque d_s bootstrapé, on calcule :

\[
T_{\log} = (d_s - 4) \ln(n_{system}), \quad n_{system} = 3265.
\]

- médiane T_log ≈ **−15.77** ;
- intervalle 95 % ≈ [**−23.68**, **+3.42**].

Fichiers produits :

- `results/sunspots_external/external_Tlog_summary.csv` (n_system, d_s_point, d_s_boot_median, quantiles, T_log median et quantiles) ;
- `results/sunspots_external/external_ds_boot.csv` (d_s bootstrap) ;
- `results/sunspots_external/external_Tlog_boot.csv` (T_log bootstrap) ;
- `results/sunspots_external/external_Tlog_hist.png` (histogramme T_log bootstrap).

### 2.7 Null-model rapide (temporal shuffle)

Optionnellement, la cellule :

- mélange la série temporelle (shuffle) ;
- refait embedding, graphe, Laplacien, petits eigenvalues ;
- estime un d_s_null avec la même fonction `estimate_ds_from_eigs`.

Observation :

- d_s_null ≈ **15.0** (très élevé), indiquant une structure spectrale radicalement différente pour le shuffle.

Interprétation :

- ce null est utile comme test directionnel, mais un seul run ne suffit pas ;
- il souligne que le shuffle casse la structure du signal et produit un spectre très différent ;
- pour une comparaison rigoureuse, il faudrait plusieurs nulls traités exactement comme la série observée.

---

## 3. Cellule de diagnostics détaillés pour `sunspots_external`

Une seconde cellule construit des diagnostics à partir des fichiers précédents :

- lecture de `laplacian_eigenvalues.csv` et `external_ds_boot.csv` ;
- création d’un dossier `results/sunspots_external/diagnostics`.

Diagnostics produits :

1. **Spectre index–λ** :
   - figure `spectrum_index_lambda.png` (index vs λ, échelle log) ;
2. **N(λ) log‑log + fit Theil–Sen** :
   - figure `Nlambda_loglog_fit.png` : N(λ) log‑log, droite TS sur λ ≤ 0.2, vertical λ_max ;
3. **Histogramme de d_s bootstrap** :
   - `ds_boot_hist.png` : distribution de d_s, médiane, quantiles 2.5 % et 97.5 %, surlignage des outliers (d_s < 0.5 ou d_s > 4) ;
   - CSV `ds_boot_top_high.csv` listant les d_s les plus élevés (queue droite) ;
4. **Résumé CSV** :
   - `diagnostic_summary.csv` récapitule : n_lambda_total, n_points_fit_used, d_s_point, d_s_boot_median, quantiles, n_boot_retained.

La cellule imprime également des **recommandations opérationnelles** :

- vérifier visuellement l’alignement du fit small‑λ ;
- inspecter les outliers d_s très élevés dans `ds_boot_top_high.csv` ;
- envisager la réduction de λ_max (p. ex. 0.1) ou l’exclusion de certains petits λ ;
- répéter le null-model avec plusieurs runs identiques.

---

## 4. Grille (λ_max, exclusion des k plus petits λ) et stabilité de d_s / T_log

Une cellule suivante explore une petite **grille de robustesse** :

- λ_max ∈ {0.1, 0.2} ;
- exclusion des k plus petits eigenvalues avec k ∈ {0, 1, 2, 3}.

Pour chaque combo (λ_max, k) :

- on enlève k plus petits λ ;
- on ajuste Theil–Sen sur N(λ) log‑log restreint à λ ≤ λ_max ;
- on calcule :
  - d_s ;
  - `n_points_used` ;
  - `T_log = (d_s − 4) ln(3265)` ;
  - un drapeau `note` si d_s > 4 (high_ds_outlier) ou d_s < 0.5.

Les résultats sont sauvegardés dans :

- `results/sunspots_external/robust_grid_lambda_exclude_summary.csv`.

Tableau synthétique (extraits) :

- λ_max=0.1 :
  - k=0 : d_s≈1.44, T_log≈−20.70 (9 points) ;
  - k=1 : d_s≈1.98, T_log≈−16.37 (8 points) ;
  - k=2 : d_s≈2.82, T_log≈−9.54 (7 points) ;
  - k=3 : d_s≈4.08, T_log≈+0.67 (**outlier**, très peu de points) ;
- λ_max=0.2 :
  - k=0 : d_s≈2.00, T_log≈−16.19 (19 points) ;
  - k=1 : d_s≈2.30, T_log≈−13.72 (18 points) ;
  - k=2 : d_s≈2.76, T_log≈−9.99 (17 points) ;
  - k=3 : d_s≈3.24, T_log≈−6.18 (16 points).

Interprétation :

- plus on exclut de petits λ, plus d_s augmente et T_log se rapproche de 0 voire devient positif ;
- mais ces cas utilisent de moins en moins de points et sont plus instables ;
- les configurations avec **n_points_used élevé** sont plus fiables ;
- λ_max=0.2, k=0 offre un bon compromis (19 points, d_s≈2, T_log≈−16.2).

---

## 5. Choix final de configuration et artefacts prêt‑à‑committer

La dernière cellule fixe la configuration :

- `lambda_max = 0.2`, `exclude_k = 0` ;
- reprend les eigenvalues, refait le fit Theil–Sen sur λ ≤ 0.2 ;
- obtient :
  - `d_s ≈ 1.9995`,
  - `T_log ≈ −16.186`,
  - `n_points_used = 19`.

Artifacts écrits :

- `results/sunspots_external/final_choice_summary.csv` (timestamp, λ_max, exclude_k, n_lambda_total, n_points_used, slope, d_s, T_log) ;
- `results/sunspots_external/diagnostics/Nlambda_loglog_fit_final.png` (N(λ) log‑log + fit final annoté) ;
- append dans `results/ds_remove_small_lambda/run_ready_for_commit.txt` une ligne :

  - timestamp UTC,
  - λ_max, exclude_k,
  - d_s, T_log,
  - n_points_used.

Cette note sert de **trace textuelle** pour valider la configuration retenue lors d’un commit Git.

Conclusion quantitative pour `sunspots_external` (configuration finale) :

- `d_s ≈ 2.0`,
- `T_log(n=3265, d_s≈2.0) ≈ −16` (nettement négatif).

---

## 6. Rôle de la Partie 12 dans le pipeline Sunspots V0.5

La Partie 12 fournit un **pipeline condensé et autonome** pour Sunspots, adapté à des tests rapides ou des reproductions externes :

- elle re‑implémente toute la chaîne (Kaggle → embedding → graphe → Laplacien → d_s → T_log) dans une seule cellule exécutable ;
- elle ajoute une couche de **diagnostics graphiques** et de **tests de robustesse** (grille λ_max / exclude_k) ;
- elle force un **choix final explicite** des hyperparamètres spectrales (λ_max, exclusion de petits λ), avec artefacts prêts à être commités.

Sur le plan scientifique :

- elle confirme, de façon indépendante, que pour Sunspots et les paramètres retenus, la dimension spectrale effective est ≈ 2, donc d_s < 4 ;
- par conséquent, **T_log(n, d_s) est nettement négatif** pour n=3265, ce qui place le système dans le régime de **Divergence** ;
- elle montre cependant que des choix différents de λ_max ou d’exclusion de λ peuvent déplacer d_s et T_log, d’où l’importance de documenter la configuration choisie.

Ainsi, cette dernière partie clôt le pipeline Sunspots V0.5 en fournissant à la fois :

- une **implémentation compacte** pour reproductibilité externe ;
- et un **ancrage décisionnel** (paramètres spectrals et T_log final) pour les analyses de divergence basées sur ce jeu de données.

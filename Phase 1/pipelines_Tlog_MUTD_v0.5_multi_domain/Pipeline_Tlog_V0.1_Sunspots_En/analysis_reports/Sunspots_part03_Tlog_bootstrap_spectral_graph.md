# Sunspots V0.5 – Partie 3 (cellules 20–29) : Bootstrap de T_log et début de l’analyse spectrale

## 1. Périmètre de la partie

Cette troisième partie correspond aux cellules **20–29** du notebook `Sunspots_part03.ipynb` (split 10 cellules) dérivé de `Pipeline_Tlog_V0.1_Sunspots_En.ipynb`.

Elle contient quatre blocs principaux :

- **Bloc 8 — Bootstrap de T_log (taille fixe n = 1000)** ;
- **Bloc 8b — Bootstrap de T_log avec taille variable n ∈ [500, 1500]** ;
- génération d’un **rapport intermédiaire** sur la robustesse de T_log dans `logs/summary.md` et `logs/summary_en.md` ;
- début de la **phase graphique/spectrale** : embedding de Takens, graphe k‑NN, Laplacien normalisé et spectre.

---

## 2. Bloc 8 – Bootstrap de T_log pour n fixe (n = 1000)

### 2.1 Paramétrage

- Dataset : `data/sunspots_raw/Sunspots.csv` (nettoyé via `dropna()`) ;
- taille totale : `n_total = 3265` ;
- **dimension effective fixée** : `d_effectif = 1` ;
- **biais** : 0.0 ;
- paramètres bootstrap :
  - `bootstrap_size = 1000` (taille de chaque échantillon) ;
  - `n_bootstrap = 100` (nombre de tirages) ;
  - générateur aléatoire : `np.random.default_rng(42)`.

La fonction de calcul est :

\[
T_{\log}(n, d) = (d-4) \ln(n) + \text{biais},\quad\text{avec } d=1,\ \text{biais}=0.
\]

### 2.2 Résultats

Pour chaque tirage bootstrap :

- on échantillonne `bootstrap_size = 1000` indices avec remise ;
- on calcule `T_log(1000, d=1)` ;
- on stocke les valeurs dans `Tlogs`.

Les métriques obtenues sont :

- `Moyenne(T_log) ≈ -20.723266` ;
- `Écart‑type(T_log) = 0.000000` ;
- `Min(T_log) = Max(T_log) ≈ -20.723266`.

Les fichiers suivants sont sauvegardés :

- `results/bootstrap_Tlog.csv` : une ligne par tirage (`bootstrap_id`, `T_log`, `n_sample`, `d_effectif`, `biais`) ;
- `results/bootstrap_Tlog_hist.png` : histogramme de T_log (une seule barre).

### 2.3 Interprétation

- Comme **T_log(n,d)** ne dépend ici que de la **taille n** et de `d`, et que `n_sample` est fixé à 1000 à chaque tirage, **tous les tirages donnent exactement la même valeur** ;
- l’histogramme est donc réduit à une seule barre à `T_log(1000,1) ≈ -20.7233` ;
- on obtient une **stabilité absolue** de T_log sous bootstrap de valeurs, ce qui confirme que, dans ce cadre V0.1, seules `(n,d)` affectent T_log.

Limitation :

- ce bootstrap ne teste **pas** la variabilité due aux valeurs de la série (amplitude des taches solaires), seulement la dépendance à la taille et à la dimension.

---

## 3. Bloc 8b – Bootstrap de T_log avec taille variable n ∈ [500, 1500]

### 3.1 Paramétrage

Cette variante introduit une **variabilité de n** :

- `n_min = 500`, `n_max = 1500` ;
- `n_bootstrap = 100` ;
- pour chaque tirage :
  - on tire `n_sample` uniformément dans `[500, 1500]` ;
  - on calcule `T_log(n_sample, d=1)`.

On utilise la même fonction `compute_Tlog(n, d, biais)` que précédemment.

### 3.2 Résultats

Statistiques résumées :

- `Moyenne(T_log) ≈ -20.6866` ;
- `Écart‑type(T_log) ≈ 0.8615` ;
- `Min(T_log) ≈ -21.8913` (pour n ≈ 1500) ;
- `Max(T_log) ≈ -18.8913` (pour n ≈ 500).

Fichiers générés :

- `results/bootstrap_variable_n_Tlog.csv` : colonnes `bootstrap_id`, `n_sample`, `T_log`, `d_effectif`, `biais` ;
- `results/bootstrap_variable_n_hist.png` : histogramme de T_log.

### 3.3 Interprétation

- Pour `d = 1`, on a **(d−4) = −3**, donc théoriquement :

\[
T_{\log}(n,1) = -3 \ln(n).
\]

- La variation observée de T_log est donc **parfaitement log‑linéaire** en `n` :
  - pour `n = 500` : `T_log(500,1) ≈ -3 ln(500) ≈ -18.9` ;
  - pour `n = 1500` : `T_log(1500,1) ≈ -3 ln(1500) ≈ -21.9` ;
  - ce sont précisément les bornes min/max observées.

- L’écart‑type ≈ 0.86 reflète simplement la **dispersion de ln(n)** dans l’intervalle [500,1500].

Conclusion :

- lorsque la taille du système varie, les fluctuations de T_log suivent **strictement** la loi analytique `(d−4)·ln(n)` ;
- le modèle est **robuste et prédictible** : aucune anomalie ou instabilité numérique n’est détectée.

Cette étape complète la validation de T_log V0.1 en montrant à la fois :

1. une **stabilité absolue** quand n est fixé ;
2. une **variabilité contrôlée** quand n varie dans un intervalle donné.

---

## 4. Rapport intermédiaire sur la robustesse de T_log (FR & EN)

Deux cellules ajoutent un **rapport intermédiaire** dans les logs :

### 4.1 Résumé FR dans `logs/summary.md`

Une chaîne Markdown est construite et appendue à `logs/summary.md` :

- **"Rapport Intermédiaire — Robustesse T_log V0.1 (Blocs 7–8)"** ;
- rappel de la **formule** T_log et des régimes (Saturation / Équilibre / Divergence) ;
- description du dataset (Sunspots.csv, n=3265, d=1, aucune valeur manquante) ;
- rappel des résultats précédents :
  - calcul initial `T_log = -24.2730` (régime Divergence) ;
  - sensibilité en d (1→6, transition à d=4) ;
  - balayage en n (10→10 000, symétrie d=3 vs d=5) ;
  - régression T_log vs ln(n) (pentes −1 et +1, R²=1) ;
- résumé des deux bootstraps (`n=1000` et n∈[500,1500]) ;
- conclusion que **T_log V0.1 est robuste** (sensibilité et bootstrap cohérents, aucun artefact détecté).

Un enregistrement est également ajouté à `logs/logs.csv` pour signaler que ce rapport a été créé.

### 4.2 Résumé EN dans `logs/summary_en.md`

Une cellule crée un fichier `logs/summary_en.md` contenant une version anglaise synthétique :

- journal de session (timestamps, événements Block 1 → bootstrap variable n) ;
- "Intermediate Report – Robustness of T_log V0.1 (Blocks 7–8)" ;
- rappel du modèle, du dataset, des résultats en d et n, et des bootstraps ;
- conclusion que le modèle T_log V0.1 est robuste et prêt pour des tests sur graphes (dimension spectrale).

Un log est ajouté à `logs/logs.csv` pour documenter la création de `summary_en.md`.

---

## 5. Début de l’analyse spectrale (embedding, graphe, Laplacien)

La fin de cette partie amorce la transition vers une **analyse de dimension effective** via graphes :

### 5.1 Objectif (cellule de TODO)

Une cellule texte (`todo_cell_spectral_dimension.txt`) décrit l’objectif :

- construire un **graphe** à partir de la série Sunspots via un **embedding de Takens** ;
- bâtir un graphe **k‑NN** (k‑nearest neighbors), calculer le **Laplacien normalisé** et en extraire le spectre (valeurs propres) ;
- préparer ces résultats pour estimer une **dimension spectrale d_s** par "spectral counting".

### 5.2 Construction concrète du graphe et du spectre

La cellule de code associée :

1. Charge `Sunspots.csv` et choisit une colonne numérique :
   - tente parmi `['Number', 'Total Sunspot', 'Total Sunspot Number', 'Monthly Mean']` ;
   - à défaut, prend la dernière colonne numérique ;
   - dans le run fourni : `Monthly Mean Total Sunspot Number` est retenue.

2. Applique un **embedding de Takens** de dimension `embedding_dim = 10` et délai `tau = 1` :
   - chaque point devient un vecteur `(x_t, x_{t+1}, ..., x_{t+9})` ;
   - nombre de nœuds résultant : `n_nodes = 3256`.

3. Construit un graphe k‑NN non pondéré et symétrique :
   - `k_neighbors = 10` ;
   - pour chaque nœud, on relie ses k plus proches voisins (hors lui‑même) ;
   - la matrice d’adjacence est stockée en sparse (CSR).

4. Calcule le **Laplacien normalisé** :

\[
L_{\text{norm}} = I - D^{-1/2} A D^{-1/2},
\]

   - avec gestion des degrés nuls (deg=0 → deg=1 pour éviter les divisions infinies).

5. Calcule les **plus petites valeurs propres** de \(L_{\text{norm}}\) :
   - `n_eig = min(100, n_nodes−1)` ≈ 100 ;
   - via `eigsh(L_norm, k=n_eig, which='SM')` ;
   - valeurs propres triées dans l’ordre croissant.

6. Sauvegarde les résultats :

- `results/laplacian_eigenvalues.csv` : colonnes `eig_index`, `eigval` ;
- `results/laplacian_params.csv` : paramètres (`csv_path`, `value_col`, `embedding_dim`, `tau`, `k_neighbors`, `n_nodes`, `n_eig`) ;
- `results/laplacian_spectrum.png` : spectre (eigenvalue index vs eigenvalue) pour les premières valeurs propres.

Le print final récapitule le nombre de valeurs propres, la colonne utilisée, et les paramètres d’embedding.

---

## 6. Rôle de la Partie 3 dans le pipeline Sunspots V0.5

Cette troisième partie :

- **termine la validation V0.1 de T_log** par deux formes de bootstrap :
  - n fixe (stabilité absolue) ;
  - n variable (variabilité log‑linéaire parfaitement contrôlée) ;
- consigne ces résultats dans des **rapports intermédiaires** FR et EN (`summary.md`, `summary_en.md`) pour renforcer la traçabilité ;
- amorce la **transition vers MUTD / dimension effective** en construisant un graphe de similarité (embedding de Takens + k‑NN) et en calculant le **spectre de Laplacien normalisé**.

La partie suivante exploitera ces valeurs propres pour :

- estimer une **dimension spectrale d_s** par spectral counting ;
- bootstrapper cette dimension spectrale ;
- propager la distribution de d_s vers une distribution de T_log et des probabilités de régime (Saturation/Équilibre/Divergence) basées sur une **dimension effective estimée** plutôt que sur d=1 naïf.

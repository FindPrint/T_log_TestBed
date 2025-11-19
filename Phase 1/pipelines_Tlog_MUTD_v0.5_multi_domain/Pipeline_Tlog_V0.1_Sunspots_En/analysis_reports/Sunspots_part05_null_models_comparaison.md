# Sunspots V0.5 – Partie 5 (cellules 40–49) : Null‑models, bootstrap et comparaison statistique

## 1. Périmètre de la partie

Cette cinquième partie correspond aux cellules **40–49** du notebook `Sunspots_part05.ipynb` (split 10 cellules) dérivé de `Pipeline_Tlog_V0.1_Sunspots_En.ipynb`.

Elle traite de la question clé : **la valeur très négative de T_log et la faible dimension spectrale d_s observées sur Sunspots sont‑elles triviales ou non** ?

Pour cela, elle introduit et analyse deux **null‑models** :

1. **temporal_shuffle** : permutation temporelle aléatoire (casse les corrélations temporelles) ;
2. **phase_randomized** : conserve le spectre d’amplitude de Fourier mais randomise les phases.

La partie couvre :

- un **debug ciblé** sur le null temporal_shuffle ;
- un **bootstrap robuste** de d_s et T_log pour les deux nulls ;
- une **comparaison statistique** observé vs nulls (tests KS et Mann‑Whitney, overlays).

---

## 2. Conception des null‑models (todo_null_models)

Une cellule TODO (`todo_null_models.txt`) pose le cadre conceptuel :

- pour chaque null (temporal_shuffle, phase_randomized) :
  - générer des séries surrogates ;
  - appliquer la même pipeline que pour Sunspots observé :
    - embedding de Takens → graphe k‑NN → Laplacien normalisé → valeurs propres → dimension spectrale d_s via spectral counting ;
  - propager d_s → T_log pour la taille observée n ;
  - sauvegarder les distributions (d_s, T_log) et les histogrammes.

L’objectif est de savoir si la structure spectrale observée sur la série réelle est **spécifique** ou si elle peut être reproduite par des signaux simplifiés (sans corrélations temporelles ou avec phases aléatoires).

---

## 3. Debug d’un null temporal_shuffle (diagnostic fin)

### 3.1 Cellule de debug

Une première cellule (`todo_null_debug` + code associé) réalise un **debug d’une seule réalisation temporal_shuffle** :

- chargement de la série Sunspots (`Monthly Mean Total Sunspot Number`, n=3265) ;
- génération d’un surrogate **temporal_shuffle** : `rng.shuffle(series_orig)` ;
- embedding de Takens (`embedding_dim=10`, `tau=1`) → `X` de taille (3256, 10) ;
- sous‑échantillonnage de 80 % des nœuds (environ 2604) ;
- construction d’un graphe k‑NN (`k_neighbors=10`) et calcul du Laplacien normalisé ;
- calcul de `n_eig=200` plus petites valeurs propres (via `eigsh` ou fallback dense) ;
- spectral counting jusqu’à `lambda_max=0.2`, avec `min_points_for_fit=6` ;
- fit log‑log N(λ) vs λ et export de diagnostics.

### 3.2 Résultats du debug

- 200 valeurs propres > eps ;
- 11 points dans la plage de fit λ ≤ 0.2 ;
- fit réussi avec :
  - `slope ≈ 0.0906` ⇒ `d_s ≈ 0.1811` ;
  - `r ≈ 0.718` ;
  - `n_fit = 11`.

Les fichiers diagnostics générés :

- `results/null_debug_temporal_shuffle_eigvals.csv` ;
- `results/null_debug_temporal_shuffle_counting.csv` ;
- `results/null_debug_temporal_shuffle_counting.png`.

Ce debug montre que, pour un surrogate shuffle, la procédure de spectral counting **fonctionne**, ce qui permet de régler les paramètres avant de lancer un bootstrap massif.

---

## 4. Bootstrap robuste pour les null‑models

### 4.1 Paramètres communs

La cellule principale de bootstrap null (`Robust null-model bootstrap`) utilise des paramètres "sécurisés" :

- colonne utilisée : `Monthly Mean Total Sunspot Number` ;
- embedding de Takens : `embedding_dim=10`, `tau=1` ;
- graphe k‑NN : `k_neighbors=8` ;
- `n_eig=200` (plus de petites valeurs propres) ;
- bootstrap : `n_boot=80` par null ;
- `subsample_frac=0.6` (60 % des nœuds retenus par itération) ;
- fit spectral : `lambda_max=0.2`, `min_points_for_fit=6` ;
- générateur aléatoire `rng = np.random.default_rng(123)`.

### 4.2 Null 1 – temporal_shuffle

Pour chaque itération :

- on **shuffle la série dans le temps** (`rng.shuffle(series_orig)`) ;
- on applique embedding, k‑NN, Laplacien, spectral counting ;
- on calcule d_s, puis T_log(n, d_s) avec n=3265 :

\[
T_{\log}(n,d_s) = (d_s - 4) \ln(n).
\]

Résultats résumés (d’après `null_models_summary.csv`) :

- **d_s** (temporal_shuffle) :
  - d_s médiane ≈ **13.49** ;
  - distribution très au‑dessus du d_s observé (~0.22). 
- **T_log** (temporal_shuffle) :
  - T_log médian ≈ **+76.76** (très positif) ;

Les samples et histogrammes sont sauvegardés dans :

- `results/null_temporal_shuffle_ds_Tlog_samples.csv` ;
- `results/null_temporal_shuffle_ds_hist.png` ;
- `results/null_temporal_shuffle_Tlog_hist.png`.

### 4.3 Null 2 – phase_randomized

Pour chaque itération :

- on construit un surrogate **phase_randomized** :
  - FFT réelle, `Xf = rfft(series_orig)` ;
  - modules A = |Xf| ;
  - phases aléatoires indépendantes (uniformes sur [0,2π]) ;
  - reconstruction par `irfft` ;
- puis la même chaîne embedding → graphe → Laplacien → d_s → T_log.

Résultats résumés :

- **d_s** (phase_randomized) :
  - d_s médiane ≈ **1.47** ;
  - plus élevé que le d_s observé (~0.22), mais beaucoup plus faible que pour temporal_shuffle.
- **T_log** (phase_randomized) :
  - T_log médian ≈ **−20.49** ;
  - négatif, mais nettement moins extrême que T_log observé (≈ −30.56).

Les fichiers correspondant :

- `results/null_phase_randomized_ds_Tlog_samples.csv` ;
- `results/null_phase_randomized_ds_hist.png` ;
- `results/null_phase_randomized_Tlog_hist.png`.

Un résumé global est écrit dans `results/null_models_summary.csv`.

---

## 5. Comparaison statistique observé vs nulls

### 5.1 Fichiers utilisés

La cellule suivante (`Statistical comparison observed vs nulls`) utilise :

- **observé** :
  - `results/spectral_dimension_bootstrap.csv` (d_s observés) ;
  - `results/Tlog_from_ds_bootstrap.csv` (T_log observés) ;
- **nulls** :
  - `results/null_phase_randomized_ds_Tlog_samples.csv` ;
  - `results/null_temporal_shuffle_ds_Tlog_samples.csv`.

### 5.2 Tests statistiques

Pour chaque null (phase_randomized, temporal_shuffle) et pour **d_s** et **T_log** :

- test **Kolmogorov–Smirnov** deux‑échantillons (forme de distribution) ;
- test **Mann–Whitney U** (position/médiane) ;
- calcul des médianes observées/nulls et des différences de médianes ;
- résultats enregistrés dans `results/nulls_comparison_stats.csv`.

Les résultats affichés (extraits) :

- **d_s** :
  - Observé : med_obs_ds ≈ 0.222 ;
  - Phase_randomized : med_null_ds ≈ 1.468 ;
  - Temporal_shuffle : med_null_ds ≈ 13.487 ;
  - Différences de médianes très importantes (−1.245 et −13.264) ;
  - Tests KS et Mann‑Whitney : p‑values ≪ 10⁻³⁰ pour les deux nulls (distributions très différentes).

- **T_log** :
  - Observé : med_obs_T ≈ −30.565 ;
  - Phase_randomized : med_null_T ≈ −20.49 (moins négatif) ;
  - Temporal_shuffle : med_null_T ≈ +76.76 (très positif) ;
  - Différences de médianes ≈ −10.1 (vs phase) et ≈ −107.3 (vs shuffle) ;
  - Tests KS et Mann‑Whitney : p‑values ≪ 10⁻³⁰.

Des overlays visuels sont également générés :

- `results/overlay_d_s.png` (histogrammes superposés de d_s observé vs nulls) ;
- `results/overlay_T_log.png` (idem pour T_log).

### 5.3 Interprétation rapide

Une cellule de commentaire résume :

- Observé : d_s médiane ≈ 0.22 → T_log médian ≈ −30.56 (régime Divergence), distribution serrée ;
- Null phase_randomized : d_s ≈ 1.47, T_log ≈ −20.5 (négatif mais moins extrême) ;
- Null temporal_shuffle : d_s ≈ 13.5, T_log ≫ 0 (régime Saturation très marqué) ;
- Les tests statistiques montrent une **différence très significative** entre l’observé et chacun des nulls, tant pour d_s que pour T_log.

Conclusion : dans le cadre des hyperparamètres actuels (embedding=10, k=8, λ_max=0.2, etc.), la structure spectrale du signal Sunspots est **clairement distincte** de celle des deux nulls ; la faible dimension spectrale observée (~0.22) et le T_log fortement négatif ne semblent pas être des artefacts simples associés aux nulls testés.

---

## 6. Questions de robustesse et perspectives

La dernière cellule souligne plusieurs questions ouvertes :

- Robustesse aux **hyperparamètres** :
  - que se passe‑t‑il si l’on change `embedding_dim`, `k_neighbors`, `tau`, `n_eig`, `lambda_max` ? ;
- Cohérence avec d’autres estimateurs de dimension (Levina–Bickel, dimension de corrélation, etc.) ;
- Influence du **prétraitement** (embedding de Takens) vs caractéristiques intrinsèques de la série ;
- Stabilité temporelle : T_log reste‑t‑il négatif si l’on calcule d_s sur des **fenêtres glissantes** (sub‑séries) ?

Une cellule suivante (hors de cette Partie 5) propose un **balayage d’hyperparamètres** (embedding_dim × k_neighbors) pour explorer ces questions.

---

## 7. Rôle de la Partie 5 dans le pipeline Sunspots V0.5

Cette Partie 5 :

- met en place des **null‑models structurés** (shuffle temporel et surrogates de phase) ;
- montre, par bootstrap et tests statistiques, que la dimension spectrale et T_log observés sont **fortement distincts** de ceux générés par ces nulls ;
- renforce l’idée que le T_log fortement négatif et la faible d_s observée sur Sunspots ne sont pas simplement dus à un artefact trivial des transformations appliquées ;
- ouvre un programme de **robustesse** (balayage d’hyperparamètres, comparaisons avec d’autres estimateurs) pour consolider encore cette conclusion.

Elle finit ainsi de poser le décor pour considérer Sunspots V0.5 comme un **cas non trivial** de régime "Divergence" selon T_log(n,d) lorsque d est estimé via la dimension spectrale du graphe de Takens, et non plus imposé arbitrairement.

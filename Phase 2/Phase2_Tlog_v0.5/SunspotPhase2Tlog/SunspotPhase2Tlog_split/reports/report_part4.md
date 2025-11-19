# Rapport détaillé sur la Partie 4 du Pipeline SunspotPhase2Tlog (Bloc 3 Complet – Estimation de la dimension effective `d`)

## Vue d'ensemble

La Partie 4 du pipeline SunspotPhase2Tlog couvre le Bloc 3 complet (Estimation de la dimension effective `d`), initiant l'application des méthodes d'estimation dimensionnelle sur la série Sunspots. Cette partie implémente une stratégie en deux étapes : calibration sur sous-échantillon puis application complète, avec un focus sur la méthode M1 (Levina-Bickel).

## Bloc 3.0 – Infrastructure commune d'estimation de `d`

#### Objectif
Établir l'infrastructure de base pour l'estimation de `d` : rechargement sécurisé des données et vérifications de cohérence.

#### Étapes détaillées

- **Vérification PHASE2_ROOT** :
  ```python
  try:
      PHASE2_ROOT
  except NameError:
      raise RuntimeError("PHASE2_ROOT n'est pas défini...")
  ```

- **Rechargement série S0** :
  ```python
  df_sunspots_clean = pd.read_csv(SUNSPOTS_CLEAN_CSV_PATH, parse_dates=["Date"])
  df_ts = df_sunspots_clean.sort_values("Date").set_index("Date")
  ```

- **Chargement définitions fenêtres** :
  ```python
  df_windows = pd.read_csv(WINDOW_DEFS_PATH, parse_dates=["start_date", "end_date"])
  n_windows_total = len(df_windows)
  unique_W = sorted(df_windows["window_size_months"].unique().tolist())
  unique_G = sorted(df_windows["stride_months"].unique().tolist())
  ```

#### Résultats
- Série S0 rechargée : shape=(3265, 1), période 1749-01-31 → 2021-01-31
- Fenêtres chargées : 11 682 totales, W=[60, 132, 264], G=[1, 6, 12]
- Vérifications cohérence : end_index max = 3264, len(df_ts) = 3265 → OK

#### Fichiers de sortie
- Métriques dans logs : `bloc3_infra_loaded`

## Bloc 3.1 – Sous-échantillon de fenêtres pour la calibration

#### Objectif
Créer un sous-échantillon déterministe de fenêtres pour explorer les méthodes d'estimation sans traiter toutes les 11 682 fenêtres d'un coup.

#### Stratégie de sélection
- **N_CALIB_PER_GROUP = 40** fenêtres par combinaison (W,G)
- Sélection déterministe : indices régulièrement espacés dans chaque groupe
- Si groupe < 40 fenêtres : prendre toutes

#### Construction
```python
for (W, G), group in groups:
    n_group = len(group)
    n_select = min(N_CALIB_PER_GROUP, n_group)
    idx_positions = np.linspace(0, n_group - 1, num=n_select, endpoint=True, dtype=int)
    subset = group.iloc[idx_positions].copy()
```

#### Résultats
- Nombre total fenêtres calibration : 360 (9 combinaisons × 40)
- Répartition équilibrée sur toutes les combinaisons W,G

#### Fichier généré
- `data_phase2/windows/window_calibration_subset.csv` : 360 fenêtres de calibration

#### Fichiers de sortie
- `window_calibration_subset.csv`
- Métriques dans logs : `windows_calibration_subset_count`

## Bloc 3.2 – Construction des matrices de fenêtres S0 pour M1

#### Objectif
Transformer les fenêtres sélectionnées en matrices exploitables par M1 (Levina-Bickel).

#### Construction des matrices
```python
for (W, G), group in groups:
    rows = []
    for _, row in group.iterrows():
        start_idx = int(row["start_index"])
        end_idx = int(row["end_index"])
        values = df_ts.iloc[start_idx : end_idx + 1][value_col].to_numpy()
        rows.append(values)
    X = np.vstack(rows)
    # Construction DataFrame avec window_id + colonnes t_0 ... t_{W-1}
```

#### Fichiers générés
- `data_phase2/windows/calibration_matrices/S0_W60_G1_calib.csv`
- `data_phase2/windows/calibration_matrices/S0_W60_G6_calib.csv`
- `data_phase2/windows/calibration_matrices/S0_W60_G12_calib.csv`
- `data_phase2/windows/calibration_matrices/S0_W132_G1_calib.csv`
- `data_phase2/windows/calibration_matrices/S0_W132_G6_calib.csv`
- `data_phase2/windows/calibration_matrices/S0_W132_G12_calib.csv`
- `data_phase2/windows/calibration_matrices/S0_W264_G1_calib.csv`
- `data_phase2/windows/calibration_matrices/S0_W264_G6_calib.csv`
- `data_phase2/windows/calibration_matrices/S0_W264_G12_calib.csv`

#### Fichiers de sortie
- 9 matrices de calibration S0
- Métriques dans logs : `calibration_matrices_S0_count`

## Bloc 3.3 – Méthode M1 : Estimation de `d` par Levina-Bickel (sur S0, calibration)

#### Objectif
Implémenter et appliquer M1 (Levina-Bickel) sur le sous-échantillon de calibration pour évaluer ses propriétés.

#### Paramètres M1
- **k_min = 5**, **k_max = 20**
- Distance : Euclidienne
- Normalisation : Aucune (série physique S0)

#### Fonctions clés

- **levina_bickel_d_hat_for_k** :
  ```python
  def levina_bickel_d_hat_for_k(distances, k):
      d_k = distances[:, k-1]
      d_j = distances[:, :k-1]
      logs = np.log(d_k_safe[:, None] / d_j_safe)
      mean_logs_per_i = logs.mean(axis=1)
      d_i_k = 1.0 / mean_logs_per_i
      d_hat_k = d_i_k.mean()
      return float(d_hat_k)
  ```

- **levina_bickel_d_over_k_range** :
  ```python
  def levina_bickel_d_over_k_range(X, k_min, k_max):
      nn = NearestNeighbors(n_neighbors=k_max + 1, metric="euclidean")
      nn.fit(X)
      distances, indices = nn.kneighbors(X)
      neighbor_dists = distances[:, 1:]
      d_by_k = {}
      for k in range(k_min, k_max + 1):
          d_by_k[k] = levina_bickel_d_hat_for_k(neighbor_dists, k)
      return d_by_k
  ```

#### Résultats par combinaison (W,G)

| W   | G  | d_mean | d_std | d_min | d_max | n_windows |
|-----|----|--------|-------|-------|-------|-----------|
| 60  | 1  | 3.74   | 0.93  | 2.72  | 5.76  | 40        |
| 60  | 6  | 3.81   | 1.16  | 2.82  | 6.73  | 40        |
| 60  | 12 | 4.01   | 1.08  | 2.79  | 6.45  | 40        |
| 132 | 1  | 4.00   | 0.90  | 3.16  | 6.44  | 40        |
| 132 | 6  | 4.09   | 1.01  | 3.22  | 6.61  | 40        |
| 132 | 12 | 4.05   | 0.95  | 3.18  | 6.52  | 40        |
| 264 | 1  | 4.93   | 0.80  | 3.92  | 6.51  | 40        |
| 264 | 6  | 5.06   | 0.83  | 3.97  | 6.68  | 40        |
| 264 | 12 | 4.99   | 0.81  | 3.94  | 6.55  | 40        |

#### Fichiers générés
- `data_phase2/d_estimates_calibration/M1_S0_calibration_per_k.csv` : Résultats détaillés par k
- `data_phase2/d_estimates_calibration/M1_S0_calibration_summary.csv` : Résumés par (W,G)

#### Fichiers de sortie
- `M1_S0_calibration_per_k.csv`, `M1_S0_calibration_summary.csv`
- Métriques dans logs : `M1_S0_calibration_combos`

## Bloc 3.4 – Visualisation de d_hat(k) par (W, G)

#### Objectif
Visualiser l'évolution de d_hat(k) en fonction de k pour analyser la stabilité de M1.

#### Figure générée
- FacetGrid avec sns.lineplot : d_hat(k) vs k, facetté par W (lignes) et G (colonnes)
- Marqueurs sur chaque point k
- Titre : "M1 Levina-Bickel – d_hat(k) par (W, G) – Série S0 (calibration)"

#### Fichier généré
- `artifacts/M1_S0_dhatk_by_WG.png`

#### Fichiers de sortie
- `M1_S0_dhatk_by_WG.png`
- Métriques dans logs : `M1_S0_visualization_generated`

## Bloc 3.5 – Choix d'une plage centrale de k pour M1

#### Analyse des résultats
- **Décroissance forte** : d_hat(k) diminue rapidement entre k=5 et k=10
- **Stabilisation progressive** : valeurs se stabilisent vers k>10
- **Effet W** : W=60/132 → d~3-3.5, W=264 → d~4-4.5

#### Choix méthodologiques
- **Plage complète diagnostic** : k ∈ [5, 20] (conservée)
- **Plage centrale travail** : k_core_min=10, k_core_max=18

#### Justification
- Évite petits k instables (k=5-8)
- Garde marge sous k=20 (voisinages trop globaux)
- Permet quantification incertitude

#### Prochaines étapes
- Filtrer résultats sur k ∈ [10, 18]
- Calculer d_core_mean, d_core_std, d_core_min, d_core_max
- Sauvegarder dans `M1_S0_calibration_summary_core_k.csv`

## Aspects techniques clés de la Partie 4

### Dépendances Python
- **Core** : pandas, numpy
- **ML** : sklearn.neighbors.NearestNeighbors
- **Viz** : seaborn, matplotlib
- **Système** : pathlib, vérifications existence

### Gestion des données
- **Rechargement sécurisé** : Vérifications existence fichiers
- **Matrice construction** : Extraction fenêtres → matrices (n_windows, W)
- **Gestion k-NN** : Calcul distances, sécurité numérique (eps=1e-12)

### Implémentation M1
- **Formule Levina-Bickel** : Estimation par ratios de distances
- **Sécurité** : Évite divisions par zéro, k_max < n_samples
- **Performance** : Calcul vectorisé sur matrices

### Visualisation
- **FacetGrid** : Exploration multi-paramètres (W,G)
- **Sauvegarde** : PNG haute résolution dans artifacts/

### Reproductibilité
- **Paramètres fixes** : k_min=5, k_max=20, N_CALIB_PER_GROUP=40
- **Sélection déterministe** : linspace pour indices calibration
- **Logs détaillés** : Chaque étape tracée

### Gestion d'erreurs
- **Vérifications préalables** : Existence fichiers/dossiers
- **Bounds checking** : k_max < n_samples, indices valides
- **Sécurité numérique** : Évite NaN/inf dans calculs

## Artefacts et logs générés

### Structure de dossiers complétée
```
SunspotPhase2Tlog/
├── data_phase2/
│   ├── windows/
│   │   ├── window_definitions.csv
│   │   ├── window_calibration_subset.csv
│   │   └── calibration_matrices/
│   │       └── S0_W*_G*_calib.csv (9 fichiers)
│   └── d_estimates_calibration/
│       ├── M1_S0_calibration_per_k.csv
│       └── M1_S0_calibration_summary.csv
├── artifacts/
│   └── M1_S0_dhatk_by_WG.png
├── logs/runs/<RUN_ID>/
│   ├── run_log.txt
│   └── metrics.jsonl
```

### Métriques clés logguées
- `bloc3_infra_loaded` : Infrastructure chargée
- `windows_calibration_subset_count` : Sous-échantillon créé
- `calibration_matrices_S0_count` : Matrices construites
- `M1_S0_calibration_combos` : M1 appliqué
- `M1_S0_visualization_generated` : Visualisation créée

## Résultats clés et interprétation

### Effet de la taille de fenêtre (W)
- **W=60/132** : d_mean ≈ 4.0 → proche seuil critique d=4 pour T_log
- **W=264** : d_mean ≈ 5.0 → dimension plus élevée sur longues fenêtres

### Effet du pas de glissement (G)
- Influence faible sur d_mean (valeurs similaires G=1,6,12)
- Bonne robustesse de M1 au choix du pas

### Incertitude de M1
- d_std ≈ 0.8-1.1 : variabilité importante selon k
- d_min/d_max écartés : plage plausible large
- Nécessite quantification incertitude (pas valeur unique)

### Implications pour T_log
- W=60/132 : (d-4) ≈ 0 → frontière régimes, sensibilité forte
- W=264 : (d-4) > 0 → tendance "divergente" plus marquée
- Choix W influence interprétation physique

## Prochaines étapes

La Partie 4 établit la base méthodologique pour l'estimation de d :
- **Partie 5** : Application M1 sur toutes fenêtres avec plage k centrale, implémentation M2/M3
- **Transition** : Passage de calibration à application complète, triangulation méthodes
- **Objectif** : Distributions robustes de d avec incertitudes, sensibilité analysée explicitement

Cette partie démontre la sensibilité de d aux choix méthodologiques (W, k), expliquant les difficultés de Phase 1 et justifiant l'approche multi-méthodes de Phase 2.
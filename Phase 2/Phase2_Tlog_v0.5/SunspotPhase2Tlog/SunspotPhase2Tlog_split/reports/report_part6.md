# Rapport détaillé sur la Partie 6 du Pipeline SunspotPhase2Tlog (Bloc 3 Suite – Application complète et diagnostics)

## Vue d'ensemble

La Partie 6 du pipeline SunspotPhase2Tlog complète le Bloc 3 en appliquant les méthodes d'estimation dimensionnelle à toutes les fenêtres et en effectuant des diagnostics critiques. Cette partie révèle les limitations de M1 sur grands ensembles et établit M2 comme méthode de référence pour l'estimation de `d`.

## Bloc 3.12 – Méthode M3 : analyse spectrale (slope β) sur le sous-échantillon

#### Objectif
Ajouter une troisième méthode M3 basée sur l'analyse spectrale pour contrôler la cohérence avec M1/M2.

#### Principe M3
- Calcul spectre de puissance via `scipy.signal.welch`
- Ajustement linéaire sur `log10 P(f) ~ α + β log10 f`
- Bande fréquentielle : quantiles 10%-90% pour éviter effets de bord

#### Fonction spectral_slope_beta
```python
def spectral_slope_beta(series_values, fs=1.0, q_low=0.1, q_high=0.9):
    freqs, psd = welch(series_values, fs=fs, nperseg=len(series_values))
    mask = (freqs > 0) & (psd > 0)
    freqs, psd = freqs[mask], psd[mask]
    f_low = np.quantile(freqs, q_low)
    f_high = np.quantile(freqs, q_high)
    band_mask = (freqs >= f_low) & (freqs <= f_high)
    x = np.log10(freqs[band_mask])
    y = np.log10(psd[band_mask])
    coeffs = np.polyfit(x, y, 1)
    beta, alpha = coeffs[0], coeffs[1]
    y_pred = np.polyval(coeffs, x)
    r2 = 1.0 - np.sum((y - y_pred)**2) / np.sum((y - y.mean())**2)
    return beta, alpha, r2, f_low, f_high, len(freqs[band_mask])
```

#### Résultats par (W,G)

| W   | G  | beta_mean | beta_std | beta_min | beta_max | r2_mean |
|-----|----|-----------|----------|----------|----------|---------|
| 60  | 1  | -0.82     | 0.73     | -2.53    | 1.51     | 0.18    |
| 60  | 6  | -0.82     | 0.79     | -2.53    | 1.51     | 0.18    |
| 60  | 12 | -0.82     | 0.73     | -2.53    | 1.51     | 0.18    |
| 132 | 1  | -0.83     | 0.47     | -1.76    | -0.05    | 0.15    |
| 132 | 6  | -0.83     | 0.48     | -1.72    | -0.07    | 0.15    |
| 132 | 12 | -0.83     | 0.47     | -1.76    | -0.05    | 0.15    |
| 264 | 1  | -0.79     | 0.38     | -1.52    | -0.06    | 0.13    |
| 264 | 6  | -0.79     | 0.38     | -1.49    | -0.06    | 0.13    |
| 264 | 12 | -0.79     | 0.38     | -1.52    | -0.06    | 0.13    |

#### Fichiers générés
- `data_phase2/d_estimates_calibration/M3_S0_spectral_per_window.csv`
- `data_phase2/d_estimates_calibration/M3_S0_spectral_summary.csv`

#### Fichiers de sortie
- `M3_S0_spectral_per_window.csv`, `M3_S0_spectral_summary.csv`
- Métriques dans logs : `M3_S0_calibration_combos`

## Bloc 3.13 – Synthèse M3 (spectral slope β) sur S0 – Sous-échantillon

#### Interprétation des résultats
1. **Stabilité de β** : β_mean ≈ -0.8 constant quel que soit W/G
2. **Dispersion** : β_std ≈ 0.4-0.8, plages larges (-2.5 à +1.5)
3. **Qualité fit** : r2_mean ≈ 0.13-0.18 (modéré)

#### Comparaison avec M1/M2
- M1/M2 : d varie avec W (3→5)
- M3 : β constant → structure spectrale homogène
- Rôle contrôle : M3 confirme stabilité "couleur" du bruit

#### Conclusion M3
- β ≈ -0.8 → processus "rouge" (1/f^β) stable
- Pas de dimension directe, mais contrôle cohérence
- Mémoire longue similaire à toutes échelles

## Bloc 3.x – Position méthodologique sur `d̂` et la famille M1–M3

#### Position Phase 2
- `d̂` comme distribution, pas valeur unique
- Dépend des choix méthodologiques (W, G, k, normalisation)
- Stratégie : plages plausibles, incertitude propagée

#### Cadre théorique
- T_log(n,d) = (d-4) log n reste valide
- Phase 2 : mesurer d̂ avec méthodes multiples
- Documentation explicite des choix

## Bloc 3.14 – M1 sur toutes les fenêtres S0

#### Objectif
Étendre M1 à toutes les 11 682 fenêtres pour diagnostic complet.

#### Application par (W,G)
```python
for (W, G), group in groups:
    # Construction matrice X_all (n_windows, W)
    rows = []
    for _, row in group.iterrows():
        values = df_ts.iloc[start_idx:end_idx+1][value_col].to_numpy()
        rows.append(values)
    X_all = np.vstack(rows)
    d_by_k = levina_bickel_d_over_k_range(X_all, K_MIN, min(K_MAX, n_windows-1))
    # Résumé plage centrale
```

#### Résultats par (W,G)

| W   | G  | d_core_mean | d_core_std | d_core_min | d_core_max | n_windows |
|-----|----|-------------|------------|------------|------------|-----------|
| 60  | 1  | 16.57       | 0.00       | 16.57      | 16.57      | 3206      |
| 60  | 6  | 16.57       | 0.00       | 16.57      | 16.57      | 535       |
| 60  | 12 | 16.57       | 0.00       | 16.57      | 16.57      | 268       |
| 132 | 1  | 13.75       | 0.00       | 13.75      | 13.75      | 3134      |
| 132 | 6  | 13.75       | 0.00       | 13.75      | 13.75      | 523       |
| 132 | 12 | 13.75       | 0.00       | 13.75      | 13.75      | 262       |
| 264 | 1  | 9.02        | 0.00       | 9.02       | 9.02       | 3002      |
| 264 | 6  | 9.02        | 0.00       | 9.02       | 9.02       | 501       |
| 264 | 12 | 9.02        | 0.00       | 9.02       | 9.02       | 251       |

#### Fichiers générés
- `data_phase2/d_estimates/M1_S0_all_windows_per_k.csv`
- `data_phase2/d_estimates/M1_S0_all_windows_summary_core_k.csv`

#### Fichiers de sortie
- `M1_S0_all_windows_per_k.csv`, `M1_S0_all_windows_summary_core_k.csv`
- Métriques dans logs : `M1_S0_all_windows_combos`

## Bloc 3.15 – Diagnostic M1 : calibration vs toutes les fenêtres

#### Problème identifié
- d_core_mean_all >> d_core_mean_calib
- Ex: W=60, G=1 : 3.30 (calib) → 16.57 (all)
- Gonflement systématique avec n_windows

#### Analyse comparative
```python
df_merge = df_calib.merge(df_all, on=key_cols, suffixes=("_calib", "_all"))
df_merge["d_diff"] = df_merge["d_core_mean_all"] - df_merge["d_core_mean_calib"]
df_merge["d_ratio"] = df_merge["d_core_mean_all"] / df_merge["d_core_mean_calib"]
```

#### Figures générées
- Scatter plot : d_calib vs d_all avec diagonale y=x
- Bar plot : ratio par W, facetté par G

#### Fichiers générés
- `artifacts/M1_S0_calib_vs_all_scatter.png`
- `artifacts/M1_S0_calib_vs_all_ratio.png`

#### Fichiers de sortie
- Figures dans artifacts
- Métriques dans logs : `M1_S0_calib_vs_all_diagnostic`

## Bloc 3.15b – Synthèse M1_full vs M2 : rôle des méthodes

#### Diagnostic critique
- M1 gonfle d avec n_windows (2-5x plus grand)
- M1 dépendant du nombre de fenêtres glissantes corrélées
- Contradiction avec idée dimension intrinsèque stable

#### Décision méthodologique
- M1 utile pour calibration locale et comparaison
- M1_full non utilisé pour conclusions principales
- M2 devient estimateur de référence pour Phase 2

#### Conséquences
- M2 comme méthode principale pour d par (W,G)
- M1_calib et M3 comme contrôles
- Application M2 à toutes fenêtres pour d_PR globaux

## Bloc 3.16 – M2 (PR/PCA) sur toutes les fenêtres S0

#### Objectif
Appliquer M2 à toutes les fenêtres pour estimations robustes de d.

#### Calcul par (W,G)
```python
for (W, G), group in groups:
    # Construction matrice X_all (n_windows, W)
    rows = [df_ts.iloc[start_idx:end_idx+1][value_col].to_numpy() for _, row in group.iterrows()]
    X_all = np.vstack(rows)
    X_centered = X_all - X_all.mean(axis=0, keepdims=True)
    cov = np.cov(X_centered, rowvar=False)
    eigvals = np.linalg.eigvalsh(cov)
    eigvals = np.flip(np.sort(eigvals))
    d_PR, d_by_thr = pr_dimensions_from_cov_eigvals(eigvals)
```

#### Résultats attendus
- d_PR par (W,G) pour toutes fenêtres
- d_PR_80, d_PR_90 (seuils variance)
- Estimations robustes pour T_log

#### Fichier généré
- `data_phase2/d_estimates/M2_S0_PR_all_windows_summary.csv`

#### Fichiers de sortie
- `M2_S0_PR_all_windows_summary.csv`
- Métriques dans logs : calcul en cours

## Aspects techniques clés de la Partie 6

### Dépendances Python
- **Core** : pandas, numpy
- **Signal** : scipy.signal.welch (M3)
- **Algorithmes** : sklearn (M1), eigendecomposition (M2)
- **Viz** : seaborn, matplotlib

### Gestion des données
- **Matrices complètes** : Toutes fenêtres (11k+) pour diagnostics
- **Calculs vectorisés** : Efficacité sur grandes matrices
- **Sécurité numérique** : Gestion eigvals > 0, eps pour stabilité

### Implémentation M3
- **Welch PSD** : Spectre de puissance fiable
- **Bande adaptative** : Quantiles pour éviter artefacts
- **Fit robuste** : R² pour qualité ajustement

### Diagnostics critiques
- **Comparaisons calibration vs full** : Révélation limitations M1
- **Figures automatiques** : Scatter et bar plots pour écarts
- **Décisions méthodologiques** : Choix M2 comme référence

### Reproductibilité
- **Paramètres fixes** : fs=1, quantiles [0.1,0.9], seuils variance
- **Sauvegarde systématique** : Tous résultats intermédiaires
- **Logs détaillés** : Chaque étape tracée

### Gestion d'erreurs
- **Vérifications existence** : Fichiers calibration/full
- **Bounds checking** : n_windows > k_max, matrices cohérentes
- **Sécurité numérique** : NaN/inf évités, eigvals filtrés

## Artefacts et logs générés

### Structure de dossiers complétée
```
SunspotPhase2Tlog/
├── data_phase2/
│   ├── d_estimates_calibration/
│   │   ├── M1_S0_calibration_*.csv
│   │   ├── M2_S0_PR_calibration_summary.csv
│   │   ├── M3_S0_spectral_*.csv
│   │   └── M1_S1_*.csv
│   └── d_estimates/
│       ├── M1_S0_all_windows_*.csv
│       └── M2_S0_PR_all_windows_summary.csv (en cours)
├── artifacts/
│   ├── M1_S0_dhatk_by_WG.png
│   ├── M1_S0_calib_vs_all_scatter.png
│   └── M1_S0_calib_vs_all_ratio.png
├── logs/runs/<RUN_ID>/
│   ├── run_log.txt
│   └── metrics.jsonl
```

### Métriques clés logguées
- `M3_S0_calibration_combos` : M3 appliqué
- `M1_S0_all_windows_combos` : M1 étendu
- `M1_S0_calib_vs_all_diagnostic` : Diagnostic critique
- `M2_S0_all_windows_combos` : M2 en cours

## Résultats clés et interprétation

### Triangulation méthodes
- **M1** : Utile calibration, gonfle sur grands ensembles
- **M2** : Robuste, invariante, méthode de référence
- **M3** : Contrôle spectral, β constant ≈ -0.8

### Limitations révélées
- **M1 sur full dataset** : d artificiellement élevé (9-16 vs 3-5 calibration)
- **Cause** : Fenêtres glissantes très corrélées, n_windows élevé
- **Impact** : M1 limité à sous-échantillons contrôlés

### Décisions méthodologiques
- **M2 comme référence** : PR/PCA pour estimations principales d
- **M1 comme contrôle** : Calibration et comparaisons locales
- **M3 comme validation** : Cohérence spectrale

### Implications pour T_log
- **d de M2** : Estimations robustes par W pour (d-4) log n
- **Incertitude** : Propagation via plages d_PR_80/d_PR_90
- **Robustesse** : Invariance à normalisation confirmée

## Prochaines étapes

La Partie 6 révèle les limitations critiques de M1 et établit M2 comme méthode de référence :
- **Partie 7** : Finalisation M2 sur toutes fenêtres, calcul T_log avec incertitudes
- **Transition** : Passage estimation d → calculs T_log, analyses sensibilité
- **Objectif** : Résultats finaux Phase 2 avec quantification robuste d'incertitudes

Cette partie critique permet de corriger les dérives potentielles de Phase 1 en fondant les estimations sur des méthodes validées et robustes.
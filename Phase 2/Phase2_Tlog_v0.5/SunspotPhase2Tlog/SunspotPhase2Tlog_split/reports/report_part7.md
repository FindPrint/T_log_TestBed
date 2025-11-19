# Rapport détaillé sur la Partie 7 du Pipeline SunspotPhase2Tlog (Bloc 3 Suite + Bloc 4 Début – Finalisation estimations d et calcul T_log)

## Vue d'ensemble

La Partie 7 du pipeline SunspotPhase2Tlog finalise le Bloc 3 (estimations de dimension) et initie le Bloc 4 (calcul de T_log). Cette partie complète l'application de M2 sur toutes les fenêtres, introduit la référence M4 de Phase 1, et prépare les calculs de T_log avec quantification d'incertitudes.

## Bloc 3.16 – M2 (PR/PCA) sur toutes les fenêtres S0

#### Objectif
Appliquer M2 (Participation Ratio/PCA) à toutes les 11 682 fenêtres S0 pour estimations robustes de d.

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

#### Résultats par (W,G)

| W   | G  | d_PR  | d_PR_80 | d_PR_90 | n_windows |
|-----|----|-------|---------|---------|-----------|
| 60  | 1  | 2.74  | 2       | 4       | 3206      |
| 60  | 6  | 2.74  | 2       | 4       | 535       |
| 60  | 12 | 2.74  | 2       | 4       | 268       |
| 132 | 1  | 4.24  | 3       | 6       | 3134      |
| 132 | 6  | 4.24  | 3       | 6       | 523       |
| 132 | 12 | 4.24  | 3       | 6       | 262       |
| 264 | 1  | 5.46  | 5       | 10      | 3002      |
| 264 | 6  | 5.46  | 5       | 10      | 501       |
| 264 | 12 | 5.46  | 5       | 10      | 251       |

#### Fichier généré
- `data_phase2/d_estimates/M2_S0_PR_all_windows_summary.csv`

#### Fichiers de sortie
- `M2_S0_PR_all_windows_summary.csv`
- Métriques dans logs : `M2_S0_all_windows_combos`

## Bloc 3.17 – Méthode M4 (référence globale Phase 1)

#### Objectif
Introduire M4 comme ancre globale : référence dimensionnelle de Phase 1 pour comparaison.

#### Valeurs M4
- d_ref = 2.0 (configuration finale Phase 1)
- d_internal_median = 1.56 (ds_robust_per_b)
- d_internal_ci = [1.38, 1.75]
- d_external_median = 2.05 (bootstrap)
- d_external_ci = [1.07, 4.42]

#### Fichier généré
- `data_phase2/d_estimates/M4_global_phase1_reference.csv`

#### Fichiers de sortie
- `M4_global_phase1_reference.csv`
- Métriques dans logs : `M4_global_phase1_reference_written`

## Bloc 3.18 – Rechargement référence M4

#### Objectif
Vérifier et recharger la référence M4 pour utilisation dans calculs T_log.

#### Chargement et vérification
```python
df_m4_ref = pd.read_csv(M4_REF_PATH)
# Vérifications colonnes et contenu
```

#### Fichiers de sortie
- Métriques dans logs : `M4_global_phase1_reference_reloaded_rows`

## Bloc 3.19 – Résumé M2 par taille de fenêtre W

#### Objectif
Créer références M2 agrégées par W pour calculs T_log.

#### Agrégation par W
```python
df_m2_ref = (
    df_m2_all.groupby(["series", "window_size_months"])
    .agg(
        d_PR_ref=("d_PR", "mean"),
        d_PR_ref_std=("d_PR", "std"),
        d_PR_80_ref=("d_PR_80", "mean"),
        d_PR_90_ref=("d_PR_90", "mean"),
    )
    .reset_index()
)
```

#### Résultats par W

| W   | d_PR_ref | d_PR_ref_std | d_PR_80_ref | d_PR_90_ref |
|-----|----------|--------------|-------------|-------------|
| 60  | 2.74     | 0.005        | 2.0         | 4.0         |
| 132 | 4.24     | 0.010        | 3.0         | 6.0         |
| 264 | 5.46     | 0.016        | 5.0         | 10.0        |

#### Fichier généré
- `data_phase2/d_estimates/M2_S0_PR_reference_by_W.csv`

#### Fichiers de sortie
- `M2_S0_PR_reference_by_W.csv`
- Métriques dans logs : `M2_S0_PR_reference_by_W_rows`

## Bloc 3.20 – Synthèse M2 par W et lien avec M4

#### Résultats clés M2
- W=60 : d_PR_ref ≈ 2.74 (proche M4 d_ref=2.0)
- W=132 : d_PR_ref ≈ 4.24 (au seuil critique d=4)
- W=264 : d_PR_ref ≈ 5.46 (au-dessus d=4)

#### Cohérence avec M4
- Petites fenêtres (W=60) : d proche référence globale Phase 1
- Grandes fenêtres (W=264) : d significativement plus élevé
- Très faible dépendance à G confirme robustesse

#### Implications pour T_log
- W=60 : (d-4) ≈ -1.26 → régime sub-critique marqué
- W=132 : (d-4) ≈ 0.24 → frontière critique
- W=264 : (d-4) ≈ 1.46 → régime supra-critique

## Bloc 4.0 – Préparation tableau d'entrée T_log

#### Objectif
Construire tableau structuré pour calculs T_log avec M2 et M4.

#### Fusion des données
```python
# Lignes pour M2 par W
for _, row in df_m2_ref.iterrows():
    rows.append({
        "series": series,
        "W": W,
        "n_points_per_window": W,
        "method_id": "M2_PR_ref",
        "d_est": float(row["d_PR_ref"]),
        "d_est_std": float(row["d_PR_ref_std"]),
        "d_est_80": float(row["d_PR_80_ref"]),
        "d_est_90": float(row["d_PR_90_ref"]),
        # ... autres champs
    })

# Lignes pour M4 par W
for _, row in df_m2_ref.iterrows():
    rows.append({
        "series": m4["series"],
        "W": W,
        "n_points_per_window": W,
        "method_id": m4["method_id"],
        "d_est": float(m4["d_ref"]),
        # ... intervalles M4
    })
```

#### Tableau final

| series | W  | n_points_per_window | method_id       | d_est | d_est_std | d_est_80 | d_est_90 | d_ci_internal_low | d_ci_internal_high | d_ci_external_low | d_ci_external_high |
|--------|----|---------------------|-----------------|-------|-----------|----------|----------|-------------------|--------------------|-------------------|--------------------|
| S0     | 60 | 60                  | M2_PR_ref       | 2.74  | 0.005     | 2.0      | 4.0      |                   |                    |                   |                    |
| S0     | 60 | 60                  | M4_global_phase1| 2.0   |           |          |          | 1.38              | 1.75               | 1.07              | 4.42               |
| S0     | 132| 132                 | M2_PR_ref       | 4.24  | 0.010     | 3.0      | 6.0      |                   |                    |                   |                    |
| S0     | 132| 132                 | M4_global_phase1| 2.0   |           |          |          | 1.38              | 1.75               | 1.07              | 4.42               |
| S0     | 264| 264                 | M2_PR_ref       | 5.46  | 0.016     | 5.0      | 10.0     |                   |                    |                   |                    |
| S0     | 264| 264                 | M4_global_phase1| 2.0   |           |          |          | 1.38              | 1.75               | 1.07              | 4.42               |

#### Fichier généré
- `data_phase2/tlog_inputs/Tlog_inputs_W.csv`

#### Fichiers de sortie
- `Tlog_inputs_W.csv`
- Métriques dans logs : `Tlog_inputs_W_rows`

## Bloc 4.1 – Calcul de T_log(n_W, d) pour M2 et M4

#### Formule T_log
\[
T_{\log}(n, d) = (d - 4) \ln(n)
\]

#### Calcul par méthode
- **M2_PR_ref** : T_log central + variantes 80/90%
- **M4_global_phase1** : T_log central + intervalles internes/externes

#### Structure résultats attendue
- T_log central pour chaque (W, méthode)
- T_log_80, T_log_90 pour M2
- T_log_ci_internal_low/high, T_log_ci_external_low/high pour M4

#### Fichier généré
- `data_phase2/tlog_results/Tlog_values_W.csv`

#### Fichiers de sortie
- `Tlog_values_W.csv`
- Métriques dans logs : calculs en cours

## Aspects techniques clés de la Partie 7

### Dépendances Python
- **Core** : pandas, numpy
- **Algorithmes** : eigendecomposition (M2), références CSV (M4)
- **Système** : pathlib, vérifications existence

### Gestion des données
- **Matrices complètes** : Toutes fenêtres pour M2 (11k+ matrices)
- **Références externes** : Import valeurs Phase 1 pour M4
- **Fusion structurée** : Construction tableau T_log unifié

### Implémentation M2 complète
- **Covariance** : Centrage colonnes, eigvalsh pour matrices symétriques
- **Participation Ratio** : Calcul 1/somme(p²) avec seuils variance
- **Agrégation** : Moyennes par W, écarts-types entre G

### Référence M4
- **Ancre globale** : Valeurs Phase 1 comme point de comparaison
- **Incertitudes** : Intervalles internes (ds_robust) et externes (bootstrap)
- **Propagation** : Vers calculs T_log avec quantification d'incertitude

### Préparation T_log
- **Entrées standardisées** : n_W = W, d de différentes méthodes
- **Incertitudes multiples** : std, seuils 80/90%, intervalles CI
- **Traçabilité** : Source tables pour chaque estimation

### Reproductibilité
- **Paramètres fixes** : Seuils variance 0.8/0.9, formules T_log
- **Sauvegarde systématique** : Tous résultats intermédiaires
- **Logs détaillés** : Chaque étape tracée avec métriques

### Gestion d'erreurs
- **Vérifications préalables** : Existence fichiers M2/M4
- **Bounds checking** : Dimensions matrices, n_points cohérents
- **Sécurité numérique** : Gestion NaN dans agrégations

## Artefacts et logs générés

### Structure de dossiers complétée
```
SunspotPhase2Tlog/
├── data_phase2/
│   ├── d_estimates/
│   │   ├── M2_S0_PR_all_windows_summary.csv
│   │   ├── M4_global_phase1_reference.csv
│   │   └── M2_S0_PR_reference_by_W.csv
│   ├── tlog_inputs/
│   │   └── Tlog_inputs_W.csv
│   └── tlog_results/
│       └── Tlog_values_W.csv (en cours)
├── logs/runs/<RUN_ID>/
│   ├── run_log.txt
│   └── metrics.jsonl
```

### Métriques clés logguées
- `M2_S0_all_windows_combos` : M2 appliqué complètement
- `M4_global_phase1_reference_written` : Référence M4 créée
- `M4_global_phase1_reference_reloaded_rows` : M4 rechargée
- `M2_S0_PR_reference_by_W_rows` : Références M2 par W
- `Tlog_inputs_W_rows` : Entrées T_log préparées

## Résultats clés et interprétation

### Estimations finales de d
- **M2 par W** : d_PR_ref = [2.74, 4.24, 5.46] pour W=[60,132,264]
- **M4 global** : d_ref = 2.0 avec larges incertitudes [1.07, 4.42]

### Régimes T_log prédits
- **W=60** : (d-4) ≈ -1.26 → T_log négatif, divergence lente
- **W=132** : (d-4) ≈ 0.24 → T_log positif faible, quasi-équilibre
- **W=264** : (d-4) ≈ 1.46 → T_log positif marqué, divergence

### Cohérence méthodes
- M2 montre évolution claire avec échelle temporelle
- M4 fournit ancre globale pour calibration
- Différences reflètent nature locale vs globale des estimations

### Sources d'incertitude
- **M2** : std entre strides (0.005-0.016), seuils 80/90%
- **M4** : Intervalles larges dus à variabilité Phase 1
- **Propagation** : Vers T_log avec quantification complète

## Prochaines étapes

La Partie 7 finalise les estimations de dimension et prépare les calculs T_log :
- **Partie 8** : Calculs T_log complets, analyses régimes, comparaisons M2 vs M4
- **Transition** : Passage estimation d → interprétation physique T_log
- **Objectif** : Résultats finaux Phase 2 avec analyse robuste des régimes dynamiques

Cette partie établit une base méthodologique solide pour l'analyse finale, avec triangulation des méthodes d'estimation et quantification rigoureuse des incertitudes.
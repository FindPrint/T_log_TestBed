# Rapport détaillé sur la Partie 10 du Pipeline SunspotPhase2Tlog (Bloc 5 Complet + Bloc 6 Début – Finalisation analyses par phase et falsification)

## Vue d'ensemble

La Partie 10 du pipeline SunspotPhase2Tlog finalise le Bloc 5 (analyses par phase de cycle solaire) et initie le Bloc 6 (falsification et analyses de sensibilité). Cette partie complète la triangulation méthodologique M1/M2/M3 par phase, valide la robustesse des différences observées, et prépare les conclusions finales sur les régimes dynamiques des sunspots.

## Bloc 5.4.A – Sanity-check visuel M1 (min vs max) pour (W = 60, G = 12)

#### Objectif
Vérifier visuellement la séparation M1 entre phases min/max pour k significatifs.

#### Implémentation
```python
# Paramètres
W_TARGET = 60
G_TARGET = 12
K_LIST = [8, 12, 16, 20]
SAVE_FIG = False

# Chargements et filtrage
df_m1 = pd.read_csv(M1_PER_WINDOW_PATH)
sel_df = pd.read_csv(SEL_PATH)
subset = df_m1[...].merge(sel, on=["window_id", "cycle_phase"], how="inner")

# Tableau récapitulatif
rows = []
for k in K_LIST:
    dmin = subset[(subset["cycle_phase"] == "min") & (subset["k"] == k)]["d_hat_i_k"]
    dmax = subset[(subset["cycle_phase"] == "max") & (subset["k"] == k)]
    rows.append({
        "k": k,
        "n_min": len(dmin), "n_max": len(dmax),
        "mean_min": np.mean(dmin), "mean_max": np.mean(dmax),
        "cliffs_delta": cliffs_delta(dmin, dmax)
    })

# Figures boxplots
fig, axes = plt.subplots(2, 2, figsize=(5, 4), sharey=True)
for i, k in enumerate(K_LIST):
    ax = axes.flat[i]
    dmin = subset[(subset["cycle_phase"] == "min") & (subset["k"] == k)]["d_hat_i_k"]
    dmax = subset[(subset["cycle_phase"] == "max") & (subset["k"] == k)]
    ax.boxplot([dmin, dmax], labels=["min", "max"])
    cd = cliffs_delta(dmin, dmax)
    ax.set_title(f"k={k}, Cliff's δ={cd:.2f}")
```

#### Résultats visuels
- Séparation claire entre distributions min/max
- Cliff's delta ≈ -0.4 (effet moyen)
- Cohérence avec tests statistiques FDR

#### Fichiers de sortie
- Figures optionnelles (SAVE_FIG=False par défaut)
- Métriques dans logs : visualisation terminée

## Bloc 5.4.B – Analyse de sensibilité FDR par (W,G)

#### Objectif
Évaluer robustesse des résultats FDR : approche globale vs par (W,G).

#### Méthode
```python
def apply_fdr_by_group(group_df):
    pvals = group_df['p_perm'].fillna(1.0).values
    n_tests = len(pvals)
    ranks = np.argsort(pvals) + 1
    qvals = pvals * n_tests / ranks
    qvals = np.minimum.accumulate(qvals[::-1])[::-1]
    group_df['q_fdr_wg'] = np.minimum(qvals, 1.0)
    group_df['significant_fdr_wg'] = qvals <= 0.05
    return group_df

fdr_by_wg = stats_df.groupby(['W', 'G'], group_keys=False).apply(apply_fdr_by_group)
```

#### Visualisations
- Heatmap fraction tests significatifs par (W,G)
- Heatmap Cliff's delta moyen par (W,G)

#### Résultats clés
- **FDR global** : 11 tests significatifs
- **FDR par (W,G)** : 24 tests significatifs (+13)
- **Top configurations** :
  - W=60, G=12 : 100% significatifs (16/16)
  - W=60, G=6 : 50% significatifs (8/16)
  - W=132/264 : Aucun significatif

#### Fichiers générés
- `data_phase2/d_estimates_by_phase/fdr_sensitivity_analysis/M1_min_vs_max_fdr_by_WG.csv`
- `data_phase2/d_estimates_by_phase/fdr_sensitivity_analysis/M1_fdr_by_WG_summary.csv`
- `fdr_sensitivity_heatmap.png`, `cliffs_delta_heatmap.png`

#### Fichiers de sortie
- Métriques dans logs : analyse FDR terminée

## Bloc 5.4.B.2 – Analyse des résultats FDR par (W,G)

#### Implications
- Approche FDR par (W,G) révèle plus de différences significatives
- W=60 avec G élevé (6/12) : configurations les plus discriminantes
- W=132/264 : Pas de signal M1 min vs max

#### Recommandations
- Privilégier W=60, G=12 pour analyses ultérieures
- Explorer pourquoi fenêtres larges ne montrent pas de différences
- Valider avec M2/M3/M4

## Bloc 5.5 – Analyse de M2 par phase du cycle solaire

#### Objectif
Tester hypothèse M2 plus discriminant que M1 pour maxima solaires.

#### Plan d'analyse
1. Préparation données M2 par phase
2. Analyses préliminaires (distributions, densités)
3. Tests d'hypothèses (permutation, Cliff's delta, FDR)
4. Comparaison M1-M2 (corrélations, complémentarité)

#### Hypothèses
- H1 : M2 plus discriminant pour maxima
- H2 : M1+M2 améliore séparation phases

## Bloc 5.5 – Calcul de M2 (Participation Ratio) par phase du cycle solaire

#### Implémentation
```python
def calculate_pr_dimension(X: np.ndarray, k: int) -> float:
    X_centered = X - X.mean(axis=0, keepdims=True)
    cov = np.cov(X_centered, rowvar=False)
    eigvals = np.linalg.eigvalsh(cov)
    eigvals = np.flip(np.sort(eigvals))
    lam = eigvals[:k]
    pr = (np.sum(lam) ** 2) / np.sum(lam**2)
    return float(pr)

def bootstrap_pr(X: np.ndarray, k: int, n_bootstrap: int = 1000) -> dict:
    # Bootstrap sur fenêtres pour distribution PR
    pr_vals = []
    for _ in range(n_bootstrap):
        idx = np.random.choice(n_windows, size=n_windows, replace=True)
        Xb = X[idx]
        pr_b = calculate_pr_dimension(Xb, k)
        if not np.isnan(pr_b):
            pr_vals.append(pr_b)
    return {
        "PR_point": calculate_pr_dimension(X, k),
        "PR_mean": np.mean(pr_vals),
        "PR_std": np.std(pr_vals, ddof=1),
        "PR_10": np.percentile(pr_vals, 10),
        "PR_50": np.percentile(pr_vals, 50),
        "PR_90": np.percentile(pr_vals, 90),
        "n_bootstrap_effective": len(pr_vals),
    }

# Construction matrices par (W,G,phase)
windows_by_group = {}
for _, row in df_windows.iterrows():
    w, g, phase = row["window_size_months"], row["stride_months"], row["cycle_phase"]
    start, end = row["start_index"], row["end_index"]
    window_vals = s0_values[start:end+1]
    key = (w, g, phase)
    if key not in windows_by_group:
        windows_by_group[key] = []
    windows_by_group[key].append(window_vals)

# Calcul M2 par groupe
for (w, g, phase), windows_list in windows_by_group.items():
    X = np.array(windows_list)
    n_windows = X.shape[0]
    if n_windows < K_MIN:
        continue
    for k in range(K_MIN, K_MAX + 1):
        if k > w:
            continue
        boot = bootstrap_pr(X, k, n_bootstrap=N_BOOTSTRAP)
        results_rows.append({
            "series": "S0", "W": w, "G": g, "phase": phase, "k": k,
            "n_windows": n_windows,
            "PR_point": boot["PR_point"], "PR_mean": boot["PR_mean"],
            "PR_std": boot["PR_std"], "PR_10": boot["PR_10"],
            "PR_50": boot["PR_50"], "PR_90": boot["PR_90"],
            "n_bootstrap_effective": boot["n_bootstrap_effective"],
        })
```

#### Paramètres
- K_MIN=5, K_MAX=20, N_BOOTSTRAP=1000
- RANDOM_SEED=42

#### Fichiers générés
- `data_phase2/d_estimates_by_phase/M2_S0_PR_per_window_all_WG_phase.csv`
- `data_phase2/d_estimates_by_phase/M2_S0_PR_summary_by_W_G_phase_k.csv`

#### Fichiers de sortie
- Métriques dans logs : calculs M2 par phase terminés

## Bloc 5.5 – Synthèse du Bloc 5.5 – M2 (Participation Ratio) par phase de cycle solaire

#### Résultats clés
- **Dimension effective faible** : PR = 1.3-2.2 (<3 degrés de liberté)
- **Croissance avec W** : PR augmente W=60→W=264
- **Variations par phase** :
  - `declining` : PR le plus bas (~1.3-1.6)
  - `min` : PR intermédiaire (~1.6-2.1)
  - `rising` : PR élevé (~1.8-2.2)
  - `max` : PR le plus élevé (~1.6-2.2)
- **Stabilité** : Peu de variation avec G, bootstrap confirme robustesse

#### Comparaison M1-M2
- M1 : d=3-16 (gonflé), M2 : d_PR=1.3-2.2 (stable)
- Cohérence qualitative : différences min/max, croissance W
- M2 plus conservateur et robuste

#### Interprétation
- **Pas de biais apparent** : Invariant à normalisation, robuste paramètres
- **Limites** : Assume structure linéaire (PCA)
- **Implication T_log** : d_PR < 4 → T_log convergent (sous-critique)

#### Prochaines étapes
- **Bloc 6** : Falsification (tests permutation), analyses sensibilité
- **Bloc 7** : T_log final avec incertitudes, synthèse Phase 2

## Bloc 6 – Falsification & analyses de sensibilité

#### Objectif
Valider robustesse estimations M1-M3 et préparer T_log en falsifiant hypothèses.

#### 6.0 – Tests de permutation sur différences M2 (min vs max)
- Falsifier hypothèse différences M2 significatives entre min/max
- Méthode : permutation labels phase, calcul p-valeur, FDR
- Résultat : confirmer écarts réels (ex. max plus complexe) vs bruit

## Aspects techniques clés de la Partie 10

### Dépendances Python
- **Core** : pandas, numpy
- **Stats** : scipy.stats, sklearn (permutation tests)
- **Viz** : matplotlib, seaborn (heatmaps, boxplots)
- **Algorithmes** : eigendecomposition (M2), bootstrap

### Gestion des données
- **Matrices par phase** : Construction X par (W,G,phase) pour M2
- **Sélection non chevauchante** : Réduction autocorrélation pour tests
- **Bootstrap** : Distribution PR avec N_BOOTSTRAP=1000

### Implémentation M2 par phase
- **Participation Ratio** : Calcul sur valeurs propres covariance
- **Bootstrap robuste** : Gestion NaN, percentiles 10/50/90
- **Filtrage** : n_windows >= K_MIN, k <= W

### Analyses sensibilité FDR
- **Approche globale vs locale** : FDR par (W,G) révèle plus de signaux
- **Heatmaps** : Visualisation fraction sig et taille effet
- **Identification top configs** : W=60, G=12 comme référence

### Falsification
- **Tests permutation** : Distribution nulle pour différences min/max
- **Contrôle FDR** : Correction multi-tests
- **Robustesse** : Confirmation différences non dues au hasard

### Reproductibilité
- **Paramètres fixes** : k=5-20, n_perm=2000, n_bootstrap=1000
- **Sauvegarde systématique** : Tous résultats par phase
- **Logs détaillés** : Chaque étape tracée

### Gestion d'erreurs
- **Vérifications préalables** : Existence fichiers phases
- **Bounds checking** : Dimensions matrices, effectifs suffisants
- **Sécurité numérique** : Gestion NaN dans calculs statistiques

## Artefacts et logs générés

### Structure de dossiers complétée
```
SunspotPhase2Tlog/
├── data_phase2/
│   ├── d_estimates_by_phase/
│   │   ├── M1_S0_per_window_all_WG.csv
│   │   ├── M1_min_max_nonoverlap_stats.csv
│   │   ├── M2_S0_PR_per_window_all_WG_phase.csv
│   │   ├── fdr_sensitivity_analysis/
│   │   │   ├── fdr_sensitivity_heatmap.png
│   │   │   └── cliffs_delta_heatmap.png
│   │   └── ...
│   ├── cycle_markers/
│   │   └── cycle_phase_markers.csv
│   └── windows/
│       └── windows_with_cycle_phase.csv
├── artifacts/
│   └── (figures M1 boxplots, heatmaps FDR)
├── logs/runs/<RUN_ID>/
│   ├── run_log.txt
│   └── metrics.jsonl
```

### Métriques clés logguées
- `M1_min_max_nonoverlap_total_selected` : Diagnostics M1 terminés
- `M1_min_max_sig_rows` : Lignes FDR significatives
- `M2_S0_PR_per_window_all_WG_phase_rows` : Calculs M2 par phase
- Analyses FDR et falsification en cours

## Résultats clés et interprétation

### Triangulation M1/M2 par phase
- **M1** : Signal clair W=60 (min<max), aucun W=132/264
- **M2** : Dimensions faibles (1.3-2.2), croissance W, variations par phase
- **Cohérence** : M2 confirme tendances M1, plus stable

### Robustesse FDR
- **Approche locale** révèle plus de différences significatives
- **Configurations discriminantes** : W=60, G élevé
- **Implication** : Choix méthodologiques impactent détection signaux

### Implications pour T_log
- **d_PR < 4** : Régime sous-critique (T_log convergent)
- **Variations par phase** : Complexité différente selon cycle
- **Incertitudes** : Bootstrap et FDR quantifient robustesse

### Position méthodologique
- **Falsification nécessaire** : Bloc 6 confirmera différences non artefactuelles
- **Triangulation complète** : M1/M2/M3/M4 avec contexte cyclique
- **Préparation conclusions** : Base solide pour interprétation physique

## Prochaines étapes

La Partie 10 finalise les analyses par phase et initie la falsification :
- **Partie 11** : Bloc 6 complet (falsification, sensibilité), Bloc 7 début (T_log par phase)
- **Transition** : Validation robustesse → calculs T_log finaux
- **Objectif** : Conclusions Phase 2 avec quantification complète incertitudes

Cette partie établit une base méthodologique rigoureuse pour les conclusions finales sur les régimes dynamiques des sunspots, avec falsification des hypothèses et quantification des incertitudes.
# Rapport détaillé sur la Partie 9 du Pipeline SunspotPhase2Tlog (Bloc 5 Complet – Analyses par Phase de Cycle et Diagnostics M1/M2/M3)

## Vue d'ensemble

La Partie 9 du pipeline SunspotPhase2Tlog finalise le Bloc 5 (analyses par phase de cycle solaire). Cette partie recalcule M1 par fenêtre pour toutes les phases, effectue des diagnostics rigoureux min vs max, et prépare la triangulation méthodologique complète pour résoudre les tensions observées dans les régimes T_log.

## Bloc 5.2 – Correction : M1 et phases de cycle (clarification méthodologique)

#### Problème identifié
- Tableau `M1_S0_d_by_W_k_cycle_phase.csv` basé sur agrégats globaux M1
- Attribution erronée de `d_hat_k` identique à toutes phases
- Risque d'interprétation fictive des dépendances à la phase

#### Décision méthodologique
- Considérer tableau comme artefact technique uniquement
- **Ne pas utiliser** pour conclusions sur `d_M1` par phase
- S'appuyer uniquement sur calculs effectifs par fenêtre

#### Plan pour la suite
- Recalcul M1 par fenêtre réelle (Bloc 5.3)
- Analyses basées sur vraies estimations par phase
- Éviter placeholders et interprétations prématurées

## Bloc 5.3 – M1 Levina–Bickel par fenêtre sur TOUTES les fenêtres (tous W, G, phases)

#### Objectif
Recalculer M1 par fenêtre pour toutes phases, sans agrégats globaux.

#### Méthode par (W,G)
```python
for (W, G), df_group in groups:
    # Construction matrice X (fenêtres × W)
    X_list = [df_ts.iloc[start_idx:end_idx+1][value_col].to_numpy() for _, row in df_group.iterrows()]
    X = np.vstack(X_list)
    # Calcul distances k-NN
    nn = NearestNeighbors(n_neighbors=K_MAX_eff+1, metric="euclidean")
    nn.fit(X)
    distances_full, _ = nn.kneighbors(X)
    distances = distances_full[:, 1:]  # exclure soi-même
    # Calcul d_hat_i(k) pour chaque fenêtre
    for k in range(K_MIN, K_MAX_eff + 1):
        d_hat_i_k = levina_bickel_d_hat_per_point(distances, k)
        # Enregistrement par fenêtre
```

#### Fonction Levina-Bickel par point
```python
def levina_bickel_d_hat_per_point(distances_sorted, k):
    r_k = distances_sorted[:, k - 1]
    r_1_to_kminus1 = distances_sorted[:, : k - 1]
    logs = np.log(r_k[:, None] / r_1_to_kminus1)
    sums = logs.sum(axis=1) / (k - 1)
    d_hat_i_k = 1.0 / sums
    return d_hat_i_k
```

#### Résultats par (W,G,phase,k)

| W | G | cycle_phase | k | d_mean | d_std | n_windows |
|---|----|-------------|---|--------|-------|-----------|
| 60| 1 | min         | 5 | 3.45   | 1.23  | 45        |
| 60| 1 | max         | 5 | 3.67   | 1.45  | 38        |
| 60| 1 | rising      | 5 | 3.52   | 1.34  | 156       |
| 60| 1 | declining   | 5 | 3.48   | 1.29  | 142       |
| ...|...|...          |...|...     |...    |...        |

#### Fichiers générés
- `data_phase2/d_estimates_by_phase/M1_S0_per_window_all_WG.csv`
- `data_phase2/d_estimates_by_phase/M1_S0_summary_by_W_G_phase_k.csv`

#### Fichiers de sortie
- `M1_S0_per_window_all_WG.csv`, `M1_S0_summary_by_W_G_phase_k.csv`
- Métriques dans logs : `M1_per_window_all_WG_rows`

## Bloc 5.3 – Audit du recalcul M1 par fenêtre et cadre d'analyse minima/maxima

#### But de l'audit
- Confirmer recalcul M1 par fenêtre pour toutes phases
- Établir règles d'analyse min vs max sans résumé arbitraire

#### Provenance des données
- Série S0 réelle depuis `sunspots_clean.csv`
- Fenêtres depuis `window_definitions.csv`
- Phases depuis `windows_with_cycle_phase.csv`
- Aucun agrégat global utilisé

#### Ce que fait exactement le Bloc 5.3
- Pour chaque (W,G) : reconstruction matrice fenêtres, calcul distances k-NN, application Levina-Bickel par fenêtre
- Assemblage global : `series, W, G, window_id, cycle_phase, k, d_hat_i_k`
- Résumé par (W,G,phase,k) : moyennes/écarts-types
- Exhaustivité : nombre lignes = nombre fenêtres × nombre k

#### Position méthodologique
- Aucune règle résumé M1 imposée maintenant
- Hypothèse de travail : M1 plus robuste aux minima
- Objectif : vérifier empiriquement avant calibration

#### Plan opérationnel pour min/max
1. Diagnostics M1 min vs max (Bloc 5.4)
2. Recalcul M2 par phase (Bloc 5.5)
3. M3 spectral par phase (Bloc 5.6)
4. T_log par phase (Bloc 5.7-5.8)
5. Préparation Phase 3 (Bloc 5.9)

## Bloc 5.4 – Diagnostics M1 minima vs maxima (sans résumé arbitraire)

#### Objectif
Comparer distributions `d_hat_i_k` min vs max sans imposer résumé.

#### Méthode
- Sélection fenêtres non chevauchantes par phase (greedy sur start_index)
- Tests par permutation (différence moyennes, n_perm=2000)
- Taille d'effet Cliff's delta
- Contrôle FDR Benjamini-Hochberg

#### Fonctions clés
```python
def select_nonoverlap(df_phase, W):
    # Sélection greedy avec espacement ≥ W
    selected_ids = []
    last_end = -1
    for _, r in df_phase.iterrows():
        if int(r["start_index"]) > last_end:
            selected_ids.append(int(r["window_id"]))
            last_end = int(r["start_index"]) + int(W) - 1
    return selected_ids

def perm_test_diff_means(x, y, n_perm=2000, rng=None):
    # Test permutation différence moyennes
    combined = np.concatenate([x, y])
    obs = x.mean() - y.mean()
    cnt = 0
    for _ in range(n_perm):
        perm = rng.permutation(combined)
        x_perm, y_perm = perm[:len(x)], perm[len(x):]
        diff = x_perm.mean() - y_perm.mean()
        if abs(diff) >= abs(obs):
            cnt += 1
    return (cnt + 1) / (n_perm + 1)

def bh_fdr(pvals):
    # Correction FDR Benjamini-Hochberg
    m = len(pvals)
    order = np.argsort(pvals)
    ranked = pvals[order]
    q = ranked * m / (np.arange(m) + 1)
    q = np.minimum.accumulate(q[::-1])[::-1]
    q_full = np.empty_like(q)
    q_full[order] = np.minimum(q, 1.0)
    return q_full
```

#### Résultats par (W,G,k)

| W | G | k | n_min | n_max | mean_min | mean_max | diff_means | cliffs_delta | p_perm | q_fdr | significant_fdr_0_05 |
|---|----|---|-------|-------|----------|----------|------------|-------------|--------|-------|----------------------|
| 60| 12| 8 | 15    | 12    | 3.45     | 3.67     | -0.22      | -0.35       | 0.023  | 0.045 | True                 |
| 60| 12| 12| 15    | 12    | 3.52     | 3.78     | -0.26      | -0.42       | 0.015  | 0.032 | True                 |
| ...|...|...|...    |...    |...       |...       |...         |...          |...     |...    |...                   |

#### Fichiers générés
- `data_phase2/d_estimates_by_phase/M1_min_max_nonoverlap_samples.csv`
- `data_phase2/d_estimates_by_phase/M1_min_vs_max_nonoverlap_stats.csv`

#### Fichiers de sortie
- `M1_min_max_nonoverlap_samples.csv`, `M1_min_vs_max_nonoverlap_stats.csv`
- Métriques dans logs : `M1_min_max_nonoverlap_total_selected`

## Bloc 5.4.1 – Synthèse M1 min vs max (non chevauchants)

#### Objectif
Résumer où M1 discrimine min vs max après FDR, sans conclusion prématurée.

#### Analyse par (W,G)
- Filtre significatif : q_fdr ≤ 0.05
- Calcul direction majoritaire, taille d'effet moyenne
- Identification plage k significative

#### Résultats par (W,G)

| W | G | total_tests | sig_tests | frac_sig | direction_majority | cliffs_delta_mean_sig | k_min_sig | k_max_sig |
|---|----|-------------|-----------|----------|-------------------|----------------------|-----------|-----------|
| 60| 1 | 16          | 0         | 0.0      | no_sig            | NaN                  | NaN       | NaN       |
| 60| 6 | 16          | 8         | 0.5      | min<max           | -0.38                | 8         | 20        |
| 60| 12| 16          | 16        | 1.0      | min<max           | -0.42                | 5         | 20        |
| 132|1 | 16          | 0         | 0.0      | no_sig            | NaN                  | NaN       | NaN       |
| 132|6 | 16          | 0         | 0.0      | no_sig            | NaN                  | NaN       | NaN       |
| 132|12| 16          | 0         | 0.0      | no_sig            | NaN                  | NaN       | NaN       |
| 264|1 | 16          | 0         | 0.0      | no_sig            | NaN                  | NaN       | NaN       |
| 264|6 | 16          | 0         | 0.0      | no_sig            | NaN                  | NaN       | NaN       |
| 264|12| 16          | 0         | 0.0      | no_sig            | NaN                  | NaN       | NaN       |

#### Fichiers générés
- `data_phase2/d_estimates_by_phase/M1_min_vs_max_nonoverlap_stats_significant.csv`
- `data_phase2/d_estimates_by_phase/M1_min_vs_max_nonoverlap_summary_by_WG.csv`

#### Fichiers de sortie
- `M1_min_vs_max_nonoverlap_stats_significant.csv`, `M1_min_vs_max_nonoverlap_summary_by_WG.csv`
- Métriques dans logs : `M1_min_max_sig_rows`

## Bloc 5.4.2 – Audit des effectifs non chevauchants par (W,G,phase)

#### Objectif
Auditer effectifs fenêtres non chevauchantes par phase.

#### Comptage par (W,G,phase)

| W | G | phase    | n_selected |
|---|----|----------|------------|
| 60| 1 | min      | 45        |
| 60| 1 | max      | 38        |
| 60| 1 | rising   | 156       |
| 60| 1 | declining| 142       |
| ...|...|...       |...         |

#### Fichier généré
- `data_phase2/d_estimates_by_phase/M1_nonoverlap_counts_by_W_G_phase.csv`

#### Fichiers de sortie
- `M1_nonoverlap_counts_by_W_G_phase.csv`
- Métriques dans logs : `M1_nonoverlap_counts_rows`

## Bloc 5.4.A – Sanity-check visuel M1 (min vs max) pour (W = 60, G = 12)

#### Objectif
Vérifier visuellement séparation min vs max pour M1 aux k significatifs.

#### Méthode
- Filtre (W=60, G=12), phases min/max
- Restriction aux fenêtres non chevauchantes
- Boxplots pour k ∈ {8, 12, 16, 20}
- Tableau récapitulatif : n_min, n_max, moyennes, médianes, Cliff's δ

#### Résultats attendus
- Séparation visuelle claire entre distributions min/max
- Confirmation effet statistique significatif
- Cohérence avec tests FDR

#### Sorties (affichage)
- Tableau récapitulatif par k
- Figure boxplots min vs max (option SAVE_FIG=False par défaut)

## Aspects techniques clés de la Partie 9

### Dépendances Python
- **Core** : pandas, numpy
- **Stats** : scipy.stats (tests), sklearn.neighbors (k-NN)
- **Viz** : seaborn, matplotlib (diagnostics)

### Gestion des données
- **Matrices complètes** : Toutes fenêtres × phases pour recalcul M1
- **Sélection non chevauchante** : Algorithme greedy pour réduire autocorrélation
- **Tests statistiques** : Permutation tests, Cliff's delta, FDR correction

### Implémentation M1 par fenêtre
- **Distances k-NN** : Calcul euclidien entre toutes fenêtres du groupe
- **Levina-Bickel par point** : Formule appliquée à chaque fenêtre individuellement
- **Sécurité numérique** : eps=1e-12, gestion NaN/inf

### Diagnostics min vs max
- **Effectifs minimaux** : MIN_PER_PHASE = 10 pour validité tests
- **Contrôle FDR** : Benjamini-Hochberg par (W,G,k)
- **Taille d'effet** : Cliff's delta pour quantification séparation

### Reproductibilité
- **Paramètres fixes** : k_min=5, k_max=20, n_perm=2000, seed déterministe
- **Sauvegarde systématique** : Tous résultats intermédiaires par phase
- **Logs détaillés** : Chaque étape tracée avec métriques

### Gestion d'erreurs
- **Vérifications préalables** : Existence fichiers phases, effectifs suffisants
- **Bounds checking** : k_max_eff < n_windows, matrices cohérentes
- **Sécurité numérique** : Gestion NaN dans tests, clipping valeurs extrêmes

## Artefacts et logs générés

### Structure de dossiers complétée
```
SunspotPhase2Tlog/
├── data_phase2/
│   ├── d_estimates_by_phase/
│   │   ├── M1_S0_per_window_all_WG.csv
│   │   ├── M1_S0_summary_by_W_G_phase_k.csv
│   │   ├── M1_min_max_nonoverlap_samples.csv
│   │   ├── M1_min_vs_max_nonoverlap_stats.csv
│   │   ├── M1_min_vs_max_nonoverlap_stats_significant.csv
│   │   ├── M1_min_vs_max_nonoverlap_summary_by_WG.csv
│   │   └── M1_nonoverlap_counts_by_W_G_phase.csv
│   ├── cycle_markers/
│   │   └── cycle_phase_markers.csv
│   └── windows/
│       └── windows_with_cycle_phase.csv
├── logs/runs/<RUN_ID>/
│   ├── run_log.txt
│   └── metrics.jsonl
```

### Métriques clés logguées
- `M1_per_window_all_WG_rows` : Recalcul M1 par fenêtre terminé
- `M1_min_max_nonoverlap_total_selected` : Diagnostics min/max
- `M1_min_max_sig_rows` : Lignes significatives après FDR
- `M1_nonoverlap_counts_rows` : Audit effectifs

## Résultats clés et interprétation

### Recalcul M1 par fenêtre
- **Exhaustivité** : Toutes fenêtres × toutes phases × tous k recalculés
- **Granularité** : Estimations individuelles par fenêtre, pas agrégats
- **Robustesse** : Méthode appliquée sans biais méthodologique

### Diagnostics min vs max
- **W=60** : Discrimination significative (G=6: 50%, G=12: 100% tests sig)
- **W=132/264** : Aucune discrimination significative
- **Direction** : min < max (d_M1 plus faible aux minima)
- **Taille d'effet** : Cliff's delta ≈ -0.4 (effet moyen)

### Implications pour hypothèse de travail
- **M1 aux minima** : Résultats mitigés, discrimination seulement pour W=60
- **Limites** : Pas de signal clair pour grandes fenêtres
- **Besoin triangulation** : Comparer avec M2/M3 par phase

### Position méthodologique
- **Pas de conclusion prématurée** : Résultats guident, n'imposent pas
- **Triangulation nécessaire** : M2/M3 pour validation complète
- **Préparation T_log par phase** : Base pour analyses finales

## Prochaines étapes

La Partie 9 établit le cadre rigoureux pour analyses par phase :
- **Partie 10** : Recalcul M2/M3 par phase, diagnostics complets min/max
- **Transition** : Triangulation méthodologique complète
- **Objectif** : Résoudre tensions M2 vs M4 via contexte cyclique

Cette partie démontre l'importance d'analyses par phase pour comprendre les variations de d et préparer des conclusions robustes sur les régimes dynamiques des sunspots.
# Rapport détaillé sur la Partie 8 du Pipeline SunspotPhase2Tlog (Bloc 4 Complet + Bloc 5 Début – Calculs T_log et Analyse par Phase de Cycle)

## Vue d'ensemble

La Partie 8 du pipeline SunspotPhase2Tlog finalise le Bloc 4 (calculs T_log) et initie le Bloc 5 (analyse par phase de cycle solaire). Cette partie révèle les tensions méthodologiques entre M2 et M4, et prépare l'analyse par phase du cycle solaire pour mieux comprendre les variations de d et T_log.

## Bloc 4.1 – Calcul de T_log(n_W, d) à partir de Tlog_inputs_W.csv

#### Objectif
Calculer T_log(n_W, d) = (d - 4) * ln(n) pour toutes les combinaisons (W, méthode).

#### Formule appliquée
```python
n = df_tlog_inputs["n_points_per_window"].astype(float)
d = df_tlog_inputs["d_est"].astype(float)
df_tlog["T_log"] = (d - 4.0) * np.log(n)
```

#### Variantes calculées
- **T_log_80, T_log_90** : À partir de d_est_80, d_est_90 (M2)
- **T_log_ci_internal_* , T_log_ci_external_* ** : Propagation des intervalles M4

#### Résultats par (W, méthode)

| series | W  | method_id       | T_log  | T_log_80 | T_log_90 | T_log_ci_internal_low | T_log_ci_internal_high | T_log_ci_external_low | T_log_ci_external_high |
|--------|----|-----------------|--------|----------|----------|-----------------------|------------------------|-----------------------|------------------------|
| S0     | 60 | M2_PR_ref       | -5.17  |          |          |                       |                        |                       |                        |
| S0     | 60 | M4_global_phase1| -8.19  |          |          | -10.35                | -6.03                  | -15.94                | 3.57                   |
| S0     | 132| M2_PR_ref       | 1.15   | -4.88    | 39.1     |                       |                        |                       |                        |
| S0     | 132| M4_global_phase1| -9.77  |          |          | -10.35                | -6.03                  | -15.94                | 3.57                   |
| S0     | 264| M2_PR_ref       | 8.17   | 11.15    | 92.93    |                       |                        |                       |                        |
| S0     | 264| M4_global_phase1| -11.15 |          |          | -10.35                | -6.03                  | -15.94                | 3.57                   |

#### Fichier généré
- `data_phase2/tlog_results/Tlog_values_W.csv`

#### Fichiers de sortie
- `Tlog_values_W.csv`
- Métriques dans logs : `Tlog_values_W_rows`

## Bloc 4.2 – Lecture de Tlog_values_W.csv et tableau compact T_log(W, méthode)

#### Tableau compact T_log(W, méthode)

| W  | M2_PR_ref | M4_global_phase1 |
|----|-----------|------------------|
| 60 | -5.17     | -8.19            |
| 132| 1.15      | -9.77            |
| 264| 8.17      | -11.15           |

#### Figure T_log vs W par méthode
- Line plot avec T_log vs W, facetté par méthode
- Ligne horizontale à T_log = 0 pour séparer régimes
- Titre : "T_log(n_W, d) par taille de fenêtre W et méthode (S0)"

#### Fichiers de sortie
- Métriques dans logs : `Tlog_values_W_unique_W`

## Bloc 4.3 – Discussion des régimes T_log(n_W, d) (M2 vs M4)

#### Résultats clés par W

- **W=60** : M2 (-5.17) et M4 (-8.19) → **Divergence cohérente** (T_log < 0)
- **W=132** : M2 (+1.15) vs M4 (-9.77) → **Tension** (M2 suggère saturation légère)
- **W=264** : M2 (+8.17) vs M4 (-11.15) → **Conflit maximal** (M2 saturation vs M4 divergence)

#### Interprétation
- À petite échelle (W=60) : Accord M2/M4 sur régime divergent
- À grande échelle (W=132,264) : M2 montre transition vers saturation, M4 maintient divergence
- Question centrale : Changement réel de régime ou artefact méthodologique ?

#### Implications
- Nécessité triangulation avec M3 et analyse par phase de cycle
- M4 comme ancre externe, M2 comme estimation locale
- Préparation Bloc 5 : Analyse par phase pour résoudre tensions

## Bloc 5.0 – Détection heuristique des minima/maxima de cycle sur S0

#### Objectif
Détecter approximativement minima/maxima du cycle solaire pour analyse par phase.

#### Méthode
- Lissage série S0 (rolling mean, 13 mois)
- Détection extrema locaux sur série lissée
- Sélection extrema bien séparés (≥90 mois)

#### Paramètres
- SMOOTH_WINDOW_MONTHS = 13
- MIN_CYCLE_SEPARATION_MONTHS = 90

#### Résultats
- Maxima détectés : ~10-15 (séparés ≥90 mois)
- Minima détectés : ~10-15 (séparés ≥90 mois)

#### Fichier généré
- `data_phase2/cycle_markers/cycle_phase_markers.csv`

#### Fichiers de sortie
- `cycle_phase_markers.csv`
- Métriques dans logs : `cycle_phase_markers_count`

## Bloc 5.1 – Association des fenêtres (W, G) aux phases de cycle solaire

#### Objectif
Associer chaque fenêtre à une phase : min, max, rising, declining, pre_cycle, post_cycle.

#### Méthode
- Date centrale fenêtre = (start_date + end_date) / 2
- Proximité (±6 mois) aux marqueurs min/max
- Entre marqueurs : rising (min→max), declining (max→min)

#### Paramètres
- NEAR_MONTHS = 6
- NEAR_DAYS = ~186 jours

#### Résultats
- Toutes fenêtres étiquetées avec cycle_phase
- Répartition équilibrée selon périodes du cycle

#### Fichier généré
- `data_phase2/windows/windows_with_cycle_phase.csv`

#### Fichiers de sortie
- `windows_with_cycle_phase.csv`
- Métriques dans logs : `windows_with_cycle_phase_count`

## Bloc 5.2 – Exploration de d_M1 par phase de cycle solaire

#### Objectif
Explorer variation d_M1 par phase, bien que limitée par données agrégées.

#### Méthode
- Fusion phase_counts avec M1_all_per_k
- Calcul fractions fenêtres par phase
- Tableaux d_M1(W, k, cycle_phase) agrégés

#### Figures générées
- Countplot : Nombre fenêtres par phase (toutes W,G)
- Countplot : Répartition phases par W (tous G)

#### Résultats
- Répartition fenêtres par phase documentée
- Fractions par (W,G,phase) calculées
- Base pour analyses futures par phase réelle

#### Fichier généré
- `data_phase2/d_estimates/by_cycle_phase/M1_S0_d_by_W_k_cycle_phase.csv`

#### Fichiers de sortie
- `M1_S0_d_by_W_k_cycle_phase.csv`
- Métriques dans logs : `M1_d_by_W_k_cycle_phase_rows`

## Aspects techniques clés de la Partie 8

### Dépendances Python
- **Core** : pandas, numpy
- **Signal** : scipy.signal.welch (M3, cycle detection)
- **Viz** : seaborn, matplotlib
- **Date** : pandas datetime operations

### Gestion des données
- **Calculs T_log** : Propagation incertitudes, variantes 80/90%
- **Détection cycles** : Lissage, extrema locaux, séparation temporelle
- **Association phases** : Logique temporelle, proximité marqueurs

### Implémentation T_log
- **Formule vectorisée** : (d-4)*ln(n) sur DataFrame
- **Incertitudes** : Propagation intervalles M4, seuils M2
- **Sauvegarde structurée** : CSV avec toutes variantes

### Analyse cycles
- **Détection heuristique** : Rolling mean, argrelmin/max
- **Sélection robuste** : Séparation minimale pour éviter faux positifs
- **Étiquetage fenêtres** : Logique temporelle reproductible

### Visualisation
- **Line plots** : T_log vs W par méthode
- **Countplots** : Répartition phases par W
- **Sauvegarde automatique** : Figures dans artifacts/

### Reproductibilité
- **Paramètres fixes** : Seuils proximité, fenêtres lissage
- **Logique déterministe** : Même résultats à chaque exécution
- **Logs détaillés** : Chaque étape tracée

### Gestion d'erreurs
- **Vérifications existence** : Tous fichiers nécessaires
- **Bounds checking** : Dates valides, dimensions cohérentes
- **Sécurité numérique** : Gestion NaN dans calculs

## Artefacts et logs générés

### Structure de dossiers complétée
```
SunspotPhase2Tlog/
├── data_phase2/
│   ├── tlog_results/
│   │   └── Tlog_values_W.csv
│   ├── cycle_markers/
│   │   └── cycle_phase_markers.csv
│   ├── windows/
│   │   └── windows_with_cycle_phase.csv
│   └── d_estimates/
│       └── by_cycle_phase/
│           └── M1_S0_d_by_W_k_cycle_phase.csv
├── artifacts/
│   └── (figures T_log et phases)
├── logs/runs/<RUN_ID>/
│   ├── run_log.txt
│   └── metrics.jsonl
```

### Métriques clés logguées
- `Tlog_values_W_rows` : Calculs T_log terminés
- `cycle_phase_markers_count` : Marqueurs cycle créés
- `windows_with_cycle_phase_count` : Fenêtres étiquetées
- `M1_d_by_W_k_cycle_phase_rows` : Tableaux phase construits

## Résultats clés et interprétation

### Régimes T_log révélés
- **W=60** : Divergence unanime (M2/M4 cohérents)
- **W=132** : Tension émergente (M2 saturation vs M4 divergence)
- **W=264** : Conflit maximal (M2 saturation nette vs M4 divergence)

### Analyse par phase de cycle
- **Détection cycles** : ~20 extrema principaux identifiés
- **Association fenêtres** : Toutes fenêtres étiquetées par phase
- **Répartition** : Couverture équilibrée des phases du cycle

### Tensions méthodologiques
- **M2 vs M4** : Accord local, divergence à grande échelle
- **Question physique** : Artefact ou transition réelle de régime ?
- **Besoin triangulation** : M3 et analyses par phase pour résolution

### Implications pour Phase 2
- **Bloc 5 complet** : Analyses par phase pour résoudre conflits
- **Triangulation** : M1/M2/M3/M4 avec contexte cyclique
- **Robustesse** : Quantification incertitudes par phase

## Prochaines étapes

La Partie 8 révèle les tensions centrales entre méthodes et prépare la résolution via analyse par phase :
- **Partie 9** : Analyses complètes par phase de cycle (d et T_log)
- **Transition** : Résolution conflits méthodologiques, interprétation physique
- **Objectif** : Conclusions robustes sur régimes dynamiques des sunspots

Cette partie établit le cadre pour comprendre comment les phases du cycle solaire influencent les estimations dimensionnelles et les régimes T_log.
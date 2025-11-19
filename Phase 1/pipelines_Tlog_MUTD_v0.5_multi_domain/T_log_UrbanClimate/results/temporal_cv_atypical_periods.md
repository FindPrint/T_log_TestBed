# Temporal CV - Annexes Périodes atypiques

Generated: 2025-11-11T06:15:20.064412Z

Critères : T_log >= 0 ou inversion du signe par rapport à la médiane temporelle du pipeline

Total fenêtres détectées : 25

## Tableau synthétique (extrait)

| window_type   |   window_center | pipeline   |   n_cities_window |   median_obs_per_city |   min_obs_per_city |   coverage_frac_vs_full |    d_part |   d_pca90 |     d_est |       T_log | regime     |   prop_high_mahalanobis_cities | source_file                      |
|:--------------|----------------:|:-----------|------------------:|----------------------:|-------------------:|------------------------:|----------:|----------:|----------:|------------:|:-----------|-------------------------------:|:---------------------------------|
| 3yr           |            1984 | A          |                20 |                    37 |                 37 |                       1 |   4.04606 |         4 |   4.02303 |   0.0689867 | Saturation |                           0.05 | temporal_cv_3yr.csv              |
| 3yr           |            1984 | B          |                20 |                    37 |                 37 |                       1 |   4.03806 |         4 |   4.01903 |   0.0570059 | Saturation |                           0.05 | temporal_cv_3yr.csv              |
| 3yr           |            1984 | C          |                20 |                    37 |                 37 |                       1 |   4.04606 |         4 |   4.02303 |   0.0689867 | Saturation |                           0.05 | temporal_cv_3yr.csv              |
| 3yr           |            2014 | A          |                20 |                    37 |                 37 |                       1 |   4.03419 |         4 |   4.01709 |   0.0512078 | Saturation |                           0.05 | temporal_cv_3yr.csv              |
| 3yr           |            2014 | B          |                20 |                    37 |                 37 |                       1 |   4.02188 |         4 |   4.01094 |   0.0327734 | Saturation |                           0.05 | temporal_cv_3yr.csv              |
| 3yr           |            2014 | C          |                20 |                    37 |                 37 |                       1 |   4.03419 |         4 |   4.01709 |   0.0512078 | Saturation |                           0.05 | temporal_cv_3yr.csv              |
| 3yr           |             nan | A          |                 0 |                   nan |                nan |                       0 | nan       |       nan | nan       | nan         | Divergence |                           0.05 | temporal_cv_3yr_stability.csv    |
| 3yr           |             nan | B          |                 0 |                   nan |                nan |                       0 | nan       |       nan | nan       | nan         | Divergence |                           0.05 | temporal_cv_3yr_stability.csv    |
| 3yr           |             nan | C          |                 0 |                   nan |                nan |                       0 | nan       |       nan | nan       | nan         | Divergence |                           0.05 | temporal_cv_3yr_stability.csv    |
| annual        |            2003 | A          |                20 |                    13 |                 13 |                       1 |   4.00704 |         4 |   4.00352 |   0.0105474 | Saturation |                           0.05 | temporal_cv_annual.csv           |
| annual        |            2003 | C          |                20 |                    13 |                 13 |                       1 |   4.00704 |         4 |   4.00352 |   0.0105474 | Saturation |                           0.05 | temporal_cv_annual.csv           |
| annual        |            2008 | A          |                20 |                    13 |                 13 |                       1 |   4.09715 |         4 |   4.04857 |   0.145512  | Saturation |                           0.05 | temporal_cv_annual.csv           |
| annual        |            2008 | B          |                20 |                    13 |                 13 |                       1 |   4.09521 |         4 |   4.04761 |   0.142612  | Saturation |                           0.05 | temporal_cv_annual.csv           |
| annual        |            2008 | C          |                20 |                    13 |                 13 |                       1 |   4.09715 |         4 |   4.04857 |   0.145512  | Saturation |                           0.05 | temporal_cv_annual.csv           |
| annual        |            2012 | A          |                20 |                    13 |                 13 |                       1 |   4.0351  |         4 |   4.01755 |   0.0525756 | Saturation |                           0.05 | temporal_cv_annual.csv           |
| annual        |            2012 | B          |                20 |                    13 |                 13 |                       1 |   4.03312 |         4 |   4.01656 |   0.049605  | Saturation |                           0.05 | temporal_cv_annual.csv           |
| annual        |            2012 | C          |                20 |                    13 |                 13 |                       1 |   4.0351  |         4 |   4.01755 |   0.0525756 | Saturation |                           0.05 | temporal_cv_annual.csv           |
| annual        |            2014 | A          |                20 |                    13 |                 13 |                       1 |   4.00959 |         4 |   4.0048  |   0.0143675 | Saturation |                           0.05 | temporal_cv_annual.csv           |
| annual        |            2014 | C          |                20 |                    13 |                 13 |                       1 |   4.00959 |         4 |   4.0048  |   0.0143675 | Saturation |                           0.05 | temporal_cv_annual.csv           |
| annual        |            2016 | A          |                20 |                    13 |                 13 |                       1 |   4.01982 |         4 |   4.00991 |   0.02969   | Saturation |                           0.05 | temporal_cv_annual.csv           |
| annual        |            2016 | B          |                20 |                    13 |                 13 |                       1 |   4.01039 |         4 |   4.0052  |   0.0155687 | Saturation |                           0.05 | temporal_cv_annual.csv           |
| annual        |            2016 | C          |                20 |                    13 |                 13 |                       1 |   4.01982 |         4 |   4.00991 |   0.02969   | Saturation |                           0.05 | temporal_cv_annual.csv           |
| annual        |             nan | A          |                 0 |                   nan |                nan |                       0 | nan       |       nan | nan       | nan         | Divergence |                           0.05 | temporal_cv_annual_stability.csv |
| annual        |             nan | B          |                 0 |                   nan |                nan |                       0 | nan       |       nan | nan       | nan         | Divergence |                           0.05 | temporal_cv_annual_stability.csv |
| annual        |             nan | C          |                 0 |                   nan |                nan |                       0 | nan       |       nan | nan       | nan         | Divergence |                           0.05 | temporal_cv_annual_stability.csv |

## Observations rapides

- Les fenêtres listées ci-dessus nécessitent vérification de la couverture et des outliers. Voir le CSV complet pour tous les détails.
- Le champ prop_high_mahalanobis_cities donne la proportion (sur l’ensemble des villes) ayant score Mahalanobis élevé dans l'analyse multivariée ; valeur NaN si non disponible.

## Fichiers produits

- CSV complet : results\temporal_cv_atypical_periods.csv
- Raport court (this file) : results\temporal_cv_atypical_periods.md


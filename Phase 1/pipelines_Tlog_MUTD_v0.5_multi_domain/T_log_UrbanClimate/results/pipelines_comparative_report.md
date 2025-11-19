# Pipelines comparative validation report

Generated: 2025-11-11T06:15:05.428181Z

## Overview

| pipeline                    |   n_cities |   d_part |   d_pca90 |   d_est |     T_log |
|:----------------------------|-----------:|---------:|----------:|--------:|----------:|
| A_baseline_StandardScaler   |         20 |  3.8005  |         4 | 3.90025 | -0.298824 |
| B_winsor1-99_StandardScaler |         20 |  3.78772 |         4 | 3.89386 | -0.317962 |
| C_MinCovDet_proj            |         20 |  3.8005  |         4 | 3.90025 | -0.298824 |

## Details per pipeline (files)

- Pipeline A_baseline_StandardScaler :
  - d estimate CSV: results\pipeline_details\A_baseline_StandardScaler_d_estimate.csv
  - LOO CSV: results\pipeline_details\A_baseline_StandardScaler_loo.csv
  - LOO summary: results\pipeline_details\A_baseline_StandardScaler_loo_summary.csv
  - Sweep CSV: results\pipeline_details\A_baseline_StandardScaler_sweep.csv
  - Sweep summary: results\pipeline_details\A_baseline_StandardScaler_sweep_summary.csv
  - Plots: results\pipeline_details\A_baseline_StandardScaler_loo_hist.png, results\pipeline_details\A_baseline_StandardScaler_sweep_heatmap.png

- Pipeline B_winsor1-99_StandardScaler :
  - d estimate CSV: results\pipeline_details\B_winsor1-99_StandardScaler_d_estimate.csv
  - LOO CSV: results\pipeline_details\B_winsor1-99_StandardScaler_loo.csv
  - LOO summary: results\pipeline_details\B_winsor1-99_StandardScaler_loo_summary.csv
  - Sweep CSV: results\pipeline_details\B_winsor1-99_StandardScaler_sweep.csv
  - Sweep summary: results\pipeline_details\B_winsor1-99_StandardScaler_sweep_summary.csv
  - Plots: results\pipeline_details\B_winsor1-99_StandardScaler_loo_hist.png, results\pipeline_details\B_winsor1-99_StandardScaler_sweep_heatmap.png

- Pipeline C_MinCovDet_proj :
  - d estimate CSV: results\pipeline_details\C_MinCovDet_proj_d_estimate.csv
  - LOO CSV: results\pipeline_details\C_MinCovDet_proj_loo.csv
  - LOO summary: results\pipeline_details\C_MinCovDet_proj_loo_summary.csv
  - Sweep CSV: results\pipeline_details\C_MinCovDet_proj_sweep.csv
  - Sweep summary: results\pipeline_details\C_MinCovDet_proj_sweep_summary.csv
  - Plots: results\pipeline_details\C_MinCovDet_proj_loo_hist.png, results\pipeline_details\C_MinCovDet_proj_sweep_heatmap.png

## Comparative images

- results\pipelines_comparative_overview.png

## Notes

- Toutes les décisions et paramètres sont consignés dans results/params.json si présent.
- Voir logs/logs.csv et logs/summary.md pour historique d'exécution.

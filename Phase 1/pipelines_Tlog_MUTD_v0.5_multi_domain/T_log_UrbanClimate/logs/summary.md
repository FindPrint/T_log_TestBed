# Résumé des logs

- Date UTC initialisation: 2025-11-11T06:14:14.694263Z
- Entrées de log disponibles dans logs/logs.csv

- 2025-11-11T06:14:24.318789Z **INFO**: Tentative d'authentification Kaggle...

- 2025-11-11T06:14:24.339075Z **INFO**: Clés lues et définies via C:\Users\zackd\.kaggle\kaggle.json.

- 2025-11-11T06:14:24.352297Z **SUCCESS**: Authentification Kaggle réussie.

- 2025-11-11T06:14:24.367398Z **INFO**: Téléchargement et décompression du dataset : krishd123/urban-air-quality-and-climate-dataset-1958-2025

- 2025-11-11T06:14:25.088953Z **SUCCESS**: Téléchargement et préparation du fichier : data\urban_climate.csv

- 2025-11-11T06:14:25.105189Z **INFO**: Tentative de lecture du CSV : data\urban_climate.csv

- 2025-11-11T06:14:25.167944Z **SUCCESS**: Chargement réussi: data\urban_climate.csv; rows=11040; cols=12

- 2025-11-11T06:14:25.184635Z **INFO**: Colonnes détectées: ['city', 'country', 'latitude', 'longitude', 'year', 'month', 'temperature_celsius', 'humidity_percent', 'precipitation_mm', 'wind_speed_ms', 'urban_heat_island_intensity', 'data_source']

- 2025-11-11T06:14:25.206830Z **INFO**: Missing per column (seulement > 0): {}

- 2025-11-11T06:14:27.767145Z INFO: Détection villes uniques pour n: 20

- 2025-11-11T06:14:27.923268Z INFO: d_participation=3.8005; d_pca90=4

- 2025-11-11T06:14:28.658811Z INFO: Calcul T_log successful: T_log=-0.298824; regime=Divergence; results saved to results\tlog_d_estimates.csv

- 2025-11-11T06:14:28.776883Z INFO: Start validation: n=20; d_estimate=3.9003; T_log=-0.298824

- 2025-11-11T06:14:28.943113Z INFO: LOO computed: mean_T=-0.353046; std_T=0.086006; rel_std_pct=24.36%

- 2025-11-11T06:14:28.962962Z INFO: Robustness relative std <10% : False

- 2025-11-11T06:14:28.984868Z INFO: T-test one-sample: t=-18.3577; p=0.000000

- 2025-11-11T06:14:30.356130Z INFO: Validation summary: mean_T_LOO=-0.353046; std_T_LOO=0.086006; rel_std_pct=24.36; pvalue=0.000000; robustness_flag=False

- 2025-11-11T06:14:30.468392Z INFO: LOO: sanitize complete (NaN replaced if any)

- 2025-11-11T06:14:30.485266Z INFO: SWEEP: sanitize complete (NaN replaced if any)

- 2025-11-11T06:14:30.505181Z INFO: SUMMARY: sanitize complete (NaN replaced if any)

- 2025-11-11T06:14:30.591353Z INFO: Final report generated: results\final_report.md

- 2025-11-11T06:14:30.638588Z INFO: Wrote locked params to results\params.json and README to results\README_method.md

- 2025-11-11T06:14:31.056215Z INFO: Locked d estimation completed: saved results\tlog_d_estimates_locked.csv and spectrum plot results\d_spectrum_locked.png

- 2025-11-11T06:14:31.647069Z INFO: Feature quality check started

- 2025-11-11T06:14:31.832245Z INFO: Computed robust stats and saved to results\feature_quality_stats.csv

- 2025-11-11T06:14:33.993311Z INFO: Saved hist, boxplot(winsor), QQ plots for each feature

- 2025-11-11T06:15:00.660818Z INFO: Saved time series plots for top cities: ['New York_USA_40.7128_-74.006', 'Los Angeles_USA_34.0522_-118.2437', 'Mexico City_Mexico_19.4326_-99.1332', 'São Paulo_Brazil_-23.5505_-46.6333', 'Delhi_India_28.7041_77.1025', 'Mumbai_India_19.076_72.8777']

- 2025-11-11T06:15:00.694707Z INFO: Saved Spearman correlation matrix

- 2025-11-11T06:15:00.810719Z INFO: Computed Mahalanobis scores (robust mcd available: True)

- 2025-11-11T06:15:00.845280Z INFO: Computed VIF for features

- 2025-11-11T06:15:00.870189Z INFO: Detected outliers summary saved to results\feature_outliers_detected.csv

- 2025-11-11T06:15:00.909664Z INFO: Feature quality report generated: results\feature_quality_report.md

- 2025-11-11T06:15:01.415094Z INFO: Robust comparison completed and saved to results\tlog_robust_comparison.csv and results\tlog_robust_comparison.png

- 2025-11-11T06:15:01.494182Z INFO: Comparative validation started for pipelines A/B/C

- 2025-11-11T06:15:01.746004Z INFO: Start pipeline A_baseline_StandardScaler

- 2025-11-11T06:15:02.763032Z INFO: Pipeline A_baseline_StandardScaler validation complete; results saved to results\pipeline_details

- 2025-11-11T06:15:02.782247Z INFO: Start pipeline B_winsor1-99_StandardScaler

- 2025-11-11T06:15:03.834490Z INFO: Pipeline B_winsor1-99_StandardScaler validation complete; results saved to results\pipeline_details

- 2025-11-11T06:15:03.854844Z INFO: Start pipeline C_MinCovDet_proj

- 2025-11-11T06:15:05.038437Z INFO: Pipeline C_MinCovDet_proj validation complete; results saved to results\pipeline_details

- 2025-11-11T06:15:05.429570Z INFO: Comparative validation finished; overview saved to results\tlog_pipelines_overview.csv; report: results\pipelines_comparative_report.md; comparative image: results\pipelines_comparative_overview.png

- 2025-11-11T06:15:05.503910Z INFO: Temporal CV started

- 2025-11-11T06:15:09.528554Z INFO: Temporal CV annual complete: saved results\temporal_cv\temporal_cv_annual.csv

- 2025-11-11T06:15:17.412478Z INFO: Temporal CV 3yr complete: saved results\temporal_cv\temporal_cv_3yr.csv

- 2025-11-11T06:15:17.430682Z INFO: Temporal CV finished; report saved to results\temporal_cv_report.md

- 2025-11-11T06:15:20.585181Z INFO: Exported atypical window 3yr_1984.00_A -> temporal_cv_atypical_period_window_3yr_1984.00_A_raw.csv (740 rows)

- 2025-11-11T06:15:20.623232Z INFO: Exported atypical window 3yr_1984.00_B -> temporal_cv_atypical_period_window_3yr_1984.00_B_raw.csv (740 rows)

- 2025-11-11T06:15:20.659822Z INFO: Exported atypical window 3yr_1984.00_C -> temporal_cv_atypical_period_window_3yr_1984.00_C_raw.csv (740 rows)

- 2025-11-11T06:15:20.694952Z INFO: Exported atypical window 3yr_2014.00_A -> temporal_cv_atypical_period_window_3yr_2014.00_A_raw.csv (740 rows)

- 2025-11-11T06:15:20.729373Z INFO: Exported atypical window 3yr_2014.00_B -> temporal_cv_atypical_period_window_3yr_2014.00_B_raw.csv (740 rows)

- 2025-11-11T06:15:20.762436Z INFO: Exported atypical window 3yr_2014.00_C -> temporal_cv_atypical_period_window_3yr_2014.00_C_raw.csv (740 rows)

- 2025-11-11T06:15:20.794392Z INFO: Exported atypical window annual_2003.00_A -> temporal_cv_atypical_period_window_annual_2003.00_A_raw.csv (260 rows)

- 2025-11-11T06:15:20.826304Z INFO: Exported atypical window annual_2003.00_C -> temporal_cv_atypical_period_window_annual_2003.00_C_raw.csv (260 rows)

- 2025-11-11T06:15:20.858957Z INFO: Exported atypical window annual_2008.00_A -> temporal_cv_atypical_period_window_annual_2008.00_A_raw.csv (260 rows)

- 2025-11-11T06:15:20.888246Z INFO: Exported atypical window annual_2008.00_B -> temporal_cv_atypical_period_window_annual_2008.00_B_raw.csv (260 rows)

- 2025-11-11T06:15:20.915846Z INFO: Exported atypical window annual_2008.00_C -> temporal_cv_atypical_period_window_annual_2008.00_C_raw.csv (260 rows)

- 2025-11-11T06:15:20.943030Z INFO: Exported atypical window annual_2012.00_A -> temporal_cv_atypical_period_window_annual_2012.00_A_raw.csv (260 rows)

- 2025-11-11T06:15:20.971025Z INFO: Exported atypical window annual_2012.00_B -> temporal_cv_atypical_period_window_annual_2012.00_B_raw.csv (260 rows)

- 2025-11-11T06:15:21.003294Z INFO: Exported atypical window annual_2012.00_C -> temporal_cv_atypical_period_window_annual_2012.00_C_raw.csv (260 rows)

- 2025-11-11T06:15:21.034093Z INFO: Exported atypical window annual_2014.00_A -> temporal_cv_atypical_period_window_annual_2014.00_A_raw.csv (260 rows)

- 2025-11-11T06:15:21.063327Z INFO: Exported atypical window annual_2014.00_C -> temporal_cv_atypical_period_window_annual_2014.00_C_raw.csv (260 rows)

- 2025-11-11T06:15:21.094104Z INFO: Exported atypical window annual_2016.00_A -> temporal_cv_atypical_period_window_annual_2016.00_A_raw.csv (260 rows)

- 2025-11-11T06:15:21.123337Z INFO: Exported atypical window annual_2016.00_B -> temporal_cv_atypical_period_window_annual_2016.00_B_raw.csv (260 rows)

- 2025-11-11T06:15:21.152397Z INFO: Exported atypical window annual_2016.00_C -> temporal_cv_atypical_period_window_annual_2016.00_C_raw.csv (260 rows)

- 2025-11-11T06:15:21.160018Z INFO: Export atypical windows completed; index saved to results\temporal_cv_atypical_windows\temporal_cv_atypical_periods_windows_index.csv
- 2025-11-11T06:15:28.442207Z INFO: Produced diagnostics for window 3yr_1984.0_A -> results\temporal_cv_atypical_windows\diagnostics\3yr_1984.0_A (rows=740, features=5)
- 2025-11-11T06:15:29.134846Z INFO: Produced diagnostics for window 3yr_1984.0_B -> results\temporal_cv_atypical_windows\diagnostics\3yr_1984.0_B (rows=740, features=5)
- 2025-11-11T06:15:29.883476Z INFO: Produced diagnostics for window 3yr_1984.0_C -> results\temporal_cv_atypical_windows\diagnostics\3yr_1984.0_C (rows=740, features=5)
- 2025-11-11T06:15:30.650201Z INFO: Produced diagnostics for window 3yr_2014.0_A -> results\temporal_cv_atypical_windows\diagnostics\3yr_2014.0_A (rows=740, features=5)
- 2025-11-11T06:15:31.387996Z INFO: Produced diagnostics for window 3yr_2014.0_B -> results\temporal_cv_atypical_windows\diagnostics\3yr_2014.0_B (rows=740, features=5)
- 2025-11-11T06:15:32.301390Z INFO: Produced diagnostics for window 3yr_2014.0_C -> results\temporal_cv_atypical_windows\diagnostics\3yr_2014.0_C (rows=740, features=5)
- 2025-11-11T06:15:33.017850Z INFO: Produced diagnostics for window annual_2003.0_A -> results\temporal_cv_atypical_windows\diagnostics\annual_2003.0_A (rows=260, features=5)
- 2025-11-11T06:15:33.744031Z INFO: Produced diagnostics for window annual_2003.0_C -> results\temporal_cv_atypical_windows\diagnostics\annual_2003.0_C (rows=260, features=5)
- 2025-11-11T06:15:34.553361Z INFO: Produced diagnostics for window annual_2008.0_A -> results\temporal_cv_atypical_windows\diagnostics\annual_2008.0_A (rows=260, features=5)
- 2025-11-11T06:15:35.282235Z INFO: Produced diagnostics for window annual_2008.0_B -> results\temporal_cv_atypical_windows\diagnostics\annual_2008.0_B (rows=260, features=5)
- 2025-11-11T06:15:35.959556Z INFO: Produced diagnostics for window annual_2008.0_C -> results\temporal_cv_atypical_windows\diagnostics\annual_2008.0_C (rows=260, features=5)
- 2025-11-11T06:15:36.695698Z INFO: Produced diagnostics for window annual_2012.0_A -> results\temporal_cv_atypical_windows\diagnostics\annual_2012.0_A (rows=260, features=5)
- 2025-11-11T06:15:37.449219Z INFO: Produced diagnostics for window annual_2012.0_B -> results\temporal_cv_atypical_windows\diagnostics\annual_2012.0_B (rows=260, features=5)
- 2025-11-11T06:15:38.202370Z INFO: Produced diagnostics for window annual_2012.0_C -> results\temporal_cv_atypical_windows\diagnostics\annual_2012.0_C (rows=260, features=5)
- 2025-11-11T06:15:38.982682Z INFO: Produced diagnostics for window annual_2014.0_A -> results\temporal_cv_atypical_windows\diagnostics\annual_2014.0_A (rows=260, features=5)
- 2025-11-11T06:15:39.713268Z INFO: Produced diagnostics for window annual_2014.0_C -> results\temporal_cv_atypical_windows\diagnostics\annual_2014.0_C (rows=260, features=5)
- 2025-11-11T06:15:40.440917Z INFO: Produced diagnostics for window annual_2016.0_A -> results\temporal_cv_atypical_windows\diagnostics\annual_2016.0_A (rows=260, features=5)
- 2025-11-11T06:15:41.471627Z INFO: Produced diagnostics for window annual_2016.0_B -> results\temporal_cv_atypical_windows\diagnostics\annual_2016.0_B (rows=260, features=5)
- 2025-11-11T06:15:42.258931Z INFO: Produced diagnostics for window annual_2016.0_C -> results\temporal_cv_atypical_windows\diagnostics\annual_2016.0_C (rows=260, features=5)

- Re-exécution Bloc 1: 2025-11-11T06:20:43.697523Z

- 2025-11-11T06:20:44.189101Z **INFO**: Tentative d'authentification Kaggle...

- 2025-11-11T06:20:44.207850Z **INFO**: Clés lues et définies via C:\Users\zackd\.kaggle\kaggle.json.

- 2025-11-11T06:20:44.226881Z **SUCCESS**: Authentification Kaggle réussie.

- 2025-11-11T06:20:44.244642Z **INFO**: Téléchargement et décompression du dataset : krishd123/urban-air-quality-and-climate-dataset-1958-2025

- 2025-11-11T06:20:45.961116Z **SUCCESS**: Téléchargement et préparation du fichier : data\urban_climate.csv

- 2025-11-11T06:20:45.978267Z **INFO**: Tentative de lecture du CSV : data\urban_climate.csv

- 2025-11-11T06:20:46.034655Z **SUCCESS**: Chargement réussi: data\urban_climate.csv; rows=11040; cols=12

- 2025-11-11T06:20:46.050283Z **INFO**: Colonnes détectées: ['city', 'country', 'latitude', 'longitude', 'year', 'month', 'temperature_celsius', 'humidity_percent', 'precipitation_mm', 'wind_speed_ms', 'urban_heat_island_intensity', 'data_source']

- 2025-11-11T06:20:46.075328Z **INFO**: Missing per column (seulement > 0): {}

- 2025-11-11T06:20:48.666155Z INFO: Détection villes uniques pour n: 20

- 2025-11-11T06:20:48.720025Z INFO: d_participation=3.8005; d_pca90=4

- 2025-11-11T06:20:49.209364Z INFO: Calcul T_log successful: T_log=-0.298824; regime=Divergence; results saved to results\tlog_d_estimates.csv

- 2025-11-11T06:20:49.292280Z INFO: Start validation: n=20; d_estimate=3.9003; T_log=-0.298824

- 2025-11-11T06:20:49.417326Z INFO: LOO computed: mean_T=-0.353046; std_T=0.086006; rel_std_pct=24.36%

- 2025-11-11T06:20:49.435468Z INFO: Robustness relative std <10% : False

- 2025-11-11T06:20:49.456415Z INFO: T-test one-sample: t=-18.3577; p=0.000000

- 2025-11-11T06:20:50.407530Z INFO: Validation summary: mean_T_LOO=-0.353046; std_T_LOO=0.086006; rel_std_pct=24.36; pvalue=0.000000; robustness_flag=False

- 2025-11-11T06:20:50.503286Z INFO: LOO: sanitize complete (NaN replaced if any)

- 2025-11-11T06:20:50.520719Z INFO: SWEEP: sanitize complete (NaN replaced if any)

- 2025-11-11T06:20:50.537693Z INFO: SUMMARY: sanitize complete (NaN replaced if any)

- 2025-11-11T06:20:50.619596Z ERROR: Erreur Bloc 5 finalisation: Missing optional dependency 'tabulate'.  Use pip or conda to install tabulate.

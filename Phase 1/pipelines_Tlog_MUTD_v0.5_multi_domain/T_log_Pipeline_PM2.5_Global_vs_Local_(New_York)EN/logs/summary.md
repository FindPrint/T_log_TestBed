# Session Log T_log V0.1

- Session started: 2025-11-11T07:14:33.220348+00:00
- Conventions: bias=0 by default, seeds fixed (42), outputs in results/

---
## Bloc 1 — Préparation
- Imports, seeds, dossiers et logger configurés.
- Env check plot: results/env_check_plot.png


- 2025-11-11T07:14:41.864797Z **INFO**: Tentative d'authentification Kaggle...

- 2025-11-11T07:14:41.884043Z **INFO**: Clés lues et définies via C:\Users\zackd\.kaggle\kaggle.json.

- 2025-11-11T07:14:41.894173Z **SUCCESS**: Authentification Kaggle réussie.

- 2025-11-11T07:14:41.913305Z **INFO**: Téléchargement et décompression du dataset : krishd123/urban-air-quality-and-climate-dataset-1958-2025

- 2025-11-11T07:14:42.323028Z **SUCCESS**: Téléchargement et préparation du fichier : data\urban_climate.csv

- 2025-11-11T07:14:42.340038Z **INFO**: Tentative de lecture du CSV : data\urban_climate.csv

- 2025-11-11T07:14:42.394511Z **SUCCESS**: Chargement réussi: data\urban_climate.csv; rows=11040; cols=12

- 2025-11-11T07:14:42.415601Z **INFO**: Colonnes détectées: ['city', 'country', 'latitude', 'longitude', 'year', 'month', 'temperature_celsius', 'humidity_percent', 'precipitation_mm', 'wind_speed_ms', 'urban_heat_island_intensity', 'data_source']

- 2025-11-11T07:14:42.429869Z **INFO**: Missing per column (seulement > 0): {}

- 2025-11-11T07:14:42.551184Z **INFO**: Inspection du fichier data/air_quality_global.csv effectuée : 6480 lignes, 0 doublons
- 2025-11-11T07:14:42.564532+00:00 [INFO] Inspection du fichier data/air_quality_global.csv : 6480 lignes, 0 doublons

- 2025-11-11T07:15:46.985870Z **INFO**: Calcul T_log global effectué: n=6480, d=1, T_log=-26.3294, régime=Divergence
- 2025-11-11T07:15:47.030849+00:00 [INFO] Calcul T_log global (PM2.5): n=6480, d=1, T_log=-26.3294, régime=Divergence

- 2025-11-11T07:16:36.447938Z **INFO**: Calcul T_log New York effectué: n=324, d=1, T_log=-17.3422, régime=Divergence
- 2025-11-11T07:16:36.471617+00:00 [INFO] Calcul T_log (New York, PM2.5): n=324, d=1, T_log=-17.3422, régime=Divergence

- 2025-11-11T07:16:44.977707Z **INFO**: Sensibilité T_log(d) PM2.5 global sauvegardée: results/Tlog_vs_d_air_quality_global.png, results/Tlog_vs_d_air_quality_global.csv
- 2025-11-11T07:16:44.977707+00:00 [INFO] Sensibilité T_log(d) PM2.5 global : CSV=results/Tlog_vs_d_air_quality_global.csv, plot=results/Tlog_vs_d_air_quality_global.png

- 2025-11-11T07:17:09.817854Z **INFO**: Sensibilité T_log(d) PM2.5 New York sauvegardée: results/Tlog_vs_d_air_quality_NewYork.png, results/Tlog_vs_d_air_quality_NewYork.csv
- 2025-11-11T07:17:09.817854+00:00 [INFO] Sensibilité T_log(d) PM2.5 New York : CSV=results/Tlog_vs_d_air_quality_NewYork.csv, plot=results/Tlog_vs_d_air_quality_NewYork.png

- 2025-11-11T07:17:19.203020Z **INFO**: Sensibilité T_log(n) PM2.5 global sauvegardée: results/Tlog_vs_n_air_quality_global.png, results/Tlog_vs_n_air_quality_global.csv
- 2025-11-11T07:17:19.203020+00:00 [INFO] Sensibilité T_log(n) PM2.5 global : CSV=results/Tlog_vs_n_air_quality_global.csv, plot=results/Tlog_vs_n_air_quality_global.png

- 2025-11-11T07:17:25.152302Z **INFO**: Sensibilité T_log(n) PM2.5 New York sauvegardée: results/Tlog_vs_n_air_quality_NewYork.png, results/Tlog_vs_n_air_quality_NewYork.csv
- 2025-11-11T07:17:25.152302+00:00 [INFO] Sensibilité T_log(n) PM2.5 New York : CSV=results/Tlog_vs_n_air_quality_NewYork.csv, plot=results/Tlog_vs_n_air_quality_NewYork.png

- 2025-11-11T07:17:31.290048Z **INFO**: Comparaison T_log(n) Global vs New York sauvegardée: results/Tlog_vs_n_comparison_Global_vs_NewYork.png
- 2025-11-11T07:17:31.290048+00:00 [INFO] Comparaison T_log(n) Global vs New York : plot=results/Tlog_vs_n_comparison_Global_vs_NewYork.png

- 2025-11-11T07:17:35.963363Z **INFO**: Rapport intermédiaire sauvegardé: results/rapport_intermediaire_PM25.md
- 2025-11-11T07:17:35.999588+00:00 [INFO] Rapport intermédiaire sauvegardé: results/rapport_intermediaire_PM25.md

- 2025-11-11T07:18:07.208065Z **INFO**: Bootstrap T_log global: B=1000, mode=subsample, p=0.0000, IC=(-26.2832,-24.3240), plot=results/bootstrap_Tlog_global.png, CSV=results/bootstrap_Tlog_global.csv
- 2025-11-11T07:18:07.231125+00:00 [INFO] Bootstrap T_log global : B=1000, mode=subsample, p=0.0000, IC=(-26.2832,-24.3240), plot=results/bootstrap_Tlog_global.png, CSV=results/bootstrap_Tlog_global.csv

- 2025-11-11T07:18:34.258266Z **INFO**: Bootstrap T_log New York: B=1000, p=0.0060, IC=(-17.2958,-15.3360), plot=results/bootstrap_Tlog_NewYork.png, CSV=results/bootstrap_Tlog_NewYork.csv
- 2025-11-11T07:18:34.280666+00:00 [INFO] Bootstrap T_log New York : B=1000, p=0.0060, IC=(-17.2958,-15.3360), plot=results/bootstrap_Tlog_NewYork.png, CSV=results/bootstrap_Tlog_NewYork.csv

- 2025-11-11T07:19:13.212939Z **INFO**: Bootstrap multi-d (PM2.5) sauvegardé: CSV=results/bootstrap_multi_d_PM25_Global_NewYork.csv, plots=results/bootstrap_pvalues_vs_d_Global_NewYork.png, results/bootstrap_Tlog_distributions_multi_d.png
- 2025-11-11T07:19:13.233513+00:00 [INFO] Bootstrap multi-d (PM2.5) : CSV=results/bootstrap_multi_d_PM25_Global_NewYork.csv, plots=results/bootstrap_pvalues_vs_d_Global_NewYork.png, results/bootstrap_Tlog_distributions_multi_d.png

- 2025-11-11T07:19:35.958647Z **INFO**: Stress tests et diagnostics sauvegardés: rapport=results/stress_tests_diagnostics_PM25.md, figure=results/residuals_diagnostics_PM25.png
- 2025-11-11T07:19:35.994790+00:00 [INFO] Stress tests et diagnostics : rapport=results/stress_tests_diagnostics_PM25.md, figure=results/residuals_diagnostics_PM25.png

- 2025-11-11T07:19:53.840677Z **INFO**: Final consolidated report saved: results/final_report_PM25_en.md
- 2025-11-11T07:19:53.867673+00:00 [INFO] Final consolidated report saved: results/final_report_PM25_en.md
---
## Bloc 1 — Préparation
- Imports, seeds, dossiers et logger configurés.
- Env check plot: results/env_check_plot.png

- 2025-11-11T07:21:07.464411+00:00 [INFO] Inspection du fichier data/air_quality_global.csv : 6480 lignes, 0 doublons
- 2025-11-11T07:21:07.498043+00:00 [INFO] Calcul T_log global (PM2.5): n=6480, d=1, T_log=-26.3294, régime=Divergence
- 2025-11-11T07:21:07.529938+00:00 [INFO] Calcul T_log (New York, PM2.5): n=324, d=1, T_log=-17.3422, régime=Divergence
- 2025-11-11T07:21:07.709438+00:00 [INFO] Sensibilité T_log(d) PM2.5 global : CSV=results/Tlog_vs_d_air_quality_global.csv, plot=results/Tlog_vs_d_air_quality_global.png
- 2025-11-11T07:21:07.912675+00:00 [INFO] Sensibilité T_log(d) PM2.5 New York : CSV=results/Tlog_vs_d_air_quality_NewYork.csv, plot=results/Tlog_vs_d_air_quality_NewYork.png
- 2025-11-11T07:21:08.231961+00:00 [INFO] Sensibilité T_log(n) PM2.5 global : CSV=results/Tlog_vs_n_air_quality_global.csv, plot=results/Tlog_vs_n_air_quality_global.png
- 2025-11-11T07:21:08.474368+00:00 [INFO] Sensibilité T_log(n) PM2.5 New York : CSV=results/Tlog_vs_n_air_quality_NewYork.csv, plot=results/Tlog_vs_n_air_quality_NewYork.png
- 2025-11-11T07:21:08.704582+00:00 [INFO] Comparaison T_log(n) Global vs New York : plot=results/Tlog_vs_n_comparison_Global_vs_NewYork.png

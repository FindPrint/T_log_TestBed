# Feature Quality Report

Generated: 2025-11-11T06:15:00.889990Z

## Features analysées

- humidity_percent
- wind_speed_ms
- urban_heat_island_intensity

## Statistiques robustes (globales)

| feature                     |     n |   nan_prop |   min |   q1 |   median |    q3 |   max |     mean |       std |   IQR |   MAD |   skewness |   kurtosis |
|:----------------------------|------:|-----------:|------:|-----:|---------:|------:|------:|---------:|----------:|------:|------:|-----------:|-----------:|
| humidity_percent            | 11040 |          0 |    20 | 39.4 |     48.2 | 57.5  |  95   | 48.4329  | 12.7924   | 18.1  |   9   |  0.0736144 |  -0.398109 |
| wind_speed_ms               | 11040 |          0 |     1 |  5.9 |      8   | 10.2  |  17.2 |  8.03559 |  2.91646  |  4.3  |   2.1 |  0.0202912 |  -0.482843 |
| urban_heat_island_intensity | 11040 |          0 |     1 |  1   |      1   |  1.25 |   2   |  1.25    |  0.433032 |  0.25 |   0   |  1.15486   |  -0.666425 |

## Spearman correlation (per-city means)

|                             |   humidity_percent |   wind_speed_ms |   urban_heat_island_intensity |
|:----------------------------|-------------------:|----------------:|------------------------------:|
| humidity_percent            |           1        |       0.180451  |                    -0.190238  |
| wind_speed_ms               |           0.180451 |       1         |                    -0.0700877 |
| urban_heat_island_intensity |          -0.190238 |      -0.0700877 |                     1         |

## VIF

|                             |     VIF |
|:----------------------------|--------:|
| humidity_percent            | 1.09739 |
| wind_speed_ms               | 1.07297 |
| urban_heat_island_intensity | 1.03727 |

## Outliers summary

| feature                     | method      |   outliers_count |   outliers_prop |   low_thresh |   high_thresh | city_key                   |   mahalanobis |
|:----------------------------|:------------|-----------------:|----------------:|-------------:|--------------:|:---------------------------|--------------:|
| humidity_percent            | IQR         |                8 |     0.000724638 |       12.25  |        84.65  | nan                        |      nan      |
| wind_speed_ms               | IQR         |                3 |     0.000271739 |       -0.55  |        16.65  | nan                        |      nan      |
| urban_heat_island_intensity | IQR         |             2760 |     0.25        |        0.625 |         1.625 | nan                        |      nan      |
| multivariate                | Mahalanobis |              nan |   nan           |      nan     |       nan     | Dallas_USA_32.7767_-96.797 |       23.6277 |

## Plots générés

- results\feature_quality_plots\box_win_humidity_percent.png
- results\feature_quality_plots\box_win_urban_heat_island_intensity.png
- results\feature_quality_plots\box_win_wind_speed_ms.png
- results\feature_quality_plots\hist_humidity_percent.png
- results\feature_quality_plots\hist_urban_heat_island_intensity.png
- results\feature_quality_plots\hist_wind_speed_ms.png
- results\feature_quality_plots\qq_humidity_percent.png
- results\feature_quality_plots\qq_urban_heat_island_intensity.png
- results\feature_quality_plots\qq_wind_speed_ms.png
- results\feature_quality_plots\timeseries_Delhi_India_28.7041_77.1025.png
- results\feature_quality_plots\timeseries_Los Angeles_USA_34.0522_-118.2437.png
- results\feature_quality_plots\timeseries_Mexico City_Mexico_19.4326_-99.1332.png
- results\feature_quality_plots\timeseries_Mumbai_India_19.076_72.8777.png
- results\feature_quality_plots\timeseries_New York_USA_40.7128_-74.006.png
- results\feature_quality_plots\timeseries_São Paulo_Brazil_-23.5505_-46.6333.png


## Notes et recommandations

- Si proportion de valeurs manquantes >5% pour une feature, considérer imputation documentée.
- Pour outliers extrêmes, proposer winsorisation documentée (p%) ou vérification des métadonnées d'instrumentation.

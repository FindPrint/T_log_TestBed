Procédure verrouillée pour estimation de d (T_log V0.1)
Date génération: 2025-11-11T06:14:30.637507Z

Résumé des choix (verrouillés) :
- Agrégation temporelle : moyenne des features par ville (group by ['city', 'country', 'latitude', 'longitude'])
- Features utilisées (exact) : ['temperature_celsius', 'humidity_percent', 'precipitation_mm', 'wind_speed_ms', 'urban_heat_island_intensity']
- Prétraitement : StandardScaler (z-score) appliqué après agrégation
- Estimateurs de d :
  * Participation ratio (spectral) : d_part = (sum(eig))^2 / sum(eig^2)
  * PCA90 : d_pca90 = plus petit k tel que variance expliquée cumulée >= 0.90
  * Fusion : d = (d_part + d_pca90) / 2
- T_log : T_log = (d - 4) * ln(n_eff) avec n_eff = max(2, n_cities)
- Sanitization : clip d dans [0.1, 100.0]; n_min for ln = 2
- Seed : 42

Exécuter ce script de manière identique pour garantir reproductibilité.

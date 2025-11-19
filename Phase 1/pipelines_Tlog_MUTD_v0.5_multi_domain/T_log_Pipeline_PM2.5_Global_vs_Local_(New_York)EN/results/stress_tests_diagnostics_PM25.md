# Stress tests et diagnostics — T_log (PM2.5, Global vs New York)

## Résumé des métriques (d=1)
- Global: MSE=0.0000, RMSE=0.0000, MAE=0.0000, R²=1.0000
- New York: MSE=0.0000, RMSE=0.0000, MAE=0.0000, R²=1.0000

## Diagnostics des résidus
- Global: Shapiro W=1.000, p=1.000; KS stat=nan, p=nan; ACF=[nan, nan, nan, nan]
- New York: Shapiro W=0.630, p=0.001; KS stat=0.468, p=0.249; ACF=[1.0, -0.08333333333333333, -0.16666666666666666, -0.25]
- Figure résidus: results/residuals_diagnostics_PM25.png

## Validation croisée (régression T_log ~ ln(n))
- Global: CV-MSE=0.0000 (± 0.0000), coeffs a=-3.0000, b=-0.0000
- New York: CV-MSE=0.0000 (± 0.0000), coeffs a=-3.0000, b=-0.0000

## Stress tests
- Global: MSE(noise)=3.3783, MSE(drop)=0.0000, extrapolation n=12960 → T_pred=-29.765, T_theory=-28.409, |Δ|=1.356
- New York: MSE(noise)=0.1290, MSE(drop)=0.0000, extrapolation n=648 → T_pred=-18.812, T_theory=-19.422, |Δ|=0.610

---
*Rapport généré le 2025-11-11T07:19:35.956649+00:00*
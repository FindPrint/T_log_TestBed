# PM2.5 Global vs Local (New York) – Partie 2 (cellules 10–19) : T_log global, T_log New York et sensibilité en fonction de d

## 1. Périmètre de la partie

Cette deuxième partie correspond aux cellules **10–19** du notebook `PM25_part02.ipynb`, dérivé de `T_log_Pipeline_PM2.5_Global_vs_Local_(New_York)EN.ipynb`.

Elle réalise les **premiers calculs de T_log** sur les données PM2.5 :

- calcul de `T_log` en mode **global** (toutes les villes, n=6480) ;
- calcul de `T_log` en mode **local New York** (n=324) ;
- étude de la **sensibilité de T_log en fonction de la dimension d** (1 ≤ d ≤ 6) pour :
  - le cas global (PM2.5 global) ;
  - le cas local (New York).

Ces calculs restent dans le cadre simple **d=1** pour les premiers T_log (séries temporelles scalaires), puis explorent des d hypothétiques pour illustrer la structure du modèle.

---

## 2. Bloc 3b – Calcul de T_log sur PM2.5 global (air_quality_global.csv)

### 2.1 Méthode

- Chargement du dataset complet : `data/air_quality_global.csv` (validé en Partie 1). 
- Construction d’un sous-dataframe :

  - `df_pm25 = df_aq[['city','year','month','pm25_ugm3']]` → toutes les villes, tous les mois, toutes les années.

- Paramètres :

  - `n = len(df_pm25) = 6480` (20 villes × 27 ans × 12 mois) ;
  - `d = 1` (série temporelle scalaire) ;
  - `biais = 0.0`.

- Définition de la fonction :

\[
T_{\log}(n,d) = (d-4) \ln(n) + \text{biais}, \quad n_{eff} = \max(n,2).
\]

- Classification du régime :

  - `T_log > 0` → Saturation ;
  - `T_log ≈ 0` (|T_log| < 1e−6) → Équilibre ;
  - `T_log < 0` → Divergence.

- Sauvegarde des résultats dans :

  - `results/Tlog_air_quality_global.csv` (scope, n, d, T_log, regime) ;
  - log dans `logs/logs.csv` + `logs/summary.md` via `log_event` et `append_summary_md`.

### 2.2 Résultats

- Valeurs manquantes PM2.5 : 0 (robuste) ;
- Paramètres : `n = 6480`, `d = 1` ;
- Calcul :

\[
T_{\log}(6480,1) = (1-4) \ln(6480) \approx -26.33.
\]

- Régime : **Divergence**.

Interprétation :

- À d=1 (< 4), le facteur `(d-4)` est négatif ;
- pour un n global très grand (6480), `ln(n)` est élevé → le produit `(d-4) ln(n)` devient fortement négatif ;
- le système PM2.5 global (20 villes) est dans un **régime de Divergence marqué**.

Ce résultat illustre la logique du modèle :

- *à dimension fixe*, plus n est grand, plus T_log devient négatif (si d < 4).

---

## 3. Bloc 3c – Calcul de T_log sur PM2.5 local (New York)

### 3.1 Méthode

- Relecture de `air_quality_global.csv` ;
- filtrage :

  - `df_ny = df_aq[df_aq['city'] == 'New York'][['year','month','pm25_ugm3']]` ;

- Paramètres :

  - `n = len(df_ny) = 324` (27 ans × 12 mois) ;
  - `d = 1` (série temporelle scalaire) ;
  - `biais = 0.0`.

- Même fonction `compute_Tlog` que pour le cas global ;
- classification de régime identique ;
- sauvegarde dans :

  - `results/Tlog_air_quality_NewYork.csv` ;
  - log + résumé dans `logs/logs.csv` et `logs/summary.md`.

### 3.2 Résultats

- Valeurs manquantes PM2.5 (New York) : 0 ;
- Paramètres : `n = 324`, `d = 1` ;

\[
T_{\log}(324,1) = (1-4) \ln(324) \approx -17.34.
\]

- Régime : **Divergence** (instabilité) ;

Interprétation :

- New York, considérée seule, reste en régime **Divergence** ;
- la magnitude |T_log| est moins grande qu’en mode global (−17.34 vs −26.33) car n est plus faible ;
- cela est cohérent avec la dépendance logarithmique : 
  - à dimension d fixe, la **taille du système n** contrôle la profondeur de la divergence.

---

## 4. Bloc 4a – Sensibilité de T_log en fonction de d (PM2.5 global, n = 6480)

### 4.1 Méthode

Ce bloc explore théoriquement l’effet de d sur T_log pour le cas global :

- Paramètres :

  - `n_fixed = 6480` ;
  - `d_values = 1..6` ;
  - `biais = 0.0`.

- Pour chaque d dans {1,2,3,4,5,6} :

\[
T_{\log}(n_{fixed}, d) = (d-4) \ln(n_{fixed}).
\]

- Régime déterminé comme précédemment ;
- sauvegarde des résultats dans :

  - `results/Tlog_vs_d_air_quality_global.csv` ;
  - figure `results/Tlog_vs_d_air_quality_global.png` (courbe T_log(d) avec ligne horizontale à 0) ;
  - logs et summary mis à jour.

### 4.2 Résultats

Tableau obtenu :

| d | n    | T_log     | régime      |
|---|------|-----------|------------|
| 1 | 6480 | -26.33    | Divergence |
| 2 | 6480 | -17.55    | Divergence |
| 3 | 6480 | -8.78     | Divergence |
| 4 | 6480 | 0.00      | Équilibre  |
| 5 | 6480 | +8.78     | Saturation |
| 6 | 6480 | +17.55    | Saturation |

Interprétation :

- on observe clairement la **dimension critique d_c = 4** :
  - d < 4 → T_log < 0 → régimes de Divergence ;
  - d = 4 → T_log = 0 → Équilibre ;
  - d > 4 → T_log > 0 → Saturation ;
- à n fixé (6480), la courbe T_log(d) est **linéaire en d** et passe par 0 à d=4 ;
- cette figure sert de **référence théorique** pour interpréter des valeurs de d_est obtenues plus tard (par exemple via dimension spectrale ou autres estimateurs).

---

## 5. Bloc 4b – Sensibilité de T_log en fonction de d (PM2.5 New York, n = 324)

### 5.1 Méthode

Même analyse, mais pour la série locale New York :

- Paramètres :

  - `n_fixed = 324` ;
  - `d_values = 1..6` ;
  - `biais = 0.0`.

- Calcul de T_log(n_fixed, d) pour d=1..6 ;
- sauvegarde dans :

  - `results/Tlog_vs_d_air_quality_NewYork.csv` ;
  - plot `results/Tlog_vs_d_air_quality_NewYork.png` (courbe T_log(d), en rouge) ;
  - logs + résumé.

### 5.2 Résultats

Tableau obtenu :

| d | n   | T_log     | régime      |
|---|-----|-----------|------------|
| 1 | 324 | -17.34    | Divergence |
| 2 | 324 | -11.56    | Divergence |
| 3 | 324 | -5.78     | Divergence |
| 4 | 324 | 0.00      | Équilibre  |
| 5 | 324 | +5.78     | Saturation |
| 6 | 324 | +11.56    | Saturation |

Interprétation :

- la structure qualitative est **identique** au cas global :
  - d < 4 → Divergence ;
  - d = 4 → Équilibre ;
  - d > 4 → Saturation ;
- la pente de T_log(d) est légèrement différente car `ln(324)` < `ln(6480)`, mais la **dimension critique** reste d_c = 4 ;
- mettre sur le même graphique (global vs New York) permettrait de visualiser l’effet de n sur la pente, tout en conservant la même transition à d=4.

---

## 6. Rôle de la Partie 2 dans le pipeline PM2.5 Global vs Local

Cette Partie 2 constitue le **premier niveau d’application du modèle T_log** au cas PM2.5 :

- **T_log global (20 villes, n=6480, d=1)** :
  - `T_log ≈ -26.33` → **Divergence forte**, robuste (données complètes, 0 NA) ;

- **T_log local (New York, n=324, d=1)** :
  - `T_log ≈ -17.34` → **Divergence**, plus modérée que le global, ce qui illustre l’effet de la taille du système ;

- **Sensibilité T_log(d)** (global et New York) :
  - confirme la **dimension critique d_c = 4** comme frontière théorique entre Divergence/Équilibre/Saturation ;
  - fournit une grille de lecture pour des valeurs futures de d_est (dimension effective) à insérer dans T_log.

En résumé, la Partie 2 :

- montre que, pour PM2.5 global et local (New York), le modèle T_log **classe clairement le système en Divergence** lorsque l’on adopte d=1 ;
- établit le lien qualitatif et quantitatif entre **taille du système n** et profondeur de la divergence ;
- pose la base théorique nécessaire pour, plus tard, remplacer d=1 par une **dimension effective estimée** (p.ex. via méthodes graph-spectrales ou dimensions intrinsèques), comme cela a été fait dans le pipeline Sunspots.

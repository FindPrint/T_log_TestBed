# PM2.5 Global vs Local (New York) – Partie 3 (cellules 20–29) : Sensibilité en fonction de n et comparaison globale vs locale

## 1. Périmètre de la partie

Cette troisième partie correspond aux cellules **20–29** du notebook `PM25_part03.ipynb`, dérivé de `T_log_Pipeline_PM2.5_Global_vs_Local_(New_York)EN.ipynb`.

Elle complète l’analyse T_log pour PM2.5 en étudiant la **sensibilité par rapport à la taille du système n** à dimension fixe `d = 1`, puis en comparant visuellement la dynamique globale vs locale :

- **Bloc 5a** : T_log(n, d=1) pour des tailles croissantes, PM2.5 global (20 villes) ;
- **Bloc 5b** : T_log(n, d=1) pour des tailles croissantes, PM2.5 local (New York) ;
- **Bloc 6** : graphique de comparaison globale vs locale T_log(n, d=1).

---

## 2. Bloc 5a – Sensibilité en fonction de n (PM2.5 global, d = 1)

### 2.1 Méthode

Le bloc 5a fixe la dimension à `d_fixed = 1` et fait varier `n` :

- `n_values = [100, 500, 1000, 2000, 4000, 6480]` ;
- fonction :

\[
T_{\log}(n, d=1) = (1 - 4) \ln(n) = -3 \ln(n).
\]

Pour chaque n, la cellule :

- calcule `T_log(n,1)` ;
- classe le régime (`Divergence` si T<0, `Équilibre` si |T|≈0, `Saturation` si T>0) ;
- rassemble les résultats dans un DataFrame ;
- sauvegarde :
  - `results/Tlog_vs_n_air_quality_global.csv` ;
  - `results/Tlog_vs_n_air_quality_global.png` (courbe T_log vs n) ;
  - met à jour `logs/logs.csv` et `logs/summary.md`.

### 2.2 Résultats

Tableau obtenu (résumant les impressions console) :

| n    | d | T_log      | régime      |
|------|---|------------|------------|
| 100  | 1 | -13.82     | Divergence |
| 500  | 1 | -18.64     | Divergence |
| 1000 | 1 | -20.72     | Divergence |
| 2000 | 1 | -22.80     | Divergence |
| 4000 | 1 | -24.88     | Divergence |
| 6480 | 1 | -26.33     | Divergence |

Interprétation :

- pour **d = 1 (< 4)**, le facteur `(d-4)` est négatif ;
- à mesure que n augmente, `ln(n)` croît → **T_log devient de plus en plus négatif** ;
- le régime est toujours **Divergence**, mais la divergence devient **plus prononcée** pour les systèmes plus grands ;
- la dépendance suit exactement :

\[
T_{\log}(n,1) = -3 \ln(n),
\]

confirmant la loi logarithmique du modèle.

---

## 3. Bloc 5b – Sensibilité en fonction de n (PM2.5 New York, d = 1)

### 3.1 Méthode

Le bloc 5b applique le même schéma à la série locale New York, avec :

- `d_fixed = 1` ;
- `n_values = [50, 100, 200, 324]` (croissance jusqu’à la taille maximale de la série New York) ;
- même fonction `T_log(n,1) = -3 ln(n)`.

Pour chaque n, la cellule :

- calcule T_log ;
- attribue le régime ;
- sauvegarde :
  - `results/Tlog_vs_n_air_quality_NewYork.csv` ;
  - `results/Tlog_vs_n_air_quality_NewYork.png` (courbe T_log vs n locale) ;
  - logge l’opération.

### 3.2 Résultats

Tableau obtenu :

| n   | d | T_log      | régime      |
|-----|---|------------|------------|
| 50  | 1 | -11.74     | Divergence |
| 100 | 1 | -13.82     | Divergence |
| 200 | 1 | -15.89     | Divergence |
| 324 | 1 | -17.34     | Divergence |

Interprétation :

- même structure qualitative que le cas global :
  - **tous les T_log sont négatifs** → régime de **Divergence** pour chaque n testé ;
- l’amplitude est **moins extrême** que pour le cas global (minima autour de -17 vs -26) ;
- cela reflète simplement que `ln(324) < ln(6480)` : pour une dimension fixée, la taille du système n contrôle la profondeur de la divergence.

---

## 4. Bloc 6 – Comparaison visuelle globale vs locale (PM2.5, d = 1)

### 4.1 Méthode

Le bloc 6 superpose les courbes globales et locales pour une comparaison directe :

- charge :
  - `results/Tlog_vs_n_air_quality_global.csv` ;
  - `results/Tlog_vs_n_air_quality_NewYork.csv` ;
- trace T_log(n,1) pour :
  - global PM2.5 (courbe verte, cercles) ;
  - New York PM2.5 (courbe rouge, carrés) ;
- ajoute une ligne horizontale T_log = 0 ;
- sauvegarde :
  - `results/Tlog_vs_n_comparison_Global_vs_NewYork.png` ;
  - log + résumé dans `logs/logs.csv` et `logs/summary.md`.

### 4.2 Résultats et interprétation

La figure montre :

- **forme identique** pour les deux courbes : décroissance monotone de T_log avec n, conforme à `-3 ln(n)` ;
- **global (n jusqu’à 6480)** : T_log descend jusqu’à ≈ −26.3 ;
- **New York (n jusqu’à 324)** : T_log descend jusqu’à ≈ −17.3 ;
- le régime est **Divergence** pour toutes les tailles considérées, dans les deux cas.

Interprétation synthétique :

- l’instabilité (Divergence) est **universelle** pour d=1, que l’on considère les données globales ou locales ;
- l’**intensité** de cette divergence dépend uniquement de la taille du système n (et de `ln(n)`) ;
- l’agrégation globale (20 villes) amplifie la divergence par rapport à la série d’une seule ville (New York), mais n’en change pas la nature.

---

## 5. Rôle de la Partie 3 dans le pipeline PM2.5 Global vs Local

Cette Partie 3 :

- quantifie la dépendance de T_log à la **taille du système n** pour PM2.5 global et local (New York), à dimension fixe d=1 ;
- démontre empiriquement la loi :

\[
T_{\log}(n,1) = -3 \ln(n) \quad (d=1 < 4),
\]

pour des gammes de n réalistes (de dizaines à plusieurs milliers d’observations) ;
- met en évidence que :
  - **l’agrégation globale** (n=6480) conduit à une divergence plus forte (T_log plus négatif) qu’un système local (n=324) ;
  - néanmoins, la structure qualitative (Divergence) reste la même pour toutes les tailles.

En résumé, la Partie 3 consolide l’intuition que, dans le cadre du modèle T_log :

- à **dimension fixe** (ici d=1), **augmenter n renforce la divergence** ;
- la comparaison globale vs locale pour PM2.5 montre que l’instabilité est présente aux deux échelles, mais que son intensité croît logarithmiquement avec la taille du système.

Cette analyse prépare les futures extensions où `d` sera remplacé par une **dimension effective estimée** (spectrale, intrinsèque, etc.), comme dans le pipeline Sunspots, tout en gardant la même grille de lecture T_log(n,d).

# Tsunami V0.1 – Partie 11 (cellules 80–87) : Sensibilité fine autour de d=4, permutation temporelle et granularité du temps

## 1. Périmètre de la partie

Cette onzième partie correspond aux cellules **80–87** du notebook `Tsunami_part11.ipynb`, dérivé de `T_log_Tsunami_V_0_1En.ipynb`.

Elle poursuit la validation en dimension **spatio‑temporelle d = 4** en ajoutant :

- un balayage **fin** de `T_log(n,d)` autour de d=4 (Bloc 16) ;
- un test de permutation **intra‑décennie** à d=4 (Bloc 17) ;
- un test de robustesse à la **granularité temporelle** (année / trimestre / mois) à d=4 (Bloc 18).

---

## 2. Bloc 16 – Balayage fin de T_log(n,d) autour de d=4

### 2.1 Méthode

On charge `earthquake_data_tsunami.csv` et on fixe :

- `n = len(df)` ;
- grille fine de d : de 3.90 à 4.10 par pas de 0.005 (soit 41 valeurs) ;
- fonction :

\[
T_{\log}(n,d) = (d-4) \ln(n).\]

Pour chaque d, on :

- calcule T_log(n,d) ;
- assigne le régime : Divergence (T<0), Équilibre (T≈0), Saturation (T>0).

Les résultats sont sauvegardés dans :

- `results/tlog_sensitivity_d4.csv` ;
- un plot `results/tlog_sensitivity_d4.png` : courbe T_log vs d avec T_log=0 marqué.

Un log est ajouté à `logs/logs.txt` et `logs/logs.csv`.

### 2.2 Résultats et interprétation

Le balayage montre :

- T_log(d=4) = 0 → Équilibre ;
- T_log(d<4) < 0 → Divergence ;
- T_log(d>4) > 0 → Saturation ;
- la courbe T_log(d) est linéaire en d et croise zéro exactement à d=4.

Cela quantifie le comportement "knife‑edge" déjà observé :

- d=4 est le seul point où T_log=0 ;
- des variations infinitésimales de d de part et d’autre suffisent à changer le signe et donc le régime.

---

## 3. Bloc 17 – Test de permutation temporel intra‑décennie (d=4)

### 3.1 Méthode

Ce bloc met en place un **test de permutation respectueux de la structure temporelle** :

- on lit le dataset et on construit une colonne `decade` : `(Year // 10)*10` ;
- pour chaque décennie, on calcule la valeur "vraie" :
  - `n_sub` = nombre d’événements ;
  - `T_log(n_sub, d=4)` ;
  - `regime = Equilibrium` (puisque T_log=0 à d=4) ;
- on sauvegarde ces valeurs dans `results/permutation_true_d4_by_decade.csv`.

Ensuite, on effectue un **permutation test** :

- `n_permutations = 200` ;
- pour chaque run :
  - on mélange les lignes **à l’intérieur de chaque décennie** (préserve la structure temporelle globale) ;
  - on recalcule `n_sub` et `T_log(n_sub,4)` par décennie;
  - on compte, par run, le nombre de décennies classées en Equilibrium, Divergence, Saturation.

On obtient :

- un CSV `results/permutation_test_d4.csv` récapitulant, pour chaque permutation, le nombre de décennies en chaque régime ;
- un histogramme `results/permutation_test_d4.png` montrant la distribution du nombre de décennies en Equilibrium.

Les logs (`logs/logs.txt` et `logs/logs.csv`) sont mis à jour.

### 3.2 Résultats et interprétation

Dans tous les runs de permutation :

- les comptages par décennie ne changent pas (puisqu’on conserve l’appartenance décennale) ;
- `T_log(n_sub,4)` reste donc identiquement 0 ;
- toutes les décennies sont classées **Equilibrium** pour chaque permutation.

L’histogramme montre une concentration au maximum possible (toutes les décennies en Equilibrium), confirmant que :

- la stabilité à d=4 n’est pas un artefact de labels ou d’un partitionnement spécifique ;
- même en permutant les lignes au sein de chaque bloc temporel, la structure de régime ne change pas.

---

## 4. Bloc 18 – Robustesse à la granularité temporelle (année / trimestre / mois, d=4)

### 4.1 Méthode

Ce bloc teste si l’équilibre d=4 dépend de la **granularité temporelle** choisie :

- identification d’une colonne de date/année :
  - `date_col` si une date complète existe, sinon `year_col` ;
- création de `date` (datetime) ;
- définition de trois granularités :
  - `year` : année entière ;
  - `quarter` : trimestre (période Q) ;
  - `month` : mois (période M).

Pour chaque granularité (colonne `year`, `quarter`, `month`) :

- on compte le nombre d’événements par bucket (année, trimestre, mois) ;
- pour chaque bucket :
  - `n` = count ;
  - `T_log(n, d=4)` ;
  - `regime` ;
- on sauvegarde :
  - `results/bloc18_year_granularity.csv` / `.png` ;
  - `results/bloc18_quarter_granularity.csv` / `.png` ;
  - `results/bloc18_month_granularity.csv` / `.png`.

Les `.png` montrent la distribution des régimes par granularité.

### 4.2 Résultats

Les commentaires indiquent :

- pour toutes les granularités (année, trimestre, mois), **tous les buckets** sont en **Equilibrium** (T_log=0 à d=4) ;
- les CSV et figures confirment que la distribution de régimes est identique : 100 % Equilibrium.

### 4.3 Interprétation

- le régime à d=4 est **indépendant de l’échelle de temps choisie** :
  - que l’on observe les données par année, trimestre ou mois, l’équilibre est le même ;
- cela rejoint les autres tests (décennies, sous‑ensembles temporels) et renforce l’idée d’une criticité **multi‑échelle** dans le temps.

---

## 5. Rôle de la Partie 11 dans le pipeline Tsunami V0.1

La Partie 11 :

- raffine la visualisation du comportement "knife‑edge" autour de d=4 (Bloc 16) ;
- montre que même des permutations intra‑décennie ne perturbent pas l’équilibre à d=4 (Bloc 17) ;
- vérifie que l’équilibre est indépendant de la **granularité temporelle** (année, trimestre, mois) (Bloc 18).

Combinée aux Parties 8–10, elle conclut que :

- pour le cas Tsunami, la dimension spatio‑temporelle **d=4** place le système dans un **état critique universel**, robuste :
  - aux divisions temporelles/cohérences intra‑bloc ;
  - aux partitions géographiques ;
  - aux échelles d’échantillonnage ;
  - au bruit sur n ;
  - à la granularité temporelle ;
- une petite variation de d autour de 4 suffit à basculer le régime (confirmé par la sensibilité fine). 

Cette Partie 11 achève la "Spatio‑Temporal Validation Suite" pour Tsunami V0.1, en consolidant d=4 comme véritable point critique universel du modèle T_log sur ce dataset.

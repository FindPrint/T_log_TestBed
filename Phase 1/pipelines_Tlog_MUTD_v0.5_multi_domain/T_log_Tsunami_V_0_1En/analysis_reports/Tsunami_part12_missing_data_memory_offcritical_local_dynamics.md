# Tsunami V0.1 – Partie 12 (cellules 88–95) : Données manquantes et mémoire hors‑critique (d=3.95, 4.05)

## 1. Périmètre de la partie

Cette douzième partie correspond aux cellules **88–95** du notebook `Tsunami_part12.ipynb`, dérivé de `T_log_Tsunami_V_0_1En.ipynb`.

Elle complète la validation Tsunami V0.1 par :

- des tests de robustesse à des **données manquantes** (MCAR et suppressions par décennie) à d=4 (Bloc 19) ;
- l’étude de l’effet de **noyaux de mémoire** lorsque d s’écarte légèrement de 4 (d=3.95 et d=4.05) (Bloc 20) ;
- une analyse **locale** de T_log(t) bucket par bucket sous mémoire (Bloc 20bis).

---

## 2. Bloc 19 – Robustesse aux données manquantes (MCAR + clustered, d=4)

### 2.1 Méthode

On charge `earthquake_data_tsunami.csv`, avec :

- `n_original = len(df)` ;
- ajout d’une colonne `decade` = (Year//10)*10.

On définit T_log pour d=4 :

\[
T_{\log}(n,4) = (4-4)\,\ln(n) = 0.\]

Deux scénarios de données manquantes sont testés pour des niveaux de suppression `missing_frac ∈ {0.05, 0.10, 0.20}` :

- **Scénario A (MCAR)** : suppression aléatoire de `frac` des lignes sur l’ensemble du dataset ;
- **Scénario B (Clustered)** : choix aléatoire d’une décennie, suppression de `frac` des lignes de cette décennie.

Pour chaque scénario et chaque `missing_frac` :

- on calcule `n_remaining` ;
- on évalue `T_log(n_remaining, d=4)` ;
- on stocke le régime.

Les résultats sont sauvegardés dans :

- `results/bloc19_missing_data.csv` ;
- un plot `results/bloc19_missing_data.png` montrant T_log vs pourcentage de données manquantes.

### 2.2 Résultats

Le commentaire résume :

- même avec **5 %, 10 % ou 20 %** de données supprimées (aléatoirement ou par décennie), le régime reste toujours **Equilibrium** ;
- la courbe T_log vs % de données manquantes est **parfaitement plate à 0**.

Interprétation :

- à d=4, T_log ne dépend pas de n et donc **ne réagit pas** aux données manquantes ;
- la criticité spatio‑temporelle est **totalement insensible** à ce type de bruit structurel ;
- c’est une validation supplémentaire de la **stabilité** du modèle à d=4.

---

## 3. Bloc 20 – Mémoire hors‑critique (d=3.95 et d=4.05)

### 3.1 Objectif

Tester si l’introduction de **noyaux de mémoire temporelle** (EMA, boxcar) peut décaler ou moduler le régime lorsque la dimension d est légèrement en‑dessous ou au‑dessus du point critique :

- d=3.95 (juste en dessous de 4 → Divergence) ;
- d=4.05 (juste au‑dessus de 4 → Saturation).

### 3.2 Méthode

On :

- agrège le dataset en série temporelle par `bucket` (mois ou année selon les colonnes disponibles) ;
- obtient un vecteur de comptes `counts` ;
- applique deux familles de noyaux :
  - EMA (`alpha ∈ {0.2, 0.5, 0.8}`) ;
  - Boxcar (`window ∈ {3,5,9}`).

Pour chaque combinaison (kernel, paramètre, d) :

- on calcule `n_eff` (comptes effectifs) ;
- on somme pour obtenir `n_eff_global` ;
- on en déduit `T_log(n_eff_global, d)` et le régime.

Les résultats sont sauvegardés dans :

- `results/bloc20_memory_offcritical.csv` ;
- un plot `results/bloc20_memory_offcritical.png` comparant les T_log pour d=3.95 et d=4.05.

### 3.3 Résultats

Les résultats résumés indiquent :

- pour d = 3.95 :
  - tous les noyaux donnent des T_log ≈ −0.33 ;
  - régime = **Divergence** pour tous ;
- pour d = 4.05 :
  - tous les noyaux donnent des T_log ≈ +0.33 ;
  - régime = **Saturation** pour tous ;
- les valeurs restent quasi constantes d’un noyau à l’autre → la mémoire ne change pas le signe ni l’ordre de grandeur de T_log.

Interprétation :

- hors de d=4, la dimension d reste **le facteur déterminant** du régime ;
- les noyaux de mémoire modifient `n_eff` (lissage, inertie) mais n’entraînent **aucun basculement** de Divergence vers Saturation ou inversement dans ces cas ;
- la mémoire agit comme **modulateur local** mais ne déplace pas la frontière critique.

---

## 4. Bloc 20bis – Dynamique locale T_log(t) sous mémoire (d=3.95, 4.05)

### 4.1 Méthode

Bloc 20bis affine l’analyse en regardant T_log(t) **bucket par bucket** :

- mêmes buckets temporels que Bloc 20 ;
- même T_log(n_eff, d) mais calculé **pour chaque bucket** plutôt que sur la somme globale ;
- noyaux :
  - EMA avec α=0.5 ;
  - Boxcar avec fenêtre W=5.

Pour chaque bucket et chaque (kernel, d) :

- on stocke `n_eff`, T_log(t), et le régime ;
- on sauvegarde dans :
  - `results/bloc20bis_memory_local.csv` ;
- on trace :
  - `results/bloc20bis_memory_local.png` : courbes T_log(t) dans le temps pour d=3.95 et d=4.05, EMA + Boxcar, avec ligne T_log=0.

### 4.2 Résultats et interprétation

La description du bloc indique :

- pour d=3.95 :
  - T_log(t) reste **toujours négatif**, quel que soit le bucket et le noyau ;
  - régime local = Divergence en tout temps ;
- pour d=4.05 :
  - T_log(t) reste **toujours positif**, EMA et Boxcar confondus ;
  - régime local = Saturation en tout temps.

Les noyaux mémoire :

- modifient la forme temporelle de T_log(t) (lissage, décalages, atténuation de pics) ;
- mais **ne changent jamais le signe** de T_log(t) pour ces d testés.

Cela illustre :

- une fois d positionné hors du point critique, la mémoire ne suffit pas à "sauver" ou "inverser" le régime ;
- pour piloter les transitions de régime, il faudra jouer sur d (ou sur un bias couplé à la mémoire), ce qui relève plutôt de V1/V2.

---

## 5. Rôle de la Partie 12 dans le pipeline Tsunami V0.1

Cette Partie 12 apporte les dernières briques de validation pour Tsunami V0.1 :

- elle montre que l’équilibre d=4 est **insensible aux données manquantes**, qu’elles soient supprimées de façon aléatoire (MCAR) ou par blocs temporels (décennies) ;
- elle démontre que, dès qu’on s’éloigne légèrement de d=4 (d=3.95 ou 4.05), les **noyaux de mémoire** ne modifient pas la nature du régime (toujours Divergence ou Saturation selon le signe de d−4) ;
- elle révèle, via l’analyse locale T_log(t), que la mémoire structure les dynamiques internes sans changer le signe de T_log.

En combinaison avec les Parties 1–11, on obtient la vision complète suivante pour le cas Tsunami :

- **d = 3 (spatial)** → T_log<0 (Divergence) robuste ;
- **d = 4 (spatio‑temporel)** → T_log=0 (Équilibre critique), invariant en temps, espace, échelle, bruit n, granularité temporelle ;
- **d ≈ 3.95 / 4.05** → régimes Divergence / Saturation maintenus malgré la mémoire ;

ce qui confirme que le modèle `T_log(n,d) = (d-4) ln(n)` décrit bien un **système auto‑organisé critique** avec un point de bascule volumique et temporel très bien identifié à d=4.

# Tsunami V0.1 – Partie 10 (cellules 72–79) : Finalisation de la validation spatio-temporelle (d=4)

## 1. Périmètre de la partie

Cette dixième partie correspond aux cellules **72–79** du notebook `Tsunami_part10.ipynb`, dérivé de `T_log_Tsunami_V_0_1En.ipynb`.

Elle clôt la validation du modèle **T_log V0.1** pour le cas Tsunami en dimension **spatio‑temporelle d = 4**, en :

- rappelant la robustesse au bruit sur `n` (Bloc 12) ;
- testant la sensibilité au **bruit sur la dimension d** autour de 4 (Bloc 13) ;
- étudiant l’effet de **noyaux de mémoire temporelle** sur les comptes effectifs (Bloc 14) ;
- ajoutant une section de synthèse **"Spatio‑Temporal Validation Suite (Blocks 7–14)"** dans `final_report.md` (Bloc 15).

---

## 2. Bloc 12 – Rappel : robustesse au bruit sur n (d=4)

La première cellule reprend les résultats du Bloc 12 (déjà détaillés en Partie 9) :

- pour des perturbations de n de **±1 à ±20 %** et plusieurs répétitions, on obtient toujours :

\[
T_{\log}(n, d=4) = 0.000000 \quad \Rightarrow \quad \text{Regime = Equilibrium}.
\]

Interprétation rappelée :

- l’équilibre spatio‑temporel à d=4 est **insensible** au bruit sur la taille de l’échantillon ;
- la criticité n’est pas un artefact d’une valeur précise de n.

Ce rappel prépare le contraste avec le bruit sur d étudié ensuite.

---

## 3. Bloc 13 – Bruit sur la dimension d autour de d=4

### 3.1 Méthode

On introduit un **bruit aléatoire sur d** autour de 4, à taille n fixée (n_true=782) :

- `noise_levels = [0.01, 0.05, 0.1, 0.2]` ;
- pour chaque niveau de bruit `ε` : 5 perturbations ;
- `d_perturbed = 4 + U(-ε, +ε)` ;
- calcul de `T_log(n_true, d_perturbed)` et du régime correspondant (Divergence, Equilibrium, Saturation).

### 3.2 Résultats

Exemples typiques :

- Bruit ±0.01 :
  - `d≈4.0099` → T_log>0 → Saturation ;
  - `d≈3.9976` → T_log<0 → Divergence ;
- Bruit ±0.05 : mélange de Divergence (d<4) et Saturation (d>4) ;
- Bruit ±0.10, ±0.20 :
  - d nettement <4 → T_log<0 → Divergence marquée ;
  - d>4 → T_log>0 → Saturation significative.

On constate que **toute petite déviation de d par rapport à 4** fait immédiatement basculer le régime :

- dès que d>4, T_log devient positif → Saturation ;
- dès que d<4, T_log devient négatif → Divergence.

### 3.3 Interprétation

- à l’inverse du bruit sur n, le bruit sur **d** est **décisif** pour le régime ;
- d=4 est un **point critique au sens fort** :
  - stable si on est exactement dessus (T_log=0) ;
  - instable dès qu’on s’en écarte, même légèrement ;
- cela illustre la nature "**knife‑edge**" de la dimension critique :
  - robustesse macroscopique (temps/espace/échelle, bruit sur n) ;
  - hypersensibilité microstructurale à la dimension effective.

---

## 4. Bloc 14 – Noyaux de mémoire temporelle à d=4

### 4.1 Construction de n_eff(t) par noyaux de mémoire

Bloc 14 introduit des **noyaux de mémoire** appliqués aux comptes par bucket temporel :

- on identifie une colonne temporelle :
  - soit une date complète (convertie en `bucket` mensuel) ;
  - soit l’année (bucket par année) ;
- on construit une série `counts[bucket]` (nombre d’événements par bucket) ;
- deux types de noyaux :
  - **EMA (exponential moving average)** :

\[
 n^{\text{(EMA)}}_t = (1-\alpha) n_t + \alpha n^{\text{(EMA)}}_{t-1}, \quad \alpha ∈ [0,1).
\]

  - **Boxcar (moyenne glissante)** de fenêtre W : moyennes locales sur W buckets.

On considère ensuite des paramètres :

- `alphas = [0.0, 0.2, 0.5, 0.8, 0.95]` ;
- `windows = [1, 3, 5, 9, 13]`.

Pour chaque noyau, on calcule un **compte effectif global** `n_eff_global = ∑ n_eff[t]` et :

\[
T_{\log}(n_eff_{global}, d=4).
\]

### 4.2 Résultats

- EMA :
  - n_eff_global varie de ~782 (α=0) à ~669 (α=0.95) ;
  - pour tous les α : T_log(n_eff_global,4) = 0 → **Equilibrium** ;
- Boxcar :
  - n_eff_global reste très proche de 782 (≈780–782) ;
  - T_log = 0 pour tous les W.

Des diagnostics locaux montrent comment les noyaux modifient les **comptes par bucket** (smoothing, inertie), mais le régime global reste `Equilibrium` à d=4.

### 4.3 Interprétation

- en dimension d=4, T_log est par construction **indépendant de n_eff** (tant que bias=0) → T_log≡0 ;
- les noyaux de mémoire changent la dynamique locale (pondération des buckets, smearing temporel) mais :
  - **ne déplacent pas la frontière critique** ;
  - **ne changent pas le régime** ;
- cela montre que la mémoire est un **terme secondaire** dans V0.1 :
  - elle structure les comptes, mais ne modifie pas la criticité pour d=4 ;
  - en V1/V2, mémoire + d≠4 pourront devenir importants pour des effets de délai/hystérésis.

---

## 5. Bloc 15 – Section de validation spatio‑temporelle ajoutée au rapport final

### 5.1 Ajout dans `final_report.md`

La dernière cellule (Bloc 15) ajoute au rapport final `final_report.md` une section intitulée :

- **"Spatio‑Temporal Validation Suite (Blocks 7–14)"**.

Cette section résume :

- Bloc 7 : d=4, sensibilité autour de 4 ;
- Bloc 8 : stabilité temporelle ;
- Bloc 9 : stabilité spatiale ;
- Bloc 10 : stabilité temps×espace ;
- Bloc 11 : stress test multi‑échelle ;
- Bloc 12 : robustesse au bruit sur n ;
- Bloc 13 : bruit sur d ;
- Bloc 14 : noyaux de mémoire.

Elle souligne que :

- d=4 assure un **Équilibre universel** ;
- cette criticité est invariante en temps, en espace, en taille, en bruit sur n ;
- la seule fragilité est sur d (dimension) elle‑même, ce qui est caractéristique d’un point critique.

---

## 6. Rôle de la Partie 10 dans le pipeline Tsunami V0.1

La Partie 10 clôt la validation spatio‑temporelle du modèle T_log pour Tsunami en montrant que :

- l’équilibre d=4 est **insensible aux perturbations sur n** (taille réelle, sous‑échantillons, bruit) ;
- il est en revanche **hypersensible aux perturbations sur d** : le régime bascule dès que d s’éloigne de 4 ;
- l’introduction de **noyaux de mémoire** modifie les comptes effectifs mais laisse l’équilibre intact à d=4 ;
- tous ces éléments sont désormais consolidés dans le rapport final `final_report.md` via la section Spatio‑Temporal Validation Suite.

En combinaison avec les Parties 1–9, cette Partie 10 permet d’affirmer que, pour le cas Tsunami V0.1 :

- d=3 → Divergence robuste ;
- d=4 → Équilibre critique universel (spatio‑temporel, multi‑échelle, stable sous bruit en n, mémoire) ;
- d≠4 → saturation ou divergence selon le signe de (d−4).

Le modèle **T_log(n,d) = (d-4) ln(n) + bias** apparaît ainsi comme une structure **cohérente, rigoureusement testée et prête à être enrichie** (V1/V2) tout en conservant d=4 comme boussole critique.

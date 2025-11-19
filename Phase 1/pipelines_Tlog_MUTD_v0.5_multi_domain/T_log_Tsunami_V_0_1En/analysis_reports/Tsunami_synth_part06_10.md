# Tsunami V0.1 – Synthèse des parties 6 à 10

## 1. Périmètre

Cette synthèse couvre :
- Tsunami_part06 – calibration proxy et test de permutation.
- Tsunami_part07 – ablation du biais et validation étendue en d=4.
- Tsunami_part08 – dimension spatio‑temporelle d=4, équilibre global.
- Tsunami_part09 – robustesse multi‑échelle et au bruit (d=4).
- Tsunami_part10 – validation spatio‑temporelle étendue (bruit sur n et d, mémoire).

Ensemble, ces parties consolident **d=4** comme point critique dans un cadre spatio‑temporel réaliste.

---

## 2. Calibration, permutation et biais (Parties 6–7)

- **Calibration proxy** (Partie 6) :
  - ajustement de paramètres pour que T_log reflète correctement l’équilibre attendu ;
  - vérification de la cohérence hors‑échantillon (proxy / OOS) ;
- **Test de permutation** :
  - mélange des labels ou des dates pour vérifier que la structure T_log ne provient pas d’un artefact temporel ou d’un sur‑apprentissage ;
  - les résultats montrent que les régimes observés se dégradent fortement lorsque la structure réelle est détruite, ce qui renforce la validité de T_log.
- **Ablation du biais** (Partie 7) :
  - étude de l’effet d’un terme de biais dans la loi ;
  - constat qu’un biais mal choisi détériore la cohérence des régimes, alors qu’un biais nul ou calibré conserve la frontière d=4 ;
  - ajout d’une section de validation étendue dans le rapport final.

Conclusion : la calibration et les permutations confirment que les résultats en d=4 ne sont pas de simples artefacts statistiques ou de sur‑ajustement.

---

## 3. Dimension spatio‑temporelle d=4 (Partie 8)

- Passage explicite à une dimension **spatio‑temporelle** : temps + espace combinés dans une dimension effective d=4.
- Analyse de la **stabilité temporelle** de T_log à d=4 :
  - bilan par périodes (décennies, années) ;
  - vérification que T_log reste en équilibre (≈0) sur de longues fenêtres.
- Analyse de la **stabilité spatiale** agrégée :
  - l’équilibre global ne dépend pas de la répartition géographique fine.

Résultat clé : d=4 apparaît comme le point où la dynamique spatio‑temporelle du système Tsunami se stabilise, sans tendance persistante à la divergence ou à la saturation.

---

## 4. Robustesse multi‑échelle et au bruit (Partie 9)

- Variation de la granularité temporelle (multi‑échelle) :
  - changement de la taille des fenêtres temporelles ;
  - observation que le signe de T_log à d=4 reste nul, même si la variance locale change.
- Ajout de **bruit sur n** (taille effective) à d=4 :
  - perturbations multiplicatives modérées sur la taille des échantillons ;
  - T_log reste centré sur 0 → le régime d=4 est stable face aux fluctuations de comptage.

Ces tests montrent que l’équilibre en d=4 n’est pas un artefact d’un choix particulier de résolution ; il est présent de l’échelle fine à l’échelle plus agrégée.

---

## 5. Validation spatio‑temporelle étendue, bruit sur d et mémoire (Partie 10)

- Poursuite des tests de robustesse en dimension 4 :
  - bruit sur **n** (complément aux tests précédents) ;
  - bruit sur **d** (légères perturbations autour de 4) ;
  - introduction de **noyaux de mémoire** (EMA, Boxcar) pour lisser la série temporelle et modéliser des effets d’inertie.
- Résultats :
  - de petites variations de d autour de 4 produisent des T_log légèrement positifs ou négatifs, cohérents avec la théorie (Saturation ou Divergence) ;
  - la mémoire modifie la forme temporelle (plus lisse, plus inertielle) mais ne renverse pas le signe de T_log ;
  - l’équilibre global à d=4 reste visible une fois les effets de mémoire correctement interprétés.

Cette partie prépare les analyses encore plus fines des parties 11–15 (données manquantes, mémoire hors‑critique, quadrants, etc.).

---

## 6. Message global des parties 6–10

Les parties 6 à 10 confirment et approfondissent plusieurs points :

- la loi T_log reste cohérente lorsque l’on teste des scénarios "cassés" (permutation) ou mal calibrés (biais incorrect) ;
- la dimension spatio‑temporelle **d=4** apparaît comme le véritable **point d’équilibre** pour le système Tsunami ;
- cet équilibre résiste :
  - à la variation de granularité temporelle (multi‑échelle) ;
  - au bruit sur n ;
  - à de légers déplacements de d autour de 4 ;
  - à l’introduction de noyaux de mémoire qui modifient la dynamique mais pas le régime.

Ces résultats renforcent la thèse que d=4 n’est pas un simple réglage, mais une **frontière structurelle** du système, sur laquelle le reste du pipeline (parties 11–15) va appliquer des stress tests plus agressifs (données manquantes, mémoire hors‑critique, multi‑facteur, modèles concurrents, cross‑validation).

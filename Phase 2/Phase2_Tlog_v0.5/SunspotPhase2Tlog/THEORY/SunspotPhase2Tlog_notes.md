# Sunspots – T_log v0.5 – Phase 2 (Notes de base)

## 1. But du projet

Cette Phase 2 a pour objectif de construire un pipeline **plus robuste** et **plus auditable** pour appliquer la formule T_log v0.5 (et le cadre MUTD v0.5.5) aux données de taches solaires (**sunspots**).

Contrairement à la Phase 1, qui était surtout une **démonstration** de la formule sur un jeu de données, la Phase 2 se concentre sur :

- une meilleure **estimation de la dimension effective** `d` ;
- la **quantification de l’incertitude** sur `d` et sur `T_log(n, d)` ;
- l’usage de **baselines** et de **modèles nuls** pour tester/falsifier les interprétations ;
- une **traçabilité forte** : logs en sortie de cellules, fichiers de log, manifeste de run, notes.

La Phase 2 ne modifie pas les pipelines de la Phase 1 : elle vit dans un dossier séparé
`c:\Users\zackd\OneDrive\Desktop\Phase2_Tlog_v0.5`.

---

## 2. Formules clés

### 2.1. T_log v0.5

La formule centrale est :

\[
T_{\log}(n, d) = (d - 4) \, \log(n)
\]

où :

- \( n \) est lié à la taille du système (par exemple le nombre d’observations, la taille d’une fenêtre, etc.) ;
- \( d \) est une **dimension effective** du système (dimension fractale, dimension d’immersion, dimension effective estimée par une méthode donnée).

Interprétation qualitative :

- \( d - 4 > 0 \) : régime de **tension croissante / divergence** ;
- \( d - 4 \approx 0 \) : régime d’**équilibre / frontière critique** ;
- \( d - 4 < 0 \) : régime de **saturation / confinement**.

### 2.2. MUTD v0.5.5 (schéma général)

Dans le cadre MUTD v0.5.5, on distingue deux couches :

1. **Complexité structurelle** (dimension effective) :

   \[
   D_{\mathrm{eff}} = \frac{\log(n)}{\log(d_{\mathrm{obs}})}
   \]

   (cette forme peut être adaptée selon la définition de \( d_{\mathrm{obs}} \) et du contexte).

2. **Tension dynamique** :

   \[
   T_{\mathrm{dyn}} = (D_{\mathrm{eff}} - 4) \, \log(n)
   \]

La Phase 2 n’a pas pour but de changer les formules, mais plutôt de **mieux les appliquer** et de **mieux quantifier leurs limites** (incertitude, identification de `d`, tests de robustesse).

---

## 3. Données

- Jeu de données principal : **sunspots (taches solaires)**.
- Source canonique (Phase 1) : fichier CSV déjà utilisé dans le pipeline Sunspots T_log v0.5.
- Règle importante : la Phase 2 **lit** les données à partir de ces fichiers, mais **n’écrit jamais** dans les dossiers de la Phase 1.

Un zip Kaggle peut exister comme archive, mais la Phase 2 ne dépend pas d’un accès Kaggle pour fonctionner.

---

## 4. Organisation prévue de la Phase 2

La Phase 2 est organisée en blocs (sections) dans un notebook principale, par exemple `SunspotPhase2Tlog` :

- **Bloc 0** – Infrastructure Phase 2  
  Définir la racine du projet, la structure des dossiers (logs, reports, artifacts, config, cache, data_phase2), les fichiers de configuration, les requirements, le logging et le manifeste de run.

- **Bloc 1** – Données & traçabilité  
  Décrire la provenance des données, les chemins utilisés, la copie éventuelle en `data_phase2`, le schéma des colonnes, les premières statistiques descriptives.

- **Bloc 2** – Prétraitements & fenêtres  
  Définir les éventuels prétraitements (normalisation, filtrage, découpe en fenêtres temporelles) et discuter de leurs impacts potentiels sur l’estimation de la dimension `d`.

- **Bloc 3** – Estimation de la dimension effective `d`  
  Appliquer plusieurs méthodes (par exemple : dimension spectrale, Levina–Bickel, Participation Ratio / PCA, etc.), obtenir des **distributions** de `d` et des **intervalles de confiance**, et analyser les diagnostics de fiabilité.

- **Bloc 4** – Calcul de \( T_{\log}(n, d) \) avec incertitude  
  Propager l’incertitude sur `d` (et éventuellement sur `n`) jusqu’à `T_log`, produire des barres d’erreur et des scénarios (d_min, d_med, d_max).

- **Bloc 5** – Baselines & modèles nuls  
  Construire des séries de contrôle (shuffle, modèles AR/ARMA simples, etc.), estimer `d` et `T_log` sur ces baselines, et comparer aux résultats sur la série réelle.

- **Bloc 6** – Falsification & analyses de sensibilité  
  Concevoir des tests de falsification où la théorie T_log devrait échouer, et étudier la sensibilité aux choix de méthode de `d`, de fenêtre, de prétraitement, etc.

- **Bloc 7** – Synthèse & rapport Phase 2  
  Rédiger un rapport global (Markdown) qui résume les méthodes, les résultats, les limites, et fournit une checklist d’audit.

---

## 5. Règles d’interaction avec Cascade (assistant)

Pour ce projet, une règle forte est adoptée :

- **Toutes les actions sur le code et les fichiers passent par cette conversation.**  
- L’assistant (Cascade) ne crée ni ne modifie directement de fichiers ou dossiers dans l’IDE, **sauf** demande ou accord explicite de l’utilisateur.
- L’utilisateur copie-colle lui-même :
  - le code proposé (cellules “Code” dans le notebook),  
  - le texte Markdown proposé (cellules “Markdown” dans le notebook),  
  - le contenu des fichiers auxiliaires (requirements, notes, etc.).

Cette règle renforce la **traçabilité** et le **contrôle humain** sur chaque étape du pipeline.

---

## 6. Style du notebook Phase 2

Le notebook Phase 2 est structuré en **alternance** :

- Cellule **Markdown** : contexte, objectifs, description des opérations.  
- Cellule **Code** : implémentation correspondante.  
- Retour dans cette conversation pour analyser les sorties (audit) et décider de la prochaine étape.

Cette organisation vise à :

- clarifier la logique scientifique,  
- faciliter les revues et audits,  
- limiter les erreurs ou “sauts” méthodologiques.
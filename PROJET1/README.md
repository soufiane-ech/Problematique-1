# POC – Analyse automatisée des évaluations de formation

Proof of Concept réalisé dans le cadre du programme **Think To Deploy (T2D)** – Safran.  
Ce projet vise à démontrer la faisabilité d’une analyse automatisée des évaluations de formation à l’aide de workflows, d’IA et de visualisation de données.

---

## Objectif

- Automatiser l’analyse des évaluations de formation
- Exploiter les données quantitatives et les commentaires libres
- Intégrer une analyse de sentiment multilingue (FR / EN / AR / Darija)
- Produire des indicateurs exploitables via un dashboard
- Proposer une architecture modulaire et industrialisable

---

## Architecture (vue d’ensemble)

- **Formulaire** : collecte des évaluations
- **n8n** : orchestration du workflow
- **Python** : traitement des données
- **APIs IA** :
  - Hugging Face (multilingue)
  - API Darija dédiée (Dockerisée)
- **Google Sheets** : base de données POC
- **Power BI** : visualisation

> ⚠️ Aucun accès direct au SI Safran – environnement POC isolé.

---

## Workflow automatisé (n8n)

1. Réception des réponses du formulaire
2. Normalisation des données
3. Génération des identifiants :
   - `formation_id`
   - `formateur_id`
   - `evaluation_id`
4. Routage intelligent selon la langue
5. Analyse de sentiment
6. Stockage des résultats dans Google Sheets
7. Mise à jour automatique du dashboard Power BI

---

## Analyse de sentiment

### Langues supportées
- Français
- Anglais
- Arabe standard
- Darija

### Logique
- FR / EN / AR → modèles multilingues Hugging Face
- Darija → API dédiée

### Commentaires longs
- Découpage > 480 caractères
- Analyse par fragment
- Agrégation par moyenne

---

## API Darija (Docker)

Le modèle `BenhamdaneNawfal/sentiment-analysis-darija` est exposé via une API FastAPI **containerisée**.


## Configuration & Data sources

Le POC s’appuie sur deux Google Sheets externes servant de sources de référence et de stockage.
Ces documents ne sont **pas versionnés** dans le repository et restent découplés du code.

### 1. Référentiel formateurs

Google Sheet utilisé comme table de correspondance entre les formateurs et leurs identifiants.

- Contenu :
  - `formateur_id`
  - `nom_formateur`
- Utilisation :
  - Résolution automatique du `formateur_id` dans le workflow n8n

🔗 Lien :  
👉 **[Google Sheet – Référentiel formateurs](https://docs.google.com/spreadsheets/d/1wtgV75fivrMk-QbPD3ThmEmxd8_wRaEIktGmlS0B_WY/edit?usp=sharing)**

---

### 2. Base centrale des évaluations

Google Sheet servant de base de données POC pour le stockage des évaluations enrichies et analysées.

- Contenu :
  - données quantitatives
  - commentaires libres
  - langue
  - sentiment
  - métadonnées (date, ids, etc.)
- Utilisation :
  - alimentation du dashboard Power BI
  - suivi dynamique des indicateurs

🔗 Lien :  
👉 **[Google Sheet – Base centrale des évaluations](https://docs.google.com/spreadsheets/d/18iZnNQu2acAME7AgxIMKLSKSdd765H2kEdhqqYZbh-M/edit?usp=sharing)**


### Image Docker
soufianeech/b2c-web:latest


## Utilisation

### 1. Formulaire d’évaluation
🔗 **Formulaire** : [Accéder au formulaire](https://n8ncourse.echchafiy.cfd/form/c8ae436f-74f8-45ff-9b3c-ea758d1ee0c0)

L’utilisateur remplit et soumet le formulaire.  
Aucune autre action n’est requise.

---

### 2. Traitement automatique

À chaque soumission :
- les données sont collectées et normalisées,
- l’analyse de sentiment est exécutée automatiquement,
- les résultats sont stockés dans la base centrale,
- le dashboard est mis à jour.

---


Le dashboard est connecté dynamiquement à la base de données.
Toute nouvelle évaluation ou modification est prise en compte automatiquement.

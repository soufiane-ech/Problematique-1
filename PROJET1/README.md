##  README — Proof of Concept (POC)
Analyse automatisée des évaluations de formation

Think To Deploy – Safran

##  Contexte et objectif du POC

Dans le cadre du programme Think To Deploy (T2D), Safran souhaite explorer des solutions basées sur l’IA et la Data Science afin d’améliorer l’exploitation des évaluations « à chaud » des formations.
Ce Proof of Concept (POC) vise à démontrer la faisabilité technique, la valeur métier et la capacité d’industrialisation d’une solution permettant :
d’automatiser l’analyse des évaluations de formation,
d’exploiter à la fois les données quantitatives et les commentaires libres,
d’intégrer une analyse de sentiment multilingue (français, anglais, arabe, darija),
de restituer des insights exploitables via un dashboard dynamique,
tout en respectant les contraintes de sécurité, de confidentialité et de non-intrusion dans le SI Safran.

##  Périmètre du POC
##   Fonctionnalités couvertes

Le POC couvre les fonctionnalités suivantes :
Collecte automatisée des évaluations via formulaire
Normalisation et structuration des données
Génération d’identifiants uniques d’évaluation
Analyse statistique des critères de formation
Analyse de sentiment multilingue des commentaires libres
Traitement spécifique des commentaires longs
Stockage centralisé des résultats
Visualisation dynamique via Power BI

##   Hors périmètre

Les éléments suivants ne sont pas inclus dans ce POC :
Intégration directe au SI Safran
Utilisation de données réelles Safran
Authentification LDAP / SSO
Déploiement industriel en production
##   Architecture globale de la solution

La solution repose sur une architecture modulaire, découplée et industrialisable, composée des briques suivantes :
Formulaire d’évaluation : point d’entrée des données
n8n : orchestration du workflow automatisé
Scripts Python : traitement des données et logique métier
APIs IA :
API Hugging Face pour l’analyse multilingue
API dédiée FastAPI pour la darija
Base de données POC : Google Sheets
Restitution : Dashboard Power BI connecté dynamiquement
Cette architecture garantit :
l’absence d’accès direct au SI Safran,
la séparation claire des composants,
la facilité d’évolution vers un déploiement sécurisé.

##   Description détaillée du workflow automatisé

Le workflow, orchestré via n8n, couvre l’ensemble du cycle de traitement des évaluations :
##  Collecte des données
Le workflow est déclenché à la soumission du formulaire d’évaluation, qui collecte :
le type de formation,
le formateur,
les évaluations quantitatives,
le commentaire libre,
la langue,
la date de soumission.
Les réponses qualitatives (« Très insatisfaisant » à « Très satisfait ») sont automatiquement converties en scores numériques de 1 à 5.

##   Enrichissement et normalisation

Plusieurs mécanismes d’enrichissement sont appliqués :
Formation ID
Attribution automatique d’un formation_id à partir du type de formation.
(Hypothèse POC : un type de formation = un identifiant)
Formateur ID
Récupération du formateur_id via un Google Sheet de référence.
Evaluation ID
Génération d’un identifiant unique (A + 8 chiffres) garantissant l’unicité et la traçabilité.

##   Stockage centralisé

Les données sont structurées selon le schéma suivant :
evaluation_id
formation_id
type_formation
formateur_id
satisfaction
contenu
logistique
applicabilite
commentaire
langue
date
sentiment
Elles sont ensuite stockées dans une base centrale (Google Sheets) servant de socle unique pour l’analyse et la visualisation.

##  Routage intelligent pour l’analyse de sentiment

Le workflow intègre une logique conditionnelle basée sur la langue :
Darija
Envoi du commentaire vers une API FastAPI dédiée
Analyse via un modèle Hugging Face spécialisé
Français / Anglais / Arabe standard
Analyse via un modèle multilingue Hugging Face
Gestion des commentaires longs
Seuil : 480 caractères
Découpage automatique en fragments cohérents
Analyse indépendante de chaque fragment
Agrégation par moyenne pour produire un sentiment global fiable
##  Création de l’API d’analyse de sentiment Darija
##   Problématique

Le modèle BenhamdaneNawfal/sentiment-analysis-darija n’étant pas déployé par un fournisseur d’inférence standard, une API dédiée a été développée pour l’exposer et l’intégrer au pipeline.

##   Mise en place technique

Création d’un projet Python isolé
Environnement virtuel (venv)
Installation des dépendances :
FastAPI
Uvicorn
Torch
Transformers

##  Développement de l’API

L’API FastAPI :
charge le modèle une seule fois au démarrage,
expose l’endpoint POST /sentiment/darija,
retourne un sentiment (Positive / Negative) et un class_id.
##   Déploiement et accès réseau

L’API est lancée via Uvicorn et exposée sur le réseau local.
L’utilisation de l’IP locale permet à n8n d’y accéder sans conflit (127.0.0.1 non accessible).

##   Intégration avec n8n

Un HTTP Request Node est utilisé dans n8n :
Méthode : POST
Body JSON : commentaire Darija
Réception automatique du sentiment analysé
Les résultats sont ensuite stockés dans la base centrale.

##   Visualisation et insights via Power BI

Un dashboard Power BI connecté dynamiquement à la base permet :
le suivi des indicateurs clés (satisfaction, contenu, logistique, applicabilité),
l’analyse des tendances temporelles,
la visualisation de la distribution des sentiments,
la comparaison par formateur et type de formation,
la détection de signaux faibles,
l’identification d’axes d’amélioration exploitables.
Toute nouvelle évaluation est automatiquement prise en compte.

##  Technologies utilisées

n8n – Orchestration des workflows
Python – Traitement des données et IA
FastAPI – Exposition de modèles IA
Hugging Face Transformers
Google Sheets – Base de données POC
Power BI – Visualisation
LaTeX – Rapport final

##   Instructions de lancement du POC

Créer les Google Sheets de référence
Configurer le formulaire d’évaluation
Importer et activer le workflow n8n
Lancer l’API FastAPI Darija
Configurer les clés API Hugging Face
Connecter Power BI à la base centrale
Soumettre des évaluations de test

##   Limites du POC

Hypothèses simplificatrices sur les formations
Modèles non fine-tunés sur données Safran
Sécurité simulée
Environnement non productif

##  . Vision d’évolution vers la production

Référentiel formations et sessions
Hébergement sécurisé (on-premise / cloud Safran)
Authentification et contrôle d’accès
Journalisation et auditabilité
Enrichissement NLP (topics, clustering)
Industrialisation du pipeline

##   Valeur métier pour Safran

La solution permet :

un gain de temps significatif pour les équipes RH,
une exploitation intelligente des retours collaborateurs,
une amélioration continue des formations,
une prise de décision data-driven,
une architecture prête à être industrialisée.
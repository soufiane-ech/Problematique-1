##              Chatbot RH Intelligent
## Introduction
Ce projet présente la conception et le développement d’un chatbot RH intelligent, réalisé dans le cadre du programme Think To Deploy.
Le chatbot permet aux collaborateurs d’obtenir des réponses fiables à leurs questions Ressources Humaines en langage naturel, tout en adaptant les réponses en fonction du profil utilisateur.
La solution est développée sous forme de Proof of Concept (POC) et vise à démontrer la faisabilité technique, la valeur métier et la compatibilité avec un environnement industriel contraint.

## Modèle NLP

Le chatbot repose sur des techniques avancées de traitement automatique du langage naturel (NLP) basées sur des modèles de type Transformer.
Il n’utilise pas de modèle génératif (LLM), mais une approche de recherche sémantique permettant de récupérer des réponses validées depuis une base de connaissances RH.

Le modèle utilisé est :

`paraphrase-multilingual-MiniLM-L12-v2` (Sentence Transformers)

Ce modèle permet :

La compréhension multilingue (français, anglais, arabe)
La gestion des synonymes et reformulations
Une forte fiabilité des réponses (absence d’hallucination)

Le modèle est chargé automatiquement au démarrage du backend.

## Source des données

Les données RH sont simulées à l’aide d’un fichier Excel structuré :
  `RH_Infos_Quest_Réponses.xlsx`

Ce fichier contient :
Les questions RH
Les réponses validées
Les domaines fonctionnels RH
Les langues
Les profils salariés

Cette structure représente une abstraction des systèmes RH existants (SAP, bases internes, LMS) et peut être remplacée par une source automatisée dans une phase d’industrialisation.

## Backend

Le backend est développé avec FastAPI et expose une API REST consommée par le frontend.

La logique principale est implémentée dans une classe ModelInterface, qui :

Charge la base de connaissances RH
Encode les questions en vecteurs sémantiques
Calcule les similarités
Filtre les réponses selon le profil
Retourne la réponse la plus pertinente
Enregistre les indicateurs de performance

## Endpoints principaux
/login [POST]
Authentification des utilisateurs
/chat_messages [POST]
Traitement des questions RH
/kpis [GET]
Accès aux indicateurs RH
/status [GET]
Vérification de l’état du service

Le modèle NLP est chargé de manière différée (lazy loading) afin d’optimiser le temps de démarrage.

## Lancer le backend
`uvicorn main:app --reload`

## Frontend
Le frontend est développé avec Streamlit et permet :
La connexion des utilisateurs
L’interaction avec le chatbot
L’accès au dashboard RH (profil RH uniquement)
Le frontend communique avec le backend via des requêtes HTTP.

## Lancer le frontend
``streamlit run app.py`
attend jusque avoir ca "✅ Modèle RH chargé
## Prérequis et installation
Prérequis :
Python 3.10 ou supérieur
pip
Accès Internet (pour le téléchargement du modèle NLP)

Système d’exploitation : Windows, Linux ou macOS

## Installation des dépendances

Il est recommandé d’utiliser un environnement virtuel (optionnel).
`pip install fastapi uvicorn streamlit pandas scikit-learn sentence-transformers plotly openpyxl`

## Fonctionnalités
Authentification par profil salarié
Adaptation des réponses selon le profil
Gestion multilingue (FR / EN / AR)
Recherche sémantique basée sur NLP
Escalade automatique vers RH en cas d’incertitude
Tableau de bord RH avec indicateurs

## KPIs et pilotage RH
Le tableau de bord RH permet de suivre :
Taux de compréhension des questions
Taux de réponse correcte
Taux d’escalade vers le service RH
Temps moyen de réponse
Nombre de profils connectés
Répartition des domaines RH
Classement des domaines les plus sollicités

## Sécurité et conformité

Aucune donnée sensible traitée
Données RH génériques uniquement
Journalisation anonymisée
Contrôle d’accès par profil
Respect des principes RGPD
Architecture compatible LDAP / SSO (évolutions futures)

## Limites
Données RH simulées (Excel)
Authentification simplifiée
Pas d’intégration directe avec SAP ou SI RH réel
Pas de base vectorielle dédiée

## Perspectives d’évolution

Intégration avec les systèmes RH existants
Automatisation des mises à jour
Utilisation d’une base vectorielle
Ajout d’un moteur génératif contrôlé
Déploiement cloud sécurisé

## Exemple

Un exemple d’utilisation du chatbot est disponible via l’interface Streamlit après authentification.
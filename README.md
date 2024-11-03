# NiortConnect

**Projet de fin d'études SNIR2 - NiortConnect**

## Objectif
Développer une application web et mobile pour les étudiants de Niort, afin de centraliser des informations pratiques et de faciliter l'accès aux services locaux (logement, sport, culture, événements, etc.).

## Auteurs et Contributions

- **Rim El Guennouni** : Responsable du package base de données (BDD)
- **Jimmy** : Responsable du package interface homme-machine (IHM)
- **Madjiguène** : Responsable du package application mobile

**Encadrants** : M. Sallé, Mme Candillier, M. Arnault.

## Présentation du Projet

### Contexte
La ville de Niort cherche à offrir aux étudiants une meilleure intégration et un accès facilité aux informations locales. Ce projet vise à combler l'absence d'une plateforme centralisée dédiée aux étudiants.

### Fonctionnalités Principales

1. **Gestion des utilisateurs** : Inscription, connexion, gestion des rôles et profils.
2. **Publications et Commentaires** : Création et gestion de publications par les utilisateurs, incluant un système de commentaires.
3. **Gestion des notifications** : Envoi de notifications personnalisées aux étudiants.
4. **Informations contextuelles** : Accès aux informations sur les écoles, les services locaux et autres ressources utiles.

## Technologies Utilisées

- **Backend** : Flask (API RESTful)
- **Base de données** : SQLite (stockage des informations des utilisateurs et publications)
- **Frontend** : HTML, CSS, JavaScript (pour l'interface utilisateur)
- **Containerisation** : Docker (pour le déploiement sur un VPS)
- **Outils de développement** : Postman (tests API), DB Browser (gestion SQLite), MondayDev (gestion de projet), Discord (communication)

## Déploiement et Hébergement

L'application est conteneurisée avec Docker pour assurer la portabilité et la facilité de déploiement. Un fichier `Dockerfile` est inclus pour configurer et lancer l'application sur un serveur avec toutes les dépendances nécessaires.

## Installation Locale

1. **Cloner le dépôt** :
   ```bash
   git clone https://github.com/RimMaths/NiortConnectBdd.git
Installer les dépendances :



pip install -r requirements.txt
Lancer l'application :


python app.py
Accéder à l'application : Ouvrez http://localhost:5000 pour accéder à l'application en local.

Utilisation de l'API
L'API RESTful de NiortConnect propose plusieurs endpoints. Voici quelques exemples :

Connexion : /connexion - Authentification des utilisateurs.
Inscription : /inscription - Création d'un nouveau compte utilisateur.
Récupérer les utilisateurs : /utilisateurs - Affiche tous les utilisateurs.
Créer une publication : /publications/new - Ajoute une nouvelle publication.
Chaque endpoint peut être testé avec Postman ou via des requêtes HTTP directement.

Organisation du Projet
Le projet est organisé autour des trois packages principaux :

Package BDD : Responsable de la gestion de la base de données et des API.
Package IHM : Interface utilisateur pour l'accès aux données et aux fonctionnalités.
Package Mobile : Gestion des notifications et de l'affichage des données sur mobile.

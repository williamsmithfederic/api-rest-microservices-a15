# API REST Microservices – A15

## 📚 Description

Ce projet a été réalisé dans le cadre du cours **420-A15-BB – Services API REST** au Collège de Bois-de-Boulogne.

Il s'agit d'une architecture inspirée des **microservices**, développée en Python avec Flask, permettant la gestion :

- des incidents
- des absences
- des services faits
- de l’authentification sécurisée (JWT)
- de l’analyse BI

---

##  Architecture

Le projet est structuré en plusieurs services indépendants :

- `srv_incident` → Gestion des incidents
- `srv_authentification` → Authentification JWT
- `srv_incident_dao` → Accès base de données incidents
- `srv_authentification_dao` → Accès base utilisateurs
- `client_admin` → Interface d’administration
- `client_employee` → Déclaration incidents / absences
- `client_mobile` → Déclaration services faits
- `client_bi` → Analyse et tableaux de bord

Base de données : SQLite

---

##  Sécurité

- Authentification via **JWT (JSON Web Token)**
- Architecture stateless
- Séparation authentification / logique métier

---

## 📄 Documentation API

La documentation Swagger est disponible via : http://127.0.0.1:5000/apidocs/#/

Elle permet :
- Visualisation des endpoints
- Test direct des requêtes HTTP
- Consultation des formats JSON

---

## 🧪 Tests Unitaires

Les tests sont réalisés avec **pytest**.

Pour lancer les tests : pytest


---

## 🐳 Containerisation Docker

Construction de l’image : docker build -t incident-api .
Lancement du container : docker run -p 5000:5000 incident-api

---

## ☁ Simulation Déploiement

L’application est prête pour un déploiement sur :

- AWS
- Azure
- Google Cloud
- Heroku
- RapidAPI

La containerisation garantit portabilité et scalabilité.

---

##  Objectifs pédagogiques atteints

- Développement d’une API REST en Flask
- Implémentation CRUD
- Authentification JWT
- Documentation OpenAPI (Swagger)
- Tests unitaires
- Containerisation Docker
- Simulation de déploiement cloud

---

## 👨‍💻 Auteur

Youcef ATMANI & Mohamed Amine Ghazel  
AEC –  Analyste-programmeur  
Collège de Bois-de-Boulogne
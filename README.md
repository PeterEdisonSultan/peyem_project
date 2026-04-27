# Peyem Project

## Auteur
**Peter Edison Sultan**

## Cours
Application Web

## Institution
ISTEAH — Institut des sciences, des technologies et des études avancées d'Haïti

## Session
Hiver 2026

## Description du Projet

Peyem est une plateforme de paiement web développée avec Django, conçue spécifiquement pour le marché haïtien. Cette application permet aux marchands (commerçants) de s'inscrire, de gérer leur profil et d'accepter des paiements via les méthodes de paiement locales populaires : NatCash et MonCash.

Le projet vise à faciliter les transactions en ligne pour les entreprises haïtiennes en fournissant une interface simple et sécurisée pour les paiements électroniques.

## Fonctionnalités Principales

### Pour les Marchands
- **Inscription et Authentification** : Création de compte avec informations d'entreprise
- **Génération de Clé API** : Chaque marchand reçoit une clé API unique pour intégrer les paiements
- **Configuration des Méthodes de Paiement** : Choix entre NatCash et MonCash
- **Tableau de Bord** : Visualisation des transactions, statistiques et gestion du profil
- **Gestion des Transactions** : Suivi des paiements reçus avec statuts (En attente, Succès, Échec)

### Pour les Clients
- **Page de Paiement** : Interface de checkout simple et intuitive
- **Simulation de Paiement** : Processus de paiement simulé pour NatCash et MonCash
- **Confirmation de Paiement** : Page de succès avec détails de la transaction

### API de Paiement
- **Initiation de Paiement** : Endpoint API pour démarrer une transaction
- **Validation de Clé API** : Sécurisation des transactions par authentification API
- **Génération d'URL de Paiement** : Création automatique de liens de paiement

## Technologies Utilisées

- **Backend** : Django 5.1.7 (Framework Python)
- **Base de Données** : SQLite (pour développement)
- **Frontend** : HTML5, CSS3, JavaScript
- **Framework CSS** : Bootstrap 5
- **Animations** : Animate.css, WOW.js
- **Carrousels** : Owl Carousel
- **API** : Django REST Framework (implicite via vues JSON)
- **Sécurité** : Django Authentification, CSRF Protection
- **Déploiement** : Configuration pour serveurs locaux et potentiellement ngrok pour tunneling

## Structure du Projet

```
peyem_project/
├── peyem/                    # Configuration principale Django
│   ├── settings.py          # Paramètres de l'application
│   ├── urls.py              # Routage principal
│   ├── wsgi.py              # Configuration WSGI
│   └── asgi.py              # Configuration ASGI
├── base/                     # Application de base
│   ├── templates/           # Templates HTML
│   ├── static/              # Fichiers statiques (CSS, JS, images)
│   └── views.py             # Vues de la page d'accueil
├── merchant/                 # Application des marchands
│   ├── models.py            # Modèle MerchantProfile
│   ├── views.py             # Vues d'inscription, connexion, dashboard
│   ├── forms.py             # Formulaires d'inscription
│   ├── templates/           # Templates spécifiques aux marchands
│   └── urls.py              # Routage de l'application merchant
├── payments/                 # Application de paiements
│   ├── models.py            # Modèle Transaction
│   ├── views.py             # API et vues de paiement
│   ├── templates/           # Template de checkout
│   └── urls.py              # Routage de l'application payments
├── staticfiles/              # Fichiers statiques collectés
├── db.sqlite3                # Base de données SQLite
├── manage.py                 # Script de gestion Django
└── test_api.py               # Script de test de l'API
```

## Installation et Configuration

### Prérequis
- Python 3.8 ou supérieur
- pip (gestionnaire de paquets Python)
- Git (pour cloner le dépôt)

### Étapes d'Installation

1. **Cloner le dépôt**
   ```bash
   git clone https://github.com/PeterEdisonSultan/peyem_project.git
   cd peyem_project
   ```

2. **Créer un environnement virtuel**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Sur Windows: venv\Scripts\activate
   ```

3. **Installer les dépendances**
   ```bash
   pip install -r requirements.txt
   ```

4. **Appliquer les migrations**
   ```bash
   python manage.py migrate
   ```

5. **Créer un superutilisateur (administrateur)**
   ```bash
   python manage.py createsuperuser
   ```

6. **Collecter les fichiers statiques**
   ```bash
   python manage.py collectstatic
   ```

## Utilisation

### Démarrer le serveur de développement
```bash
python manage.py runserver
```

L'application sera accessible à l'adresse : `http://127.0.0.1:8000`

### Pages principales
- **Page d'accueil** : `/`
- **Inscription marchand** : `/merchant/register/`
- **Connexion marchand** : `/merchant/login/`
- **Tableau de bord** : `/merchant/dashboard/`
- **Administration** : `/admin/`

### Test de l'API

Utilisez le script `test_api.py` pour tester l'API de paiement :

```bash
python test_api.py
```

Ce script :
1. Envoie une requête d'initiation de paiement
2. Ouvre automatiquement le navigateur vers la page de checkout
3. Permet de simuler un paiement

## API Documentation

### Endpoint : Initiater un Paiement
**URL** : `/payment/api/initiate/`  
**Méthode** : POST  
**Content-Type** : application/json

**Corps de la requête** :
```json
{
    "api_key": "votre-cle-api",
    "amount": 1000.00,
    "description": "Description du paiement"
}
```

**Réponse de succès** :
```json
{
    "success": true,
    "payment_url": "http://127.0.0.1:8000/payment/checkout/uuid/",
    "reference_id": "uuid-de-la-transaction"
}
```

## Modèles de Données

### MerchantProfile
- `user` : Lien vers l'utilisateur Django
- `company_name` : Nom de l'entreprise
- `phone` : Numéro de téléphone
- `address` : Adresse (optionnel)
- `api_key` : Clé API unique générée automatiquement
- `accepts_natcash` / `accepts_moncash` : Booléens pour méthodes acceptées
- `natcash_name` / `moncash_name` : Noms associés aux comptes
- `natcash_number` / `moncash_number` : Numéros de compte

### Transaction
- `reference_id` : UUID unique de la transaction
- `merchant` : Marchand destinataire
- `amount` : Montant en HTG
- `description` : Description du paiement
- `status` : Statut (PENDING, SUCCESS, FAILED)
- `provider` : Fournisseur utilisé (natcash/moncash)
- `payer_name` : Nom du payeur
- `created_at` / `updated_at` : Timestamps

## Sécurité

- Authentification Django pour les marchands
- Validation des clés API pour les transactions
- Protection CSRF sur les formulaires
- Validation des données d'entrée
- Gestion sécurisée des sessions

## Perspectives d'Amélioration

- Intégration réelle avec les APIs NatCash et MonCash
- Système de notifications (email/SMS)
- Analytics avancés pour les marchands
- Support multi-devises
- Interface mobile responsive optimisée
- Déploiement en production avec serveurs dédiés

## Contribution

Ce projet a été développé dans le cadre du cours Application Web à l'ISTEAH. Pour toute question ou suggestion d'amélioration, veuillez contacter l'auteur.

---

**Note** : Cette application est conçue pour un environnement de développement. Pour un déploiement en production, des configurations supplémentaires de sécurité et de performance sont nécessaires.
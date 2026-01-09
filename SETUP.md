# CRM POC - Setup Completo

## Architettura

```
┌────────────┐        HTTP         ┌──────────────┐
│ Frontend   │ ───────────────▶   │ Django API   │
│ (React)    │                    │ (CRM)        │
└────────────┘                    └──────┬───────┘
                                         │
                                         ▼
                                   ┌──────────┐
                                   │ Database │
                                   │ (MySQL)  │
                                   └──────────┘

┌────────────┐        HTTP         ┌──────────────┐
│ Drupal     │ ───────────────▶   │ Django API   │
│ (cron)     │                    │ (CRM)        │
└────────────┘                    └──────────────┘
```

## Setup Backend

### 1. Configurazione Variabili d'Ambiente

Copia `.env.example` a `.env` e configura i parametri:

```bash
cp .env.example .env
```

Modifica il file `.env` con i tuoi parametri di database.

### 2. Installazione Dipendenze

```bash
cd backend
pip install -r requirements.txt
```

### 3. Migrazioni Database

```bash
python manage.py migrate
```

### 4. Creazione Superuser

```bash
python manage.py createsuperuser
```

### 5. Avvio del Server Django

```bash
python manage.py runserver 0.0.0.0:8000
```

Il backend sarà disponibile su `http://localhost:8000`

## Setup Frontend

### 1. Installazione Dipendenze

```bash
cd frontend
npm install
```

### 2. Variabili d'Ambiente

Crea un file `.env.local` (opzionale):

```env
VITE_API_URL=http://localhost:8000/api
```

### 3. Avvio Server di Sviluppo

```bash
npm run dev
```

L'app sarà disponibile su `http://localhost:3000`

### 4. Build per Produzione

```bash
npm run build
```

## Setup con Docker

### 1. Configurare il file .env

```bash
cp .env.example .env
```

### 2. Avviare i Container

```bash
docker-compose up -d
```

Questo avvierà:
- **MySQL** sulla porta 3306
- **Django API** sulla porta 8000

### 3. Eseguire le Migrazioni

```bash
docker-compose exec backend python manage.py migrate
docker-compose exec backend python manage.py createsuperuser
```

## Integrazione Drupal

### Modulo Drupal

Il modulo Drupal (`drupal-module-1.1.2-Mod`) integra il tuo sito Drupal con il CRM.

#### Funzionalità:

- **Sync Contatti**: Sincronizza gli utenti Drupal come contatti nel CRM
- **Sync Webforms**: Invia le submission dei form Drupal al CRM
- **Campagne**: Gestisce campagne marketing dal CRM
- **Target List**: Sincronizza liste target con Drupal

#### Configurazione:

1. Installa il modulo Drupal nel tuo sito
2. Configura l'URL base del CRM nell'admin di Drupal
3. Configura la chiave API
4. Abilita la sincronizzazione automatica

### API Endpoints per Drupal

L'API Django espone i seguenti endpoint per Drupal:

```
POST   /api/drupal/sync/contact/              - Sincronizza un contatto
POST   /api/drupal/sync/webform-submission/   - Sincronizza webform
GET    /api/drupal/status/                    - Stato della connessione
POST   /api/drupal/test-connection/           - Test connessione
GET    /api/drupal/logs/                      - Log sincronizzazioni
```

## App Django

### core
- Configurazione centrale dell'app

### persons
- Gestione dei contatti/persone
- CRUD operations
- Modello: email (unique), first_name, last_name, phone, company

### webforms
- Gestione dei moduli web
- CRUD operations
- Modello: title, endpoint, description, created_at

### users
- Gestione degli utenti del sistema

### drupal_integration
- Integrazione con Drupal
- Sincronizzazione dati
- Log delle operazioni
- Gestione configurazione

## Endpoints API

### Persons
```
GET    /api/persons/           - Lista persone (paginated)
POST   /api/persons/           - Crea persona
GET    /api/persons/{id}/      - Dettagli persona
PUT    /api/persons/{id}/      - Aggiorna persona
DELETE /api/persons/{id}/      - Elimina persona
```

### WebForms
```
GET    /api/webforms/          - Lista form (paginated)
POST   /api/webforms/          - Crea form
GET    /api/webforms/{id}/     - Dettagli form
PUT    /api/webforms/{id}/     - Aggiorna form
DELETE /api/webforms/{id}/     - Elimina form
```

### Drupal Integration
```
GET    /api/drupal/status/                    - Stato integrazione
POST   /api/drupal/sync/contact/              - Sync contatto
POST   /api/drupal/sync/webform-submission/   - Sync webform
POST   /api/drupal/test-connection/           - Test connessione
GET    /api/drupal/logs/                      - Log di sincronizzazione
```

## Struttura Frontend

```
frontend/
├── src/
│   ├── components/
│   │   ├── PersonsList.jsx         - Lista contatti
│   │   ├── PersonForm.jsx          - Form contatto
│   │   ├── WebFormsList.jsx        - Lista form
│   │   ├── WebFormForm.jsx         - Form modulo
│   │   ├── Dashboard.jsx           - Dashboard principale
│   │   ├── Header.jsx              - Header navigazione
│   │   └── Footer.jsx              - Footer
│   ├── pages/
│   │   ├── PersonsPage.jsx         - Pagina persone
│   │   ├── WebFormsPage.jsx        - Pagina form
│   │   └── IntegrationPage.jsx     - Pagina integrazione Drupal
│   ├── services/
│   │   ├── apiClient.js            - Client Axios
│   │   └── api.js                  - API endpoints
│   ├── styles/
│   │   └── main.css                - Stili globali
│   ├── App.jsx                     - Root component
│   └── main.jsx                    - Entry point
```

## Sviluppo

### Backend
- **Django 6.0** con Django REST Framework
- **MySQL** per il database
- **CORS** abilitato per il frontend

### Frontend
- **React 18** con Vite
- **Axios** per le chiamate API
- **React Router** per la navigazione

## Produzione

### Backend (Docker)
```bash
docker-compose build
docker-compose up -d
```

### Frontend (Build statico)
```bash
cd frontend
npm run build
# Distribuisci la cartella dist su un web server
```

## Troubleshooting

### Errori di connessione database
- Verifica i parametri in `.env`
- Assicurati che MySQL sia in esecuzione
- Per Docker: `docker-compose logs mysql`

### Errori CORS
- Verifica `CORS_ALLOW_ALL_ORIGINS` in settings.py
- In produzione, configura host specifici

### Drupal non si connette
- Verifica l'URL base del CRM
- Controlla la chiave API
- Consulta i log in `/api/drupal/logs/`

## Supporto

Per problemi o domande:
1. Controlla i log del backend: `docker-compose logs backend`
2. Controlla la console del browser (F12)
3. Verifica gli endpoint API con Postman/Insomnia

# CRM Integration - Drupal ↔ Django

Una soluzione **scalabile e production-ready** che integra **Drupal 10** con un **backend Django REST** per la gestione centralizzata di contatti e webform submissions.

## 🎯 Caratteristiche Principali

✅ **Sincronizzazione Bidirezionale** - Webform Drupal → Backend Django  
✅ **Gestione Contatti** - Deduplica, importa da CSV, sincronizza da webform  
✅ **Dashboard Web** - React + Vite per visualizzazione e gestione dati  
✅ **API REST Tokenizzata** - Token-based authentication, endpoint pubblici/privati  
✅ **Importazione CSV** - Drag-and-drop upload con mappatura campi flessibile  
✅ **Sincronizzazione Manuale** - Bypass per il cron bug di Drupal  
✅ **Docker Compose** - Setup one-command con MySQL, Drupal, Django, Vite

---

## 📋 Requisiti

- **Docker** e **Docker Compose** (v2.0+)
- **Git** (per clonare il repository)
- **Windows PowerShell** o **Bash** (per script di avvio)

Non serve installare PHP, Python, Node.js localmente - tutto gira in container Docker!

---

## 🚀 Avvio Veloce

### 1. Clone il repository
```bash
git clone https://github.com/yourusername/crm-poc.git
cd crm-poc
```

### 2. Avvia il progetto
```bash
# Windows
.\start_crm.bat

# Linux/Mac
docker-compose up -d
```

### 3. Accedi ai servizi

| Servizio | URL | Note |
|----------|-----|------|
| **Frontend** | http://localhost:5173 | Dashboard React |
| **Backend API** | http://localhost:8000/api | Django REST API |
| **Drupal Admin** | http://localhost:8080/admin | User: admin, Pass: admin |
| **MySQL** | localhost:3306 | User: root, Pass: root |

---

## 📁 Struttura del Progetto

```
crm-poc/
├── backend/                      # Django REST Framework
│   ├── config/                  # Impostazioni Django
│   │   ├── settings.py         # Configurazione progetto
│   │   ├── urls.py             # URL routing principale
│   │   └── middleware.py        # Token authentication middleware
│   ├── persons/                 # App per gestione contatti
│   │   ├── models.py           # Modello Person
│   │   ├── views.py            # ViewSet REST
│   │   └── serializers.py       # Serializzatori DRF
│   ├── webforms/               # App per webform/submissions
│   │   ├── models.py           # WebformSubmission, Webform, Website
│   │   ├── views.py            # ViewSet + azione sync_from_drupal
│   │   ├── serializers.py       # Serializzatori
│   │   └── sync_drupal_webforms.py  # Script sincronizzazione
│   ├── manage.py               # CLI Django
│   ├── requirements.txt         # Dipendenze Python
│   └── Dockerfile              # Immagine Docker backend
│
├── frontend/                    # React + Vite
│   ├── src/
│   │   ├── components/         # Componenti React
│   │   │   ├── Header.jsx      # Intestazione
│   │   │   ├── PersonsList.jsx # Lista contatti
│   │   │   ├── CSVImportModal.jsx  # Import CSV
│   │   │   └── WebformSyncButton.jsx  # Pulsante sync Drupal
│   │   ├── pages/              # Pagine (Dashboard, Persone, Webform)
│   │   ├── services/           # API client
│   │   └── App.jsx             # Root component
│   ├── package.json            # Dipendenze Node.js
│   ├── vite.config.js          # Configurazione Vite
│   ├── Dockerfile              # Immagine Docker frontend
│   └── index.html              # HTML entry point
│
├── drupal-module-1.1.2-Mod/    # Modulo Drupal crm_integration
│   ├── crm_integration.module  # Hook e logica principale
│   ├── crm_integration.routing.yml  # Route Drupal
│   ├── crm_integration.info.yml     # Metadati modulo
│   ├── src/
│   │   └── integration/
│   │       └── BackendIntegration.php  # Classe sincronizzazione
│   └── config/                 # Configurazione modulo
│
├── docker-compose.yml          # Orchestrazione container
├── init-mysql.sql              # Script inizializzazione DB
├── start_crm.bat               # Script avvio (Windows)
├── requirements.txt            # Dipendenze globali
└── README.md                   # Questo file
```

---

## 🔌 API REST Endpoints

### Autenticazione
```bash
# Token authentication per admin/Drupal
Authorization: Token 4e67bd0be3c363eda173bb895b0af754df3a2fd2
```

### Persone/Contatti
```
GET    /api/persons/              # Lista contatti (pubblico)
POST   /api/persons/              # Crea contatto (token required)
GET    /api/persons/{id}/         # Dettagli contatto
PUT    /api/persons/{id}/         # Aggiorna contatto (token required)
DELETE /api/persons/{id}/         # Elimina contatto (token required)
POST   /api/persons/import_csv/   # Importa da CSV (token required)
```

### Webform & Submissions
```
GET    /api/webforms/              # Lista webform (pubblico)
POST   /api/webforms/              # Crea webform (token required)
GET    /api/webform-submissions/   # Lista submissions (pubblico)
POST   /api/webform-submissions/   # Crea submission (token required)
POST   /api/webform-submissions/sync_from_drupal/  # Sincronizza da Drupal (token required)
```

### Website
```
GET    /api/websites/              # Lista siti web (pubblico)
POST   /api/websites/              # Crea website (token required)
```

---

## 🔐 Autenticazione

### Setup Token (Admin)
1. Accedi a Django Admin: http://localhost:8000/admin
2. Vai a **Tokens** → **Add Token**
3. Seleziona user "drupal-api"
4. Copia il token generato
5. Usa negli header: `Authorization: Token <your-token>`

### Per Drupal
Il modulo `crm_integration` usa il token hardcoded in:  
`drupal-module-1.1.2-Mod/crm_integration.module` (linea ~50)

---

## 🔄 Sincronizzazione Drupal

### Setup Modulo Drupal
1. Copia `drupal-module-1.1.2-Mod/` a `drupal/modules/custom/crm_integration`
2. Accedi a http://localhost:8080/admin/modules
3. Abilita **CRM Integration**
4. Configura l'URL backend in **Configuration** → **CRM Integration Settings**

### Webform → Backend
```
Drupal Webform (crm_poc)
    ↓ (Backend Integration Module)
Django Backend (/api/webform-submissions/)
    ↓ (Auto-create Person)
Database (Persons + WebformSubmissions)
    ↓ (Frontend refresh)
React Dashboard
```

### Sincronizzazione Manuale
Se il cron di Drupal non funziona, usa il frontend:
1. Vai a **Webform** nel dashboard
2. Clicca **🔄 Importa da Drupal**
3. I dati si sincronizzano immediatamente

---

## 📊 Dashboard Frontend

### Sezione Contatti (👥 Contatti)
- **Lista** di tutti i contatti (CSV + Webform + Manuali)
- **Ricerca** per email, nome, cognome, organizzazione
- **Crea** nuovo contatto manualmente
- **Importa CSV** con mappatura campi flessibile
- **Sincronizza** webform da Drupal

### Sezione Webform (📝 Webform)
- **Lista** di submissions da tutti i webform
- **Filtro** per webform specifico
- **Dettagli** completi della submission
- **Sincronizza manuale** per bypass cron bug

### Dashboard (📊 Dashboard)
- **Statistiche** contatti, webform, submissions
- **Ultimi import** e sync
- **Status** sistema

---

## 📥 Importazione CSV

### Formato Supportato
```csv
email,first_name,last_name,organisation,country,website,source_website
user1@example.com,Giovanni,Rossi,Acme Inc,Italia,www.acme.com,https://acme.com
user2@example.com,Maria,Bianchi,TechCorp,UK,www.techcorp.com,https://techcorp.com
```

### Colonne Disponibili
- **email** *(obbligatorio)*
- **first_name**
- **last_name**
- **organisation**
- **country**
- **website**
- **source_website**
- **domain**
- **tags**
- **roles**
- **ppg**
- **type**
- **webform**

### Step Importazione
1. Vai a **Contatti** → **📄 Importa CSV**
2. Seleziona file CSV
3. **Mappa** colonne CSV a campi Backend
4. **Anteprima** dati
5. **Importa** - sistema deduplica automaticamente

---

## 🐛 Troubleshooting

### Frontend non carica
```bash
# Riavvia frontend
docker restart crm-poc-frontend-1
docker logs crm-poc-frontend-1 -f
```

### Backend API non risponde
```bash
# Controlla backend
docker logs crm-poc-backend-1 -f
# Riavvia se necessario
docker restart crm-poc-backend-1
```

### Drupal non si connette a Backend
```bash
# Verifica connettività
docker exec crm-poc-drupal-1 curl -H "Authorization: Token 4e67bd0be3c363eda173bb895b0af754df3a2fd2" http://backend:8000/api/persons/

# Controlla token in modulo
docker exec crm-poc-drupal-1 grep -n "4e67bd0be3c363eda173bb895b0af754df3a2fd2" /var/www/html/modules/custom/crm_integration/crm_integration.module
```

### MySQL non accetta connessioni
```bash
# Reset MySQL
docker-compose down
docker volume rm crm-poc_mysql_data  # ATTENZIONE: cancella dati!
docker-compose up -d
```

---

## 🛠️ Sviluppo

### Aggiungere nuovo campo a Person
1. **Backend**: Modifica `backend/persons/models.py`
2. **Migration**: `docker exec crm-poc-backend-1 python manage.py makemigrations`
3. **Applica**: `docker exec crm-poc-backend-1 python manage.py migrate`
4. **Serializer**: Aggiorna `backend/persons/serializers.py`
5. **Frontend**: Aggiorna componenti React in `frontend/src/`

### Script Amministrazione
```bash
# Shell Django
docker exec crm-poc-backend-1 python manage.py shell

# Crea utente admin
docker exec crm-poc-backend-1 python manage.py createsuperuser

# Statistiche database
docker exec crm-poc-backend-1 python manage.py dbshell
```

---

## 📈 Performance & Scaling

- **Contatti**: Indexed su email, domain - lookup O(log n)
- **Submissions**: Indexed su webform_id, person_id - filtraggio veloce
- **CSV**: Batch import 1000+ record con deduplicazione
- **Drupal Cron**: Bypass con sincronizzazione manuale se lento

---

## 📄 Licenza

MIT License - vedi LICENSE.md

---

## 👥 Support

Per problemi o domande:
1. Controlla i log: `docker-compose logs -f`
2. Verifica connettività: `docker exec <container> curl <endpoint>`
3. Apri un issue su GitHub

---

## Funzionalità del sistema

Il sistema essere usato per:
- ✅ Creare/gestire contatti nel dashboard
- ✅ Importare contatti da CSV
- ✅ Sincronizzare webform da Drupal
- ✅ Visualizzare/filtrare tutti i dati
- ✅ Espandere con nuovi campi/moduli

**Buon utilizzo!** 🚀

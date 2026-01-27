# CRM POC – Drupal ↔ Django Integration

Una soluzione completa che integra **Drupal 10**, **Django REST Framework** e **React** per la gestione centralizzata di contatti e webform submissions.  
L’intero sistema gira in **Docker**, senza necessità di installare PHP, Python o Node.js localmente.


# 🚀 Quick start

## 1. Download repository
```bash
git clone https://github.com/Mike9277/crm-poc.git
cd crm-poc
```

## 2. Avvia l’intero sistema

### Windows
```bash
./start_crm.bat
```
Esempio di output:

```
========================================
       CRM POC is ready!
========================================
Backend API:  http://localhost:8000/api
Frontend:     http://172.17.112.1:5173
Drupal:       http://localhost:8080
========================================
```

### Linux/Mac
```bash
docker-compose up -d
```

Lo script Windows:

- avvia MySQL, Django, Drupal, React  
- ripara cache e lock Drupal  
- ricostruisce la registry  
- rileva automaticamente l’IP locale (`%LOCAL_IP%`)  
- avvia il frontend su `http://%LOCAL_IP%:5173`

> Nota: su alcune reti Docker, `http://localhost:5173` non funziona.  
> Lo script mostra automaticamente l’IP corretto, es. `http://172.17.112.1:5173`.

---

# 🌐 Accesso ai servizi

| Servizio | URL | Note |
|----------|-----|------|
| **Frontend** | http://%LOCAL_IP%:5173 | Dashboard React |
| **Backend API** | http://localhost:8000/api | Django REST API |
| **Drupal** | http://localhost:8080 | Installazione Drupal |
| **MySQL** | localhost:3306 | root / root |

---

# 🧩 Installazione Drupal (primo avvio)

Apri:

```
http://localhost:8080
```

Drupal chiederà di completare l’installazione.

## 1. Configurazione Database

| Campo | Valore |
|-------|--------|
| **Database name** | `drupal` |
| **Database user** | `drupal` |
| **Database password** | `drupal` |
| **Host** | `mysql` |
| **Port** | `3306` |

## 2. Configurazione Sito

| Campo | Valore consigliato |
|-------|---------------------|
| **Site name** | CRM POC |
| **Admin user** | admin |
| **Admin password** | admin |
| **Email** | admin@example.com |
| **Location** | Italy |
| **Timezone** | Europe/Rome |

---

# 🔧 Configurazione Drupal dopo installazione

## 1. Attiva i moduli necessari

Vai su:

```
/admin/modules
```

Attiva:

- **CRM Integration**
- **Webform**
- **Webform UI**

## 2. Configura CRM Integration

Vai su:

```
/admin/config/crm-integration
```

Imposta:

- **Backend URL:** `http://backend:8000/api`
- **API Token:** 12e40283023131fa0c7eac1c95eace9ec88664f1

---

# 📝 Creazione Webform richiesto

1. Vai su:

```
/admin/structure/webform
```

2. Clicca **Add Webform**
3. Nome macchina: `crm_poc`
4. Aggiungi almeno questi campi:

| Campo | Tipo |
|-------|------|
| `first_name` | Textfield |
| `last_name` | Textfield |
| `email` | Email |

5. Salva il webform  
6. Compila e invia una submission di test

---

# 🔄 Test Sincronizzazione Drupal → Backend

1. Apri il **Frontend**:

```
http://%LOCAL_IP%:5173
```

2. Clicca **🔄 Sincronizza Drupal**

Se tutto è configurato correttamente:

- le submissions del webform `crm_poc` vengono importate nel backend  
- vengono creati automaticamente i contatti  
- la dashboard si aggiorna  

---

# 📁 Struttura del Progetto

```
crm-poc/
├── backend/                      # Django REST Framework
├── frontend/                     # React + Vite
├── drupal-module-1.1.2-Mod/      # Modulo custom CRM Integration
├── drupal-modules/               # Moduli Drupal contrib (Webform e Webform UI)
├── docker-compose.yml
├── init-mysql.sql
├── LICENSE.md
├── README.md
├── requirements.txt
├── start_crm.bat                 # Startup script Windows
└── start-frontend.bat
```

---

# 🐛 Troubleshooting

### Frontend non raggiungibile su localhost:5173
Usa l’IP rilevato dallo script:

```
http://%LOCAL_IP%:5173
```

### Drupal non vede il backend
Dal container Drupal:
```bash
docker exec crm_drupal curl http://backend:8000/api
```

### Webform non appare
Assicurati che:

```
drupal-modules/contrib/webform
```

sia presente nel repo.

### Backend “Page not found”
È normale: la root non ha una pagina HTML.  
Usa:

```
http://localhost:8000/api
```
---

# 🎉 Il sistema è pronto!

Puoi:

- creare contatti  
- importare CSV  
- sincronizzare webform da Drupal  
- visualizzare dashboard e statistiche  
- estendere backend, frontend e modulo Drupal  

Buon lavoro! 🚀

# CRM POC - Guida d'Avvio

## 🚀 Avvio Veloce

### Prerequisiti
- Docker e Docker Compose installati
- Node.js v18+ installato localmente (per il frontend)

### 1. Avviare Backend + MySQL (Docker)

```bash
cd crm-poc
docker-compose up -d
```

Questo avvia:
- MySQL su `localhost:3306`
- Django Backend su `localhost:8000`

### 2. Avviare Frontend (Locale)

**Su Windows (PowerShell):**
```powershell
cd crm-poc
cd frontend
npm install  # Solo al primo avvio
npm run dev
```

**Su Windows (CMD):**
```cmd
start-frontend.bat
```

**Su Linux/Mac:**
```bash
bash start-frontend.sh
```

Il frontend sarà disponibile su `http://localhost:5173`

### 3. Accedere all'applicazione

- **Frontend**: http://localhost:5173
- **Backend API**: http://localhost:8000/api
- **Admin Django**: http://localhost:8000/admin

---

## 📊 Verifiche di funzionamento

### Test Backend
```bash
curl http://localhost:8000/api/persons/
```

Dovrebbe tornare una lista (vuota inizialmente) di contatti.

### Test Frontend
Vai su http://localhost:5173 e dovresti vedere:
- Dashboard con statistiche
- Pagina Contatti per CRUD
- Pagina Webform per visualizzare submissioni

---

## 🛑 Fermare i servizi

### Backend (Docker)
```bash
docker-compose down
```

### Frontend
Premi `Ctrl+C` nel terminale dove sta girando `npm run dev`

---

## 📁 Struttura

```
crm-poc/
├── backend/              # Django API
│   ├── persons/         # App Contatti
│   ├── webforms/        # App Webform
│   └── config/          # Impostazioni Django
├── frontend/            # React + Vite
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── services/
│   │   └── styles/
│   └── package.json
└── docker-compose.yml
```

---

## ⚡ Performance

- **Backend**: Avviato in < 1 secondo (Docker)
- **Frontend**: Avviato in < 30 secondi (locale con npm)
- **Hot reload**: Abilitato su entrambi

---

## 🐛 Troubleshooting

### Frontend non si connette al Backend
- Verificare che il backend sia in esecuzione: `curl http://localhost:8000/api/persons/`
- Verificare che VITE_API_URL sia impostato correttamente in `.env.local`

### Port già in uso
- Backend: `lsof -i :8000` (Linux/Mac) o `netstat -ano | findstr :8000` (Windows)
- Frontend: `lsof -i :5173` (Linux/Mac) o `netstat -ano | findstr :5173` (Windows)

### Docker non avvia MySQL
```bash
docker-compose logs mysql
```

---

## 📝 Note

- Le dipendenze npm vengono installate automaticamente al primo `npm install`
- Il frontend ha hot-reload abilitato (modifica file e vedi i cambiamenti istantaneamente)
- CORS è configurato per permettere richieste dal frontend al backend

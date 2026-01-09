# CRM POC Frontend

Frontend React moderno per la gestione di Contatti e Submissioni Webform.

## Funzionalità

- **Dashboard**: Visualizzazione delle statistiche principali
- **Gestione Contatti**: CRUD completo per i contatti (Persons)
- **Visualizzazione Webform**: Lista delle submissioni dai webform

## Tecnologie

- **React 18** - Libreria UI
- **Vite** - Build tool e dev server
- **React Router v6** - Routing
- **Axios** - HTTP client
- **CSS3** - Styling

## Setup

### 1. Installazione dipendenze

```bash
cd frontend
npm install
```

### 2. Variabili d'ambiente

Crea un file `.env.local` nella cartella `frontend`:

```
VITE_API_URL=http://localhost:8000/api
```

### 3. Avviare il dev server

```bash
npm run dev
```

Il frontend sarà disponibile su `http://localhost:5173`

### 4. Build per produzione

```bash
npm run build
```

## Struttura del progetto

```
frontend/
├── src/
│   ├── components/       # Componenti riutilizzabili
│   │   ├── Header.jsx
│   │   ├── Footer.jsx
│   │   ├── PersonForm.jsx
│   │   └── PersonsList.jsx
│   ├── pages/            # Pagine/view principali
│   │   ├── Dashboard.jsx
│   │   ├── PersonsPage.jsx
│   │   └── WebFormsPage.jsx
│   ├── services/         # API client e servizi
│   │   └── api.js
│   ├── styles/           # CSS moduli
│   │   ├── main.css
│   │   ├── header.css
│   │   ├── footer.css
│   │   ├── dashboard.css
│   │   ├── persons.css
│   │   ├── webforms.css
│   │   ├── form.css
│   │   └── list.css
│   ├── App.jsx           # Root component con routing
│   └── main.jsx          # Entry point
├── index.html
├── vite.config.js
├── tsconfig.json
└── package.json
```

## API Endpoints utilizzati

### Persons
- `GET /api/persons/` - Lista contatti
- `GET /api/persons/{id}/` - Dettagli contatto
- `POST /api/persons/` - Crea contatto
- `PUT /api/persons/{id}/` - Aggiorna contatto
- `DELETE /api/persons/{id}/` - Elimina contatto

### WebForm Submissions
- `GET /api/webforms/` - Lista submissioni
- `GET /api/webforms/{id}/` - Dettagli submissione

## Autore

CRM POC - 2026

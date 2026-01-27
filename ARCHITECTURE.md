# 🏗️ Architecture Overview

Guida architetturale del sistema CRM Integration.

---

## High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     FRONTEND (React + Vite)                 │
│  http://localhost:5173                                       │
│  - Dashboard / Contatti / Webform                            │
│  - CSV Import Modal                                          │
│  - Webform Sync Button                                       │
└─────────────────────────────────────────────────────────────┘
                            ↓ HTTP/REST
┌─────────────────────────────────────────────────────────────┐
│           API GATEWAY / REVERSE PROXY (Nginx)                │
│  Handles CORS, SSL, Rate Limiting                            │
└─────────────────────────────────────────────────────────────┘
                    ↓                        ↓
        ┌───────────────────┐    ┌──────────────────┐
        │                   │    │                  │
        ↓                   ↓    ↓                  ↓
  ┌─────────────┐    ┌─────────────────┐   ┌──────────────┐
  │   BACKEND   │    │    DRUPAL 10    │   │   DATABASE   │
  │  (Django)   │    │    (PHP 8.3)    │   │   (MySQL 8)  │
  │  :8000/api/ │    │   :8080/admin   │   │   :3306      │
  └─────────────┘    └─────────────────┘   └──────────────┘
       ↓                      ↓                   ↓
    - Persons            - Webforms          - Contacts
    - WebformSubmissions - crm_integration   - Submissions
    - Websites           - Config            - Website data
```

---

## System Components

### 1. **Frontend (React + Vite)**

```
frontend/
├── src/
│   ├── components/
│   │   ├── Header.jsx              # Navigation header
│   │   ├── PersonsList.jsx         # Contact list view
│   │   ├── PersonForm.jsx          # Add/edit contact
│   │   ├── CSVImportModal.jsx      # CSV import wizard
│   │   ├── WebformSyncButton.jsx   # Drupal sync button
│   │   └── Footer.jsx              # Footer
│   ├── pages/
│   │   ├── Dashboard.jsx           # Stats & overview
│   │   ├── PersonsPage.jsx         # Contacts management
│   │   └── WebFormsPage.jsx        # Submissions view
│   ├── services/
│   │   └── api.js                  # REST API client
│   ├── styles/                     # CSS modules
│   └── App.jsx                     # Root component
└── vite.config.js                  # Build config
```

**Key Features:**
- 🎨 React component architecture
- ⚡ Vite for fast development
- 🔄 Auto-refresh on data changes
- 📱 Responsive design
- 🎯 Client-side filtering & search

---

### 2. **Backend (Django REST Framework)**

```
backend/
├── config/
│   ├── settings.py        # Django settings
│   ├── urls.py            # URL routing
│   ├── wsgi.py            # WSGI app
│   └── middleware.py      # Token authentication
├── persons/
│   ├── models.py          # Person model + deduplica
│   ├── views.py           # PersonViewSet
│   ├── serializers.py     # JSON serialization
│   └── urls.py            # Persons endpoints
├── webforms/
│   ├── models.py          # Webform, WebformSubmission
│   ├── views.py           # WebformViewSet + sync action
│   ├── serializers.py     # Webform serializers
│   ├── sync_drupal_webforms.py  # Manual sync script
│   └── urls.py            # Webform endpoints
├── websites/
│   ├── models.py          # Website model
│   ├── views.py           # WebsiteViewSet
│   ├── serializers.py     # Website serializers
│   └── urls.py            # Website endpoints
├── manage.py              # Django CLI
└── requirements.txt       # Dependencies
```

**Data Models:**

```python
# Persons
Person
├── id (PK)
├── email (unique)
├── first_name
├── last_name
├── organisation
├── country
├── domain
├── created_at
└── updated_at

# Webforms
Website
├── id (PK)
├── name
├── url (unique)
└── external_id

Webform
├── id (PK)
├── website_id (FK)
├── name
├── external_id (unique per website)
└── description

WebformSubmission
├── id (PK)
├── webform_id (FK)
├── person_id (FK)
├── external_id (drupal sid)
├── payload (JSON with form data)
├── source_website
├── created_at
└── updated_at
```

**API Endpoints:**

```
GET    /api/persons/              # List all (public)
POST   /api/persons/              # Create (auth required)
GET    /api/persons/{id}/         # Detail
PUT    /api/persons/{id}/         # Update (auth required)
DELETE /api/persons/{id}/         # Delete (auth required)
POST   /api/persons/import_csv/   # CSV import (auth required)

GET    /api/webforms/             # List all (public)
POST   /api/webforms/             # Create (auth required)

GET    /api/webform-submissions/  # List all (public)
POST   /api/webform-submissions/sync_from_drupal/  # Manual sync (auth required)

GET    /api/websites/             # List all (public)
POST   /api/websites/             # Create (auth required)
```

**Authentication:**
- Token-based (header: `Authorization: Token <token>`)
- Protected endpoints: POST, PUT, DELETE
- Public endpoints: GET (lists)

---

### 3. **Drupal Module (crm_integration)**

```
drupal-module-1.1.2-Mod/
├── crm_integration.module       # Hooks & cron
├── crm_integration.info.yml     # Module metadata
├── crm_integration.routing.yml  # Routes
├── src/
│   └── integration/
│       └── BackendIntegration.php    # Main sync class
└── config/
    └── install/                      # Default config
```

**Key Functions:**

```php
// Sync on webform submission
hook_webform_submission_insert()
  └─> BackendIntegration::syncSubmission()
      ├─ Extract form data
      ├─ Call Backend API: POST /api/webform-submissions/
      └─ Auto-create Person if new email

// Periodic sync (cron)
hook_cron()
  └─> BackendIntegration::syncUnsentSubmissions()
      ├─ Read config timestamp
      ├─ Find new submissions since last sync
      ├─ POST to backend
      └─ Update timestamp (BUG: global, not per-webform)

// Admin form
hook_form_alter()
  └─> Add CRM settings to webform config
```

---

### 4. **Database (MySQL 8)**

**Schema Overview:**

```sql
-- Drupal DB
drupal.webform
drupal.webform_submission
drupal.webform_submission_data
drupal.config

-- Backend DB (crm)
crm.persons_person
crm.webforms_webform
crm.webforms_webformsubmission
crm.webforms_website
```

---

## Data Flow Diagrams

### Create Contact Flow

```
User fills webform in Drupal
    ↓
Drupal webform_submission_insert hook
    ↓
BackendIntegration::syncSubmission()
    ↓
POST /api/webform-submissions/
    {
      "webform_id": 5,
      "person_id": 46,
      "payload": {"email": "...", "first_name": "...", ...},
      "external_id": "drupal_sid_123"
    }
    ↓
Django WebformSubmissionViewSet.create()
    ├─ Check if Person exists (by email)
    ├─ If not: auto-create Person
    ├─ Create WebformSubmission record
    └─ Return 201 Created
    ↓
Frontend auto-refreshes
    ↓
New contact appears in dashboard
```

### CSV Import Flow

```
User selects CSV file
    ↓
Frontend CSVImportModal
    ├─ Parse CSV
    ├─ Show field mapping UI
    ├─ Preview data
    └─ User confirms
    ↓
POST /api/persons/import_csv/
    [
      {"email": "...", "first_name": "...", ...},
      ...
    ]
    ↓
Django PersonViewSet.import_csv()
    ├─ Loop each record
    ├─ Check dedup_key (email unique)
    ├─ If exists: skip or update (on_conflict='skip')
    ├─ If new: create Person
    └─ Return stats (created, updated, skipped)
    ↓
Frontend shows results:
    "5 created, 2 updated, 1 skipped"
    ↓
Frontend refreshes list
    ↓
New contacts appear in dashboard
```

### Manual Drupal Sync Flow

```
User clicks "🔄 Importa da Drupal" button
    ↓
Frontend POST /api/webform-submissions/sync_from_drupal/
    ↓
Django action sync_from_drupal()
    ├─ Call sync_drupal_webforms.py script
    ├─ Script connects directly to Drupal DB
    ├─ Query webform_submission table
    ├─ Extract submission data
    ├─ Call backend import logic
    └─ Return results
    ↓
Frontend shows:
    "✅ 2 submissions imported"
    ↓
Frontend auto-refreshes lists
    ↓
Submissions appear in Webform section
```

---

## Authentication Flow

```
Initial Setup:
  1. Django admin creates User "drupal-api"
  2. Generate Token for this user
  3. Token saved in Drupal module config
  4. Token stored in .env or Docker secret

Request Flow:
  1. Drupal module sends HTTP request with:
     Authorization: Token <token>
     
  2. Django TokenAuthentication middleware:
     ├─ Extract token from header
     ├─ Lookup Token in database
     ├─ Find associated User
     ├─ Attach User to request.user
     └─ Allow or deny based on permissions
     
  3. ViewSet checks permissions:
     ├─ Public endpoints (GET): AllowAny
     ├─ Write endpoints (POST/PUT/DELETE): IsAuthenticated
     ├─ Admin endpoints: IsAdminUser
     
  4. Return response or 401 Unauthorized
```

---

## Deployment Architecture

### Development (Docker Compose - Local)

```
localhost:5173   ←→  frontend container
localhost:8000   ←→  backend container (Django)
localhost:8080   ←→  drupal container (Drupal 10)
localhost:3306   ←→  mysql container (MySQL 8)
```

### Production (Suggested)

```
Browser (HTTPS)
    ↓
Nginx (SSL/TLS)
    ├─→ :5173 → Frontend (Node)
    ├─→ :8000 → Backend (Gunicorn)
    └─→ :8080 → Drupal (Apache)
    
Databases:
    ├─→ PostgreSQL (managed RDS/Heroku)
    ├─→ Redis (caching)
    └─→ S3 (file storage)

Monitoring:
    ├─→ Sentry (error tracking)
    ├─→ ELK Stack (logging)
    └─→ Prometheus (metrics)
```

---

## Performance Considerations

### Database Queries

```python
# ✗ Bad: N+1 queries
submissions = WebformSubmission.objects.all()
for sub in submissions:
    print(sub.webform.name)  # Extra query each loop!

# ✓ Good: Prefetch related
submissions = WebformSubmission.objects.select_related('webform', 'person').all()
for sub in submissions:
    print(sub.webform.name)  # No extra query
```

### Caching Strategy

```python
# Cache frequent queries
@cache_page(60 * 5)  # 5 minutes
def list_persons(request):
    return Response(...)

# Cache specific fields
from django.views.decorators.cache import cache_page
CACHE_TIMEOUT = 300
persons = cache.get_or_set('all_persons', get_all_persons, CACHE_TIMEOUT)
```

### Frontend Optimization

```javascript
// Code splitting
const PersonsList = lazy(() => import('./PersonsList'));

// Lazy load on scroll
IntersectionObserver for infinite scroll

// Batch API calls
Promise.all([fetch1(), fetch2(), fetch3()])

// Request debouncing
const [searchTerm, setSearchTerm] = useState('');
const debouncedSearch = debounce((term) => {
  api.search(term);
}, 300);
```

---

## Security Architecture

```
┌─────────────────────────────────────────────────────┐
│           LAYER 1: Network Security                 │
│ - HTTPS/SSL                                         │
│ - Firewall rules                                    │
│ - DDoS protection (CloudFlare)                      │
└─────────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────────┐
│         LAYER 2: Application Security               │
│ - CORS whitelisting                                 │
│ - CSRF protection                                   │
│ - Rate limiting                                     │
│ - Input validation                                  │
└─────────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────────┐
│      LAYER 3: Authentication & Authorization        │
│ - Token-based auth                                  │
│ - Permission checks                                 │
│ - Role-based access (RBAC)                          │
└─────────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────────┐
│          LAYER 4: Data Security                     │
│ - Database encryption                              │
│ - Secrets management                               │
│ - Audit logging                                    │
│ - Regular backups                                  │
└─────────────────────────────────────────────────────┘
```

---

## Monitoring & Logging

```
Application Logs:
  Django: /var/log/django.log
  Drupal: /var/log/apache2/error.log
  Frontend: Browser console

Error Tracking:
  Sentry integration for exceptions

Metrics:
  - Request count/latency
  - Database query performance
  - Cache hit rate
  - Sync success rate

Health Checks:
  GET /api/health/
  - Database connectivity
  - Cache availability
  - Drupal reachability
```

---

## Scaling Considerations

### Horizontal Scaling

```
Load Balancer (HAProxy/Nginx)
    ├─→ Backend 1
    ├─→ Backend 2
    └─→ Backend 3

Shared:
    ├─→ PostgreSQL (read replicas)
    ├─→ Redis (distributed cache)
    └─→ S3 (shared storage)
```

### Vertical Scaling

```
Single Instance Optimization:
    - Increase CPU cores
    - Increase RAM
    - SSD storage
    - Connection pooling
```

### Database Scaling

```
Read Replicas:
    Primary (write) → Replica 1 (read)
                  → Replica 2 (read)

Sharding (future):
    Shard by person_id or webform_id
```

---

## Future Architecture Improvements

- [ ] Microservices: Separate sync service
- [ ] Message Queue: Celery for async tasks
- [ ] GraphQL: Alternative to REST API
- [ ] Event Sourcing: Track all state changes
- [ ] CQRS: Separate read/write models
- [ ] Multi-tenant: Support multiple Drupal sites
- [ ] Mobile App: React Native client

---

**Last Updated**: 2026-01-21

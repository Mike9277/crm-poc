# ⚡ Quick Start

Get up and running in **5 minutes**!

---

## Prerequisites

✅ **Docker** installed ([Download](https://www.docker.com/products/docker-desktop))  
✅ **Git** installed ([Download](https://git-scm.com/))  
✅ **Admin access** on your machine  
✅ **Ports 5173, 8000, 8080, 3306** available

---

## Step 1: Clone & Enter Directory

```bash
git clone https://github.com/yourusername/crm-poc.git
cd crm-poc
```

---

## Step 2: Start Everything

### Windows (PowerShell)
```powershell
.\start_crm.bat
```

### Linux/Mac (Bash)
```bash
docker-compose up -d
```

⏳ **Wait 30-60 seconds** for containers to start...

---

## Step 3: Access Services

Open in your browser:

| Service | URL | User | Pass |
|---------|-----|------|------|
| 🎨 **Frontend** | http://localhost:5173 | - | - |
| 📊 **Backend API** | http://localhost:8000/api | - | - |
| 🔧 **Django Admin** | http://localhost:8000/admin | admin | admin |
| 🌐 **Drupal Admin** | http://localhost:8080/admin | admin | admin |

---

## Step 4: First Test - Create a Contact

### Via Frontend
1. Go to http://localhost:5173
2. Click **👥 Contatti**
3. Click **+ Nuovo Contatto**
4. Fill form:
   - Email: `test@example.com`
   - Nome: `John`
   - Cognome: `Doe`
5. Click **Salva**
6. ✅ Contact appears in list!

### Via API
```bash
curl -X POST http://localhost:8000/api/persons/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "first_name": "John",
    "last_name": "Doe"
  }'
```

---

## Step 5: Import from CSV

### Create Sample CSV
Save as `contacts.csv`:
```csv
email,first_name,last_name,organisation
alice@company.com,Alice,Smith,Acme Inc
bob@company.com,Bob,Jones,TechCorp
charlie@company.com,Charlie,Brown,StartUp
```

### Import via Frontend
1. Go to **👥 Contatti**
2. Click **📄 Importa CSV**
3. Select `contacts.csv`
4. **Map fields** (auto-detected)
5. **Review** the 3 rows
6. Click **Importa**
7. ✅ 3 new contacts added!

---

## Step 6: Test Webform Sync

### Create Webform in Drupal
1. Go to http://localhost:8080/admin
2. Navigate to **Webform** → **Forms**
3. Create new webform named `test_form`
4. Add fields:
   - **Email** (text/email)
   - **Nome** (text)
   - **Cognome** (text)
5. Save webform
6. **Submit a test form** with:
   - Email: `drupal@test.com`
   - Nome: `Mario`
   - Cognome: `Rossi`

### Sync to Backend
1. Go to http://localhost:5173
2. Go to **📝 Webform**
3. Click **🔄 Importa da Drupal**
4. Wait for "✅ Sincronizzazione completata"
5. ✅ Submission appears in list!

### Check Contact Created
1. Go to **👥 Contatti**
2. Search for `drupal@test.com`
3. ✅ Contact was auto-created from webform submission!

---

## Verify Everything Works

### ✅ Checklist

```
□ Frontend loads (http://localhost:5173)
□ Dashboard shows statistics
□ Can create contact manually
□ Can see contacts list
□ CSV import works
□ Can see webform submissions
□ Drupal sync button works
□ Drupal admin accessible
□ Backend API returns data
```

---

## Useful Commands

### View Logs
```bash
# All containers
docker-compose logs -f

# Specific container
docker logs crm-poc-backend-1 -f

# Last 50 lines
docker logs crm-poc-backend-1 --tail 50
```

### Access Shell
```bash
# Django shell
docker exec -it crm-poc-backend-1 python manage.py shell

# MySQL
docker exec -it crm-poc-mysql-1 mysql -u root -proot crm

# Drupal
docker exec -it crm-poc-drupal-1 bash
```

### Restart Service
```bash
# Restart backend
docker restart crm-poc-backend-1

# Restart all
docker-compose restart
```

### Database Backup
```bash
docker exec crm-poc-mysql-1 mysqldump -u root -proot crm > backup.sql
```

---

## Troubleshooting

### Frontend doesn't load
```bash
docker logs crm-poc-frontend-1 -f
# Check for port 5173 conflicts
# Try: docker-compose restart crm-poc-frontend-1
```

### Backend API error
```bash
docker logs crm-poc-backend-1 -f
# Check database connectivity
curl http://localhost:8000/api/persons/
```

### Drupal not responding
```bash
docker logs crm-poc-drupal-1 -f
# Wait 30 seconds for startup
# Check http://localhost:8080
```

### Port already in use
```bash
# Find process using port 8000
netstat -ano | findstr :8000

# Change docker-compose.yml port mapping
# Change: "8000:8000" to "8001:8000"
```

---

## Next Steps

📖 **Full Documentation**:
- [README.md](README.md) - Complete setup & features
- [ARCHITECTURE.md](ARCHITECTURE.md) - Technical architecture
- [DEPLOYMENT.md](DEPLOYMENT.md) - Production deployment
- [CONTRIBUTING.md](CONTRIBUTING.md) - Development guide

🎓 **Learn More**:
- [Django REST docs](https://www.django-rest-framework.org/)
- [React docs](https://react.dev/)
- [Drupal 10 docs](https://www.drupal.org/docs/drupal-apis)

🤝 **Contribute**:
- See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines
- Fork on GitHub and submit PRs

---

## API Quick Reference

### Get All Contacts
```bash
curl http://localhost:8000/api/persons/
```

### Create Contact
```bash
curl -X POST http://localhost:8000/api/persons/ \
  -H "Content-Type: application/json" \
  -d '{"email":"new@test.com","first_name":"New","last_name":"User"}'
```

### Get All Webforms
```bash
curl http://localhost:8000/api/webforms/
```

### Get Submissions
```bash
curl http://localhost:8000/api/webform-submissions/
```

### Manual Drupal Sync (requires auth token)
```bash
curl -X POST http://localhost:8000/api/webform-submissions/sync_from_drupal/ \
  -H "Authorization: Token 4e67bd0be3c363eda173bb895b0af754df3a2fd2"
```

---

## Support

- 📖 Check [README.md](README.md) for detailed docs
- 🐛 Found a bug? Report on GitHub Issues
- 💡 Have an idea? Open a GitHub Discussion

---

**Everything working? Great! 🎉**

Now explore the full [README](README.md) to learn all features!

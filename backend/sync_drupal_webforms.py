#!/usr/bin/env python
"""
Script manuale per sincronizzare webform submissions da Drupal a Backend.
Questo bypassa il cron che ha un bug.
"""

import os
import django
import json
from datetime import datetime
import MySQLdb

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from webforms.models import Website, Webform, WebformSubmission
from persons.models import Person

print("=" * 70)
print("SINCRONIZZAZIONE WEBFORM SUBMISSIONS - Drupal to Backend")
print("=" * 70)

# Connessione diretta al database Drupal (MySQLdb)
drupal_conn = None
drupal_cursor = None

try:
    drupal_conn = MySQLdb.connect(
        host="mysql",
        user="root",
        passwd="root",
        db="drupal"
    )
    drupal_cursor = drupal_conn.cursor()
    print("\n✓ Connesso al database Drupal")
except Exception as e:
    print(f"✗ Errore connessione Drupal: {e}")
    exit(1)

# Configurazione
DRUPAL_SITE_URL = "http://localhost:8080"
DRUPAL_WEBSITE_NAME = "Drupal Site"

try:
    # Step 1: Ottieni o crea il website di Drupal nel backend
    print("\n[STEP 1] Verifica website Drupal nel backend...")
    website, created = Website.objects.get_or_create(
        url=DRUPAL_SITE_URL,
        defaults={'name': DRUPAL_WEBSITE_NAME}
    )
    if created:
        print(f"✓ Website creato: {website.id}")
    else:
        print(f"✓ Website trovato: {website.id}")
    
    # Step 2: Leggi i webform dalla tabella webform di Drupal
    print("\n[STEP 2] Leggi webform abilitati da Drupal...")
    drupal_cursor.execute("""
        SELECT webform_id FROM webform
    """)
    webforms_drupal = drupal_cursor.fetchall()
    
    print(f"✓ Trovati {len(webforms_drupal)} webform in Drupal:")
    for (webform_id_item,) in webforms_drupal:
        print(f"  - {webform_id_item}")
    
    # Step 3: Per ogni webform, importa le submissions
    print("\n[STEP 3] Importa submissions da ogni webform...")
    total_submissions_found = 0
    total_submissions_imported = 0
    
    for (webform_id_item,) in webforms_drupal:
        webform_id = webform_id_item  # webform_id è il nome del webform
        print(f"\n  Elaborazione webform: {webform_id}")
        
        # Ottieni il titolo dal file di configurazione
        drupal_cursor.execute("""
            SELECT data FROM config
            WHERE name = %s AND collection = 'webform.webform'
        """, (webform_id,))
        config_row = drupal_cursor.fetchone()
        title = webform_id  # default al nome se non trovato
        
        if config_row:
            config_data = config_row[0]
            # Estrai il label/title dal YAML (semplice regex)
            import re
            match = re.search(r"label:\s['\"]?([^'\"\n]+)", config_data)
            if match:
                title = match.group(1)
        
        # Ottieni o crea il webform nel backend
        backend_webform, created = Webform.objects.get_or_create(
            website=website,
            external_id=webform_id,
            defaults={
                'name': title,
                'description': f'Imported from Drupal: {title}'
            }
        )
        
        if created:
            print(f"    ✓ Webform creato nel backend: {backend_webform.id}")
        else:
            print(f"    ✓ Webform trovato nel backend: {backend_webform.id}")
        
        # Leggi le submissions completate da questa webform
        drupal_cursor.execute("""
            SELECT sid, created FROM webform_submission 
            WHERE webform_id = %s AND completed IS NOT NULL
            ORDER BY sid
        """, (webform_id,))
        
        submissions = drupal_cursor.fetchall()
        print(f"    • Trovate {len(submissions)} submissions completate")
        
        for sid, created_timestamp in submissions:
            total_submissions_found += 1
            
            # Controlla se già importata (usa external_id = drupal sid)
            if WebformSubmission.objects.filter(
                external_id=str(sid),
                webform=backend_webform
            ).exists():
                print(f"      ℹ Submission {sid} già importata")
                continue
            
            # Leggi i dati della submission da webform_submission_data
            # Questa tabella ha (sid, webform_id, name, value)
            drupal_cursor.execute("""
                SELECT name, value FROM webform_submission_data 
                WHERE sid = %s AND webform_id = %s
                ORDER BY name
            """, (sid, webform_id))
            
            data_rows = drupal_cursor.fetchall()
            
            # Organizza i dati in un dizionario
            submission_data = {}
            for name, value in data_rows:
                submission_data[name] = value
            
            print(f"      → Importing submission {sid}: {json.dumps(submission_data)}")
            
            # Estrai i campi rilevanti
            email = submission_data.get('email', '').strip()
            first_name = submission_data.get('first_name', '').strip()
            last_name = submission_data.get('last_name', '').strip()
            
            if not email:
                print(f"      ⚠ Submission {sid} ha email vuota - skip")
                continue
            
            # Crea Person se non esiste
            person, created = Person.objects.get_or_create(
                email=email,
                defaults={
                    'first_name': first_name,
                    'last_name': last_name,
                }
            )
            if created:
                print(f"      ✓ Created Person: {first_name} {last_name} ({email})")
            else:
                print(f"      ✓ Person exists: {first_name} {last_name} ({email})")
            
            # Crea WebformSubmission
            ws = WebformSubmission.objects.create(
                webform=backend_webform,
                person=person,
                external_id=str(sid),
                payload=submission_data,
                source_website=DRUPAL_SITE_URL,
            )
            print(f"      ✓ Created WebformSubmission {ws.id}")
            total_submissions_imported += 1
    
    print("\n" + "=" * 70)
    print(f"RISULTATI: {total_submissions_imported} submissions importate su {total_submissions_found} trovate")
    print("=" * 70)

except Exception as e:
    print(f"\n✗ Errore durante sincronizzazione: {e}")
    import traceback
    traceback.print_exc()

finally:
    if drupal_cursor:
        drupal_cursor.close()
    if drupal_conn:
        drupal_conn.close()
    print("\n✓ Chiusa connessione Drupal")

#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Test CSV import service"""
import os
import sys
import django
import traceback
import logging

# Force UTF-8 output
os.environ['PYTHONIOENCODING'] = 'utf-8'
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

logging.basicConfig(level=logging.DEBUG)

from persons.services.csv_import import CSVImportService
from persons.models import Person

# Test parsing CSV
csv_content = """email,first_name,last_name,source_website
test_import1@example.com,Mario,Rossi,Website A
test_import2@example.com,Luigi,Bianchi,Website B
test_import3@example.com,Anna,Verdi,Website C"""

records = CSVImportService.parse_csv(csv_content)
print(f"Parsed {len(records)} records:")
for r in records:
    print(f"  {r}")

# Test import - direct creation first
print("\nTesting direct Person.objects.create()...")
try:
    p = Person.objects.create(
        email='direct_test@example.com',
        first_name='Direct',
        last_name='Test',
        source_website='Test'
    )
    print(f"  Direct create success: {p}")
except Exception as e:
    print(f"  Direct create failed: {e}")
    traceback.print_exc()

# Test import via service
print("\nTesting CSVImportService.import_persons()...")
try:
    stats = CSVImportService.import_persons(records)
    print(f"  Created: {stats['created']}")
    print(f"  Updated: {stats['updated']}")
    print(f"  Skipped: {stats['skipped']}")
    print(f"  Errors: {len(stats['errors'])}")

    if stats['errors']:
        print("\nError details:")
        for err in stats['errors']:
            print(f"  Row {err['row']}: {err['error']}")
except Exception as e:
    print(f"\nException: {e}")
    traceback.print_exc()

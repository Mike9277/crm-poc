#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
from pathlib import Path

# Carica variabili di ambiente da .env e .env.local
from dotenv import load_dotenv
env_file = Path(__file__).resolve().parent / '.env'
env_local = Path(__file__).resolve().parent / '.env.local'
if env_file.exists():
    load_dotenv(env_file)
if env_local.exists():
    load_dotenv(env_local)


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()

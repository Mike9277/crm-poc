import csv
import io
import logging
from django.db import IntegrityError
from persons.models import Person

logger = logging.getLogger(__name__)

class CSVImportService:
    """
    Servizio per importare Person da CSV con mapping dei campi.
    Supporta configurazione flessibile dei mapping.
    """

    REQUIRED_FIELDS = ['email']
    OPTIONAL_FIELDS = [
        'first_name', 'last_name', 'source_website', 'external_id',
        'country', 'organisation', 'domain', 'tags', 'roles', 'ppg', 'type', 'website', 'webform'
    ]

    @staticmethod
    def validate_mapping(mapping):
        if 'email' not in mapping:
            raise ValueError("Mapping deve contenere almeno il campo 'email'")
        
        valid_fields = set(CSVImportService.REQUIRED_FIELDS + CSVImportService.OPTIONAL_FIELDS)
        for field in mapping.keys():
            if field not in valid_fields:
                raise ValueError(f"Campo '{field}' non valido. Campi supportati: {valid_fields}")

    @staticmethod
    def clean_value(value):
        """
        Pulisce un valore CSV rimuovendo spazi e virgolette indesiderate.
        """
        if not value:
            return None
        
        # Rimuovi spazi bianchi iniziali e finali
        value = value.strip()
        
        # Rimuovi virgolette all'inizio e alla fine se presenti
        while value.startswith('"') or value.startswith("'"):
            value = value[1:]
        while value.endswith('"') or value.endswith("'"):
            value = value[:-1]
        
        # Rimuovi di nuovo eventuali spazi dopo aver tolto le virgolette
        value = value.strip()
        
        return value if value else None

    @staticmethod
    def parse_csv(file_content, mapping=None, skip_header=True):
        """
        Parsa un file CSV e ritorna lista di records mappati.
        Gestisce correttamente BOM, virgolette e spazi.
        """
        if isinstance(file_content, bytes):
            # L'encoding 'utf-8-sig' rimuove automaticamente il BOM
            content_str = file_content.decode('utf-8-sig')
            file_content = io.StringIO(content_str)
        elif isinstance(file_content, str):
            # Se è già stringa, rimuoviamo manualmente il BOM se presente
            file_content = io.StringIO(content_str.lstrip('\ufeff'))

        # Usa csv.DictReader per gestire meglio i CSV
        if mapping is None:
            if not skip_header:
                raise ValueError("Se skip_header è False, mapping deve essere fornito")
            
            # Usa DictReader che gestisce automaticamente l'header
            reader = csv.DictReader(file_content, skipinitialspace=True)
            
            # Verifica che ci siano colonne
            if reader.fieldnames is None:
                raise ValueError("Il file CSV è vuoto")
            
            # Pulisci i nomi delle colonne
            cleaned_fieldnames = [CSVImportService.clean_value(name) for name in reader.fieldnames]
            reader.fieldnames = cleaned_fieldnames
            
            # Valida i campi
            mapping = {field: field for field in cleaned_fieldnames}
            CSVImportService.validate_mapping(mapping)
            
            records = []
            for row in reader:
                if not any(row.values()):  # Salta righe vuote
                    continue
                
                # Pulisci tutti i valori della riga
                record = {
                    key: CSVImportService.clean_value(value)
                    for key, value in row.items()
                }
                records.append(record)
        else:
            # Modalità con mapping personalizzato
            reader = csv.reader(file_content, skipinitialspace=True)
            
            if skip_header:
                try:
                    next(reader)  # Salta l'header
                except StopIteration:
                    raise ValueError("Il file CSV è vuoto")
            
            CSVImportService.validate_mapping(mapping)
            
            records = []
            for row in reader:
                if not any(row):  # Salta righe vuote
                    continue
                
                record = {}
                for field, col_idx in mapping.items():
                    if col_idx < len(row):
                        record[field] = CSVImportService.clean_value(row[col_idx])
                    else:
                        record[field] = None
                records.append(record)

        return records

    @staticmethod
    def import_persons(records, on_conflict='update'):
        """
        Importa una lista di person records nel database.
        Default on_conflict impostato su 'update' per maggiore utilità.
        """
        stats = {'created': 0, 'updated': 0, 'skipped': 0, 'errors': []}

        for idx, record in enumerate(records, start=1):
            try:
                email = record.get('email')
                if not email:
                    stats['errors'].append({
                        'row': idx,
                        'error': 'Email mancante',
                        'data': record
                    })
                    stats['skipped'] += 1
                    continue

                # Prepariamo i defaults
                defaults = {
                    field: record.get(field, '') if field in ['first_name', 'last_name'] else record.get(field)
                    for field in CSVImportService.OPTIONAL_FIELDS
                }
                
                # Se on_conflict è 'skip', dobbiamo prima controllare se esiste
                if on_conflict == 'skip':
                    person, created = Person.objects.get_or_create(
                        email=email,
                        defaults=defaults
                    )
                else:
                    # 'update' (default) o 'error'
                    person, created = Person.objects.update_or_create(
                        email=email,
                        defaults=defaults
                    )

                if created:
                    stats['created'] += 1
                    logger.info(f"Created person: {email}")
                else:
                    if on_conflict == 'skip':
                        stats['skipped'] += 1
                        logger.info(f"Skipped existing person: {email}")
                    else:
                        stats['updated'] += 1
                        logger.info(f"Updated person: {email}")

            except IntegrityError as e:
                error_msg = f'Errore integrità: {str(e)}'
                stats['errors'].append({'row': idx, 'error': error_msg, 'data': record})
                logger.error(f"Row {idx}: {error_msg}")
            except Exception as e:
                error_msg = f'Errore: {str(e)}'
                stats['errors'].append({'row': idx, 'error': error_msg, 'data': record})
                logger.error(f"Row {idx}: {error_msg}")

        return stats
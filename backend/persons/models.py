from django.db import models
import logging

logger = logging.getLogger(__name__)


class Person(models.Model):
    # Campi di base
    first_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField(unique=True)
    source_website = models.CharField(max_length=255, blank=True, null=True)
    
    # Informazioni aggiuntive
    country = models.CharField(max_length=100, blank=True, null=True)
    organisation = models.CharField(max_length=255, blank=True, null=True)
    domain = models.CharField(max_length=255, blank=True, null=True)
    website = models.CharField(max_length=255, blank=True, null=True)
    webform = models.CharField(max_length=255, blank=True, null=True)
    tags = models.CharField(max_length=500, blank=True, null=True)  # CSV format
    roles = models.CharField(max_length=500, blank=True, null=True)  # CSV format
    ppg = models.CharField(max_length=255, blank=True, null=True)
    type = models.CharField(max_length=100, blank=True, null=True)
    
    # Campi Drupal per deduplicazione
    external_id = models.CharField(max_length=255, blank=True, null=True, unique=True)
    dedup_key = models.CharField(max_length=500, blank=True, null=True, db_index=True)
    
    # Timestamp
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        logger.warning(f"[PERSON.__INIT__] country={self.country}, website={self.website}, webform={self.webform}")

    def save(self, *args, **kwargs):
        logger.warning(f"[PERSON.SAVE] Before save: country={self.country}, website={self.website}, webform={self.webform}, type={self.type}")
        super().save(*args, **kwargs)
        logger.warning(f"[PERSON.SAVE] After save: ID={self.id}, country={self.country}, website={self.website}")

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['email']),
            models.Index(fields=['external_id']),
        ]

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.email})"

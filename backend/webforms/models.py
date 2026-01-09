from django.db import models
from persons.models import Person


class Website(models.Model):
    """Rappresenta un sito web da cui provengono webform"""
    name = models.CharField(max_length=255)
    url = models.URLField(unique=True)
    external_id = models.CharField(max_length=255, blank=True, null=True, unique=True)
    dedup_key = models.CharField(max_length=500, blank=True, null=True, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['url']),
            models.Index(fields=['external_id']),
        ]

    def __str__(self):
        return self.name


class Webform(models.Model):
    """Rappresenta un modulo webform"""
    website = models.ForeignKey(Website, on_delete=models.CASCADE, related_name="webforms")
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    external_id = models.CharField(max_length=255)
    dedup_key = models.CharField(max_length=500, blank=True, null=True, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        unique_together = ['website', 'external_id']
        indexes = [
            models.Index(fields=['website', 'external_id']),
        ]

    def __str__(self):
        return f"{self.website.name} - {self.name}"


class WebformSubmission(models.Model):
    """Rappresenta una submission di un webform"""
    webform = models.ForeignKey(
        Webform,
        on_delete=models.CASCADE,
        related_name="submissions",
        null=True,  # Temporarily nullable per migration
        blank=True
    )
    person = models.ForeignKey(
        Person,
        on_delete=models.CASCADE,
        related_name="webform_submissions"
    )
    external_id = models.CharField(max_length=255, blank=True, null=True)
    dedup_key = models.CharField(max_length=500, blank=True, null=True, db_index=True, unique=True)
    payload = models.JSONField()
    source_website = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['webform', 'external_id']),
            models.Index(fields=['person', 'created_at']),
        ]

    def __str__(self):
        webform_name = self.webform.name if self.webform else "unknown"
        return f"{webform_name} - {self.person.email} - {self.created_at.strftime('%Y-%m-%d')}"

from rest_framework import serializers
from .models import Person
import logging

logger = logging.getLogger(__name__)


class PersonSerializer(serializers.ModelSerializer):
    """Serializer per Person - allineato con payload Drupal"""
    class Meta:
        model = Person
        fields = [
            'id',
            'first_name',
            'last_name',
            'email',
            'source_website',
            'website',
            'webform',
            'country',
            'organisation',
            'domain',
            'tags',
            'roles',
            'ppg',
            'type',
            'external_id',
            'dedup_key',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def create(self, validated_data):
        logger.warning(f"[SERIALIZER.CREATE] validated_data keys: {list(validated_data.keys())}")
        logger.warning(f"[SERIALIZER.CREATE] country={validated_data.get('country')}, website={validated_data.get('website')}, tags={validated_data.get('tags')}")
        instance = super().create(validated_data)
        logger.warning(f"[SERIALIZER.CREATE] After save: country={instance.country}, website={instance.website}")
        return instance

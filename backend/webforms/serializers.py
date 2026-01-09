from rest_framework import serializers
from persons.models import Person
from .models import Webform, Website, WebformSubmission


class WebsiteSerializer(serializers.ModelSerializer):
    """Serializer per Website"""
    class Meta:
        model = Website
        fields = [
            'id',
            'name',
            'url',
            'external_id',
            'dedup_key',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class WebformSerializer(serializers.ModelSerializer):
    """Serializer per Webform"""
    website_id = serializers.IntegerField(write_only=True)
    website = WebsiteSerializer(read_only=True)

    class Meta:
        model = Webform
        fields = [
            'id',
            'website',
            'website_id',
            'name',
            'description',
            'external_id',
            'dedup_key',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class WebformSubmissionSerializer(serializers.ModelSerializer):
    """Serializer per WebformSubmission - allineato con payload Drupal"""
    person_id = serializers.IntegerField(write_only=True, required=False)
    person = serializers.SerializerMethodField(read_only=True)
    webform_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = WebformSubmission
        fields = [
            'id',
            'webform_id',
            'person_id',
            'person',
            'external_id',
            'dedup_key',
            'payload',
            'source_website',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'person', 'created_at', 'updated_at']

    def get_person(self, obj):
        return {
            'id': obj.person.id,
            'email': obj.person.email,
            'first_name': obj.person.first_name,
            'last_name': obj.person.last_name,
        }

    def create(self, validated_data):
        """Crea submission - se email nel payload, auto-crea/associa Person"""
        webform_id = validated_data.pop('webform_id')
        person_id = validated_data.pop('person_id', None)
        payload = validated_data.get('payload', {})

        # Se person_id non fornito, cerca/crea da email nel payload
        if not person_id and isinstance(payload, dict):
            email = payload.get('email') or payload.get('data', {}).get('email')
            if email:
                person, _ = Person.objects.get_or_create(
                    email=email,
                    defaults={'first_name': payload.get('first_name', '')}
                )
                person_id = person.id

        if not person_id:
            raise serializers.ValidationError("person_id o email nel payload è richiesto")

        webform = Webform.objects.get(id=webform_id)

        return WebformSubmission.objects.create(
            webform=webform,
            person_id=person_id,
            **validated_data
        )

from rest_framework import serializers
from persons.models import Person
from .models import Webform, Website, WebformSubmission


class WebsiteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Website
        fields = [
            'id', 'name', 'url', 'external_id', 'dedup_key',
            'created_at', 'updated_at',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class WebformSerializer(serializers.ModelSerializer):
    website_id = serializers.IntegerField(write_only=True)
    website = WebsiteSerializer(read_only=True)

    class Meta:
        model = Webform
        fields = [
            'id', 'website', 'website_id', 'name', 'description',
            'external_id', 'dedup_key', 'created_at', 'updated_at',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class WebformSubmissionSerializer(serializers.ModelSerializer):
    """
    Serializer per WebformSubmission
    Supporta sia person_id che auto-creazione da email nel payload
    """
    person_id = serializers.IntegerField(write_only=True, required=False)
    webform_id = serializers.IntegerField(write_only=True)
    person = serializers.SerializerMethodField(read_only=True)
    webform = WebformSerializer(read_only=True)

    class Meta:
        model = WebformSubmission
        fields = [
            'id', 'webform_id', 'person_id', 'person',
            'webform', 'external_id', 'dedup_key', 'payload',
            'source_website', 'created_at', 'updated_at',
        ]
        read_only_fields = ['id', 'person', 'webform', 'created_at', 'updated_at']

    def get_person(self, obj):
        return {
            'id': obj.person.id,
            'email': obj.person.email,
            'first_name': obj.person.first_name,
            'last_name': obj.person.last_name,
        }

    def create(self, validated_data):
        webform_id = validated_data.pop('webform_id')
        person_id = validated_data.pop('person_id', None)
        payload = validated_data.get('payload', {})

        # Se person_id non fornito, cerca/crea da email nel payload
        if not person_id and isinstance(payload, dict):
            email = payload.get('email')
            if email:
                person, _ = Person.objects.get_or_create(
                    email=email,
                    defaults={
                        'first_name': payload.get('first_name', email.split('@')[0])
                    }
                )
                person_id = person.id

        if not person_id:
            raise serializers.ValidationError(
                "person_id o email nel payload è richiesto"
            )

        webform = Webform.objects.get(id=webform_id)

        return WebformSubmission.objects.create(
            webform=webform,
            person_id=person_id,
            **validated_data
        )
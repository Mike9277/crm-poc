from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from persons.models import Person
from .models import Webform, Website, WebformSubmission
from .serializers import WebformSerializer, WebsiteSerializer, WebformSubmissionSerializer


class WebsiteViewSet(ModelViewSet):
    """
    ViewSet per Website
    Endpoint: /api/websites/
    Drupal invia: {'name': '...', 'url': '...'}
    """
    queryset = Website.objects.all()
    serializer_class = WebsiteSerializer
    filterset_fields = ['url', 'external_id']
    ordering = ['-created_at']

    def create(self, request, *args, **kwargs):
        """Gestisci 409 Conflict per dedup_key"""
        serializer = self.get_serializer(data=request.data)
        
        dedup_key = request.data.get('dedup_key')
        if dedup_key:
            existing = Website.objects.filter(dedup_key=dedup_key).first()
            if existing:
                return Response(
                    {'id': existing.id, 'name': existing.name},
                    status=status.HTTP_409_CONFLICT
                )

        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class WebformViewSet(ModelViewSet):
    """
    ViewSet per Webform
    Endpoint: /api/webforms/
    Drupal invia: {'external_id': '...', 'name': '...', 'website_id': '...', 'dedup_key': '...'}
    """
    queryset = Webform.objects.all()
    serializer_class = WebformSerializer
    filterset_fields = ['website', 'external_id']
    ordering = ['-created_at']

    def create(self, request, *args, **kwargs):
        """Gestisci 409 Conflict per dedup_key"""
        serializer = self.get_serializer(data=request.data)
        
        dedup_key = request.data.get('dedup_key')
        if dedup_key:
            existing = Webform.objects.filter(dedup_key=dedup_key).first()
            if existing:
                return Response(
                    {'id': existing.id, 'name': existing.name},
                    status=status.HTTP_409_CONFLICT
                )

        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class WebformSubmissionViewSet(ModelViewSet):
    """
    ViewSet per WebformSubmission
    Endpoint: /api/webform-submissions/ o POST /api/webforms/{webform_id}/submissions/
    """
    queryset = WebformSubmission.objects.all()
    serializer_class = WebformSubmissionSerializer
    filterset_fields = ['webform', 'person', 'external_id']
    ordering = ['-created_at']

    def create(self, request, *args, **kwargs):
        """
        POST /api/webform-submissions/
        Payload Drupal:
        {
            "webform_id": 1,
            "external_id": "...",
            "data": {...},
            "dedup_key": "website|webform|submission",
            "contact_id": 123 (opzionale)
        }
        """
        serializer = self.get_serializer(data=request.data)
        
        # Gestisci dedup_key per duplicati
        dedup_key = request.data.get('dedup_key')
        if dedup_key:
            existing = WebformSubmission.objects.filter(dedup_key=dedup_key).first()
            if existing:
                return Response(
                    {'id': existing.id},
                    status=status.HTTP_409_CONFLICT
                )

        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import action
import subprocess
import json

from persons.models import Person
from .models import Webform, Website, WebformSubmission
from .serializers import WebformSerializer, WebsiteSerializer, WebformSubmissionSerializer


class WebsiteViewSet(ModelViewSet):
    queryset = Website.objects.all()
    serializer_class = WebsiteSerializer
    filterset_fields = ['url', 'external_id']
    ordering = ['-created_at']
    
    def get_permissions(self):
        """Allow public READ, but protect WRITE operations for Drupal (Token auth)"""
        if self.request.method in ['GET', 'HEAD', 'OPTIONS']:
            return [AllowAny()]
        return [IsAuthenticated()]

    def create(self, request, *args, **kwargs):
        dedup_key = request.data.get('dedup_key')
        if dedup_key:
            existing = Website.objects.filter(dedup_key=dedup_key).first()
            if existing:
                return Response(
                    {'id': existing.id, 'name': existing.name},
                    status=status.HTTP_409_CONFLICT
                )

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class WebformViewSet(ModelViewSet):
    queryset = Webform.objects.all()
    serializer_class = WebformSerializer
    filterset_fields = ['website', 'external_id']
    ordering = ['-created_at']
    
    def get_permissions(self):
        """Allow public READ, but protect WRITE operations for Drupal (Token auth)"""
        if self.request.method in ['GET', 'HEAD', 'OPTIONS']:
            return [AllowAny()]
        return [IsAuthenticated()]

    def create(self, request, *args, **kwargs):
        dedup_key = request.data.get('dedup_key')
        if dedup_key:
            existing = Webform.objects.filter(dedup_key=dedup_key).first()
            if existing:
                return Response(
                    {'id': existing.id, 'name': existing.name},
                    status=status.HTTP_409_CONFLICT
                )

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class WebformSubmissionViewSet(ModelViewSet):
    queryset = WebformSubmission.objects.all()
    serializer_class = WebformSubmissionSerializer
    permission_classes = [AllowAny]  # Frontend pubblico può leggere submissions
    filterset_fields = ['webform', 'person', 'external_id']
    ordering = ['-created_at']

    def create(self, request, *args, **kwargs):
        """
        Gestisce POST per creare submission
        Payload atteso:
        {
            "webform_id": 1,
            "person_id": 123,
            "external_id": "sub_123",
            "payload": {...},
            "dedup_key": "..."
        }
        """
        dedup_key = request.data.get('dedup_key')
        if dedup_key:
            existing = WebformSubmission.objects.filter(dedup_key=dedup_key).first()
            if existing:
                return Response(
                    {'id': existing.id},
                    status=status.HTTP_409_CONFLICT
                )

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def sync_from_drupal(self, request):
        """
        Sincronizza manualmente le submissions da Drupal
        Bypass del cron per risolvere il bug del timestamp globale
        Endpoint PUBBLICO per il POC - in produzione aggiungere protezione
        """
        try:
            # Esegui lo script di sincronizzazione
            result = subprocess.run(
                ['python', '/app/sync_drupal.py'],
                capture_output=True,
                text=True,
                timeout=60
            )
            
            # Parse dell'output per estrarre i risultati
            output = result.stdout + result.stderr
            
            return Response({
                'status': 'success' if result.returncode == 0 else 'error',
                'returncode': result.returncode,
                'output': output,
                'message': 'Sincronizzazione da Drupal completata con successo' if result.returncode == 0 else 'Errore durante la sincronizzazione'
            }, status=status.HTTP_200_OK if result.returncode == 0 else status.HTTP_400_BAD_REQUEST)
        
        except subprocess.TimeoutExpired:
            return Response({
                'status': 'error',
                'message': 'La sincronizzazione ha superato il timeout (60 secondi)'
            }, status=status.HTTP_408_REQUEST_TIMEOUT)
        
        except Exception as e:
            return Response({
                'status': 'error',
                'message': f'Errore durante la sincronizzazione: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
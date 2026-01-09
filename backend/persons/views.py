from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
import logging

from .models import Person
from .serializers import PersonSerializer
from .services.csv_import import CSVImportService

logger = logging.getLogger(__name__)


def normalize_empty_strings(data):
    """
    Converte le stringhe vuote "" in None
    Necessario per far salvare correttamente i campi opzionali
    """
    return {
        key: (value if value != "" else None)
        for key, value in data.items()
    }


class PersonViewSet(ModelViewSet):
    queryset = Person.objects.all()
    serializer_class = PersonSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['email', 'source_website']
    ordering_fields = ['created_at', 'updated_at']

    def create(self, request, *args, **kwargs):
        logger.warning(f"[DEBUG] POST raw data: {request.data}")

        data = normalize_empty_strings(request.data)

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)

        self.perform_create(serializer)

        logger.warning(f"[DEBUG] Created Person ID={serializer.data.get('id')}")
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()

        data = normalize_empty_strings(request.data)

        serializer = self.get_serializer(
            instance,
            data=data,
            partial=partial
        )
        serializer.is_valid(raise_exception=True)

        self.perform_update(serializer)

        logger.warning(f"[DEBUG] Updated Person ID={serializer.data.get('id')}")
        return Response(serializer.data)

    @action(detail=False, methods=['post'])
    def import_preview(self, request):
        """
        POST /api/persons/import_preview/
        Preview CSV import con mapping configurato
        """
        file = request.FILES.get('file')
        mapping = request.data.get('mapping')
        skip_header = request.data.get('skip_header', True)

        if not file:
            return Response(
                {"error": "File CSV richiesto"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            file_content = file.read()
            records = CSVImportService.parse_csv(
                file_content,
                mapping=mapping,
                skip_header=skip_header
            )
            return Response({
                "count": len(records),
                "sample": records[:5],
                "records": records
            })
        except Exception as e:
            logger.exception("Errore preview CSV")
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

    @action(detail=False, methods=['post'])
    def import_execute(self, request):
        """
        POST /api/persons/import_execute/
        Esegue l'import dei records CSV
        """
        records = request.data.get('records', [])
        on_conflict = request.data.get('on_conflict', 'skip')

        if not records:
            return Response(
                {"error": "Records richiesti"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            stats = CSVImportService.import_persons(
                records,
                on_conflict=on_conflict
            )
            return Response(stats, status=status.HTTP_201_CREATED)
        except Exception as e:
            logger.exception("Errore import CSV")
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

    @action(detail=False, methods=['post'])
    def bulk_import(self, request):
        """
        POST /api/persons/bulk_import/
        Import bulk da frontend
        """
        records = request.data.get('records', [])

        if not records:
            return Response(
                {
                    "created": 0,
                    "updated": 0,
                    "skipped": 0,
                    "errors": ["Nessun record fornito"]
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            stats = CSVImportService.import_persons(
                records,
                on_conflict='skip'
            )
            return Response(stats, status=status.HTTP_201_CREATED)
        except Exception as e:
            logger.exception("Errore bulk import")
            return Response(
                {
                    "created": 0,
                    "updated": 0,
                    "skipped": 0,
                    "errors": [str(e)]
                },
                status=status.HTTP_400_BAD_REQUEST
            )

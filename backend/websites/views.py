from rest_framework.viewsets import ModelViewSet
from .models import Website
from .serializers import WebsiteSerializer


class WebsiteViewSet(ModelViewSet):
    queryset = Website.objects.all()
    serializer_class = WebsiteSerializer

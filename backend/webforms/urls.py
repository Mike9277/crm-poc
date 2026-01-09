from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import WebsiteViewSet, WebformViewSet, WebformSubmissionViewSet

# Router principale
router = DefaultRouter()
router.register(r'websites', WebsiteViewSet, basename='website')
router.register(r'webforms', WebformViewSet, basename='webform')
router.register(r'webform-submissions', WebformSubmissionViewSet, basename='webform-submission')

urlpatterns = [
    path('', include(router.urls)),
]

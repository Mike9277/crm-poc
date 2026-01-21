from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import WebsiteViewSet, WebformViewSet, WebformSubmissionViewSet

router = DefaultRouter()
router.register(r'websites', WebsiteViewSet, basename='website')
router.register(r'webforms', WebformViewSet, basename='webform')
router.register(r'webform-submissions', WebformSubmissionViewSet, basename='webform-submission')

urlpatterns = [
    path('', include(router.urls)),
    
    # Endpoint esplicito per sincronizzazione manuale
    path('webform-submissions/sync_from_drupal/', 
         WebformSubmissionViewSet.as_view({'post': 'sync_from_drupal'}),
         name='webform-sync-drupal'),
    
    # Endpoint aggiuntivo per Drupal: POST /webforms/{webform_id}/submissions/
    path('webforms/<int:webform_id>/submissions/', 
         WebformSubmissionViewSet.as_view({'post': 'create_for_webform'}),
         name='webform-create-submission'),
]
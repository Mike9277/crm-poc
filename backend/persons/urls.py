from rest_framework.routers import DefaultRouter
from .views import PersonViewSet

router = DefaultRouter()
router.register(r"persons", PersonViewSet, basename="person")
# Alias per compatibilità Drupal
router.register(r"contacts", PersonViewSet, basename="contact")

urlpatterns = router.urls

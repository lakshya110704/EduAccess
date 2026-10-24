from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import AppointmentViewSet, MeView, NotificationViewSet, ProfessorViewSet

router = DefaultRouter()
router.register(r'appointments', AppointmentViewSet, basename='appointment')
router.register(r'notifications', NotificationViewSet, basename='notification')
router.register(r'professors', ProfessorViewSet, basename='professor')

urlpatterns = [
    path('me/', MeView.as_view(), name='me'),
    path('', include(router.urls)),
]

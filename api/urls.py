from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AppointmentViewSet, NotificationViewSet, CustomUserViewSet

router = DefaultRouter()
router.register(r'appointments', AppointmentViewSet)
router.register(r'notifications', NotificationViewSet)
router.register(r'users', CustomUserViewSet, basename='customuser')

urlpatterns = [
    path('', include(router.urls)),
]

from django.urls import path
from .views import get_professors_data

urlpatterns += [
    path('professors/', get_professors_data, name='get_professors_data'),
]
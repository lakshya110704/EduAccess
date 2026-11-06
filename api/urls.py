from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    AppointmentViewSet,
    CampusBlocksView,
    MeView,
    MyCabinView,
    NotificationViewSet,
    OpenTimeViewSet,
    ProfessorViewSet,
    SignupOptionsView,
    SignupView,
)

router = DefaultRouter()
router.register(r'appointments', AppointmentViewSet, basename='appointment')
router.register(r'notifications', NotificationViewSet, basename='notification')
router.register(r'professors', ProfessorViewSet, basename='professor')
router.register(r'open-times', OpenTimeViewSet, basename='open-time')

urlpatterns = [
    path('me/', MeView.as_view(), name='me'),
    path('me/cabin/', MyCabinView.as_view(), name='my_cabin'),
    path('campus-blocks/', CampusBlocksView.as_view(), name='campus_blocks'),
    path('signup/', SignupView.as_view(), name='api_signup'),
    path('signup/options/', SignupOptionsView.as_view(), name='api_signup_options'),
    path('', include(router.urls)),
]

from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from api.views import login_view, student_dashboard

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
    path('login/', login_view, name='login'),  # ✅ Custom login route
    path('api-auth/', include('rest_framework.urls')),  # DRF login/logout

    # Frontend routes
    path('', TemplateView.as_view(template_name='index.html')),
    path('student/', student_dashboard, name='student_dashboard'),
    path('professor/', TemplateView.as_view(template_name='professor-dashboard.html')),
]
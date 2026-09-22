from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from api.views import login_view, student_dashboard

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
    path('login/', login_view, name='login'),
    path('', login_view, name='login'),  # 👈 Root route points to login
    path('api-auth/', include('rest_framework.urls')),

    # Frontend routes
    path('student/', student_dashboard, name='student_dashboard'),
    path('professor/', TemplateView.as_view(template_name='professor-dashboard.html'), name='professor_dashboard'),
]
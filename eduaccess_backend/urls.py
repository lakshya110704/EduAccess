from django.contrib import admin
from django.http import JsonResponse
from django.urls import include, path

from api.views import login_view, logout_view, professor_dashboard, signup_done, signup_view, student_dashboard


def healthz(request):
    return JsonResponse({'status': 'ok'})


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
    path('', login_view, name='home'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('signup/', signup_view, name='signup'),
    path('signup/done/', signup_done, name='signup_done'),
    path('student/', student_dashboard, name='student_dashboard'),
    path('professor/', professor_dashboard, name='professor_dashboard'),
    path('healthz/', healthz, name='healthz'),
]

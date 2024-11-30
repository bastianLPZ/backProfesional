from django.urls import path

from estadio.roles.profesor.dashboard import views

urlpatterns = [
    path('general/', views.dashboard_metrics),
    path('progreso-cupos/', views.progreso_cupos_clases),
]
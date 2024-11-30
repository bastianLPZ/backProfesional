from django.urls import path, include
from estadio.roles.administrador.reportes import views

urlpatterns = [
    path('resumen-general/', views.resumen_general),
    path('reservas-por-usuario/', views.reservas_por_usuario),
    path('uso-canchas-subcanchas/', views.uso_canchas_subcanchas),
    path('mantenimientos/', views.mantenimiento),
    path('clases/', views.clases),
]
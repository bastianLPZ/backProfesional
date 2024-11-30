from django.urls import path, include
from estadio.roles.administrador.dashboard import views

urlpatterns = [
    
    path('total-usuarios/', views.total_usuarios),
    path('total-reservas/', views.total_reservas),
    path('canchas-disponibles/', views.canchas_disponibles),
    path('reservas-canceladas/', views.reservas_canceladas),
    path('listar-canchas/', views.listar_canchas),
    path('info-cancha/', views.info_cancha),
       
]
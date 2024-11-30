from django.urls import path
from estadio.roles.administrador.reservas import views

urlpatterns = [
    
    # Canchas
    path('crear-cancha/', views.crear_cancha),
    path('listar-canchas/', views.listar_canchas),
    path('eliminar-cancha/', views.eliminar_cancha),
    path('editar-cancha/', views.editar_cancha),
    
    # Subcanchas
    path('crear-subcancha/', views.crear_subcancha),
    path('listar-subcanchas/', views.listar_subcanchas),
    path('eliminar-subcancha/', views.eliminar_subcancha),
    path('editar-subcancha/', views.editar_subcancha),
    path('canchas-disponibles/', views.canchas_disponibles),
    path('orientaciones-disponibles/', views.orientaciones_disponibles),
    
    #Horas
    path('listar-horas-ocupadas/', views.listar_horas),
    path('estado-disponible/', views.estados_disponibles),
    path('listar-canchas-disponibles/', views.listar_canchas_disponibles),
    path('editar-reserva/', views.editar_reserva),
    path('crear-reserva/', views.crear_reserva),
    path('subcanchas-disponibles/', views.subcanchas_disponibles),
    path('listar-horas-cancha/', views.listar_horas_cancha),
    
    #Equipamientos
    path('crear-equipamiento/', views.crear_equipamiento),
    path('listar-equipamientos/', views.listar_equipamiento),
    path('eliminar-equipamiento/', views.eliminar_equipamiento),
    path('editar-equipamiento/', views.editar_equipamiento),
    path('equipamiento-disponible/', views.equipamiento_disponible),


       
]
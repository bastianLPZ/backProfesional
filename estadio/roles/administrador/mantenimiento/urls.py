from django.urls import path, include
from estadio.roles.administrador.mantenimiento import views

urlpatterns = [
    path('listar-mantenimientos/', views.listar_mantenimientos),
    path('crear-mantenimiento/', views.crear_mantenimiento),
    path('editar-mantenimiento/', views.editar_mantenimiento),
    path('eliminar-mantenimiento/', views.eliminar_mantenimiento),
]
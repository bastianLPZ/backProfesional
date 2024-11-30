from django.urls import path
from estadio.roles.administrador.clases import views

urlpatterns = [
    path('listar-clases/', views.listar_clases),
    path('crear-clase/', views.crear_clases),
    path('editar-clase/', views.modificar_clase),
    path('eliminar-clase/', views.eliminar_clase),
    
    path('profesores-disponibles/', views.profesores_disponibles),
    path('alumnos/', views.alumnos_con_estado),
    path('añadir-alumnos/', views.añadir_alumnos),
]
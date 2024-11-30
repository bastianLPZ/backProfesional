from django.urls import path
from estadio.roles.administrador.usuarios import views

urlpatterns = [
    
    # Administradores
    path('listar-administradores/', views.listar_administradores),
    path('crear-administrador/', views.crear_administrador),
    path('editar-administrador/', views.editar_administrador),
    path('eliminar-administrador/', views.eliminar_administrador),
    
    # Profesores
    path('listar-profesores/', views.listar_profesores),
    path('crear-profesor/', views.crear_profesor),
    path('editar-profesor/', views.editar_profesor),
    path('eliminar-profesor/', views.eliminar_profesor),
    
    # Usuarios
    path('listar-usuarios/', views.listar_usuarios),
    path('crear-usuario/', views.crear_usuario),
    path('editar-usuario/', views.editar_usuario),
    path('eliminar-usuario/', views.eliminar_usuario),
    
    # Personal
    path('listar-personal/', views.listar_personal),
    path('crear-personal/', views.crear_personal),
    path('editar-personal/', views.editar_personal),
    path('eliminar-personal/', views.eliminar_personal),
    
    
    
    
]
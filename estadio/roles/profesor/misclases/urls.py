from django.urls import path

from estadio.roles.profesor.misclases import views

urlpatterns = [
    path('listar-clases/', views.list_class),
    path('crear-clase/', views.crear_class),
    path('editar-clase/', views.editar_clase),
    path('eliminar-clase/', views.eliminar_clase),
]
from django.urls import path
from estadio.roles.personal import views

urlpatterns = [
    path('listar-clases-disponibles/', views.listar_clases_disponibles ),
    path('unirse-clase/', views.unirse_clase ),
    path('salir-clase/', views.salir_clase ),
]
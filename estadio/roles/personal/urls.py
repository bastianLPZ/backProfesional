from django.urls import path
from estadio.roles.personal import views

urlpatterns = [
    path('listar-clases-disponibles/', views.listar_clases_disponibles ),
]
from django.urls import path, include
from estadio.roles.profesor import views
from estadio.roles.profesor.dashboard import urls as dashboard_urls  # Importa correctamente las urls de dashboard
from estadio.roles.profesor.misclases import urls as misclases_urls  # Importa correctamente las urls de misclases

urlpatterns = [
    path('dashboard/', include(dashboard_urls)),  # Incluye las urls del dashboard aquí
    path('mis-clases/', include(misclases_urls)),  # Incluye las urls de misclases aquí
    
]
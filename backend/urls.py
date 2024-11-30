from django.contrib import admin
from django.urls import path, include

from estadio import urls as general_urls

from estadio.roles.administrador import urls as administrador_urls
from estadio.roles.personal import urls as personal_urls
from estadio.roles.profesor import urls as profesor_urls

urlpatterns = [
    path('admin/', admin.site.urls),
    
    path('general/', include(general_urls)),
    
    path('administrador/', include(administrador_urls)),
    path('personal/', include(personal_urls)),
    path('profesor/', include(profesor_urls)),
    
]

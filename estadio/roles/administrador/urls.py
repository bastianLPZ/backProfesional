#  Ejemplo base urls

# urlpatterns = [
#     # path('obt-user/', views.obt_user),
#     path('login/', views.login_user),
#     path('get-csrf-token/', views.get_csrf_token),
#     path('logout/', views.logout)
# ]


#Url administrador/
from django.urls import path, include
from estadio.roles.administrador import views
from estadio.roles.administrador.dashboard import urls as dashboard_urls
from estadio.roles.administrador.reservas import urls as reservas_urls
from estadio.roles.administrador.usuarios import urls as usuarios_urls
from estadio.roles.administrador.clases import urls as clases_urls
from estadio.roles.administrador.mantenimiento import urls as mantenimiento_urls
from estadio.roles.administrador.reportes import urls as reportes_urls

urlpatterns = [
    
    path('dashboard/', include(dashboard_urls)),
    path('reservas/', include(reservas_urls)),
    path('usuarios/', include(usuarios_urls)),
    path('clases/', include(clases_urls)),
    path('mantenimiento/', include(mantenimiento_urls)),
    path('reportes/', include(reportes_urls)),
    
       
]
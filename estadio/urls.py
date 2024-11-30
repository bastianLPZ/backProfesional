#  Ejemplo base urls
# from django.urls import path
# from aplicacion import views

# urlpatterns = [
#     # path('obt-user/', views.obt_user),
#     path('login/', views.login_user),
#     path('get-csrf-token/', views.get_csrf_token),
#     path('logout/', views.logout)
# ]


#Url general/ sistema. logout, login, etc.

from django.urls import path
from estadio import views

urlpatterns = [
    path('login/', views.login),
    path('logout/', views.logout_sesion),
]
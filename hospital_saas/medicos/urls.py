from django.urls import path
from . import views

urlpatterns = [
    path('registro/', views.registrar_medico, name='registro_medico'),
    path('login/', views.login_medico, name='login_medico'),
    path('logout/', views.logout_medico, name='logout_medico'),
]
"""
URL configuration for proyecto_gaes5 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from  . import views
from sesiones import views
#from sesiones.forms import RegistrationForm
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    #admin:index
    #path('admin:index/', admin.site.urls),
    path('', views.inicio, name='inicio'),
    path('Error404', views.Error404, name='Error404'),
    path('Error', views.Error, name='Error'),
    path('contactosInicio', views.contactosInicio, name='contactosInicio'),
    path('login', views.user_login, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('registro/', views.registro, name='registro'),
    path('agendar/', views.agendar, name='agendar'),
    path('index/', views.index, name='index'),
    path('Menu/', views.Menu, name='Menu'),
    path('agendar/', views.agendar, name='agendar'),
    path('ver_inventario/', views.ver_inventario, name='ver_inventario'),
    path('ver_servicios/', views.ver_servicios, name='ver_servicios'),
    path('asignarR/', views.asignarR, name='asignarR'),
    path('contactos/', views.contactos, name='contactos'),
    path('crear_cita/', views.crear_cita, name='crear_cita'),
    path('reagendar/<int:cita_id>/', views.reagendar_cita, name='reagendar_cita'),
    path('eliminar_cita/<int:cita_id>/', views.eliminar_cita, name='eliminar_cita'),
    # path('confirmar_eliminar_cita/', views.confirmar_eliminar_cita, name='confirmar_eliminar_cita'),
    
    #url reenvio de contraseña 
    path('reset_password/', auth_views.PasswordResetView.as_view(template_name="password-reset.html"), name='password_reset'),
    path('reset_password_send/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="password-confirm.html"), name='password_reset_confirm'),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name="password-reset-complete.html"), name='password_reset_complete' ),

]   + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


# urlpatterns = [
#     # Tus otras URLs aquí
# ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
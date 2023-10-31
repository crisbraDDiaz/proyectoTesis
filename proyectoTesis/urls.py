"""
URL configuration for proyectoTesis project.

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
from . import views
from .views import *

def admin_redirect(request):
    return redirect(reverse_lazy('admin:index'))

urlpatterns = [
    path("admin/", admin.site.urls),
    path("",views.inicio,name="inicio"),
    path('login/', custom_login, name='login'),
    path('registro/', register_user, name='registro_usuario'),
    path('logout/', custom_logout, name='logout'),
    path("register_user/",views.register_user,name="register_user"),
    path('custom_login/', views.custom_login, name='custom_login'),
    path('datos_ubicacion_formulario/',views.datos_ubicacion_formulario,name='datos_ubicacion_formulario' ),
    path('guardar_ubicacion/',views.guardar_ubicacion,name='guardar_ubicacion'),
    path('datos_ubicacion_formulario/',views.datos_ubicacion_formulario,name='datos_ubicacion_formulario' ),
    path('completar_perfil/',views.completar_perfil,name='completar_perfil' ),
    path('datos_usuario/',views.datos_usuario,name='datos_usuario' ),
    path('olvide_contrasena/', views.olvide_contrasena, name='olvide_contrasena'),
    path('reset_password/', views.reset_password, name='reset_password' ),
    path('reset_password/confirm/<str:uidb64>/<str:token>/', views.reset_password_confirm, name='reset_password_confirm'),
    path('reset_password_complete/', views.reset_password_complete, name='reset_password_complete'),
    path('reset_password_done/', views.reset_password_done, name='reset_password_done'),
    path('mostrar_ubicacion/',views.mostrar_ubicacion,name='mostrar_ubicacion'),
    path('solicitud_recoleccion/',views.solicitud_recoleccion,name='solicitud_recoleccion'),
    path('admin_redirect/', views.admin_redirect, name='admin_redirect'),
    path('quines_somos/',views.quienesSomos,name='quienes somos'),
    path('mostrar_materiales_fotos/', views.mostrar_materiales_fotos, name='mostrar_materiales_fotos'),
    path('obtener_foto_material/<str:nombre>/', views.obtener_foto_material, name='obtener_foto_material'),
    path('guardar_foto/',views.guardar_foto,name='guardar_foto'),
    path('buscar_material/',views.buscar_material,name='buscar_material'),
    path("confirmar_solicitud/",views.confirmar_solicitud,name="confirmar_solicitud"),
    path("finalizar_solicitud/",views.finalizar_solicitud,name="finalizar_solicitud"),
    path("perfil_usuario/",views.perfil_usuario,name="perfil_usuario"),
    path("actualizar_datos/",views.actualizar_datos,name="actualizar_datos"),
    path("donar_puntos/",views.donar_puntos,name="donar_puntos"),
    path("comentarios/",views.comentarios,name="comentarios"),
    path("guardar_comentario/",views.guardar_comentario,name="guardar_comentario"),
    path("verificar_solicitudes/",views.verificar_solicitudes,name="verificar_solicitudes"),
]

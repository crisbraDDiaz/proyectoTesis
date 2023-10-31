from django.contrib import admin
from .models import  MaterialReciclable,Bloqueados, QuejasSugerencias,SolicitudRecoleccion, PuntosRecompensa, UbicacionReciclaje, DonacionMaterialReciclable
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from urllib.parse import urlencode
from django.shortcuts import redirect
from django.urls import reverse
from django.contrib import messages

import json

class MaterialReciclable_Resource(resources.ModelResource):
    class Meta:
        model = MaterialReciclable

class SolicitudRecoleccion_Resource(resources.ModelResource):
    class Meta:
        model = SolicitudRecoleccion

class PuntosRecompensa_Resource(resources.ModelResource):
    class Meta:
        model = PuntosRecompensa

class UbicacionReciclaje_Resource(resources.ModelResource):
    class Meta:
        model = UbicacionReciclaje

class DonacionMaterialReciclable_Resource(resources.ModelResource):
    class Meta:
        model = DonacionMaterialReciclable



class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'email', 'direccion_domicilio', 'latitud', 'longitud')
    search_fields = ('username', 'email')

class MaterialReciclableAdmin(ImportExportModelAdmin):
    list_display = ('id', 'nombre', 'precio_por_kilo')
    search_fields = ('id', 'nombre')
    exclude = ('foto',)
    resource_class = MaterialReciclable_Resource
    def ver_estudiantes_con_fotos(self, request, queryset):
        if request.user.is_superuser:
            # Seleccionar solo los campos en list_display
            selected_fields = ["id", "nombre", "precio_por_kilo"]
            selected_data = queryset.values(*selected_fields)

            # Serializa los datos a JSON
            data = json.dumps(list(selected_data))

            # Codifica los datos como parámetros de consulta en la URL
            params = urlencode({'data': data})
            url = reverse('mostrar_materiales_fotos') + '?' + params

            # Redirige a la página que muestra los estudiantes con sus fotos
            return redirect(url)
        else:
            messages.error(request, "No tienes permiso para realizar esta acción.")
            return None

    ver_estudiantes_con_fotos.short_description = "Ver los materiales"
    actions = [ver_estudiantes_con_fotos]

class SolicitudRecoleccionAdmin(ImportExportModelAdmin):
    list_display = ('id', 'usuario', 'material','estado', 'peso_kilos','fecha_solicitud_aceptada','fecha_solicitud', 'fecha_recoleccion','reciclador')
    search_fields = ('usuario__username', 'material__nombre')
    resource_class = SolicitudRecoleccion_Resource

class PuntosRecompensaAdmin(ImportExportModelAdmin):
    list_display = ('id', 'usuario', 'cantidad_puntos', 'fecha_creacion')
    search_fields = ('usuario__username',)
    resource_class = PuntosRecompensa_Resource

class UbicacionReciclajeAdmin(ImportExportModelAdmin):
    list_display = ('id', 'nombre', 'direccion', 'latitud', 'longitud')
    resource_class = UbicacionReciclaje_Resource

class DonacionMaterialReciclableAdmin(ImportExportModelAdmin):
    list_display = ('id', 'usuario', 'puntos', 'fecha_donacion')
    search_fields = ('usuario__username', 'material__nombre')
    resource_class = DonacionMaterialReciclable_Resource


class Comentarios(ImportExportModelAdmin):
    list_display = ('usuario', 'comentario', 'fecha')

class reciclador_bloqueados(ImportExportModelAdmin):
    list_display = ('correos_baneados', 'fecha')
    
    

admin.site.register(MaterialReciclable, MaterialReciclableAdmin)
admin.site.register(SolicitudRecoleccion, SolicitudRecoleccionAdmin)
admin.site.register(PuntosRecompensa, PuntosRecompensaAdmin)
admin.site.register(UbicacionReciclaje, UbicacionReciclajeAdmin)
admin.site.register(DonacionMaterialReciclable, DonacionMaterialReciclableAdmin)
admin.site.register(QuejasSugerencias, Comentarios)
admin.site.register(Bloqueados, reciclador_bloqueados)
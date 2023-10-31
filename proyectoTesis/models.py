from django.db import models
from django.contrib.auth.models import User

class UbicacionUsuario(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE) 
    direccion_domicilio = models.CharField(max_length=255, blank=True, null=True)
    latitud = models.DecimalField(max_digits=10, decimal_places=6, blank=True, null=True)
    longitud = models.DecimalField(max_digits=10, decimal_places=6, blank=True, null=True)

    def __str__(self):
        return self.usuario.username

class MaterialReciclable(models.Model):
    nombre = models.CharField(max_length=255)
    precio_por_kilo = models.CharField(max_length=255,blank=True, null=True)
    foto = models.TextField(blank=True, null=True)
    descripcion = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nombre

class SolicitudRecoleccion(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)  # Utilizando el modelo de usuario de Django
    material = models.ForeignKey(MaterialReciclable, on_delete=models.CASCADE)
    peso_kilos = models.CharField(max_length=255,null=True, blank=True)
    fecha_solicitud = models.DateField()
    fecha_solicitud_aceptada = models.DateField(null=True, blank=True)
    fecha_recoleccion = models.DateField(null=True, blank=True)
    estado = models.CharField(max_length=255,null=True, blank=True)
    reciclador = models.CharField(max_length=255,null=True, blank=True)


class PuntosRecompensa(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)  
    cantidad_puntos = models.IntegerField()
    fecha_creacion = models.DateField()

class UbicacionReciclaje(models.Model):
    nombre = models.CharField(max_length=255)
    direccion = models.CharField(max_length=255)
    latitud = models.CharField(max_length=255)
    longitud = models.CharField(max_length=255)

class DonacionMaterialReciclable(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)  
    puntos = models.CharField(max_length=255,null=True, blank=True)
    fecha_donacion = models.DateField()

class QuejasSugerencias(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)  
    comentario = models.TextField(blank=True, null=True)
    fecha = models.DateField(null=True, blank=True)

class Bloqueados(models.Model):
    correos_baneados = models.CharField(max_length=255,blank=True, null=True)
    fecha = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.correos_baneados
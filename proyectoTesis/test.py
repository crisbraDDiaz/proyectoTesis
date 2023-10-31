from django.test import TestCase
from .models import MaterialReciclable, UbicacionUsuario, SolicitudRecoleccion, PuntosRecompensa, UbicacionReciclaje, DonacionMaterialReciclable
from django.contrib.auth.models import User
import datetime

class MaterialReciclableTestCase(TestCase):
    def test_creacion_material_reciclable(self):
        material = MaterialReciclable.objects.create(nombre='Plástico', precio_por_kilo='2.5', descripcion='Material plástico reciclable')
        self.assertEqual(material.nombre, 'Plástico')

    def test_actualizacion_material_reciclable(self):
        material = MaterialReciclable.objects.create(nombre='Plástico', precio_por_kilo='2.5', descripcion='Material plástico reciclable')
        material.nombre = 'Nuevo Plástico'
        material.precio_por_kilo = '3.0'
        material.descripcion = 'Nuevo material plástico'
        material.save()
        self.assertEqual(material.nombre, 'Nuevo Plástico')

    def test_mostrar_material_reciclable(self):
        material = MaterialReciclable.objects.create(nombre='Plástico', precio_por_kilo='2.5', descripcion='Material plástico reciclable')
        material_recuperado = MaterialReciclable.objects.get(id=material.id)
        self.assertEqual(material_recuperado.nombre, 'Plástico')

    def test_eliminar_material_reciclable(self):
        material = MaterialReciclable.objects.create(nombre='Plástico', precio_por_kilo='2.5', descripcion='Material plástico reciclable')
        material_id = material.id
        material.delete()
        with self.assertRaises(MaterialReciclable.DoesNotExist):
            MaterialReciclable.objects.get(id=material_id)

class UbicacionUsuarioTestCase(TestCase):
    def test_creacion_ubicacion_usuario(self):
        user = User.objects.create_user(username='testuser', email='test@example.com', password='testpassword')
        ubicacion = UbicacionUsuario.objects.create(usuario=user, direccion_domicilio='123 Calle Principal', latitud='40.7128', longitud='-74.0060')
        self.assertEqual(ubicacion.direccion_domicilio, '123 Calle Principal')

    def test_actualizacion_ubicacion_usuario(self):
        user = User.objects.create_user(username='testuser', email='test@example.com', password='testpassword')
        ubicacion = UbicacionUsuario.objects.create(usuario=user, direccion_domicilio='123 Calle Principal', latitud='40.7128', longitud='-74.0060')
        ubicacion.direccion_domicilio = '456 Nueva Calle'
        ubicacion.latitud = '45.6789'
        ubicacion.longitud = '-80.1234'
        ubicacion.save()
        self.assertEqual(ubicacion.direccion_domicilio, '456 Nueva Calle')

    def test_mostrar_ubicacion_usuario(self):
        user = User.objects.create_user(username='testuser', email='test@example.com', password='testpassword')
        ubicacion = UbicacionUsuario.objects.create(usuario=user, direccion_domicilio='123 Calle Principal', latitud='40.7128', longitud='-74.0060')
        ubicacion_recuperada = UbicacionUsuario.objects.get(id=ubicacion.id)
        self.assertEqual(ubicacion_recuperada.direccion_domicilio, '123 Calle Principal')

    def test_eliminar_ubicacion_usuario(self):
        user = User.objects.create_user(username='testuser', email='test@example.com', password='testpassword')
        ubicacion = UbicacionUsuario.objects.create(usuario=user, direccion_domicilio='123 Calle Principal', latitud='40.7128', longitud='-74.0060')
        ubicacion_id = ubicacion.id
        ubicacion.delete()
        with self.assertRaises(UbicacionUsuario.DoesNotExist):
            UbicacionUsuario.objects.get(id=ubicacion_id)

class SolicitudRecoleccionTestCase(TestCase):
    def test_creacion_solicitud_recoleccion(self):
        user = User.objects.create_user(username='testuser', email='test@example.com', password='testpassword')
        material = MaterialReciclable.objects.create(nombre='Plástico', precio_por_kilo='2.5', descripcion='Material plástico reciclable')
        solicitud = SolicitudRecoleccion.objects.create(usuario=user, material=material, peso_kilos='5', estado='Pendiente',fecha_solicitud=datetime.date.today())
        self.assertEqual(solicitud.peso_kilos, '5')

    def test_actualizacion_solicitud_recoleccion(self):
        user = User.objects.create_user(username='testuser', email='test@example.com', password='testpassword')
        material = MaterialReciclable.objects.create(nombre='Plástico', precio_por_kilo='2.5', descripcion='Material plástico reciclable')
        solicitud = SolicitudRecoleccion.objects.create(usuario=user, material=material, peso_kilos='5', estado='Pendiente',fecha_solicitud=datetime.date.today())
        solicitud.peso_kilos = '10'
        solicitud.save()
        self.assertEqual(solicitud.peso_kilos, '10')

    def test_mostrar_solicitud_recoleccion(self):
        user = User.objects.create_user(username='testuser', email='test@example.com', password='testpassword')
        material = MaterialReciclable.objects.create(nombre='Plástico', precio_por_kilo='2.5', descripcion='Material plástico reciclable')
        solicitud = SolicitudRecoleccion.objects.create(usuario=user, material=material, peso_kilos='5', estado='Pendiente',fecha_solicitud=datetime.date.today())
        solicitud_recuperada = SolicitudRecoleccion.objects.get(id=solicitud.id)
        self.assertEqual(solicitud_recuperada.peso_kilos, '5')

    def test_eliminar_solicitud_recoleccion(self):
        user = User.objects.create_user(username='testuser', email='test@example.com', password='testpassword')
        material = MaterialReciclable.objects.create(nombre='Plástico', precio_por_kilo='2.5', descripcion='Material plástico reciclable')
        solicitud = SolicitudRecoleccion.objects.create(usuario=user, material=material, peso_kilos='5', estado='Pendiente',fecha_solicitud=datetime.date.today())
        solicitud_id = solicitud.id
        solicitud.delete()
        with self.assertRaises(SolicitudRecoleccion.DoesNotExist):
            SolicitudRecoleccion.objects.get(id=solicitud_id)

class PuntosRecompensaTestCase(TestCase):
    def test_creacion_puntos_recompensa(self):
        user = User.objects.create_user(username='testuser', email='test@example.com', password='testpassword')
        puntos = PuntosRecompensa.objects.create(usuario=user, cantidad_puntos=100, fecha_creacion=datetime.date.today())
        self.assertEqual(puntos.cantidad_puntos, 100)

    def test_actualizacion_puntos_recompensa(self):
        user = User.objects.create_user(username='testuser', email='test@example.com', password='testpassword')
        puntos = PuntosRecompensa.objects.create(usuario=user, cantidad_puntos=100, fecha_creacion=datetime.date.today())
        puntos.cantidad_puntos = 200
        puntos.save()
        self.assertEqual(puntos.cantidad_puntos, 200)

    def test_mostrar_puntos_recompensa(self):
        user = User.objects.create_user(username='testuser', email='test@example.com', password='testpassword')
        puntos = PuntosRecompensa.objects.create(usuario=user, cantidad_puntos=100, fecha_creacion=datetime.date.today())
        puntos_recuperados = PuntosRecompensa.objects.get(id=puntos.id)
        self.assertEqual(puntos_recuperados.cantidad_puntos, 100)

    def test_eliminar_puntos_recompensa(self):
        user = User.objects.create_user(username='testuser', email='test@example.com', password='testpassword')
        puntos = PuntosRecompensa.objects.create(usuario=user, cantidad_puntos=100, fecha_creacion=datetime.date.today())
        puntos_id = puntos.id
        puntos.delete()
        with self.assertRaises(PuntosRecompensa.DoesNotExist):
            PuntosRecompensa.objects.get(id=puntos_id)

class UbicacionReciclajeTestCase(TestCase):
    def test_creacion_ubicacion_reciclaje(self):
        ubicacion_reciclaje = UbicacionReciclaje.objects.create(nombre='Centro de Reciclaje', direccion='456 Calle Secundaria', latitud='40.7128', longitud='-74.0060')
        self.assertEqual(ubicacion_reciclaje.nombre, 'Centro de Reciclaje')

    def test_actualizacion_ubicacion_reciclaje(self):
        ubicacion_reciclaje = UbicacionReciclaje.objects.create(nombre='Centro de Reciclaje', direccion='456 Calle Secundaria', latitud='40.7128', longitud='-74.0060')
        ubicacion_reciclaje.nombre = 'Nuevo Centro de Reciclaje'
        ubicacion_reciclaje.direccion = '789 Nueva Calle'
        ubicacion_reciclaje.latitud = '45.6789'
        ubicacion_reciclaje.longitud = '-80.1234'
        ubicacion_reciclaje.save()
        self.assertEqual(ubicacion_reciclaje.nombre, 'Nuevo Centro de Reciclaje')

    def test_mostrar_ubicacion_reciclaje(self):
        ubicacion_reciclaje = UbicacionReciclaje.objects.create(nombre='Centro de Reciclaje', direccion='456 Calle Secundaria', latitud='40.7128', longitud='-74.0060')
        ubicacion_reciclaje_recuperada = UbicacionReciclaje.objects.get(id=ubicacion_reciclaje.id)
        self.assertEqual(ubicacion_reciclaje_recuperada.nombre, 'Centro de Reciclaje')

    def test_eliminar_ubicacion_reciclaje(self):
        ubicacion_reciclaje = UbicacionReciclaje.objects.create(nombre='Centro de Reciclaje', direccion='456 Calle Secundaria', latitud='40.7128', longitud='-74.0060')
        ubicacion_reciclaje_id = ubicacion_reciclaje.id
        ubicacion_reciclaje.delete()
        with self.assertRaises(UbicacionReciclaje.DoesNotExist):
            UbicacionReciclaje.objects.get(id=ubicacion_reciclaje_id)

class DonacionMaterialReciclableTestCase(TestCase):
    def test_creacion_donacion_material_reciclable(self):
        user = User.objects.create_user(username='testuser', email='test@example.com', password='testpassword')
        donacion = DonacionMaterialReciclable.objects.create(usuario=user,  puntos='10', fecha_donacion=datetime.date.today())
        self.assertEqual(donacion.puntos, '10')

    def test_actualizacion_donacion_material_reciclable(self):
        user = User.objects.create_user(username='testuser', email='test@example.com', password='testpassword')
        donacion = DonacionMaterialReciclable.objects.create(usuario=user, puntos='10', fecha_donacion=datetime.date.today())
        donacion.puntos = '20'
        donacion.save()
        self.assertEqual(donacion.puntos, '20')

    def test_mostrar_donacion_material_reciclable(self):
        user = User.objects.create_user(username='testuser', email='test@example.com', password='testpassword')
        donacion = DonacionMaterialReciclable.objects.create(usuario=user,  puntos='10', fecha_donacion=datetime.date.today())
        donacion_recuperada = DonacionMaterialReciclable.objects.get(id=donacion.id)
        self.assertEqual(donacion_recuperada.puntos, '10')

    def test_eliminar_donacion_material_reciclable(self):
        user = User.objects.create_user(username='testuser', email='test@example.com', password='testpassword')
        donacion = DonacionMaterialReciclable.objects.create(usuario=user,  puntos='10', fecha_donacion=datetime.date.today())
        donacion_id = donacion.id
        donacion.delete()
        with self.assertRaises(DonacionMaterialReciclable.DoesNotExist):
            DonacionMaterialReciclable.objects.get(id=donacion_id)

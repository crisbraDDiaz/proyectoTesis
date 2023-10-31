import base64
import datetime
import timedelta
import io
import json
import re
from django.conf import settings

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.views import LoginView, LogoutView
from django.core.mail import EmailMessage, send_mail

from django.http import HttpResponse, JsonResponse, response
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from PIL import Image
from django_cron import CronJobBase, Schedule
from smtplib import SMTPException
from datetime import datetime, timedelta,date



from proyectoTesis.models import (
    MaterialReciclable,
    SolicitudRecoleccion,
    UbicacionReciclaje,
    UbicacionUsuario,
    PuntosRecompensa,
    DonacionMaterialReciclable,
    QuejasSugerencias,
    Bloqueados
)

from .forms import *

from django.core.mail import send_mail
from django.conf import settings


def enviar_correo(subject,message,from_email,recipient_list):
    send_mail(subject, message, from_email, recipient_list, fail_silently=False)

def verificar_solicitudes(request):
    print("Verificando solicitudes")
    dia_atras = datetime.now() - timedelta(days=1)
    dos_dia_atras = datetime.now() - timedelta(days=2)
    print(dia_atras)
    try:
        solicitudes = SolicitudRecoleccion.objects.filter(
            estado='En Proceso', fecha_solicitud_aceptada__lte=dia_atras
        )
        solicitudes_dos_dias = SolicitudRecoleccion.objects.filter(
            estado='En Proceso', fecha_solicitud_aceptada__lte=dos_dia_atras
        )

        for solicitud in solicitudes:
            # Enviar correo al reciclador
            subject = 'Recordatorio de Solicitud Pendiente'
            message = 'Recuerda completar la solicitud de recolección, si dejas pasar un dia mas, tu cuenta sera eliminada.'
            from_email = settings.EMAIL_HOST_USER  # Remitente del correo
            recipient_list = [solicitud.reciclador.email]
            
            enviar_correo(subject, message, from_email, recipient_list)
            print("solicitudes Verificadas")
            # Actualizar solicitud y eliminar reciclador si han pasado dos días
            solicitud.estado = 'Pendiente'
            solicitud.reciclador = None
            solicitud.save()
            return render(
                request,
                "confirmacion/confirmacion.html",
                {"mensaje": "Solicitudes actualizadas."},
            )

        for solicitud in solicitudes_dos_dias:
            # Enviar correo al reciclador
            subject = 'Eliinación  de tu cuenta'
            message = 'Hola, debido que no has completado tu solicitud pendiente, tuvimos que eliminar tu cuenta al no cumplir con las politicas de nuestra aplicación.'
            from_email = settings.EMAIL_HOST_USER  # Remitente del correo
            recipient_list = [solicitud.reciclador.email]
            bloqueado = Bloqueados.objects.create(
                correos_baneados = solicitud.reciclador.email,
                fecha = date.today()
            )
            bloqueado.save()
            
            enviar_correo(subject, message, from_email, recipient_list)
            reciclador = User.objects.get(email=solicitud.reciclador.email)
            reciclador.delete()
            print("solicitudes Verificadas")
            # Actualizar solicitud y eliminar reciclador si han pasado dos días
            solicitud.estado = 'Pendiente'
            solicitud.reciclador = None
            solicitud.save()
            return render(
                request,
                "confirmacion/confirmacion.html",
                {"mensaje": "Solicitudes actualizadas."},
            )
        


    except SMTPException as e:
        print(f"Error al enviar el correo: {e}")
        return render(
                request,
                "confirmacion/confirmacion.html",
                {"mensaje": "Se genero un error por favor vuelve a intentar"},
            )
    except Exception as e:
        print(f"Error inesperado: {e}")
        return render(
                request,
                "confirmacion/confirmacion.html",
                {"mensaje": "Se genero un error por favor vuelve a intentar"},
            )
    return render(
                request,
                "confirmacion/confirmacion.html",
                {"mensaje": "Solicitudes actualizadas."},
            )




def custom_login(request):
    if request.method == "POST":
        form = CustomLoginForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            remember_me = form.cleaned_data.get("remember_me")
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                # La autenticación fue exitosa, puedes redirigir a donde desees
                return redirect("inicio")  # Cambia 'inicio' por la URL de tu elección
    else:
        form = CustomLoginForm()

    return render(request, "login.html", {"form": form})


def register_user(request):
    if request.method == "POST":
        form = CustomRegistrationForm(request.POST)
        if form.is_valid():
            print("usuario valido")
            user = form.save()
            es_reciclador = request.POST.get("is_staff")
            if es_reciclador:
                # Agrega al usuario al grupo "Recicladores"
                grupo_recicladores, created = Group.objects.get_or_create(
                    name="reciclador"
                )
                user.groups.add(grupo_recicladores)

            login(request, user)  # Inicia sesión automáticamente después del registro
            return redirect("datos_ubicacion_formulario")
    else:
        print("usuario no valido")
        form = CustomRegistrationForm()

    return render(request, "registro.html", {"form": form})


def guardar_ubicacion(request):
    if request.method == "POST":
        form = UbicacionUsuarioForm(request.POST)
        if form.is_valid():
            ubicacion = form.save(commit=False)
            ubicacion.usuario = request.user
            ubicacion.save()
            return redirect("datos_usuario")
    else:
        form = UbicacionUsuarioForm()
    return render(request, "datos_ubicacion_formulario.html", {"form": form})



def custom_logout(request):
    logout(request)
    return redirect("inicio")


# Vista de inicio simple (requiere inicio de sesión)
@login_required
def inicio(request):
    material = MaterialReciclable.objects.all()
    depositos = UbicacionReciclaje.objects.all()
    materiales = MaterialReciclable.objects.all()
    usuario_es_reciclador = (
        request.user.groups.filter(name="reciclador").exists()
        or request.user.is_superuser
    )
    solicitud = SolicitudRecoleccion.objects.all()
    return render(
        request,
        "home.html",
        {
            "usuario_es_reciclador": usuario_es_reciclador,
            "materiales": material,
            "solicitudes": solicitud,
            "depositos": depositos,
            "materiales": materiales,
        },
    )


def datos_ubicacion_formulario(request):
    return render(request, "datos_usuario/datos_ubicacion_formulario.html")


def datos_usuario(request):
    return render(request, "datos_usuario/datos_usuario.html")


def completar_perfil(request):
    if request.method == "POST":
        form = UserProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            # Redirige a la página de perfil o a donde desees después de completar el formulario
            return redirect("inicio")
    else:
        form = UserProfileForm(instance=request.user)

    return render(request, "completar_perfil.html", {"form": form})


def olvide_contrasena(request):
    # Tu lógica de vista aquí
    return render(request, "reset_password.html")


def reset_password(request):
    if request.method == "POST":
        # Obtén el correo electrónico ingresado por el usuario en el formulario
        correo = request.POST.get("correo")

        # Busca un usuario con el correo electrónico proporcionado
        try:
            user = User.objects.get(email=correo)

        except User.DoesNotExist:
            user = None

        if user:
            # Genera un token único para el usuario
            token = default_token_generator.make_token(user)

            # Codifica el ID del usuario en base64 para incluirlo en el enlace
            uidb64 = urlsafe_base64_encode(force_bytes(user.pk))

            # Construye la URL de restablecimiento de contraseña con el token y el ID del usuario
            reset_url = f"{request.scheme}://{request.get_host()}/reset_password/confirm/{uidb64}/{token}/"

            # Construye el mensaje de correo electrónico
            subject = "Restablecimiento de contraseña"
            message = f"Haga clic en el siguiente enlace para restablecer su contraseña:\n\n{reset_url}"
            from_email = "brandon-diaz@upc.edu.co"  # Cambia esto a tu dirección de correo electrónico
            recipient_list = [correo]

            # Envía el correo electrónico
            send_mail(subject, message, from_email, recipient_list)

            # Redirige al usuario a la página de confirmación
            return render(
                request,
                "reset_password.html",
                {
                    "mensaje": "Se ha enviado un correo electrónico con instrucciones para restablecer su contraseña."
                },
            )

    # Renderiza el formulario de solicitud de restablecimiento de contraseña
    return render(request, "reset_password.html")


def reset_password_done(request):
    return render(request, "password_reset_confirmation.html")


def reset_password_confirm(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = get_user_model().objects.get(pk=uid)
        if default_token_generator.check_token(user, token):
            if request.method == "POST":
                new_password = request.POST.get("password")
                user.set_password(new_password)  # Establece la nueva contraseña
                user.save()  # Guarda el usuario actualizado en la base de datos

                messages.success(
                    request,
                    "Contraseña restablecida con éxito. Inicia sesión con tu nueva contraseña.",
                )
                return redirect("admin_redirect")  # Redirige al inicio de sesión
            else:
                return render(request, "reset_password_confirm.html")
        else:
            return render(request, "token_invalid.html")
    except (TypeError, ValueError, OverflowError, get_user_model().DoesNotExist):
        return render(request, "token_invalid.html")


def reset_password_complete(request):
    return render(request, "password_reset_confirmation.html")


def mostrar_ubicacion(request):
    ubicacion = UbicacionUsuario.objects.get(usuario=request.user)
    depositos = UbicacionReciclaje.objects.all()
    materiales = MaterialReciclable.objects.all()
    return render(
        request,
        "mapa/mostrar_ubicaciones.html",
        {"ubicacion": ubicacion, "depositos": depositos, "materiales": materiales},
    )


def solicitud_recoleccion(request):
    if request.method == "POST":
        materiales_ids = request.POST.getlist("materiales")
        print(materiales_ids)
        for material_id in materiales_ids:
            material = MaterialReciclable.objects.get(pk=material_id)
            solicitud_existente = SolicitudRecoleccion.objects.filter(
                usuario=request.user, material=material, estado="Pendiente"
            ).exists()
            solicitud_existente_proceso = SolicitudRecoleccion.objects.filter(
                usuario=request.user, material=material, estado="En Proceso"
            ).exists()
            if solicitud_existente:
                # Ya existe una solicitud para este usuario y material
                form = SolicitudRecicladorForm()
                return render(
                    request,
                    "mapa/mostrar_ubicaciones.html",
                    {
                        "form": form,
                        "Mensaje": "Ya Hiciste una solicitud con este material",
                    },
                )
            elif solicitud_existente_proceso:
                form = SolicitudRecicladorForm()
                return render(
                    request,
                    "mapa/mostrar_ubicaciones.html",
                    {
                        "form": form,
                        "Mensaje": "Ya Hiciste una solicitud con este material y esta en proceso, pronto pasara una persona para recoger tu material",
                    },
                )
            else:
                solicitud = SolicitudRecoleccion(
                    usuario=request.user,
                    material=material,
                    fecha_solicitud= date.today(),
                    estado="Pendiente",
                )
                solicitud.save()

            form = SolicitudRecicladorForm()
            return render(
                request,
                "mapa/mostrar_ubicaciones.html",
                {
                    "form": form,
                    "Mensaje": "Ya se envio tu solicitud, pronto pasara una persona para recoger tu material",
                },
            )
    else:
        form = SolicitudRecicladorForm()
    return render(request, "mapa/mostrar_ubicaciones.html", {"form": form})


def admin_redirect(request):
    return redirect("admin:index")


@login_required
def quienesSomos(request):
    usuario_es_reciclador = (
        request.user.groups.filter(name="reciclador").exists()
        or request.user.is_superuser
    )
    
    return render(
        request, "quienes_somos.html", {"usuario_es_reciclador": usuario_es_reciclador}
    )


def mostrar_materiales_fotos(request):
    data = request.GET.get("data")

    try:
        data_list = json.loads(data)
        print("hola todo bien")
    except json.JSONDecodeError:
        data_list = []
        print("_________Error________")

    return render(request, "materiales/mostrar_materiales.html", {"data": data_list})


def obtener_foto_material(request, nombre):
    material = get_object_or_404(MaterialReciclable, nombre=nombre)
    foto_base64 = material.foto

    return JsonResponse({"foto": foto_base64})


def guardar_foto(request):
    if request.method == "POST":
        nombre = request.POST.get("nombre")
        nueva_foto = request.FILES.get("nueva_foto")
        material = get_object_or_404(MaterialReciclable, nombre=nombre)
        imagen_bytes = nueva_foto.read()
        imagen = Image.open(io.BytesIO(imagen_bytes))
        nuevo_tamano = (300, 300)  
        imagen = imagen.resize(nuevo_tamano, Image.ANTIALIAS)
        buffer = io.BytesIO()
        imagen.save(
            buffer, format="PNG"
        ) 

       
        imagen_redimensionada_bytes = buffer.getvalue()
        imagen_base64 = base64.b64encode(imagen_redimensionada_bytes).decode("utf-8")
        imagen_base64_con_prefijo = "data:image/png;base64," + imagen_base64

        # Guardar la imagen en el campo 'foto' del estudiante
        material.foto = imagen_base64_con_prefijo
        material.save()

        return render(
            request,
            "materiales/mostrar_materiales.html",
            {"mensaje": "Se ha actualizado tu foto"},
        )
    else:
        # Manejar el caso donde el método de solicitud no es POST
        return render(
            request,
            "materiales/mostrar_materiales.html",
            {"mensaje": "Se generó un error, por favor intenta de nuevo"},
        )


def buscar_material(request):
    if request.method == "POST":
        nombre = request.POST.get("nombre")
        material = MaterialReciclable.objects.all()
        depositos = UbicacionReciclaje.objects.all()
        usuario_es_reciclador = (
            request.user.groups.filter(name="reciclador").exists()
            or request.user.is_superuser
        )
        if get_object_or_404(MaterialReciclable, nombre=nombre):
            material_buscar = MaterialReciclable.objects.filter(nombre=nombre)
            solicitudes = SolicitudRecoleccion.objects.filter(
                material__in=material_buscar, estado="Pendiente"
            )
            usuarios_solicitudes = User.objects.filter(
                solicitudrecoleccion__in=solicitudes
            )

            ubicaciones = UbicacionUsuario.objects.filter(
                usuario__in=usuarios_solicitudes
            )
            return render(
                request,
                "home.html",
                {
                    "material_buscar": material_buscar,
                    "material": material,
                    "usuario_es_reciclador": usuario_es_reciclador,
                    "solicitudes": solicitudes,
                    "ubicaciones": ubicaciones,
                    "depositos": depositos,
                },
            )
        else:
            return render(
                request,
                "home.html",
                {
                    "mensaje": "No se encontro el material reciclable",
                    "material": material,
                    "usuario_es_reciclador": usuario_es_reciclador,
                },
            )
    else:
        return render(
            request,
            "home.html",
            {
                "mensaje": "No se encontro el material reciclable",
                "material": material,
                "usuario_es_reciclador": usuario_es_reciclador,
            },
        )


def confirmar_solicitud(request):
    if request.method == "POST":
        usuario_nombre = request.POST.get("usuario")
        reciclador = request.POST.get("reciclador")
        material_nombre = request.POST.get("material")


        usuario = get_object_or_404(User, username=usuario_nombre)

        material = get_object_or_404(MaterialReciclable, nombre=material_nombre)
        solicitud = SolicitudRecoleccion.objects.get(
            usuario=usuario, material=material, estado= "Pendiente"
        )

        try:
            solicitud_pendiente = SolicitudRecoleccion.objects.get(estado= "En Proceso",reciclador = reciclador)
        except:
            solicitud_pendiente = False

        if solicitud_pendiente:
            return render(
                request,
                "confirmacion/confirmacion.html",
                {"mensaje": "Ya tienes una solicitud pendiente, por favor finaliza esa solicitud"},
            )
        else:

            # Actualizar el reciclador y el estado
            solicitud.reciclador = reciclador
            solicitud.estado = "En Proceso"
            solicitud.fecha_solicitud_aceptada =date.today()
            solicitud.save()

            return render(
                request,
                "confirmacion/confirmacion.html",
                {"mensaje": "Solicitud confirmada exitosamente."},
            )

    else:
        # Manejar el caso en el que el método de solicitud no es POST
        return render(
            request,
            "confirmacion/confirmacion.html",
            {"mensaje": "Se genero un error, por favor vuelve a intentarlo"},
        )


def finalizar_solicitud(request):
    if request.method == "POST":
        usuario_nombre = request.POST.get("usuario")
        print(usuario_nombre)
        reciclador = request.POST.get("reciclador")
        material_nombre = request.POST.get("material")
        peso = request.POST.get("peso_kilos")

        usuario = get_object_or_404(User, username=usuario_nombre)

        material = get_object_or_404(MaterialReciclable, nombre=material_nombre)
        solicitud = SolicitudRecoleccion.objects.get(
            usuario=usuario, material=material,estado="En Proceso"
        )

        # Actualizar el reciclador y el estado
        solicitud.reciclador = reciclador
        solicitud.peso_kilos = peso
        solicitud.estado = "Finalizado"
        solicitud.fecha_solicitud_aceptada = None
        solicitud.fecha_recoleccion = date.today()
        solicitud.save()

        cantidad_puntos = int(peso)
        precio = int(material.precio_por_kilo)
        total = cantidad_puntos * precio

        puntos = PuntosRecompensa.objects.get(
            usuario=usuario,
            
        )

        catidad_actual = int(puntos.cantidad_puntos)
        puntos.cantidad_puntos = catidad_actual + total
        puntos.fecha_creacion= date.today()

        puntos.save()

        return render(
            request,
            "confirmacion/confirmacion.html",
            {
                "mensaje": "Se ha finalizado la solicitud, ya puedes seguir aceptando otras solicitudes. Gracias por tu servicio"
            },
        )
    else:
        # Manejar el caso en el que el método de solicitud no es POST
        return render(
            request,
            "confirmacion/confirmacion.html",
            {"mensaje": "Se genero un error, por favor vuelve a intentarlo"},
        )

def perfil_usuario(request):

    if request.method == "POST":
        usuarios = request.user
        Ubicacion = UbicacionUsuario.objects.get(usuario=usuarios)
        try:
            puntos = PuntosRecompensa.objects.get(usuario=usuarios)
            solicitudes = SolicitudRecoleccion.objects.filter(usuario=usuarios)
            usuario_es_reciclador = (
                request.user.groups.filter(name="reciclador").exists()
                or request.user.is_superuser
            )
            return render(request, "datos_usuario/perfil.html", {"usuarios": usuarios, "Ubicacion": Ubicacion, "puntos": puntos,"solicitudes":solicitudes,"usuario_es_reciclador":usuario_es_reciclador})

        except:
            usuario_es_reciclador = (
                request.user.groups.filter(name="reciclador").exists()
                or request.user.is_superuser
            )
            return render(request, "datos_usuario/perfil.html", {"usuarios": usuarios, "Ubicacion": Ubicacion,"usuario_es_reciclador":usuario_es_reciclador})



@login_required
def actualizar_datos(request):
    if request.method == "POST":

        usuario = request.user
        ubicacion_usuario = UbicacionUsuario.objects.get(usuario=usuario)

        nombre = request.POST.get("nombre")
        apellido = request.POST.get("apellido")
        email = request.POST.get("email")
        direccion = request.POST.get("direccion")  

        usuario.first_name = nombre
        usuario.last_name = apellido
        usuario.email = email
        usuario.save()

        ubicacion_usuario.direccion_domicilio = direccion
        ubicacion_usuario.save()

        
        return perfil_usuario(request) 
    else:
        return perfil_usuario(request) 

def donar_puntos(request): 
    if request.method == "POST":
        puntos = request.POST.get("puntos")
        puntos = int(puntos)
        if puntos > 0:
            usuario = request.user
            fecha = date.today()

            donacion_inicial = DonacionMaterialReciclable.objects.filter(usuario=usuario).first()

            if donacion_inicial:
                donacion_final = int(donacion_inicial.puntos) + int(puntos)
                donacion_inicial.puntos = donacion_final
                donacion_inicial.save()
            else:
                # Si no hay donación previa, crear una nueva instancia de DonacionMaterialReciclable
                DonacionMaterialReciclable.objects.create(usuario=usuario, puntos=puntos, fecha_donacion=fecha)

            # Actualizar puntos de recompensa
            puntos_nuevos = PuntosRecompensa.objects.get(usuario=usuario)
            puntos_nuevos.cantidad_puntos = 0
            puntos_nuevos.save()
        else:
            return render(request, "datos_usuario/perfil.html", {"mensaje": "error, por favor vuelva a intentarlo"})
    else:
        return render(request, "datos_usuario/perfil.html", {"mensaje": "error, por favor vuelva a intentarlo"})
    
    return perfil_usuario(request)

def comentarios(request):
    return render(request,"comentarios/comentarios.html")

def guardar_comentario(request):
    if request.method == "POST":
        usaurio = request.user
        comentario = request.POST.get("comentario")
        comantarios = QuejasSugerencias.objects.create(
            usuario = usaurio,
            comentario = comentario,
            fecha = date.today()
        )
        comantarios.save()
        return render(
            request,
            "confirmacion/confirmacion.html",
            {"mensaje": "Se ha enviado tu comentario, estaremos gestionando tu solicitud"},
        )
    else:
        return render(
            request,
            "confirmacion/confirmacion.html",
            {"mensaje": "Se genero un error, por favor vuelve a intentarlo"},
        )


        


from django_cron import CronJobBase, Schedule
from proyectoTesis.views import verificar_solicitudes
from django.core.mail import send_mail
from django.conf import settings

class MiTareaDiaria(CronJobBase):
    RUN_AT_TIMES = ['11:18']
    print("hola")
    code = 'proyectoTesis.views.verificar_solicitudes'

    def do(self):
        verificar_solicitudes()
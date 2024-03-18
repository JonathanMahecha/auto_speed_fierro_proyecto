from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.template.loader import render_to_string
from django.conf import settings
from .models import Garantia
from django.db.models.signals import pre_save
from .models import Garantia, EstadosGarantia,GarantiaProducto,RevisionGarantiaProducto, RevisionGarantiaServicio
from datetime import date

@receiver(post_save, sender=Garantia)
def enviar_correo_garantia(sender, instance, created, **kwargs):
    if created:
        # Renderizar el contenido del correo a partir de la plantilla HTML
        mensaje_html = render_to_string('correo_garantia.html', {
            'codigo_garantia': instance.codigo_garantia,
            'detalles_garantia': instance.detalles_garantia,
            'fecha_vencimiento': instance.fecha_vencimiento,
            'estado': instance.estados.estados,
            'servicio_con_garantia': instance.servicio_con_garantia,
            # Agrega más datos si es necesario
        })

        # Enviar el correo electrónico
        send_mail(
            'Registro Garantia',
            '',  # Dejar el mensaje en blanco, ya que el contenido está en el mensaje HTML
            settings.EMAIL_HOST_USER,  # Utiliza la dirección de correo electrónico configurada
            [instance.correo_electronico],  # Lista de destinatarios
            html_message=mensaje_html,  # Especifica el mensaje HTML
            fail_silently=False,  # Controla si se debe ignorar el fallo al enviar el correo
        )
        
#validacion fechas para  modelo Garantia
@receiver(pre_save, sender=Garantia)
def actualizar_estado_garantia(sender, instance, **kwargs):
    # Obtener los estados preexistentes de la base de datos
    estado_activa = EstadosGarantia.objects.get(estados='activa')
    estado_finalizada = EstadosGarantia.objects.get(estados='finalizada')
    estado_realizada = EstadosGarantia.objects.get(estados='realizada')

    # Verificar si la fecha de vencimiento ha pasado y el estado no es 'realizada'
    if instance.fecha_vencimiento < date.today() and instance.estados != estado_realizada:
        # Actualizar el estado a 'finalizada'
        instance.estados = estado_finalizada

#Validacion Fechas para modelo GarantiaProducto
@receiver(pre_save, sender=GarantiaProducto)
def actualizar_estado_garantia(sender, instance, **kwargs):
    # Obtener los estados preexistentes de la base de datos
    estado_activa = EstadosGarantia.objects.get(estados='activa')
    estado_finalizada = EstadosGarantia.objects.get(estados='finalizada')
    estado_realizada = EstadosGarantia.objects.get(estados='realizada')

    # Verificar si la fecha de vencimiento ha pasado y el estado no es 'realizada'
    if instance.fecha_vencimiento < date.today() and instance.estados != estado_realizada:
        # Actualizar el estado a 'finalizada'
        instance.estados = estado_finalizada
        
        
#envio de correo para GarantiasProducto
@receiver(post_save, sender=GarantiaProducto)
def enviar_correo_garantia(sender, instance, created, **kwargs):
    if created:
        # Renderizar el contenido del correo a partir de la plantilla HTML
        mensaje_html = render_to_string('correo_garantia_producto.html', {
            'codigo_garantia': instance.codigo_garantia,
            'detalles_garantia': instance.detalles_garantia,
            'fecha_vencimiento': instance.fecha_vencimiento,
            'estado': instance.estados.estados,
            # Agrega más datos si es necesario
        })

        # Enviar el correo electrónico
        send_mail(
            'Registro Garantia',
            '',  # Dejar el mensaje en blanco, ya que el contenido está en el mensaje HTML
            settings.EMAIL_HOST_USER,  # Utiliza la dirección de correo electrónico configurada
            [instance.correo_electronico],  # Lista de destinatarios
            html_message=mensaje_html,  # Especifica el mensaje HTML
            fail_silently=False,  # Controla si se debe ignorar el fallo al enviar el correo
        )
        
        
@receiver(post_save, sender=RevisionGarantiaProducto)
def enviar_correo_garantia(sender, instance, created, **kwargs):
    if created:
        # Renderizar el contenido del correo a partir de la plantilla HTML
        mensaje_html = render_to_string('correo_revision_producto.html', {
             'fecha_revision_garantia': instance.fecha_revision_garantia,
            'detalles_revision_garantia': instance.detalles_revision_garantia,
            'cantidad': instance.cantidad,
            'producto_garantia': instance.producto_garantia,
            # Agrega más datos si es necesario
        })

        # Enviar el correo electrónico
        send_mail(
            'Registro Garantia',
            '',  # Dejar el mensaje en blanco, ya que el contenido está en el mensaje HTML
            settings.EMAIL_HOST_USER,  # Utiliza la dirección de correo electrónico configurada
            [instance.correo_electronico],  # Lista de destinatarios
            html_message=mensaje_html,  # Especifica el mensaje HTML
            fail_silently=False,  # Controla si se debe ignorar el fallo al enviar el correo
        )
        
        
        
@receiver(post_save, sender=RevisionGarantiaServicio)
def enviar_correo_garantia(sender, instance, created, **kwargs):
    if created:
        mensaje_html = render_to_string('correo_revision_servicio.html', {
            'fecha_revision_garantia_servicio': instance.fecha_revision_garantia_servicio,
            'detalles_revision_garantia_servicio': instance.detalles_revision_garantia_servicio,
            'cantidad_producto_servicio': instance.cantidad_producto_servicio,
            'producto_garantia_servicio': instance.producto_garantia_servicio.name if instance.producto_garantia_servicio else '',  
        })

        send_mail(
            'Registro Garantía',
            '',  
            settings.EMAIL_HOST_USER,
            [instance.correo_electronico],
            html_message=mensaje_html,
            fail_silently=False,
        )

        

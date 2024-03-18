from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.template.loader import render_to_string
from django.conf import settings
from .models import Sale_service

@receiver(post_save, sender=Sale_service)
def enviar_correo_venta_servicio(sender, instance, created, **kwargs):
    if created:
        # Renderizar el contenido del correo a partir de la plantilla HTML
        mensaje_html = render_to_string('correo_venta_servicio.html', {
            #'cite' : instance.cite,
            'id' : instance.id,
            'service': instance.service,
            'client_name': instance.client_name,
            'client_email': instance.client_email,
            'client_id': instance.client_id,
            'brand': instance.brand,
            'model': instance.model,
            'year': instance.year,
            'color': instance.color,
            'plate_number': instance.plate_number,
            'notes': instance.notes,
            'price': instance.price,
            'product_price': instance.product_price,
            'total_price': instance.total_price,
            'sale_date': instance.sale_date,
            'time_date': instance.time_date,

            #'garantia': instance.garantia.codigo_garantia,
            # Agrega más datos si es necesario
        })

        # Enviar el correo electrónico
        send_mail(
            'Registro venta servicio',
            '',  # Dejar el mensaje en blanco, ya que el contenido está en el mensaje HTML
            settings.EMAIL_HOST_USER,  # Utiliza la dirección de correo electrónico configurada
            [instance.client_email],  # Lista de destinatarios
            html_message=mensaje_html,  # Especifica el mensaje HTML
            fail_silently=False,  # Controla si se debe ignorar el fallo al enviar el correo
        )
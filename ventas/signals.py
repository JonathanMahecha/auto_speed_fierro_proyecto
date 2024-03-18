from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.template.loader import render_to_string
from django.conf import settings    
from .models import Sale_product

@receiver(post_save, sender=Sale_product)
def enviar_correo_venta_producto(sender, instance, created, **kwargs):
    if created:
        # Renderizar el contenido del correo a partir de la plantilla HTML
        mensaje_html = render_to_string('correo_venta_producto.html', {
            'id' : instance.id,
            'product': instance.product.name,
            'quantity_sold': instance.quantity_sold,
            'unit_price': instance.unit_price,
            'total_price': instance.total_price,
            'sale_date': instance.sale_date,
            'client_name': instance.client_name,
            'client_email': instance.client_email,
            'client_id': instance.client_id,
            #'garantia': instance.garantia.codigo_garantia,
            # Agrega más datos si es necesario
        })

        # Enviar el correo electrónico
        send_mail(
            'Registro venta producto',
            '',  # Dejar el mensaje en blanco, ya que el contenido está en el mensaje HTML
            settings.EMAIL_HOST_USER,  # Utiliza la dirección de correo electrónico configurada
            [instance.client_email],  # Lista de destinatarios
            html_message=mensaje_html,  # Especifica el mensaje HTML
            fail_silently=False,  # Controla si se debe ignorar el fallo al enviar el correo
        )
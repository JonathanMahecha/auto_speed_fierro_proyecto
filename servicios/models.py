from django.db import models
from django.utils import timezone

from inventario.models import Product
from garantias.models import Garantia, ServicioConGarantia
from clienteAtencion.models import Service, cite

from django.core.mail import send_mail
from django.conf import settings
from datetime import timedelta


from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

def validate_cantidad_no_cero(value):
    if value == 0:
        raise ValidationError(_('No se puede ingresar una cantidad de cero.'))
        
def validate_not_future_date(value):
    if value > timezone.now().date():
        raise ValidationError('La fecha no puede ser en el futuro.')

def validate_not_past_date(value):
    thirty_days_ago = timezone.now().date() - timedelta(days=30)
    if value < thirty_days_ago:
        raise ValidationError('La fecha de compra no puede ser hace más de treinta días.')

class Producto_requerido_servicio(models.Model):
    #sale_service = models.ForeignKey(Sale_service, on_delete=models.CASCADE, blank=True, verbose_name='Venta de servicio')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Nombre producto')
    quantity_used = models.PositiveIntegerField(validators=[validate_cantidad_no_cero], verbose_name='Cantidad del producto usada')
    date = models.DateField(validators=[validate_not_future_date, validate_not_past_date], verbose_name='Fecha servicio del producto')

    def __str__(self):
        return f"{self.product}"

    # def save(self, *args, **kwargs):
    #     self.date = self.sale_service.sale_date
        
    #     #self.total_price = self.quantity_sold * self.unit_price
    #     super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Producto requerido del servicio'
        verbose_name_plural = 'Productos requeridos del servicio'
        db_table = 'producto_requerido_servicio'
        ordering = ['id']

#Tabla de ventas de servicios
class Sale_service(models.Model):
    cite = models.ForeignKey(cite, on_delete=models.CASCADE, verbose_name='Cita', null=True)
    #service = models.ForeignKey(ServicioConGarantia, on_delete=models.CASCADE, verbose_name='Nombre servicio')
    service = models.CharField(max_length=40, verbose_name='Nombre servicio')
    client_name = models.CharField(max_length=50, verbose_name='Nombre del cliente')
    client_email = models.EmailField(max_length=254, verbose_name='Email del cliente')
    client_id = models.CharField(max_length=12, verbose_name='Identificación del cliente')
    brand = models.CharField(max_length=50, verbose_name='Marca del vehiculo')
    model = models.CharField(max_length=50, verbose_name='Modelo del vehiculo')
    year = models.PositiveIntegerField(verbose_name='Año del vehiculo')
    color = models.CharField(max_length=50, verbose_name='Color del vehículo')
    plate_number = models.CharField(max_length=20,verbose_name='Número de placa')
    notes = models.TextField(blank=True, null=True, verbose_name='Detalles del vehículo')
    price = models.DecimalField(max_digits=12, decimal_places=2, verbose_name='Precio mano de obra')
    product_price = models.DecimalField(max_digits=12, decimal_places=2, verbose_name='Precio productos')
    total_price = models.DecimalField(max_digits=12, decimal_places=2, verbose_name='Precio total')
    sale_date = models.DateField(verbose_name='Fecha de venta', default=timezone.now)
    time_date = models.TimeField(verbose_name='Hora de venta', default=timezone.now)
    state = models.CharField(max_length=20, choices=[('En proceso', 'En proceso'), ('Finalizado', 'Finalizado')], default='En proceso', verbose_name='Estado del servicio')
    producto_usado = models.ForeignKey(Producto_requerido_servicio, on_delete=models.CASCADE, null=True, blank=True, verbose_name='Productos usados')
    garantia = models.ForeignKey(Garantia, on_delete=models.CASCADE, null=True, blank=True, verbose_name='servicio con garantía')

    def __str__(self):
        return f"{self.id} - {self.service}"
    
    def enviar_correo_venta_servicio(self):
        mensaje = f"REGISTRO VENTA DE SERVICIO:\n\n"
        mensaje += f"Detalles de la venta de servicio: {self.price}\n"
        mensaje += f"Detalles del vehículo: {self.service}\n"

        send_mail(
            'TU FACTURA DE VENTA DE SERVICIO',
            mensaje,
            settings.EMAIL_HOST_USER,
            [self.client_email],
            fail_silently=False,
        )

    def save(self, *args, **kwargs):
        self.price = self.cite.service.price
        self.product_price = self.cite.service.product_price
        #self.service = self.cite.service
        self.service = self.cite.service.nombre
        self.client_email = self.cite.client_email
        self.client_name = self.cite.client_name
        self.client_id = self.cite.client_id
        self.brand = self.cite.brand
        self.model = self.cite.model
        self.year = self.cite.year
        self.color = self.cite.color
        self.notes = self.cite.notes
        self.plate_number = self.cite.plate_number
        self.total_price = self.price + self.product_price
        #self.sale_date = self.cite.date
        #self.time_date = self.cite.time
        #self.enviar_correo_venta_servicio()
        super().save(*args, **kwargs)
    
    class Meta:
        verbose_name = 'Venta de servicios'
        verbose_name_plural = 'Ventas de servicios'
        db_table = 'venta_servicio'
        ordering = ['id']
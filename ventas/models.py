from django.db import models
from inventario.models import Product
from garantias.models import Garantia, GarantiaProducto

from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator

from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from django.core.mail import send_mail
from django.conf import settings

from datetime import timedelta

#Tabla de ventas de productos

def validate_fecha_venta(value):
    today = timezone.now().date()
    if value > today:
        raise ValidationError(_('La fecha de venta no puede ser en el futuro.'))
    
def validate_not_past_date(value):
    thirty_days_ago = timezone.now().date() - timedelta(days=30)
    if value < thirty_days_ago:
        raise ValidationError('La fecha de compra no puede ser hace más de treinta días.')

def validate_cantidad_no_cero(value):
    if value == 0:
        raise ValidationError(_('No se puede vender una cantidad de cero.'))

def validate_client_id_length(value):
    if not 6 <= len(str(value)) <= 12:
        raise ValidationError('El ID del cliente debe tener entre 6 y 12 dígitos.')


class Sale_product(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Nombre producto')
    #quantity_sold = models.PositiveIntegerField(validators=[validate_enough_quantity], verbose_name='Cantidad vendida')
    quantity_sold = models.PositiveIntegerField(validators=[validate_cantidad_no_cero], verbose_name='Cantidad vendida')
    unit_price = models.DecimalField(max_digits=12, decimal_places=2, verbose_name='Precio unitario')
    total_price = models.DecimalField(default=0, max_digits=12, decimal_places=2, verbose_name='Precio total')
    METODO_PAGO_CHOICES = [
        ('Efectivo', 'Efectivo'),
        # ('Tarjeta de crédito', 'Tarjeta de crédito'),
        # ('Transferencia bancaria', 'Transferencia bancaria'),
        # ('Cheque', 'Cheque'),
        #('Otro', 'Otro'),
    ]
    metodo_pago = models.CharField(max_length=30, choices=METODO_PAGO_CHOICES, default='Efectivo', verbose_name='Método de pago')
    sale_date = models.DateField(validators=[validate_fecha_venta, validate_not_past_date], verbose_name='Fecha de venta', default=timezone.now)
    client_name = models.CharField(max_length=50, verbose_name='Nombre del cliente', validators=[
            RegexValidator(
                regex=r'^[a-zA-Z ]+$', 
                message='Ingrese un nombre válido (solo letras y espacios).'
            )],)
    client_email = models.EmailField(max_length=254, verbose_name='Email del cliente')
    client_id = models.IntegerField(validators=[validate_client_id_length], verbose_name='Identificación del cliente')
    garantia = models.ForeignKey(GarantiaProducto, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"{self.quantity_sold} of {self.product.name} sold on {self.sale_date}"

    def enviar_correo_venta_producto(self):
        mensaje = f"REGISTRO VENTA DE PRODUCTO:\n\n"
        mensaje += f"Detalles de la venta de producto: {self.product}\n"
        mensaje += f"Detalles del vehículo: {self.quantity_sold}\n"

        send_mail(
            'TU FACTURA DE VENTA DE PRODUCTO',
            mensaje,
            settings.EMAIL_HOST_USER,
            [self.client_email],
            fail_silently=False,
        )

    def save(self, *args, **kwargs):
        self.unit_price = self.product.price
        self.total_price = self.quantity_sold * self.unit_price
        product = self.product
        quantity_sold = self.quantity_sold
        super().save(*args, **kwargs)


    class Meta:
        verbose_name = 'Venta de producto'
        verbose_name_plural = 'Ventas de productos'
        db_table = 'venta_producto'
        ordering = ['id']
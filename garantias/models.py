from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
import random
from django.core.mail import send_mail
from django.conf import settings
from django.db.models.signals import pre_save
from django.dispatch import receiver
from inventario.models import Product,Purchase
from datetime import datetime, timedelta
from django.core.validators import MinValueValidator


def validate_not_zero(value):
    if value == 0:
        raise ValidationError('La cantidad no puede ser cero.')

class ServicioConGarantia(models.Model):
    nombre = models.CharField(max_length=100, verbose_name='Nombre')
    descripcion = models.TextField(verbose_name='Descripción')
    price = models.DecimalField(validators=[validate_not_zero, MinValueValidator(0)], max_digits=12, decimal_places=2, verbose_name='Precio mano de obra')
    product_price = models.DecimalField(validators=[validate_not_zero, MinValueValidator(0)], max_digits=12, decimal_places=2, verbose_name='Precio productos')
    imagen = models.ImageField(upload_to='imagen', verbose_name='Imagen_servicio')

    def __str__(self):
        return self.nombre
    
    class Meta:
        verbose_name = 'Servicio'
        verbose_name_plural = 'Servicios'
        db_table = 'servicios'
        ordering = ['id']
        

def generate_codigo_garantia():
    while True:
        nuevo_codigo = random.randint(1000, 9999)
        if not Garantia.objects.filter(codigo_garantia=nuevo_codigo).exists() and not GarantiaProducto.objects.filter(codigo_garantia=nuevo_codigo).exists():
            return nuevo_codigo


def validate_fecha_vencimiento(value):
    pass

class EstadosGarantia(models.Model):
    estados = models.CharField(max_length=20)

    def __str__(self):
        return self.estados

    class Meta:
        verbose_name = "Estado de Garantía"
        verbose_name_plural = "Estados de Garantía"
        db_table = "EstadosGarantia"
        ordering = ['id']
        
def validate_not_future_date(value):
    if value > timezone.now().date():
        raise ValidationError('La fecha no puede ser en el futuro.')

def validate_not_past_date(value):
    thirty_days_ago = timezone.now().date() - timedelta(days=30)
    if value < thirty_days_ago:
        raise ValidationError('La fecha de revisión no puede ser hace más de treinta días.')
        
class RevisionGarantiaServicio(models.Model):
    fecha_revision_garantia_servicio = models.DateField(validators=[validate_not_future_date, validate_not_past_date], verbose_name='Fecha revisión del servicio') 
    detalles_revision_garantia_servicio = models.CharField(max_length=100)
    correo_electronico = models.EmailField(max_length=254, verbose_name='Correo Electrónico')
    cantidad_producto_servicio = models.PositiveIntegerField(verbose_name='Cantidad de productos con garantía', blank=True, null=True)
    producto_garantia_servicio = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Producto con garantía', blank=True, null=True)
    
    def enviar_correo_garantia_revision_producto(self):
        mensaje = f"REGISTRO GARANTIA:\n\n"
        mensaje += f"Detalles de la revision de garantia: {self.detalles_garantia}\n"

        send_mail(
            'TU GARANTIA',
            mensaje,
            settings.EMAIL_HOST_USER,
            [self.correo_electronico],
            fail_silently=False,
        )
    
    def __str__(self):
        if self.producto_garantia_servicio:
            return f"{self.producto_garantia_servicio.name} - {self.detalles_revision_garantia_servicio}"
        else:
            return f"Revisión de garantía sin producto - {self.detalles_revision_garantia_servicio}"

    class Meta:
        verbose_name = "Revision Garantía Servicio"
        verbose_name_plural = "Revision Garantía Servicio"
        db_table = "revision_garantia_servicio"
        ordering = ['id']

    def __str__(self):
        if self.producto_garantia_servicio:
            return f"{self.producto_garantia_servicio.name} - {self.detalles_revision_garantia_servicio}"
        else:
            return f"Revisión de garantía sin producto - {self.detalles_revision_garantia_servicio}"

    class Meta:
        verbose_name = "Revision Garantía Servicio"
        verbose_name_plural = "Revision Garantía Servicio"
        db_table = "revision_garantia_servicio"
        ordering = ['id']

    def clean(self):
        if self.cantidad_producto_servicio is not None and self.cantidad_producto_servicio <= 0:
            raise ValidationError("La cantidad debe ser mayor que 0.")

        if self.cantidad_producto_servicio is not None and self.producto_garantia_servicio is not None:
            if self.cantidad_producto_servicio > self.producto_garantia_servicio.quantity:
                raise ValidationError("La cantidad a restar no puede ser mayor que la cantidad disponible en el producto.")

            # Verificar si la cantidad disponible después de restar es igual o menor a 5
            if self.producto_garantia_servicio.quantity - self.cantidad_producto_servicio <= 5:
                raise ValidationError("La cantidad de producto disponible después de restar sería igual o menor a 5. No se puede restar más cantidad.")
    
    def save(self, *args, **kwargs):
        if self.cantidad_producto_servicio is not None and self.producto_garantia_servicio is not None:
            self.producto_garantia_servicio.quantity -= self.cantidad_producto_servicio
            self.producto_garantia_servicio.save()
        super().save(*args, **kwargs)

class Garantia(models.Model):
    servicio_con_garantia = models.ForeignKey(ServicioConGarantia, on_delete=models.CASCADE, verbose_name='Servicio con garantía')
    fecha_vencimiento = models.DateField(blank=True, null=True)
    codigo_garantia = models.PositiveIntegerField(unique=True, default=generate_codigo_garantia)
    detalles_garantia = models.CharField(max_length=100)
    estados = models.ForeignKey(EstadosGarantia, on_delete=models.CASCADE)
    correo_electronico = models.EmailField(max_length=254, verbose_name='Correo Electrónico')
    revision_garantia_servicio = models.ForeignKey(RevisionGarantiaServicio, on_delete=models.CASCADE, blank=True, null=True, verbose_name='revision garantia SERVICIO')
    

    def enviar_correo_garantia(self):
        mensaje = f"REGISTRO GARANTIA:\n\n"
        mensaje += f"Detalles de la garantía: {self.detalles_garantia}\n"
        

        send_mail(
            'TU GARANTIA',
            mensaje,
            settings.EMAIL_HOST_USER,
            [self.correo_electronico],
            fail_silently=False,
        )

    def __str__(self):
        return str(self.codigo_garantia) or str(self.id)

    class Meta:
        verbose_name = "Garantia_servicio"
        verbose_name_plural = "Garantías Servicio"
        db_table = "Garantia_servicio"
        ordering = ['id']
        
@receiver(pre_save, sender=Garantia)
def actualizar_fecha_vencimiento(sender, instance, **kwargs):
    # Obtener la fecha actual
    fecha_actual = timezone.now().date()

    # Obtener el servicio seleccionado
    servicio = instance.servicio_con_garantia

    # Inicializar la variable fecha_vencimiento
    fecha_vencimiento = None

    # Definir las fechas de vencimiento según el servicio seleccionado
    if servicio.nombre == 'Cambio de aceite y filtro':
        fecha_vencimiento = fecha_actual + timedelta(weeks=1)
    elif servicio.nombre == 'Alineacion y balanceo':
        fecha_vencimiento = fecha_actual + timedelta(weeks=26)  # 6 meses
    elif servicio.nombre == 'Cambio de pastillas de freno':
        fecha_vencimiento = fecha_actual + timedelta(weeks=52)  # 1 año
    elif servicio.nombre == 'Reparacion de sistema de suspension':
        fecha_vencimiento = fecha_actual + timedelta(weeks=26)  # 6 meses
    elif servicio.nombre == 'Reparacion de sistema de direccion':
        fecha_vencimiento = fecha_actual + timedelta(weeks=52)  # 1 año
    elif servicio.nombre == 'Cambio de neumaticos':
        fecha_vencimiento = fecha_actual + timedelta(weeks=26)  # 6 meses
    elif servicio.nombre == 'Cambio de bujias':
        fecha_vencimiento = fecha_actual + timedelta(weeks=26)  # 6 meses
    elif servicio.nombre == 'Cambio de piezas':
        fecha_vencimiento = fecha_actual + timedelta(weeks=13)  # 3 meses
    elif servicio.nombre == 'Mantenimiento preventivo':
        fecha_vencimiento = fecha_actual + timedelta(weeks=4)  # 1 mes
    else:
        # Si no se cumple ninguno de los casos anteriores, asignamos una fecha de vencimiento predeterminada
        fecha_vencimiento = fecha_actual

    # Asignar la fecha de vencimiento al objeto Garantia
    instance.fecha_vencimiento = fecha_vencimiento


        
class RevisionGarantiaProducto(models.Model):
    fecha_revision_garantia = models.DateField(validators=[validate_not_future_date, validate_not_past_date], verbose_name='Fecha revisión del producto') 
    detalles_revision_garantia = models.CharField(max_length=100)
    correo_electronico = models.EmailField(max_length=254, verbose_name='Correo Electrónico')
    cantidad = models.PositiveIntegerField(verbose_name='cantidad de productos con garantia')
    producto_garantia = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Producto con garantia')

    def enviar_correo_garantia_revision_producto(self):
        mensaje = f"REGISTRO GARANTIA:\n\n"
        mensaje += f"Detalles de la revision de garantia: {self.detalles_garantia}\n"

        send_mail(
            'TU GARANTIA',
            mensaje,
            settings.EMAIL_HOST_USER,
            [self.correo_electronico],
            fail_silently=False,
        )

    def __str__(self):
        return f"{self.producto_garantia.name} - {self.fecha_revision_garantia}"
    
    def clean(self):
        if self.cantidad <= 0:
            raise ValidationError("La cantidad debe ser mayor que 0.")

        if self.producto_garantia.quantity <= 5:
            raise ValidationError("cantidad de producto no disponible en este momento.")

        if self.cantidad > self.producto_garantia.quantity - 5:
            raise ValidationError("cantidad de producto no disponible en este momento")
        

    def save(self, *args, **kwargs):
        self.full_clean()  # Ejecutar la validación antes de guardar
        # Restar la cantidad seleccionada del producto
        self.producto_garantia.quantity -= self.cantidad
        self.producto_garantia.save()  # Guardar la instancia actualizada del producto
        super().save(*args, **kwargs)
        
    
        
      
    class Meta:
        verbose_name = "RevisionGarantiaProducto"
        verbose_name_plural = "Revision Garantia Producto"
        db_table = "RevisionGarantiaProducto"
        ordering = ['id']
    
def validate_only_future_date(value):
    if value < timezone.now().date():
        raise ValidationError('La fecha no puede ser en el pasado.')
        
class GarantiaProducto(models.Model):
    producto_con_garantia = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Producto con garantía')
    fecha_vencimiento = models.DateField(blank=True, null=True)
    codigo_garantia = models.PositiveIntegerField(unique=True, default=generate_codigo_garantia)
    detalles_garantia = models.CharField(max_length=100)
    estados = models.ForeignKey(EstadosGarantia, on_delete=models.CASCADE)
    correo_electronico = models.EmailField(max_length=254, verbose_name='Correo Electrónico')
    revision_garantia = models.ForeignKey(RevisionGarantiaProducto, on_delete=models.CASCADE, blank=True, null=True, verbose_name='revision garantia PRODUCTO')
    
    
    def save(self, *args, **kwargs):
        if self.producto_con_garantia.garantia != '0':  # Si la garantía no es "Sin garantía"
            tiempo_garantia = int(self.producto_con_garantia.garantia)  # Obtener el tiempo de garantía seleccionado
            fecha_actual = datetime.now().date()  # Obtener la fecha actual
            self.fecha_vencimiento = fecha_actual + timedelta(days=30 * tiempo_garantia)  # Calcular la fecha de vencimiento sumando los meses
        # else:
        #     self.fecha_vencimiento = None  # Si es "Sin garantía", establecer la fecha de vencimiento como None
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.detalles_garantia
    
    class Meta:
        verbose_name = "GarantíaProducto"
        verbose_name_plural = "Garantías Producto"
        db_table = "Garantia_Producto"
        ordering = ['id']
        
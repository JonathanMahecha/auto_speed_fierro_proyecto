from django.db import models
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import timedelta
from django.core.validators import MinValueValidator

class Category(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name='Nombre')
    description = models.CharField(max_length=255, verbose_name='Descripción')

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Categoría'
        verbose_name_plural = 'Categorías'
        db_table = 'categoria'
        ordering = ['id']

def validate_not_zero(value):
    if value == 0:
        raise ValidationError('La cantidad no puede ser cero.')

class Product(models.Model):
    name = models.CharField(max_length=100, verbose_name='Nombre')
    brand = models.CharField(default=0, max_length=100, verbose_name='Marca')
    description = models.TextField(verbose_name='Descripción')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Categoría')
    price = models.DecimalField(validators=[validate_not_zero, MinValueValidator(0)], max_digits=12, decimal_places=2, verbose_name='Precio', )
    quantity = models.PositiveIntegerField(default=0, verbose_name='Cantidad')
    #fecha_vencimiento = models.CharField()
    GARANTIA_CHOICES = [
        ('1', '1 mes'),
        ('3', '3 meses'),
        ('6', '6 meses'),
        ('12', '1 año'),
        # ('0', 'Sin garantía'),
    ]
    garantia = models.CharField(max_length=2, choices=GARANTIA_CHOICES, default='0', verbose_name='Garantía')
    image = models.ImageField(upload_to='producto', verbose_name='Imagen_producto')

    def __str__(self):
        return self.name
    
    

    class Meta:
        verbose_name = 'Producto'
        verbose_name_plural = 'Productos'
        db_table = 'producto'
        ordering = ['id']


#Tabla de proveedores
class Supplier(models.Model):
    name = models.CharField(unique=True, max_length=100, verbose_name='Nombre')
    #contact_person = models.CharField(max_length=100)
    email = models.EmailField(unique=True, verbose_name='Correo electrónico')
    phone_number = models.CharField(unique=True, max_length=12, validators=[RegexValidator(regex='^[0-9]{10}$', message='El número de contacto debe tener 10 dígitos numéricos')], verbose_name='Número de celular')

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Proveedor'
        verbose_name_plural = 'Proveedores'
        db_table = 'proveedor'
        ordering = ['id']
        
#Tabla de compra de productos
def validate_not_zero(value):
    if value == 0:
        raise ValidationError('La cantidad no puede ser cero.')

def validate_not_future_date(value):
    if value > timezone.now().date():
        raise ValidationError('La fecha de compra no puede ser en el futuro.')

def validate_not_past_date(value):
    thirty_days_ago = timezone.now().date() - timedelta(days=30)
    if value < thirty_days_ago:
        raise ValidationError('La fecha de compra no puede ser hace más de treinta días.')

class Purchase(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Nombre producto')
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, verbose_name='Proveedor')
    quantity = models.PositiveIntegerField(validators=[validate_not_zero], verbose_name='Cantidad')
    unit_price = models.DecimalField(validators=[validate_not_zero, MinValueValidator(0)], max_digits=12, decimal_places=2, verbose_name='Precio unitario')
    total_price = models.DecimalField(max_digits=12, decimal_places=2, verbose_name='Precio total')
    purchase_date = models.DateField(verbose_name='Fecha de compra', validators=[validate_not_future_date, validate_not_past_date])

    def __str__(self):
        return f"{self.quantity} de {self.product.name} comprados a {self.supplier.name}"

    def save(self, *args, **kwargs):
        self.total_price = self.quantity * self.unit_price
        super().save(*args, **kwargs)
    
    class Meta:
        verbose_name = 'Compra'
        verbose_name_plural = 'Compras'
        db_table = 'compra'
        ordering = ['id']
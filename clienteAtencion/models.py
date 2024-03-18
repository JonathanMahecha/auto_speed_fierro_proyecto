from django.db import models
# from servicios.models import Service

from django.contrib.auth import get_user_model
from garantias.models import ServicioConGarantia
from django.core.validators import RegexValidator

class Service(models.Model):
    name = models.CharField(max_length=100, verbose_name='Nombre')
    description = models.TextField(verbose_name='Descripción')
    image = models.ImageField(upload_to='imagen', verbose_name='Imagen_servicio')

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Servicio'
        verbose_name_plural = 'Servicios'
        db_table = 'servicio'
        ordering = ['id']
        
User = get_user_model()

class cite(models.Model):
    
    ESTADO = [
    ('En espera', 'En espera'),
    ('En proceso', 'En proceso'),
    ('Re agendada', 'Re agendada'),
    ('Ausente', 'Ausente'),
    ('Finalizada', 'Finalizada'),
    ]
    
    MARCAS_DE_VEHICULOS = [
    ('Toyota', 'Toyota'),
    ('Ford', 'Ford'),
    ('Volkswagen', 'Volkswagen'),
    ('BMW', 'BMW (Bayerische Motoren Werke)'),
    ('Mercedes-Benz', 'Mercedes-Benz'),
    ('Honda', 'Honda'),
    ('Chevrolet', 'Chevrolet'),
    ('Audi', 'Audi'),
    ('Nissan', 'Nissan'),
    ('Tesla', 'Tesla'),
    ('Hyundai', 'Hyundai'),
    ('Kia', 'Kia'),
    ('Subaru', 'Subaru'),
    ('Porsche', 'Porsche'),
    ('Fiat', 'Fiat'),
    ('Mazda', 'Mazda'),
    ('Volvo', 'Volvo'),
    ('Jaguar', 'Jaguar'),
    ('Land Rover', 'Land Rover'),
    ('Jeep', 'Jeep'),
    ('Renault', 'Renault'),
    ('Suzuki', 'Suzuki'),
    ('Mitsubishi', 'Mitsubishi'),
    ('Peugeot', 'Peugeot'),
    ('Citroën', 'Citroën'),
    ('Chery', 'Chery'),
    ('Great Wall Motors', 'Great Wall Motors'),
    ('BYD', 'BYD'),
    ('Geely', 'Geely'),
    ('JAC Motors', 'JAC Motors'),
    ('Dongfeng', 'Dongfeng'),
    ('Tata Motors', 'Tata Motors'),
    ('Mahindra', 'Mahindra'),
    ('SsangYong', 'SsangYong'),
    ('Isuzu', 'Isuzu'),
    ('Zotye', 'Zotye'),
    ('Foton', 'Foton'),
    ('Mini', 'Mini'),
    ('Alfa Romeo', 'Alfa Romeo'),
    ('MG', 'MG'),
    ('Lada', 'Lada'),
    ('Haima', 'Haima'),
    ('GAC Motors', 'GAC Motors'),
    ('BAIC', 'BAIC'),
    ('Haval', 'Haval'),
    ('Wuling', 'Wuling'),
    ('DS Automobiles', 'DS Automobiles'),
    ('Proton', 'Proton'),
    ('Perodua', 'Perodua'),
    ('Changan', 'Changan'),
    ('Hawtai', 'Hawtai'),
    ('FAW', 'FAW'),
    ('SAIC Motor', 'SAIC Motor'),
    ('Roewe', 'Roewe'),
    ('Soueast Motors', 'Soueast Motors'),
    ('VinFast', 'VinFast'),
    ('Chang\'an', 'Chang\'an'),
    ('Lifan', 'Lifan')
]

    COLORES = [
        ('Blanco', 'Blanco'),
        ('Negro', 'Negro'),
        ('Gris', 'Gris'),
        ('Azul', 'Azul'),
        ('Rojo', 'Rojo'),
        ('Verde', 'Verde'),
        ('Amarillo', 'Amarillo'),
        ('Naranja', 'Naranja'),
        ('Marrón', 'Marrón'),
        ('Beige', 'Beige'),
        ('Rosa', 'Rosa'),
        ('Morado', 'Morado'),
        ('Turquesa', 'Turquesa'),
        ('Celeste', 'Celeste'),
        ('Plateado', 'Plateado'),
        ('Dorado', 'Dorado'),
        ('Crema', 'Crema'),
        ('Verde oliva', 'Verde oliva'),
        ('Azul marino', 'Azul marino'),
        ('Violeta', 'Violeta'),
        ('Cian', 'Cian'),
        ('Magenta', 'Magenta'),
        ('Lavanda', 'Lavanda'),
        ('Aguamarina', 'Aguamarina'),
        ('Coral', 'Coral'),
        ('Marfil', 'Marfil'),
        ('Esmeralda', 'Esmeralda'),
        ('Índigo', 'Índigo'),
        ('Melocotón', 'Melocotón'),
        ('Borgoña', 'Borgoña'),
        ('Lima', 'Lima'),
        ('Teal', 'Teal'),
        ('Amaranto', 'Amaranto'),
        ('Gris perla', 'Gris perla'),
        ('Fucsia', 'Fucsia'),
        ('Menta', 'Menta'),
        ('Ocre', 'Ocre'),
        ('Caqui', 'Caqui'),
        ('Ámbar', 'Ámbar'),
        ('Carmesí', 'Carmesí'),
        ('Púrpura', 'Púrpura'),
        ('Rubí', 'Rubí'),
        ('Gris pizarra', 'Gris pizarra'),
        ('Ónice', 'Ónice'),
        ('Mauve', 'Mauve'),
        ('Lima oscuro', 'Lima oscuro'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, verbose_name='Usuario')
    client_name = models.CharField(max_length=50, verbose_name='Nombre del cliente')
    client_email = models.EmailField(max_length=254, verbose_name='Email del cliente')
    client_id = models.IntegerField(verbose_name='Identificación del cliente')
    brand = models.CharField(max_length=50, choices=MARCAS_DE_VEHICULOS, verbose_name='Marca del vehiculo')
    model = models.CharField(max_length=50, verbose_name='Modelo del vehiculo')
    year = models.PositiveIntegerField(verbose_name='Año del vehiculo')
    color = models.CharField(
        max_length=50,
        choices=COLORES,
        verbose_name='Color del vehículo'
    )
    plate_number_validator = RegexValidator(
        regex=r'^[A-Za-z]{3}\d{3}$',  
        message='La placa debe tener el formato correcto: tres letras seguidas de tres números.'
    )
    plate_number = models.CharField(
        max_length=20,
        verbose_name='Número de placa',
        validators=[plate_number_validator]  
    )

    notes = models.TextField(blank=True, null=True, verbose_name='Detalles del vehículo')
    service = models.ForeignKey(ServicioConGarantia, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()
    estado = models.CharField(
        max_length=50,
        choices=ESTADO,
        verbose_name='Estado de cita',
        null=True,
    )
    
    def __str__(self):
        return f"{self.client_name} Para el servicio: {self.service.nombre}"

    class Meta:
        verbose_name = 'Cita'
        verbose_name_plural = 'Citas'
        db_table = 'cite'
        ordering = ['id']

class comment(models.Model):
    headLine = models.CharField(max_length=30, verbose_name='Título')
    cite = models.ForeignKey(cite, on_delete=models.CASCADE, verbose_name='Cita')
    description = models.TextField(verbose_name='Descripción')

    def __str__(self):
        return self.headLine

    class Meta:
        verbose_name = 'Comentario'
        verbose_name_plural = 'Comentarios'
        db_table = 'comment'
        ordering = ['id']

class contacts(models.Model):
    first_name = models.CharField(max_length=30, verbose_name='Nombres')
    last_name = models.CharField(max_length=30, verbose_name='Apellidos')
    email = models.EmailField(verbose_name='Correo electrónico')
    contact = models.CharField(max_length=12, validators=[RegexValidator(regex='^[0-9]{10}$', message='El número de contacto debe tener 10 dígitos numéricos')], verbose_name='Número de celular')

    #contact = models.IntegerField()

    def __str__(self):
        return "%s %s" % (self.first_name, self.last_name)

    class Meta:
        verbose_name = 'Contacto'
        verbose_name_plural = 'Contactos'
        db_table = 'contacts'
        ordering = ['id']
      
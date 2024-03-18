import pytest
from django.core.exceptions import ValidationError
from django.utils import timezone
#from django.contrib.auth.models import User
from django.contrib.auth import get_user_model

from servicios.models import Sale_service
from clienteAtencion.models import cite
from garantias.models import ServicioConGarantia, Garantia


# @pytest.fixture
# def cita():
#     return cite.objects.create(nombre='Cita de ejemplo')

# @pytest.fixture
# def servicio():
#     return ServicioConGarantia.objects.create(nombre='Servicio de ejemplo')

# @pytest.fixture
# def garantia():
#     return Garantia.objects.create(nombre='Garantía de ejemplo')

User = get_user_model()

@pytest.fixture
def user():
    return User.objects.create_user(
        username='test_user',
        email='test_user@example.com',
        password='test_password'
    )

@pytest.fixture
def servicio_con_garantia():
    return ServicioConGarantia.objects.create(
        nombre='Servicio de ejemplo',
        descripcion='Descripción de ejemplo',
        imagen='imagen/imagen_ejemplo.jpg'
    )

@pytest.mark.django_db
def test_create_servicio_con_garantia(servicio_con_garantia):
    assert servicio_con_garantia.nombre == 'Servicio de ejemplo'
    assert servicio_con_garantia.descripcion == 'Descripción de ejemplo'
    assert servicio_con_garantia.imagen == 'imagen/imagen_ejemplo.jpg'

@pytest.fixture
def cita(user):
    return cite.objects.create(
        user=user,
        client_name='Cliente de ejemplo',
        client_email='cliente@example.com',
        client_id='1234567890',
        brand='Toyota',
        model='Camry',
        year=2020,
        color='Negro',
        plate_number='ABC123',
        notes='Detalles del vehículo',
        service=ServicioConGarantia.objects.create(nombre='Servicio de ejemplo', descripcion='Descripción de ejemplo', imagen='imagen/imagen_ejemplo.jpg'),
        date='2024-03-05',
        time='10:00:00'
    )

@pytest.mark.django_db
def test_create_cita(cita):
    assert cita.user.username == 'test_user'
    assert cita.client_name == 'Cliente de ejemplo'
    assert cita.client_email == 'cliente@example.com'
    assert cita.client_id == '1234567890'
    assert cita.brand == 'Toyota'
    assert cita.model == 'Camry'
    assert cita.year == 2020
    assert cita.color == 'Negro'
    assert cita.plate_number == 'ABC123'
    assert cita.notes == 'Detalles del vehículo'
    assert cita.service.nombre == 'Servicio de ejemplo'
    assert cita.date == '2024-03-05'
    assert cita.time == '10:00:00'


@pytest.mark.django_db
def test_create_sale_service(cita, servicio, garantia):
    sale_service = Sale_service.objects.create(
        cite=cita,
        service=servicio,
        client_name='Cliente de ejemplo',
        client_email='cliente@example.com',
        client_id='1234567890',
        brand='Toyota',
        model='Corolla',
        year=2022,
        color='Azul',
        plate_number='ABC123',
        price=100.00,
        product_price=50.00,
        total_price=150.00,
        sale_date=timezone.now().date(),
        time_date=timezone.now().time(),
        state='En proceso',
        garantia=garantia
    )
    assert sale_service.cite == cita
    assert sale_service.service == servicio
    assert sale_service.client_name == 'Cliente de ejemplo'
    assert sale_service.client_email == 'cliente@example.com'
    assert sale_service.client_id == '1234567890'
    assert sale_service.brand == 'Toyota'
    assert sale_service.model == 'Corolla'
    assert sale_service.year == 2022
    assert sale_service.color == 'Azul'
    assert sale_service.plate_number == 'ABC123'
    assert sale_service.price == 100.00
    assert sale_service.product_price == 50.00
    assert sale_service.total_price == 150.00
    assert sale_service.sale_date == timezone.now().date()
    assert sale_service.time_date == timezone.now().time()
    assert sale_service.state == 'En proceso'
    assert sale_service.garantia == garantia

@pytest.mark.django_db
def test_invalid_sale_service():
    with pytest.raises(ValidationError):
        Sale_service.objects.create(
            # Missing required fields
        )

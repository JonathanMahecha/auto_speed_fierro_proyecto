from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test

def is_cliente(user):
    return user.groups.filter(name='Cliente').exists()

def is_admin_or_empleado(user):
    return user.groups.filter(name__in=['Administrador', 'Empleado']).exists()

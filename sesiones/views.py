from django.shortcuts import render

from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.shortcuts import render, redirect
from proyecto_gaes5.views import *
#from .forms import RegistrationForm  

from django.contrib.auth.models import Group

import re
from .models import CustomUser
from django.contrib.auth import login as auth_login  # Renombramos la función para evitar conflictos


def user_login(request):

    if request.user.is_authenticated:
        # Si el usuario está autenticado, redirigir a una página específica
        return redirect('Error404')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        
        if user:
            login(request, user)
            messages.success(request, '¡Inicio de sesión exitoso!')
            if user.groups.filter(name='Administrador').exists():
                # Si el usuario es administrador o empleado, redirigir al panel de admin
                return redirect('admin:index')
            elif user.groups.filter(name='Empleado').exists():
                # Si el usuario es administrador o empleado, redirigir al panel de admin
                return redirect('admin:index')
            elif user.groups.filter(name='Cliente').exists():
                # Si el usuario es cliente, redirigir al menú
                return redirect('agendar')
        else:
            messages.error(request, 'Usuario o contraseña incorrectos')

    return render(request, 'login.html')

def registro(request):

    if request.user.is_authenticated:
        # Si el usuario está autenticado, redirigir a una página específica
        return redirect('Error404')
    
    if request.method == 'POST':
        # Extraer datos del formulario HTML
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        identification = request.POST.get('identification')
        cellphone_number = request.POST.get('cellphone_number')
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        password1 = request.POST.get('password1')

        # Realizar validaciones si es necesario

        # Verificar si las contraseñas coinciden
        if password != password1:
            messages.error(request, 'Las contraseñas no coinciden.')
            return render(request, 'registro.html')
        
        if len(password) < 8:
            messages.error(request, 'La contraseña debe tener al menos 8 caracteres.')
            return render(request, 'registro.html',)
        
        if not re.search(r'\d', password):
            messages.error(request, 'La contraseña debe contener al menos un número.')
            return render(request, 'registro.html',)
        
        if not re.search(r'[a-zA-Z]', password):
            messages.error(request, 'La contraseña debe contener al menos una letra.')
            return render(request, 'registro.html',)
        
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            messages.error(request, 'La contraseña debe contener al menos un carácter especial.')
            return render(request, 'registro.html',)

        if len(cellphone_number) < 7 or len(cellphone_number) > 10:
            messages.error(request, 'El número telefónico no es válido')
            return render(request, 'registro.html')

        if len(identification) < 6 or len(identification) > 12:
            messages.error(request, 'El número de identificación no es válido')
            return render(request, 'registro.html')

        # Verificar si el nombre de usuario, email o identificación ya existen
        if CustomUser.objects.filter(username=username).exists():
            messages.error(request, 'El nombre de usuario ya está en uso.')
            return render(request, 'registro.html')
        
        if CustomUser.objects.filter(email=email).exists():
            messages.error(request, 'El email ya está en uso.')
            return render(request, 'registro.html')
        
        if CustomUser.objects.filter(identification=identification).exists():
            messages.error(request, 'La identificación ya está en uso.')
            return render(request, 'registro.html')

        # Realizar la validación de las contraseñas
        if password == password1:
            # Si las contraseñas coinciden, crea el usuario
            user = CustomUser.objects.create_user(
                username=username,
                email=email,
                password=password,
                identification=identification,
                cellphone_number=cellphone_number
            )
            user.first_name = first_name
            user.last_name = last_name
            user.save()

            # Asignar el rol de cliente al usuario
            cliente_group = Group.objects.get(name='Cliente')
            cliente_group.user_set.add(user)

            # Redirige a la página deseada después del registro exitoso
            messages.success(request, '¡Registro exitoso! Ahora puedes iniciar sesión.')
            return redirect('login')  

    return render(request, 'registro.html')

def logout_view(request):
    logout(request)
    messages.success(request, 'Sesión finalizada')
    return redirect('login')

from django.shortcuts import render, redirect
from .forms import SaleProductForm

def crear_venta_producto(request):
    if request.method == 'POST':
        form = SaleProductForm(request.POST)
        if form.is_valid():
            garantia = form.save()
            garantia.enviar_correo_venta_producto()  # Aquí se llama al método para enviar el correo electrónico
            return redirect('pagina_exitosa')  # Redirecciona a una página de éxito o a donde desees
    else:
        form = SaleProductForm()
    return render(request, 'formulario_venta_producto.html', {'form': form})
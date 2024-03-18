from django.contrib import admin
from django.http import HttpResponse
from .models import Sale_service, Producto_requerido_servicio
from .forms import SaleServiceForm
from import_export.admin import ImportExportModelAdmin
from clienteAtencion.models import cite  # Ajusta esto al nombre correcto del modelo
from import_export import resources

from django import forms
from django.utils.translation import gettext_lazy as _

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.platypus import Table, TableStyle
from reportlab.lib import colors

from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image

# Define la función para descargar el reporte PDF de venta de servicio
#generacion pdf de la venta de servicio con los campos de 'ID', 'Nombre servicio', 'Precio', 'Fecha de venta', 'Garantía', 'Cita'

def download_pdf_venta_servicio(self, request, queryset):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="sale_service_report.pdf"'

    # Crear el PDF
    pdf = SimpleDocTemplate(response, pagesize=letter)

    # Definir estilos para el título y el contenido
    styles = getSampleStyleSheet()
    style_title = styles["Title"]
    style_body = styles["BodyText"]

    # Definir el título del reporte
    title = "Reporte de Ventas de Servicios-Auto Speed Fierro"

    # Agregar el logo de la empresa
    logo_path = 'static/img/iconodon.png'  # Ruta de la imagen del logo
    logo = Image(logo_path, width=40, height=25)

    # Crear elementos del PDF
    elements = []

    # Agregar el logo al PDF
    elements.append(logo)

    # Agregar espacio horizontal
    elements.append(Spacer(-2, -2))  # Ajusta el tamaño del espacio horizontal según tus necesidades

    # Agregar título al PDF
    elements.append(Paragraph(title, style_title))

    # Agregar espacio
    elements.append(Spacer(1, 12))

    # Definir las columnas del encabezado del PDF
    headers = ['ID', 'Nombre servicio', 'Precio mano de obra','precio productos','total', 'Fecha de venta', 'Garantía',]

    # Obtener los datos de los objetos Sale_service del queryset y agregarlos a la lista de datos
    data = [headers]
    for obj in queryset:
        data_row = [obj.id, obj.service.nombre, obj.price,obj.product_price,obj.total_price, obj.sale_date, obj.garantia,]  # Ajusta esto si el campo no se llama 'cite'
        data.append(data_row)

    # Crear la tabla con los datos y aplicar estilos
    table = Table(data)
    # Estilo de la tabla
    style_table = TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.blue),
                              ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
                              ('GRID', (0, 0), (-1, -1), 1, colors.black)])
    # table.setStyle(TableStyle([
    #     ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
    #     ('GRID', (0, 0), (-1, -1), 1, colors.black),
    # ]))
    table.setStyle(style_table)
    # Agregar tabla al PDF
    elements.append(table)

    # Construir el PDF
    pdf.build(elements)

    return response

download_pdf_venta_servicio.short_description = 'Descargar reporte PDF de venta servicio'

#funcion para generar los pdf con la información del cliente de la venta de servicio
def download_pdf_venta_servicio_cliente(self, request, queryset):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="venta_servicio_cliente_report.pdf"'

    # Crear el PDF
    pdf = SimpleDocTemplate(response, pagesize=letter)

    # Definir estilos para el título y el contenido
    styles = getSampleStyleSheet()
    style_title = styles["Title"]
    style_body = styles["BodyText"]

    # Definir el título del reporte
    title = "Reporte de Ventas de Servicios información de Clientes-Auto Speed Fierro"

    # Agregar el logo de la empresa
    logo_path = 'static/img/iconodon.png'  # Ruta de la imagen del logo
    logo = Image(logo_path, width=40, height=25)

    # Crear elementos del PDF
    elements = []

    # Agregar el logo al PDF
    elements.append(logo)

    # Agregar espacio horizontal
    elements.append(Spacer(-2, -2))  # Ajusta el tamaño del espacio horizontal según tus necesidades

    # Agregar título al PDF
    elements.append(Paragraph(title, style_title))

    # Agregar espacio
    elements.append(Spacer(1, 12))

    # Definir las columnas del encabezado del PDF
    headers = ['ID', 'Nombre del cliente', 'Email del cliente', 'Identificación del cliente']

    # Obtener los datos de los objetos Sale_service del queryset y agregarlos a la lista de datos
    data = [headers]
    for obj in queryset:
        data_row = [obj.id, obj.client_name, obj.client_email, obj.client_id]
        data.append(data_row)

    # Crear la tabla con los datos y aplicar estilos
    table = Table(data)

    # Estilo de la tabla
    style_table = TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.blue),
                              ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
                              ('GRID', (0, 0), (-1, -1), 1, colors.black)])

    # Aplicar el estilo a la tabla
    table.setStyle(style_table)

    # Agregar tabla al PDF
    elements.append(table)

    # Construir el PDF
    pdf.build(elements)

    return response

download_pdf_venta_servicio_cliente.short_description = 'Descargar reporte PDF cliente'

class Sale_serviceResource(resources.ModelResource):
    class Meta:
        model = Sale_service
        fields = ('id', 'cite','service', 'price', 'product_price', 'total_price', 'sale_date', 'client_name', 'client_email', 'client_id', 'garantia', )

@admin.register(Sale_service)
class Sale_serviceAdmin(ImportExportModelAdmin):
    form = SaleServiceForm
    list_display = ('id','cite', 'service', 'price','product_price','total_price', 'sale_date', 'display_garantia',)  # Ajusta esto si el campo no se llama 'cite'
    def display_garantia(self, obj):
        if obj.garantia is None:
            return "Sin garantía"
        else:
            return obj.garantia
    
    display_garantia.short_description = 'Garantía'  # Esto cambia el encabezado de la columna en el admin
    search_fields = ('service__name',)  # Solo ajusta esto si necesitas buscar en otros campos relacionados
    list_per_page = 5
    exclude = ['client_name', 'client_id', 'brand', 'model', 'year', 'color', 'plate_number', 'notes', 'client_email', 'total_price', 'service', 'price', 'product_price']
    actions = [download_pdf_venta_servicio, download_pdf_venta_servicio_cliente]  # Agrega las acciones necesarias

#generacion pdf de los productos requeridos
def download_pdf_producto_requerido_servicio(self, request, queryset):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="producto_requerido_servicio_report.pdf"'

    # Crear el PDF
    pdf = SimpleDocTemplate(response, pagesize=letter)

    # Definir estilos para el título y el contenido
    styles = getSampleStyleSheet()
    style_title = styles["Title"]
    style_body = styles["BodyText"]

    # Definir el título del reporte
    title = "Reporte de Producto Requerido del Servicio- Auto Speed Fierro"

    # Agregar el logo de la empresa
    logo_path = 'static/img/iconodon.png'  # Ruta de la imagen del logo
    logo = Image(logo_path, width=40, height=25)

    # Crear elementos del PDF
    elements = []

    # Agregar el logo al PDF
    elements.append(logo)

    # Agregar espacio horizontal
    elements.append(Spacer(-2, -2))  # Ajusta el tamaño del espacio horizontal según tus necesidades

    # Agregar título al PDF
    elements.append(Paragraph(title, style_title))

    # Agregar espacio
    elements.append(Spacer(1, 12))

    # Definir las columnas del encabezado del PDF
    headers = ['Producto', 'Cantidad utilizada', 'Fecha']

    # Obtener los datos de los objetos Producto_requerido_servicio del queryset y agregarlos a la lista de datos
    data = [headers]
    for obj in queryset:
        data_row = [obj.product.name, str(obj.quantity_used), str(obj.date)]
        data.append(data_row)

    # Crear la tabla con los datos y aplicar estilos
    table = Table(data)
    
    # Estilo de la tabla
    style_table = TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.blue),
                              ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
                              ('GRID', (0, 0), (-1, -1), 1, colors.black)])

    # Aplicar el estilo a la tabla
    table.setStyle(style_table)

    # Agregar tabla al PDF
    elements.append(table)

    # Construir el PDF
    pdf.build(elements)

    return response

download_pdf_producto_requerido_servicio.short_description = 'Descargar reporte PDF'

class Producto_requerido_servicioResource(resources.ModelResource):
    class Meta:
        model = Producto_requerido_servicio
        fields = ('id', 'product', 'quantity_used', 'date',)

class Producto_requerido_servicioAdminForm(forms.ModelForm):
    class Meta:
        model = Producto_requerido_servicio
        fields = '__all__'

    # def clean_quantity_used(self):
    #     quantity_used = self.cleaned_data['quantity_used']
    #     product = self.cleaned_data.get('product')  # Obtener el producto seleccionado
    #     if product and quantity_used > product.quantity:
    #         raise forms.ValidationError(_('No hay suficiente cantidad en el inventario'))
    #     return quantity_used

    def clean_quantity_used(self):
        quantity_used = self.cleaned_data['quantity_used']
        product = self.cleaned_data.get('product')  # Obtener el producto seleccionado

        if product:
            if quantity_used > product.quantity:
                raise forms.ValidationError(_('No hay suficiente cantidad en el inventario'))
            elif product.quantity < 5:
                raise forms.ValidationError(_('Solo queda la cantidad de reserva en el inventario'))
            elif (product.quantity - quantity_used) < 5:
                raise forms.ValidationError(_('Solo queda la cantidad de reserva en el inventario'))
        return quantity_used

@admin.register(Producto_requerido_servicio)
class Producto_requerido_servicioAdmin(ImportExportModelAdmin):
    form = Producto_requerido_servicioAdminForm
    list_display = ('product', 'quantity_used', 'date', )
    #list_display_links = ('name')
    #list_editable = ('price',)
    search_fields = ('product__name', 'date',)
    #list_filter = ('email',)
    list_per_page = 5
    exclude = []
    actions = [download_pdf_producto_requerido_servicio] 




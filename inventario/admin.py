from django import forms
from django.contrib import admin
from django.utils.html import format_html

from import_export.admin import ImportExportModelAdmin
from import_export import resources

from .models import Category
from .models import Product
from .models import Supplier
from .models import Purchase

from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from django.http import HttpResponse
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image

# class Sale_serviceResource(resources.ModelResource):
#     class Meta:
#         model = Category
#         fields = ('id', 'name', 'description',)

@admin.register(Category)
class CategoryAdmin(ImportExportModelAdmin):
    list_display = ('name', 'description',)
    list_display_links = ('name',)
    #list_editable = ('price',)
    search_fields = ('name',)
    list_filter = ('name',)
    list_per_page = 3

class QuantityStatusFilter(admin.SimpleListFilter):
    title = 'Disponibilidad'
    parameter_name = 'quantity_status'

    def lookups(self, request, model_admin):
        return (
            ('low', 'Por agotarse'),
            ('sufficient', 'Suficiente'),
            ('empty', 'Agotado'),
        )

    def queryset(self, request, queryset):
        if self.value() == 'low':
            return queryset.filter(quantity__lt=6, quantity__gt=0)
        elif self.value() == 'sufficient':
            return queryset.filter(quantity__gte=6)
        elif self.value() == 'empty':
            return queryset.filter(quantity=0)

class ProductResource(resources.ModelResource):
    class Meta:
        model = Product
        fields = ('id', 'name', 'brand', 'description','price', 'quantity', )

# Función para descargar el reporte PDF de Garantía
def download_pdf_producto(self, request, queryset):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="producto_report.pdf"'
    
    # Crear el PDF
    pdf = SimpleDocTemplate(response, pagesize=letter)

    # Definir estilos para el título y el contenido
    styles = getSampleStyleSheet()
    style_title = styles["Title"]
    style_body = styles["BodyText"]

    # Definir el título del reporte
    title = "Reporte de productos- Auto Speed Fierro"
    
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
    headers = ['Nombre', 'Marca', 'Descripción', 'Categoría','Precio', 'Cantidad']

# Obtener los datos de los objetos Garantia del queryset y agregarlos a la lista de datos
    data = [headers]
    for obj in queryset:
        data_row = [
        obj.name,
        str(obj.brand),  # Servicio
        str(obj.description),  # Fecha
        str(obj.category),
        str(obj.price),
        str(obj.quantity)]  # Hora
        data.append(data_row)


    # Crear la tabla con los datos
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

download_pdf_producto.short_description = 'Descargar reporte PDF productos'

@admin.register(Product)
class ProductAdmin(ImportExportModelAdmin):
#class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'brand', 'description', 'category', 'price', 'quantity', 'quantity_status')
    #list_display_links = ('name')
    #list_editable = ('price',)
    search_fields = ('name', 'brand','category__name', 'price', )
    list_filter = ('category', QuantityStatusFilter)
    list_per_page = 10
    actions = [download_pdf_producto]

    def quantity_status(self, obj):
        if obj.quantity < 6 and obj.quantity > 0:
            return format_html('<span style="color:red;">¡Por agotarse!</span>', obj.quantity)
        elif obj.quantity >= 6:
            return 'Suficiente'
        elif obj.quantity == 0:
            return format_html('<span style="color:red;">¡Agotado!</span>', obj.quantity)
    quantity_status.short_description = 'Disponibilidad'

class SupplierResource(resources.ModelResource):
    class Meta:
        model = Supplier
        fields = ('id', 'name', 'email', 'phone_number', )

@admin.register(Supplier)
class SupplierAdmin(ImportExportModelAdmin):
    list_display = ('name', 'email', 'phone_number')
    #list_display_links = ('name')
    #list_editable = ('price',)
    search_fields = ('name', 'email', 'phone_number',)
    list_filter = ('email',)
    list_per_page = 3

class PurchaseResource(resources.ModelResource):
    class Meta:
        model = Purchase
        fields = ('id', 'product', 'supplier', 'quantity', 'unit_price', 'total_price', 'purchase_date', )

# Función para descargar el reporte PDF de compras
def download_pdf_compras(self, request, queryset):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="compras_report.pdf"'
    
    # Crear el PDF
    pdf = SimpleDocTemplate(response, pagesize=letter)

    # Definir estilos para el título y el contenido
    styles = getSampleStyleSheet()
    style_title = styles["Title"]
    style_body = styles["BodyText"]

    # Definir el título del reporte
    title = "Reporte de compras- Auto Speed Fierro"
    
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
    headers = ['Producto', 'Proveedor', 'Cantidad', 'Precio','Precio total', 'Fecha']

# Obtener los datos de los objetos Garantia del queryset y agregarlos a la lista de datos
    data = [headers]
    for obj in queryset:
        data_row = [
        obj.product,
        str(obj.supplier),  # Servicio
        str(obj.quantity),  # Fecha
        str(obj.unit_price),
        str(obj.total_price),
        str(obj.purchase_date)]  # Hora
        data.append(data_row)


    # Crear la tabla con los datos
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

download_pdf_compras.short_description = 'Descargar reporte PDF compras'

@admin.register(Purchase)
class PurchaseAdmin(ImportExportModelAdmin):
    list_display = ('product', 'supplier', 'quantity', 'unit_price', 'total_price', 'purchase_date', )
    #list_display_links = ('name')
    #list_editable = ('price',)
    search_fields = ('product', 'unit_price', 'supplier',)
    #list_filter = ('email',)
    list_per_page = 3
    actions = [download_pdf_compras]
    exclude = ['total_price']  # Excluir el campo total_price del formulario


from django.contrib import admin

from .models import Sale_product
from import_export.admin import ImportExportModelAdmin
from import_export import resources

from django import forms
#from .forms import SaleProductAdminForm
from django.utils.translation import gettext_lazy as _

from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from django.http import HttpResponse
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image

class SaleProductAdminForm(forms.ModelForm):
    class Meta:
        model = Sale_product
        fields = '__all__'

    def clean_quantity_sold(self):
        quantity_sold = self.cleaned_data['quantity_sold']
        product = self.cleaned_data.get('product')  # Obtener el producto seleccionado

        if product:
            if quantity_sold > product.quantity:
                raise forms.ValidationError(_('No hay suficiente cantidad en el inventario'))
            elif product.quantity < 5:
                raise forms.ValidationError(_('Solo queda la cantidad de reserva en el inventario'))
            elif (product.quantity - quantity_sold) < 5 :
                raise forms.ValidationError(_('Solo queda la cantidad de reserva en el inventario'))
        return quantity_sold

class Sale_productResource(resources.ModelResource):
    class Meta:
        model = Sale_product
        fields = ('id', 'product', 'quantity_sold', 'unit_price', 'total_price', 'sale_date', 'client_name', 'client_email', 'client_id', 'garantia',   )

# Función para descargar el reporte PDF de venta de productos
def download_pdf_venta_producto(self, request, queryset):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="venta_producto_report.pdf"'
    
    # Crear el PDF
    pdf = SimpleDocTemplate(response, pagesize=letter)

    # Definir estilos para el título y el contenido
    styles = getSampleStyleSheet()
    style_title = styles["Title"]
    style_body = styles["BodyText"]

    # Definir el título del reporte
    title = "Reporte de venta de productos - Auto Speed Fierro"
    
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
    headers = ['Producto', 'Cantidad', 'precio', 'total','fecha']

# Obtener los datos de los objetos Garantia del queryset y agregarlos a la lista de datos
    data = [headers]
    for obj in queryset:
        data_row = [
        obj.product,
        str(obj.quantity_sold),  # Servicio
        str(obj.unit_price),  # Fecha
        str(obj.total_price),
        str(obj.sale_date),]  # Hora
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

download_pdf_venta_producto.short_description = 'Descargar reporte PDF venta'

@admin.register(Sale_product)
class SaleAdmin(ImportExportModelAdmin):
    form = SaleProductAdminForm
    list_display = ('product', 'quantity_sold', 'unit_price', 'total_price' ,'sale_date', 'client_name', 'client_email', 'client_id', 'display_garantia', )
    def display_garantia(self, obj):
        if obj.garantia is None:
            return "Sin garantía"
        else:
            return obj.garantia
    display_garantia.short_description = 'Garantía'  # Esto cambia el encabezado de la columna en el admin

    #list_display_links = ('name')
    #list_editable = ('price',)
    search_fields = ('product', 'client_name', 'client_email', 'client_id',)
    #list_filter = ('email',)
    list_per_page = 5
    exclude = ['unit_price', 'total_price',]
    actions = [download_pdf_venta_producto]


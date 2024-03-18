from django.contrib import admin
from django.http import HttpResponse
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from .models import Garantia, EstadosGarantia, GarantiaProducto,RevisionGarantiaProducto, RevisionGarantiaServicio,ServicioConGarantia
from import_export import resources
from import_export.admin import ImportExportModelAdmin


@admin.register (RevisionGarantiaServicio)
class RevisionGarantiaServicioAdmin(ImportExportModelAdmin):
    list_display = ('fecha_revision_garantia_servicio', 'detalles_revision_garantia_servicio','cantidad_producto_servicio', 'producto_garantia_servicio','correo_electronico')
    
    
class RevisionGarantiaResource(resources.ModelResource):
    class Meta:
        model = RevisionGarantiaServicio
        fields = ('fecha_revision_garantia_servicio', 'detalles_revision_garantia_servicio','cantidad_producto_servicio', 'producto_garantia_servicio','correo_electronico',)


# Función para descargar el reporte PDF de Garantía
def download_pdf_garantia(self, request, queryset):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="garantia_report.pdf"'
    
    # Crear el PDF
    pdf = SimpleDocTemplate(response, pagesize=letter)

    # Definir estilos para el título y el contenido
    styles = getSampleStyleSheet()
    style_title = styles["Title"]
    style_body = styles["BodyText"]

    # Definir el título del reporte
    title = "Reporte de Garantías- Auto Speed Fierro"
    
    # Agregar el logo de la empresa
    logo_path = 'static/img/iconodon.png'  # Ruta de la imagen del logo
    logo = Image(logo_path, width=40, height=25)

    # Crear elementos del PDF
    elements = []

    # Agregar el logo al PDF
    elements.append(logo)

    # Agregar espacio horizontal
    elements.append(Spacer(-1, -1))  # Ajusta el tamaño del espacio horizontal según tus necesidades

    # Agregar título al PDF
    elements.append(Paragraph(title, style_title))

    # Agregar espacio
    elements.append(Spacer(1, 12))

    # Definir las columnas del encabezado del PDF
    headers = ['Fecha de Vencimiento', 'Código de Garantía', 'Detalles de la Garantía', 'Estado']

    # Obtener los datos de los objetos Garantia del queryset y agregarlos a la lista de datos
    data = [headers]
    for obj in queryset:
        data_row = [str(obj.fecha_vencimiento), str(obj.codigo_garantia), obj.detalles_garantia, str(obj.estados)]
        data.append(data_row)

    # Crear la tabla con los datos
    table = Table(data)

    # Estilo de la tabla
    style_table = TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.blue),
                              ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
                              ('GRID', (0, 0), (-1, -1), 1, colors.gray)])

    # Aplicar el estilo a la tabla
    table.setStyle(style_table)

    # Agregar tabla al PDF
    elements.append(table)

    # Construir el PDF
    pdf.build(elements)

    return response

download_pdf_garantia.short_description = 'Descargar reporte PDF'

# Registro de los modelos en el administrador de Django

@admin.register (Garantia)
class GarantiaAdmin(ImportExportModelAdmin):
    list_display = ('id', 'correo_electronico', 'fecha_vencimiento', 'codigo_garantia', 'detalles_garantia','estados','servicio_con_garantia','revision_garantia_servicio',)
    search_fields = ('detalles_garantia','codigo_garantia',)
    list_editable = ('estados',)
    list_filter = ('fecha_vencimiento', 'estados',) 
    list_per_page = 10
    exclude = ['fecha_vencimiento']
    actions = [download_pdf_garantia]
    
    
class GarantiaResource(resources.ModelResource):
    class Meta:
        model = Garantia
        fields = ('id', 'correo_electronico','fecha_vencimiento', 'codigo_garantia', 'detalles_garantia', 'estados','servicio_con_garantia',)

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context['mostrar_boton_pdf'] = True
        return super().changelist_view(request, extra_context=extra_context)  

@admin.register(EstadosGarantia)
class EstadosGarantiaAdmin(admin.ModelAdmin):
    list_display = ('estados',)

# Acción para descargar el reporte PDF de GarantíaProducto
def download_pdf_garantia_producto(self, request, queryset):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="garantia_producto_report.pdf"'
    
    # Crear el PDF
    pdf = SimpleDocTemplate(response, pagesize=letter)

    # Definir estilos para el título y el contenido
    styles = getSampleStyleSheet()
    style_title = styles["Title"]
    style_body = styles["BodyText"]

    # Definir el título del reporte
    title = "Reporte de Garantías de Productos"
    
    # Agregar el logo de la empresa
    logo_path = 'static/img/iconodon.png'  # Ruta de la imagen del logo
    logo = Image(logo_path, width=40, height=25)

    # Crear elementos del PDF
    elements = []

    # Agregar el logo al PDF
    elements.append(logo)

    # Agregar espacio horizontal
    elements.append(Spacer(-25, -25))  # Ajusta el tamaño del espacio horizontal según tus necesidades

    # Agregar título al PDF
    elements.append(Paragraph(title, style_title))

    # Agregar espacio
    elements.append(Spacer(1, 12))

    # Definir las columnas del encabezado del PDF
    headers = ['Fecha de Vencimiento', 'Código de Garantía', 'Detalles de la Garantía', 'Estado']

    # Obtener los datos de los objetos GarantiaProducto del queryset y agregarlos a la lista de datos
    data = [headers]
    for obj in queryset:
        data_row = [
            str(obj.fecha_vencimiento),
            str(obj.codigo_garantia),
            obj.detalles_garantia,
            str(obj.estados)
        ]
        data.append(data_row)

    # Crear la tabla con los datos
    table = Table(data)

    # Estilo de la tabla
    style_table = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.blue),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ])

    # Aplicar el estilo a la tabla
    table.setStyle(style_table)

    # Agregar tabla al PDF
    elements.append(table)

    # Construir el PDF
    pdf.build(elements)

    return response


#//////////////////////////////////////////////////////////////////////////////////////////////
#garantia productos 

download_pdf_garantia_producto.short_description = 'Descargar reporte PDF'

@admin.register (GarantiaProducto)
class GarantiaProductoAdmin(ImportExportModelAdmin):
    list_display = ('id', 'correo_electronico','fecha_vencimiento', 'codigo_garantia', 'detalles_garantia', 'estados', 'revision_garantia',)
    search_fields = ('detalles_garantia','codigo_garantia',)
    list_editable = ('estados',)
    list_filter = ('fecha_vencimiento', 'estados',) 
    list_per_page = 10
    exclude = ['fecha_vencimiento']
    actions = [download_pdf_garantia_producto]


class GarantiaProductoResource(resources.ModelResource):
    class Meta:
        model = GarantiaProducto
        fields = ('id', 'correo_electronico','fecha_vencimiento', 'codigo_garantia', 'detalles_garantia', 'estados',)
        
        
    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context['mostrar_boton_pdf'] = True
        return super().changelist_view(request, extra_context=extra_context)

@admin.register (RevisionGarantiaProducto)
class RevisionGarantiaProductoAdmin(ImportExportModelAdmin):
    list_display = ('fecha_revision_garantia', 'detalles_revision_garantia','cantidad', 'producto_garantia','correo_electronico')
    
    

class RevisionGarantiaProductoResource(resources.ModelResource):
    class Meta:
        model = RevisionGarantiaProducto
        fields = ('fecha_revision_garantia', 'detalles_revision_garantia','cantidad', 'producto_garantia','correo_electronico',)
        
@admin.register (ServicioConGarantia)
class ServicioConGarantiaProductoAdmin(ImportExportModelAdmin):
    list_display = ('nombre', 'descripcion', 'price', 'product_price' ,'imagen',)
    
    

# @admin.register (ProductosConGarantia)
# class ProductosConGarantiaAdmin(ImportExportModelAdmin):
#    list_display = ('nombreproducto', 'descripciongarantia','imagen',)
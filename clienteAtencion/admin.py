from django.contrib import admin
# from .models import occupation
# from .models import worker
#from .models import typeOfService
from .models import cite
from .models import comment
from .models import contacts, Service

from import_export.admin import ImportExportModelAdmin
from import_export import resources

from django.http import HttpResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.platypus import Table, TableStyle
from reportlab.lib import colors

class citeResource(resources.ModelResource):
    class Meta:
        model = cite
        fields = ('id', 'user', 'client_name','client_email', 'client_id', 'brand','model', 'year', 'color','plate_number', 'notes', 'service','date', 'time', 'estado',)

@admin.register(cite)
class citeAdmin(ImportExportModelAdmin):
    list_display = ('id', 'user', 'client_name','client_email', 'client_id', 'brand','model', 'year', 'color','plate_number', 'notes', 'service','date', 'time', 'estado',)
    list_display_links = ('client_name',)
    #list_editable = ('price',)
    search_fields = ('client_name','estado',)
    list_filter = ('client_name','estado',)
    list_per_page = 3

class commentResource(resources.ModelResource):
    class Meta:
        model = comment
        fields = ('id', 'headLine', 'cite','description', )

@admin.register(comment)
class commentAdmin(ImportExportModelAdmin):
    list_display = ('headLine', 'cite','description', )
    list_display_links = ('cite',)
    #list_editable = ('price',)
    search_fields = ('headLine',)
    list_filter = ('headLine',)
    list_per_page = 3

class contactsResource(resources.ModelResource):
    class Meta:
        model = contacts
        fields = ('id', 'first_name', 'last_name','email', 'contact', )

@admin.register(contacts)
class contactsAdmin(ImportExportModelAdmin):
    list_display = ('first_name', 'last_name','email', 'contact', )
    list_display_links = ('first_name',)
    #list_editable = ('price',)
    search_fields = ('first_name',)
    list_filter = ('first_name',)
    list_per_page = 3

#admin.site.register(contacts)
    



# def download_pdf_service(self, request, queryset):
#     response = HttpResponse(content_type='application/pdf')
#     response['Content-Disposition'] = 'attachment; filename="services_report.pdf"'

#     pdf = canvas.Canvas(response, pagesize=letter)
#     pdf.setTitle('PDF Report - Services')

#     # Definir las columnas del encabezado del PDF
#     headers = ['Nombre', 'Descripción',]

#     # Obtener los datos de los objetos Service del queryset y agregarlos a la lista de datos
#     data = [headers]
#     for service in queryset:
#         data_row = [service.name, service.description,]
#         data.append(data_row)

#     # Crear la tabla con los datos
#     table = Table(data)
#     table.setStyle(TableStyle([
#         ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
#         ('GRID', (0, 0), (-1, -1), 1, colors.black),
#     ]))

#     # Calcular el ancho y alto del lienzo
#     canvas_width, canvas_height = letter
#     table.wrapOn(pdf, canvas_width, canvas_height)
#     table.drawOn(pdf, 40, canvas_height - len(data) * 20)

#     pdf.save()
#     return response

# download_pdf_service.short_description = "Download selected items as a PDF"

# class ServiceResource(resources.ModelResource):
#     class Meta:
#         model = Service
#         fields = ('id', 'name', 'description', )

# @admin.register(Service)
# class ServiceAdmin(ImportExportModelAdmin):
#     list_display = ('name', 'description', )
#     #list_display_links = ('name')
#     #list_editable = ('price',)
#     search_fields = ('name', 'description', )
#     list_filter = ('name',)
#     list_per_page = 3
#     actions = [download_pdf_service] 

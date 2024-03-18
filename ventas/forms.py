from django import forms
from django.core.exceptions import ValidationError
from .models import Sale_product

class SaleProductForm(forms.ModelForm):
    class Meta:
        model = Sale_product
        fields = ['product', 'quantity_sold', 'unit_price', 'total_price', 'sale_date', 'client_name', 'client_email', 'client_id', 'garantia']
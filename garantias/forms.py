from django import forms
from .models import Garantia, GarantiaProducto, RevisionGarantiaProducto

class GarantiaForm(forms.ModelForm):
    class Meta:
        model = Garantia
        fields = ['fecha_vencimiento', 'detalles_garantia', 'correo_electronico','revision_garantia',]

class GarantiaForm(forms.ModelForm):
    class Meta:
        model = GarantiaProducto
        fields = ['fecha_vencimiento', 'detalles_garantia', 'correo_electronico', 'revision_garantia',]

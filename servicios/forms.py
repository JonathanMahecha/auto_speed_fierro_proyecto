from django import forms
from .models import Sale_service

class SaleServiceForm(forms.ModelForm):
    class Meta:
        model = Sale_service
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Ocultar el campo de garantía si el estado no es "Finalizado"
        if self.instance and self.instance.state != 'Finalizado':
            self.fields['garantia'].widget = forms.HiddenInput()

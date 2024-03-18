from django import forms
from clienteAtencion.models import cite

class CiteForm(forms.ModelForm):
    class Meta:
        model = cite
        fields = ['client_name', 'client_email', 'client_id', 'brand', 'model', 'year', 'color', 'plate_number', 'notes', 'service', 'date', 'time']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(CiteForm, self).__init__(*args, **kwargs)
        if user:
            self.fields['user'].initial = user
            self.fields['user'].widget = forms.HiddenInput()



# from django import forms
# from django.contrib.auth.forms import UserCreationForm
# from django.contrib.auth.models import User
# from django.core.exceptions import ValidationError

# class RegistrationForm(UserCreationForm):
#     username = forms.CharField(max_length=30, required=True)
#     email = forms.EmailField(max_length=254, help_text='Ingrese informacion valida de un correo electronico.')
#     password1 = forms.CharField(label='Contraseña', widget=forms.PasswordInput)
#     password2 = forms.CharField(label='Confirmar contraseña', widget=forms.PasswordInput)

#     class Meta:
#         model = User
#         fields = ['username', 'email', 'password1', 'password2']

#     def clean_password2(self):
#         password1 = self.cleaned_data.get('password1')
#         password2 = self.cleaned_data.get('password2')

#         if password1 and password2 and password1 != password2:
#             raise ValidationError("Las contraseñas no coinciden.")
        
#         return password2

#     def save(self, commit=True):
#         user = super().save(commit=False)
#         user.set_password(self.cleaned_data["password1"])
#         if commit:
#             user.save()
#         return user

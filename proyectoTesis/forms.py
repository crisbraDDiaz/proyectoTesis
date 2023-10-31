from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User # Importa el modelo User de Django
from proyectoTesis.models import UbicacionUsuario,SolicitudRecoleccion,MaterialReciclable
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserChangeForm

class CustomLoginForm(AuthenticationForm):
    remember_me = forms.BooleanField(
        required=False,
        initial=True,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        help_text="Recordar contraseña"
    )

class CustomRegistrationForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Requerido. Ingresa un correo electrónico válido.')

    class Meta:
        model = get_user_model()
        fields = ('username', 'email', 'password1', 'password2','is_staff')

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if get_user_model().objects.filter(username=username).exists():
            raise forms.ValidationError('Este nombre de usuario ya está en uso. Por favor, elige otro.')
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if get_user_model().objects.filter(email=email).exists():
            raise forms.ValidationError('Este correo electrónico ya está en uso. Por favor, elige otro.')
        return email
    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_staff = self.cleaned_data.get('is_staff', False)  # Si es reciclador, is_staff es True (1), de lo contrario, es False (0)
        if commit:
            user.save()
        return user

class UbicacionUsuarioForm(forms.ModelForm):
    class Meta:
        model = UbicacionUsuario
        fields = ['direccion_domicilio','latitud', 'longitud']

class UserProfileForm(UserChangeForm):
    class Meta:
        model = get_user_model()
        fields = ['first_name', 'last_name']

class SolicitudRecicladorForm(forms.ModelForm):
    materiales = forms.ModelMultipleChoiceField(
        queryset=MaterialReciclable.objects.all(),
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'}),
    )
    
    class Meta:
        model = SolicitudRecoleccion
        fields = ['materiales']


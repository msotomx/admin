from django import forms
from django.utils.timezone import now, localtime
from django.forms import DateInput
from core.models import EmpresaDB, Empresa

class MovimientoTimbresFilterForm(forms.Form):
    fecha_inicio = forms.DateField(
        initial=localtime(now()).date(),
        widget=DateInput(attrs={'type': 'date'}, format='%Y-%m-%d'),
        input_formats=['%Y-%m-%d'],
    )
    fecha_fin = forms.DateField(
        initial=localtime(now()).date(),
        widget=DateInput(attrs={'type': 'date'}, format='%Y-%m-%d'),
        input_formats=['%Y-%m-%d'],
    )
    
# core/forms.py
from django import forms
from django.contrib.auth import get_user_model
from django.core.validators import RegexValidator

User = get_user_model()

TIPO_USUARIO_CHOICES = (
    ('A', 'Administrador'),
    ('O', 'Operador'),
    ('V', 'Vendedor'),
)

class CrearUsuarioEmpresaForm(forms.Form):
    username = forms.CharField(
        label="Usuario",
        max_length=30,
        help_text="Solo letras, números y . @ + - _",
        validators=[RegexValidator(
            regex=r'^[\w.@+-]+$',
            message="El username contiene caracteres no permitidos.",
        )],
        widget=forms.TextInput(attrs={"class": "form-control", "autocomplete": "off"})
    )
    first_name = forms.CharField(
        label="Nombre",
        max_length=30,
        widget=forms.TextInput(attrs={"class": "form-control"})
    )
    last_name = forms.CharField(
        label="Apellidos",
        max_length=150,
        required=False,
        widget=forms.TextInput(attrs={"class": "form-control"})
    )
    email = forms.EmailField(
        label="Email (opcional)",
        required=False,
        widget=forms.EmailInput(attrs={"class": "form-control"})
    )
    tipo_usuario = forms.ChoiceField(
        label="Tipo de usuario",
        choices=TIPO_USUARIO_CHOICES,
        initial='O',
        widget=forms.Select(attrs={"class": "form-select"})
    )

    def clean_username(self):
        u = self.cleaned_data["username"].lower().strip()
        # Evitar que usen correos como username si así lo quieres
        if "@" in u:
            raise forms.ValidationError("El username no debe ser un correo.")
        if User.objects.using('default').filter(username__iexact=u).exists():
            raise forms.ValidationError("El username ya existe; elige otro.")
        return u

    def clean_email(self):
        e = self.cleaned_data.get("email", "")
        return e.lower().strip() if e else ""

from django.contrib.auth.forms import PasswordChangeForm

class BootstrapPasswordChangeForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)   
        for name, field in self.fields.items():
            field.widget.attrs.update({"class": "form-control"})
        self.fields["old_password"].widget.attrs.update({"autofocus": "autofocus"})

class EmpresaContactoForm(forms.ModelForm):
    # Declaración explícita del campo fecha
    fecha_renovacion = forms.DateField(
        required=False,
        widget=forms.DateInput(
            attrs={"type": "date", "class": "form-control"},
            format="%Y-%m-%d",     # <-- lo que pinta en el input
        ),
        input_formats=["%Y-%m-%d"], # <-- lo que acepta al hacer POST
    )

    class Meta:
        model = EmpresaDB
        fields = ["fecha_renovacion", "contacto_nombre", "contacto_telefono", "contacto_email"]
        widgets = {
            "contacto_nombre":   forms.TextInput(attrs={"class": "form-control"}),
            "contacto_telefono": forms.TextInput(attrs={"class": "form-control"}),
            "contacto_email":    forms.EmailInput(attrs={"class": "form-control"}),
        }

class EmpresaNumUsuariosForm(forms.ModelForm):
    class Meta:
        model = EmpresaDB
        fields = ["codigo_empresa", "nombre", "num_usuarios"]
        widgets = {
            "codigo_empresa":   forms.TextInput(attrs={"class": "form-control", 'readonly': 'readonly'}),
            "nombre": forms.TextInput(attrs={"class": "form-control", 'readonly': 'readonly'}),
            "num_usuarios":    forms.TextInput(attrs={"class": "form-control"}),
        }

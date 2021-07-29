from django import forms
from .models import Cliente

class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = "__all__"

class EmpresaForm():
    pass

class ArriendoForm():
    pass
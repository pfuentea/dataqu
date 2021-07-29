from django.contrib import admin
from .models import Cliente,Empresa,Arriendo

# Register your models here.
admin.site.register(Cliente)
admin.site.register(Empresa)
admin.site.register(Arriendo)
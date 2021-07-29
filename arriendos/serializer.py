from rest_framework import serializers
from .models import Cliente,Empresa,Arriendo

class ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model= Cliente
        fields = '__all__'

class EmpresaSerializer(serializers.ModelSerializer):
    class Meta:
        model= Empresa
        fields = '__all__'

class ArriendoSerializer(serializers.ModelSerializer):
    class Meta:
        model= Arriendo
        fields = '__all__'
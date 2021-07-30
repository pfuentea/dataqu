from django.db import models

# Create your models here.
class Empresa(models.Model):
    nombre = models.CharField(max_length=40)

    def __str__(self):
        return self.nombre
    
class Cliente(models.Model):
    rut = models.CharField(max_length=40)    
    nombre = models.CharField(max_length=40)
    apellido = models.CharField(max_length=40,default=None, blank=True, null=True)

        
    def __str__(self):
        return self.nombre

class Arriendo(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE)
    costo_diario = models.IntegerField()
    dias = models.IntegerField()
    fecha_arriendo = models.DateField()

   
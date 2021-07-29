from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import serializers, status
from arriendos import serializer
from .serializer import ClienteSerializer,EmpresaSerializer,ArriendoSerializer
from django.http import JsonResponse
from .models import Cliente,Empresa,Arriendo
from django.shortcuts import render,redirect,get_object_or_404
from rest_framework.renderers import JSONRenderer
import json 
from .forms import ClienteForm
from django.db.models import Avg, Count, Min, Sum,F
import datetime
from rest_framework.views import APIView
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt


@api_view(['GET'])
def Index(request):
    api_urls= {
        'Lista':'/cliente-get/',
        'Detalle':'/cliente-det/<str:pk>',
        'Crear':'/cliente-create/',
        'Actualizar':'/cliente-update/<str:pk>',
        'Borrar':'/cliente-delete/<str:pk>',
    }
    return render(request,'index.html')

@api_view(['GET'])
def ClientesList(request):
    clientes = Cliente.objects.all().order_by('-id')   
    serializer = ClienteSerializer(clientes, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def getClientesDet(request,pk):
    clientes = Cliente.objects.get(id=pk)
    serializer = ClienteSerializer(clientes, many=False)
    return Response(serializer.data)


@api_view(['POST'])
def CreaClientes(request):
    serializer = ClienteSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()

    return redirect('../clientes')
    return Response(serializer.data)

@api_view(['POST'])
def ActualizaClientes(request,pk):
    cliente = Cliente.objects.get(id=pk)
    serializer = ClienteSerializer(instance=cliente, data=request.data)

    if serializer.is_valid():
        serializer.save()
    return redirect('../clientes')
    return Response(serializer.data)

@api_view(['GET'])
def BorraClientes(request,pk):
    cliente = Cliente.objects.get(id=pk)
    cliente.delete()
    return redirect('../clientes')
    return Response('Cliente eliminado exitosamente')


''' Empieza el crud de empresas'''
@api_view(['GET'])
def EmpresasList(request):
    empresas = Empresa.objects.all().order_by('-id')    
    serializer = EmpresaSerializer(empresas, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def getEmpresasDet(request,pk):
    empresas = Empresa.objects.get(id=pk)
    serializer = EmpresaSerializer(empresas, many=False)
    return Response(serializer.data)

@api_view(['POST'])
def CreaEmpresas(request):
    serializer = EmpresaSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
    return redirect('../empresas')
    return Response(serializer.data)

@api_view(['POST'])
def ActualizaEmpresas(request,pk):
    empresas = Empresa.objects.get(id=pk)
    serializer = EmpresaSerializer(instance=empresas, data=request.data)

    if serializer.is_valid():
        serializer.save()
    return redirect('../empresas')  
    return Response(serializer.data)

@api_view(['GET'])
def BorraEmpresas(request,pk):
    empresa = Empresa.objects.get(id=pk)
    empresa.delete()
    return redirect('../empresas')
    return Response('Empresa eliminada exitosamente')

''' Empieza el crud de arriendos'''
@api_view(['GET'])
def ArriendosList(request):
    arriendos = Arriendo.objects.all().order_by('-id')    
    serializer = ArriendoSerializer(arriendos, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def getArriendosDet(request,pk):
    arriendos = Arriendo.objects.all()    
    serializer = ArriendoSerializer(arriendos, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def CreaArriendos(request):
    serializer = ArriendoSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
    return redirect('../arriendos')
    return Response(serializer.data)

@api_view(['POST'])
def ActualizaArriendos(request,pk):
    arriendos = Arriendo.objects.get(id=pk)
    serializer = ArriendoSerializer(instance=arriendos, data=request.data)

    if serializer.is_valid():
        serializer.save()
    return redirect('../arriendos')
    return Response(serializer.data)

@api_view(['GET'])
def BorraArriendos(request,pk):
    arriendo = Arriendo.objects.get(id=pk)
    arriendo.delete()
    return redirect('../arriendos')
    return Response('Empresa eliminada exitosamente')

'''Aca terminan el crud'''
def ListaClientes(request):
    clientes = Cliente.objects.all().order_by('-id')   
    serializer = ClienteSerializer(clientes, many=True)
    context={
        "data":clientes
    }   
    
    return render(request,'clientes.html',context)

def ListaEmpresas(request):
    empresas = Empresa.objects.all().order_by('-id')   
    serializer = EmpresaSerializer(empresas, many=True)
    context={
        "data":empresas
    }   
    
    return render(request,'empresas.html',context)

def ListaArriendos(request):
    return render(request,'arriendos.html')

@api_view(['GET'])
def getClientSortByLastName(request):
    clientes = Cliente.objects.all().order_by('apellido')   
    serializer = ClienteSerializer(clientes, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def getClientsSortByRentExpenses(request):
    clientes_gastos = Arriendo.objects.values("cliente").annotate(
        suma_total=Sum( F('dias') * F('costo_diario'))
        ).order_by('-suma_total')
    expensive=clientes_gastos[0]
    return Response(clientes_gastos)

@api_view(['GET'])
def getClientMoreExpenses(request,emp_id=0):
    if emp_id == 0:
        clientes_gastos = Arriendo.objects.values("cliente").annotate(
            suma_total=Sum( F('dias') * F('costo_diario'))
            ).order_by('-suma_total')
    else:
        clientes_gastos = Arriendo.objects.values("cliente").filter(empresa=emp_id).annotate(
            suma_total=Sum( F('dias') * F('costo_diario'))
            ).order_by('-suma_total')

    cliente= Cliente.objects.filter(id=clientes_gastos[0]['cliente']).values('nombre', 'apellido')
    nombre=cliente[0]['nombre']
    apellido=cliente[0]['apellido']
    expensive=clientes_gastos[0]
    expensive['nombre']=nombre+' '+apellido
    return Response(expensive)

@api_view(['GET'])
def getClientLessExpenses(request,emp_id=0):
    if emp_id == 0:
        clientes_gastos = Arriendo.objects.values("cliente").annotate(
        suma_total=Sum( F('dias') * F('costo_diario'))
        ).order_by('suma_total')
    else:
        clientes_gastos = Arriendo.objects.values("cliente").filter(empresa=emp_id).annotate(
        suma_total=Sum( F('dias') * F('costo_diario'))
        ).order_by('suma_total')

    cliente= Cliente.objects.filter(id=clientes_gastos[0]['cliente']).values('nombre', 'apellido')
    nombre=cliente[0]['nombre']
    apellido=cliente[0]['apellido']
    expensive=clientes_gastos[0]
    expensive['nombre']=nombre+' '+apellido
    return Response(expensive)

@api_view(['GET'])
def TotalArriendosMes(request):
    today = datetime.date.today()
    total_arriendos = Arriendo.objects.filter(fecha_arriendo__year=today.year,fecha_arriendo__month=today.month).count()
    return Response(total_arriendos)

@api_view(['GET'])
def newcliente(request):
    return render(request,'cliente_new.html')

@api_view(['GET'])
def updcliente(request,id=0):
    context={
        'id':id
    }
    return render(request,'cliente_edit.html',context)

@api_view(['GET'])
def newempresa(request):
    return render(request,'empresa_new.html')

@api_view(['GET'])
def updempresa(request,id=0):
    context={
        'id':id
    }
    return render(request,'empresa_edit.html',context)
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
        print("pude")
        print(serializer)
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
    #print(arriendos)
    #import pdb; pdb.set_trace()   
    
    #import pdb; pdb.set_trace()   
    serializer = ArriendoSerializer(arriendos, many=True)
    return Response(serializer.data)
    #return JsonResponse(arriendos)


@api_view(['GET'])
def getArriendosDet(request,pk):
    arriendos = Arriendo.objects.get(id=pk)    
    serializer = ArriendoSerializer(arriendos, many=False)
    return Response(serializer.data)

@api_view(['POST'])
def CreaArriendos(request):
    serializer = ArriendoSerializer(data=request.data)
    
    if serializer.is_valid():
        serializer.save()
        print("pude")
        #print(serializer)
    else:
        print("no pude")
        #print(serializer)
    return redirect('../arriendos')
    return Response(serializer.data)

@api_view(['POST'])
def ActualizaArriendos(request,pk):
    arriendos = Arriendo.objects.get(id=pk)
    serializer = ArriendoSerializer(instance=arriendos, data=request.data)

    if serializer.is_valid():
        serializer.save()
    else:
        print("no pude")
        print(serializer)
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
    arriendos = Arriendo.objects.all().order_by('-id')   
    arriendos = [{
        'id': arr.id,
        'cliente': arr.cliente.nombre+' '+arr.cliente.apellido,
        'costo_diario': arr.costo_diario,
        'dias': arr.dias,
        'fecha_arriendo': arr.fecha_arriendo,
        'empresa': arr.empresa.nombre
    } for arr in arriendos]
    context={
        "data":arriendos
    }   
    return render(request,'arriendos.html',context)

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

def getClientLessExpenses2(emp_id=0):
    if emp_id == 0:
        clientes_gastos = Arriendo.objects.values("cliente").annotate(
        suma_total=Sum( F('dias') * F('costo_diario'))
        ).order_by('suma_total')
    else:
        clientes_gastos = Arriendo.objects.values("cliente").filter(empresa=emp_id).annotate(
        suma_total=Sum( F('dias') * F('costo_diario'))
        ).order_by('suma_total')

    cliente= Cliente.objects.filter(id=clientes_gastos[0]['cliente']).values('id')
    id=cliente[0]['id']
    expensive=clientes_gastos[0]
    expensive['id']=id
    return id

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

@api_view(['GET'])
def newarriendo(request):
    return render(request,'arriendo_new.html')

@api_view(['GET'])
def updarriendo(request,id=0):
    context={
        'id':id
    }
    return render(request,'arriendo_edit.html',context)

@api_view(['GET'])
def getCompanyClientSortByName(request):
    empresas = Empresa.objects.all()  
    empresas = [{
        emp.nombre : [
            getClienteByEMpresa(emp.id)
        ]
    }for emp in empresas]
    context={
        "data":empresas
    } 
    print(empresas)
    return JsonResponse(context)

def getClienteByEMpresa(emp_id):
    clientes = Cliente.objects.filter(arriendo__empresa=emp_id).values('rut').order_by('nombre')
    #print(clientes)
    clientes = list(clientes)
    return clientes

@api_view(['GET'])
def getClientsSortByAmount(request,id=0):
    if id == 0:
        clientes_gastos = Arriendo.objects.annotate(
            suma_total=Sum( F('dias') * F('costo_diario'))
            ).order_by('-suma_total').filter(suma_total__gte=40000)
    else:
        clientes_gastos = Arriendo.objects.filter(empresa=id).annotate(
            suma_total=Sum( F('dias') * F('costo_diario'))
            ).order_by('-suma_total').filter(suma_total__gte=40000)
    resultado=[{
        cg.cliente.rut: cg.suma_total
    } for cg in clientes_gastos]
    
    context={
        "data":resultado
    } 
    return JsonResponse(context)

def getCompaniesSortByProfit(request):
    empresa_profit = Arriendo.objects.values("empresa").annotate(
        suma_total=Sum( F('dias') * F('costo_diario'))
        ).order_by('suma_total')
    expensive=empresa_profit[0]
    empresa_profit = list(empresa_profit)
    context={
        "data":empresa_profit
    } 
    return JsonResponse(context)

def getCompaniesWithRentOver1Week(request):
    
    empresas_clientes=Arriendo.objects.filter(dias__gt=6).annotate(cantidad=Count('cliente'))
    print(empresas_clientes)
    
    empresas_clientes = [{
        arr.empresa.nombre : arr.cantidad
    } for arr in empresas_clientes]
    empresas_clientes = list(empresas_clientes)
    print(empresas_clientes)
    context={
        "data":empresas_clientes
    } 
    return JsonResponse(context)


@api_view(['GET'])
def getClientsWithLessExpense(request):
    empresas = Empresa.objects.all()
    empresas = [{
        emp.nombre : getClientLessExpenses2(emp.id)        
    }for emp in empresas]

    empresas = list(empresas)
    print(empresas)
    context={
        "data":empresas
    } 
    return JsonResponse(context)

def newClientRanking():
    pass
from django.contrib import admin
from django.urls import path,include
from . import views
from python_stack.django.django_intro.dataqu import arriendos
from django.conf.urls import  url



urlpatterns = [
    path('',views.Index),

    path('cliente-get/',views.ClientesList,name='cliente-get'),
    path('cliente-det/<str:pk>',views.getClientesDet,name='cliente-det'),
    path('cliente-create/',views.CreaClientes,name='cliente-create'),
    path('cliente-update/<str:pk>',views.ActualizaClientes,name='cliente-update'),
    path('cliente-delete/<str:pk>',views.BorraClientes,name='cliente-delete'),
    path('empresa-get/',views.EmpresasList,name='empresa-get'),
    path('empresa-det/<str:pk>',views.getEmpresasDet,name='empresa-det'),
    path('empresa-create/',views.CreaEmpresas,name='empresa-create'),
    path('empresa-update/<str:pk>',views.ActualizaEmpresas,name='empresa-update'),
    path('empresa-delete/<str:pk>',views.BorraEmpresas,name='empresa-delete'),
    path('arriendo-get/',views.ArriendosList,name='arriendo-get'),
    path('arriendo-det/<str:pk>',views.getArriendosDet,name='arriendo-det'),
    path('arriendo-create/',views.CreaArriendos,name='arriendo-create'),
    path('arriendo-update/<str:pk>',views.ActualizaArriendos,name='arriendo-update'),
    path('arriendo-delete/<str:pk>',views.BorraArriendos,name='arriendo-delete'),
    
    path('cliente-get/',views.ClientesList,name='cliente-get'),
    
    path('clientes-lastname/',views.getClientSortByLastName,name='clientes-lastname'),
    path('clientes-expenses/',views.getClientsSortByRentExpenses,name='clientes-expenses'),
    

    path('arriendos-total/',views.TotalArriendosMes,name='arriendos-total'),
    path('cliente-top/',views.getClientMoreExpenses,name='cliente-top'), 
    path('cliente-top/<int:emp_id>',views.getClientMoreExpenses,name='cliente-top'), 
    path('cliente-bot/',views.getClientLessExpenses,name='cliente-bot'), 
    path('cliente-bot/<int:emp_id>',views.getClientLessExpenses,name='cliente-bot'), 

    path('clientes/',views.ListaClientes,name='clientes'),
    path('empresas/',views.ListaEmpresas,name='empresas'),
    path('arriendos/',views.ListaArriendos,name='arriendos'),

    path('newcliente',views.newcliente,name='newcliente'),
    path('updcliente/<int:id>',views.updcliente,name='updcliente'),
]
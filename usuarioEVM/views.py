# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse
from administradorEVM.models import Users
from administradorEVM.models import Proyectos
from administradorEVM.models import Proyectos_Usuarios
from administradorEVM.models import Actividades

# Create your views here.
# def index(request):
# 	return HttpResponse('Aquí va el login de usuario')
# 	# return render(request, 'usuario.html')
def index(request):
	# return HttpResponse('Aquí va el login')
	return render(request, 'login.html')

# def perfilUsuario(request, dataUser):
def perfilUsuario(request, user_id):
	idUsuario = user_id
	proyectos = Proyectos.objects.filter(id__in=Proyectos_Usuarios.objects.filter(idUsuario=idUsuario).values('idProyecto'))
	allProyectos = {'proyectos' : proyectos, 'idUsuario':idUsuario}
	fragment = loader.render_to_string('fragment_proyectos_programmer.html', allProyectos)
	return render(request, 'perfilUsuario.html', {'fragment':fragment, 'idUsuario':idUsuario})

def detalleProyecto(request):
	idProy = request.GET['idP']
	idUsuario = request.GET['idU']
	flag = request.GET['flag']
	actividades = Actividades.objects.filter(idProyecto=idProy, idResponsable=idUsuario)
	proyecto = Proyectos.objects.get(id=idProy)
	usuarios = Users.objects.filter()
	catalogoUsuarios = [usuarios.count] * 10
	catalogoActividades = [actividades.count] * 10
	for usuario in usuarios:
		catalogoUsuarios[usuario.id]=usuario.nombre

	for actividad in actividades:
		catalogoActividades[actividad.id] = actividad.idActProy
		
	for actividad in actividades:
		if actividad.idDependencia == 0:
			actividad.idDependencia = 'NA'
		else:
			actividad.idDependencia = catalogoActividades[actividad.idDependencia]
		
		actividad.idResponsable = catalogoUsuarios[actividad.idResponsable]
		actividad.idAutoriza = catalogoUsuarios[actividad.idAutoriza]
		actividad.idSoporte = catalogoUsuarios[actividad.idSoporte]
		actividad.idInformar = catalogoUsuarios[actividad.idInformar]

		if actividad.progreso is None:
			actividad.progreso = "0"
		if actividad.tiempoActual is None:
			actividad.tiempoActual = "0"	
	menuProg = loader.render_to_string('fragment_menu_programmer.html',{'flag':flag, 'proyecto':proyecto, 'idUsuario': idUsuario});
	seccion = loader.render_to_string('fragment_detalle_proyecto_programmer.html', {'actividades':actividades, 'proyecto':proyecto, 'usuarios':usuarios, 'menuProg':menuProg})
	return HttpResponse(seccion)

@csrf_exempt
def updateActividad(request):
	idA = request.POST['idA']
	progreso = request.POST['progresoEdit']
	tiempoActual = request.POST['tiempoActualEdit']
	if Actividades.objects.filter(id=idA).update(progreso=progreso,tiempoActual=tiempoActual):
		return HttpResponse('ok')
	else:
		return HttpResponse(status=204)

def estimacionProyecto(request):
	idProy = request.GET['idP']
	idUsuario = request.GET['idU']
	flag = request.GET['flag']
	proyecto = Proyectos.objects.get(id=idProy)
	menuProg = loader.render_to_string('fragment_menu_programmer.html',{'flag':flag, 'proyecto':proyecto, 'idUsuario': idUsuario});
	seccion = loader.render_to_string('fragment_estimacion_proyecto_programmer.html', {'menuProg':menuProg})
	return HttpResponse(seccion)
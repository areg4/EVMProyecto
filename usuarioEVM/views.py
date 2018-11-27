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
import time

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
	catalogoUsuarios = [usuarios.count] * 10000
	catalogoActividades = [actividades.count] * 10000
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
	actividades = Actividades.objects.filter(idProyecto=idProy)
	evActividad = {}
	pvActividad = {}
	etcActividad = {}
	iteracion = time.strftime("%Y-%m-%d")
	evs = 0
	pvs = 0
	tpc = 0
	tp = 0
	acwp = 0
	eac = 0
	etcs = 0
	cpi = 0
	spi = 0
	for actividad in actividades:
		evActividad[actividad.id] = (actividad.progreso/100) * actividad.hrsPlaneadas
		pvActividad[actividad.id] = (actividad.progreso/100) * actividad.hrsPlaneadas
		etcActividad[actividad.id] = abs(actividad.hrsPlaneadas * (1- (actividad.progreso/100)))
		if actividad.fechaEntrega.strftime("%Y-%m-%d") <= iteracion:
			pvs = pvs + actividad.hrsPlaneadas

		tpc = tpc + actividad.hrsPlaneadas
		acwp = acwp + actividad.tiempoActual

	for k,ev in evActividad.items():
		evs = evs + ev
	for k,etc in etcActividad.items():
		etcs = etcs + etc

	eac = abs(acwp) + etcs
	tp = acwp / eac
	tp = tp*100
	tp = abs(tp)
	tp = round(tp,2)
	cpi = evs / acwp
	cpi = cpi*100
	cpi = abs(cpi)
	cpi = round(cpi,2)
	spi = evs / pvs
	spi = spi*100
	spi = abs(spi)
	spi = round(spi,2)
	# print 'evs'
	# print evs
	# print 'pvs'
	# print pvs
	# print 'tpc'
	# print tpc
	# print 'tp'
	# print tp
	# print 'acwp'
	# print acwp
	# print 'eac'
	# print eac
	# print 'etcs'
	# print etcs
	# print 'cpi'
	# print cpi
	# print 'spi'
	# print spi
	menuProg = loader.render_to_string('fragment_menu_programmer.html',{'flag':flag, 'proyecto':proyecto, 'idUsuario': idUsuario})
	seccion = loader.render_to_string('fragment_estimacion_proyecto_programmer.html', {'iteracion':iteracion,'ev':evs,'pv':pvs,'tpc':tpc,'tp':tp,'cpi':cpi,'spi':spi, 'menuProg':menuProg})
	return HttpResponse(seccion)
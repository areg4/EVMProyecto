# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.shortcuts import redirect
from django.urls import reverse
from django.template import loader
from django.http import HttpResponse
from django.http import JsonResponse
from administradorEVM.models import Users
from EVMProject.settings import BASE_DIR
from usuarioEVM import views as usuarioViews
from administradorEVM.models import Proyectos
from administradorEVM.models import Proyectos_Usuarios
from administradorEVM.models import Actividades
import time
from pprint import pprint

# Create your views here.
def index(request):
	# return HttpResponse('Aquí va el login')
	return render(request, 'login.html')

def entrar(request):
	username = request.POST['user']
	password = request.POST['password']
	perfil	= request.POST['perfil']

	# u = Users.objects.filter(username = username, password = password, perfil=perfil).first()
	u = Users.objects.get(username = username, password = password, perfil=perfil)
	
	if u is None:
		return HttpResponse(status=204)
	else:
		# dataUser = {'dataUser' : u}
		dataUser = u
		if u.perfil == 1:
			return perfilAdmin(request, dataUser)
		if u.perfil == 2:
			# return usuarioViews.perfilUsuario(request, dataUser)
			# return redirect('/usuarioEVM/perfilProgramador/', idUser=dataUser.id)
			return redirect(reverse('perfilProgramador', kwargs={"user_id": dataUser.id}))

def perfilAdmin(request, dataUser):
	proyectos = Proyectos.objects.filter(idResponsable = dataUser.id)
	allProyectos = {'proyectos' : proyectos}
	fragment = loader.render_to_string('fragment_proyectos.html', allProyectos)
	return render(request, 'perfilAdmin.html', {'fragment':fragment, 'dataUser':dataUser})

def addProyecto(request):
	usuarios = Users.objects.filter()
	fragment = loader.render_to_string('fragment_add_proyecto.html', {'usuarios':usuarios})
	return HttpResponse(fragment)

@csrf_exempt
def insertarProyecto(request):
	nombreProyecto = request.POST['nombreProyecto']
	resumen = request.POST['resumen']
	objetivoPrincipal = request.POST['objetivoPrincipal']
	objetivos = request.POST['objetivos']
	fechaInicio = request.POST['fechaInicio']
	fechaFinal = request.POST['fechaFinal']
	idResponsable = request.POST['idResponsable']
	# print(fechaFinal)
	if Proyectos.objects.create(nombreProyecto=nombreProyecto,resumen=resumen,objetivoPrincipal=objetivoPrincipal,objetivos=objetivos,fechaInicio=fechaInicio,fechaFinal=fechaFinal,idResponsable=idResponsable) :
		return HttpResponse('ok')
	else:
		return HttpResponse(status=204)

def verEquipo(request):
	# miembros = Users.objects.filter().exclude(perfil=1)
	miembros = Users.objects.filter()
	fragment = loader.render_to_string('fragment_ver_equipo.html', {'miembros':miembros})
	return HttpResponse(fragment)

def verProyectos(request):
	idAdmin = request.GET['idAdmin']
	proyectos = Proyectos.objects.filter(idResponsable=idAdmin)
	allProyectos = {'proyectos' : proyectos}
	fragment = loader.render_to_string('fragment_proyectos.html', allProyectos)
	return HttpResponse(fragment)

def detalleProyecto(request):
	idProy = request.GET['idProy']
	flag = request.GET['flag']
	proyecto =  Proyectos.objects.filter(id=idProy).first()
	usuarios = Users.objects.filter()
	if flag=='scope':
		seccion = loader.render_to_string('fragment_scope_proyecto.html', {'proyecto':proyecto, 'usuarios':usuarios})	
	fragment = loader.render_to_string('fragment_detalle_proyecto.html', {'seccion':seccion, 'proyecto':proyecto, 'flag':flag})
	return HttpResponse(fragment)

def verScope(request):
	idProy = request.GET['idP']
	flag = request.GET['flag']
	proyecto =  Proyectos.objects.filter(id=idProy).first()
	usuarios = Users.objects.filter()
	seccion = loader.render_to_string('fragment_scope_proyecto.html', {'proyecto':proyecto, 'usuarios':usuarios})	
	# fragment = loader.render_to_string('fragment_detalle_proyecto.html', {'seccion':seccion, 'proyecto':proyecto, 'flag':flag})
	return HttpResponse(seccion)

@csrf_exempt
def actualizarScope(request):
	nombreProyecto = request.POST['nombreProyecto']
	resumen = request.POST['resumen']
	objetivoPrincipal = request.POST['objetivoPrincipal']
	objetivos = request.POST['objetivos']
	fechaInicio = request.POST['fechaInicio']
	fechaFinal = request.POST['fechaFinal']
	idResponsable = request.POST['idResponsable']
	idProyecto = request.POST['idP']
	if Proyectos.objects.filter(id=idProyecto).update(nombreProyecto=nombreProyecto,resumen=resumen,objetivoPrincipal=objetivoPrincipal,objetivos=objetivos,fechaInicio=fechaInicio,fechaFinal=fechaFinal,idResponsable=idResponsable):
		return HttpResponse('ok')
	else:
		return HttpResponse(status=204)

def verStakeholders(request):
	idProy = request.GET['idP']
	flag = request.GET['flag']
	# usuarios = Users.objects.filter()
	usuarios = Users.objects.filter().exclude(id__in=Proyectos_Usuarios.objects.filter(idProyecto=idProy).values('idUsuario'))
	# idsMiemPro = Proyectos_Usuarios.objects.filter(idProyecto=idProy)
	# miembrosProy = Users.objects.filter(id__in=Proyectos_Usuarios.objects.filter(idProyecto=idProy))
	miembrosProy = Users.objects.raw('SELECT u.*, up.* FROM administradorEVM_users u, administradorEVM_proyectos_usuarios up WHERE u.id = up.idUsuario AND up.idProyecto = %s', [idProy])
	
	seccion = loader.render_to_string('fragment_stakeholders_proyecto.html', {'usuarios':usuarios, 'miembrosProy':miembrosProy})
	return HttpResponse(seccion)

@csrf_exempt
def addMiembroStake(request):
	idProyecto = request.POST['idP']
	idUsuario = request.POST['idMiembro']
	tiempoAsignado = request.POST['tiempoAsig']
	if Proyectos_Usuarios.objects.create(idProyecto=idProyecto,idUsuario=idUsuario,tiempoAsignado=tiempoAsignado) :
		return HttpResponse('ok')
	else:
		return HttpResponse(status=204)

@csrf_exempt
def quitarMiembroStake(request):
	idProyecto = request.POST['idP']
	idUsuario = request.POST['idU']
	if Proyectos_Usuarios.objects.filter(idProyecto=idProyecto,idUsuario=idUsuario).delete() :
		return HttpResponse('ok')
	else:
		return HttpResponse(status=204)


def verMatrix(request):
	idProy = request.GET['idP']
	flag = request.GET['flag']
	actividades = Actividades.objects.filter(idProyecto=idProy)
	actividadesNE = Actividades.objects.filter(idProyecto=idProy)
	usuarios = Users.objects.filter(id__in=Proyectos_Usuarios.objects.filter(idProyecto=idProy).values('idUsuario'))
	catalogoUsuarios = [usuarios.count] * 1000
	catalogoActividades = [actividades.count] * 1000
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

	miLista = zip(actividades, actividadesNE)	

	seccion = loader.render_to_string('fragment_matrix_proyecto.html', {'actividades':actividades, 'usuarios':usuarios, 'actividadesNE':actividadesNE, 'miLista':miLista})
	return HttpResponse(seccion)

@csrf_exempt
def addActividad(request):
	idActProy = request.POST['idTarea']
	idDependencia = request.POST['idDependencia']
	fechaEntrega = request.POST['fechaEntrega']
	descripcion = request.POST['descripcion']
	comentario = request.POST['comentario']
	hrsPlaneadas = request.POST['hrsPlaneadas']
	idResponsable = request.POST['idResponsable']
	idAutoriza = request.POST['idAutoriza']
	idSoporte = request.POST['idSoporte']
	idInformar = request.POST['idInformar']
	idProyecto = request.POST['idP']
	if Actividades.objects.create(idActProy=idActProy,idDependencia=idDependencia,fechaEntrega=fechaEntrega,descripcion=descripcion,comentario=comentario,hrsPlaneadas=hrsPlaneadas,idResponsable=idResponsable,idAutoriza=idAutoriza,idSoporte=idSoporte,idInformar=idInformar,idProyecto=idProyecto) :
		return HttpResponse('ok')
	else:
		return HttpResponse(status=204)

@csrf_exempt
def eliminarActividad(request):
	# idAct = request.POST.get('idAct')
	idAct = request.POST['idAct']
	if Actividades.objects.filter(id=idAct).delete() :
		return HttpResponse('ok')
	else:
		return HttpResponse(status=204)

@csrf_exempt
def updateActividad(request):
	# print request
	idA = request.POST['idA']
	idActProy = request.POST['idTareaEdit']
	idDependencia = request.POST['idDependenciaEdit']
	fechaEntrega = request.POST['fechaEntregaEdit']
	descripcion = request.POST['descripcionEdit']
	comentario = request.POST['comentarioEdit']
	hrsPlaneadas = request.POST['hrsPlaneadasEdit']
	idResponsable = request.POST['idResponsableEdit']
	idAutoriza = request.POST['idAutorizaEdit']
	idSoporte = request.POST['idSoporteEdit']
	idInformar = request.POST['idInformarEdit']
	progreso = request.POST['progresoEdit']
	tiempoActual = request.POST['tiempoActualEdit']
	if Actividades.objects.filter(id=idA).update(idActProy=idActProy,idDependencia=idDependencia,fechaEntrega=fechaEntrega,descripcion=descripcion,comentario=comentario,hrsPlaneadas=hrsPlaneadas,idResponsable=idResponsable,idAutoriza=idAutoriza,idSoporte=idSoporte,idInformar=idInformar,progreso=progreso,tiempoActual=tiempoActual):
		return HttpResponse('ok')
	else:
		return HttpResponse(status=204)

def verEstimation(request):
	idProy = request.GET['idP']
	flag = request.GET['flag']
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
	seccion = loader.render_to_string('fragment_estimation_proyecto.html', {'iteracion':iteracion,'ev':evs,'pv':pvs,'tpc':tpc,'tp':tp,'cpi':cpi,'spi':spi})
	return HttpResponse(seccion)



def verPerfilMiembro(request):
	idUsuario = request.GET['idM']
	usuario = Users.objects.get(id=idUsuario)
	fragment = loader.render_to_string('fragment_perfil_miembro.html', {'miembro':usuario})
	return HttpResponse(fragment)

@csrf_exempt
def actualizarInfoMiembro(request):
	idUsuario = request.POST['idM']
	nombre = request.POST['nombreMiembro']
	perfil = request.POST['perfil']
	if Users.objects.filter(id=idUsuario).update(nombre=nombre,perfil=perfil):
		return HttpResponse('ok')
	else:
		return HttpResponse(status=204)

@csrf_exempt
def eliminarMiembro(request):
	idUsuario = request.POST['idM']
	if Users.objects.filter(id=idUsuario).delete() :
		return HttpResponse('ok')
	else:
		return HttpResponse(status=204)

def addMiembroEquipo(request):
	fragment = loader.render_to_string('fragment_add_miembro_equipo.html')
	return HttpResponse(fragment)

@csrf_exempt
def altaMiembro(request):
	nombre = request.POST['nombre']
	perfil = request.POST['perfil']
	usuario = request.POST['usuario']
	password = request.POST['pass']
	if Users.objects.create(username=usuario,password=password,nombre=nombre,perfil=perfil) :
		return HttpResponse('ok')
	else:
		return HttpResponse(status=204)
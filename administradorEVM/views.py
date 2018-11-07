# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse
from django.http import JsonResponse
from administradorEVM.models import Users
from EVMProject.settings import BASE_DIR
from usuarioEVM import views as usuarioViews
from administradorEVM.models import Proyectos
from administradorEVM.models import Proyectos_Usuarios

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
			return usuarioViews.perfilUsuario(request, dataUser)

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
	seccion = loader.render_to_string('fragment_matrix_proyecto.html')
	return HttpResponse(seccion)

def verEstimation(request):
	idProy = request.GET['idP']
	flag = request.GET['flag']
	seccion = loader.render_to_string('fragment_estimation_proyecto.html')
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
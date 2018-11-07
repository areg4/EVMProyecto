# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse
from administradorEVM.models import Users
from administradorEVM.models import Proyectos
from administradorEVM.models import Proyectos_Usuarios

# Create your views here.
# def index(request):
# 	return HttpResponse('Aquí va el login de usuario')
# 	# return render(request, 'usuario.html')

def perfilUsuario(request, dataUser):
	proyectos = Proyectos.objects.filter(idResponsable = dataUser.id)
	allProyectos = {'proyectos' : proyectos}
	fragment = loader.render_to_string('fragment_proyectos.html', allProyectos)
	return render(request, 'perfilAdmin.html', {'fragment':fragment, 'dataUser':dataUser})
	return render(request, 'perfilUsuario.html', dataUser)
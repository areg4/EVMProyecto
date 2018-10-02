# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from administradorEVM.models import Users
from EVMProject.settings import BASE_DIR
from usuarioEVM import views as usuarioViews

# Create your views here.
def index(request):
	# return HttpResponse('Aquí va el login')
	return render(request, 'login.html')

def entrar(request):
	username = request.POST['user']
	password = request.POST['password']
	perfil	= request.POST['perfil']

	u = Users.objects.filter(username = username, password = password, perfil=perfil).first()
	
	if u is None:
		return HttpResponse(status=204)
	else:
		dataUser = {'dataUser' : u}
		if u.perfil == 1:
			return perfilAdmin(request, dataUser)
		if u.perfil == 2:
			return usuarioViews.perfilUsuario(request, dataUser)

def perfilAdmin(request, dataUser):
	return render(request, 'perfilAdmin.html', dataUser)
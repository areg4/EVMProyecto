# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def index(request):
	return HttpResponse('Aquí va el login de usuario')
	# return render(request, 'usuario.html')

def perfilUsuario(request, dataUser):
	return render(request, 'perfilUsuario.html', dataUser)
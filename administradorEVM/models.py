# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.

class Users(models.Model):
	"""docstring for Users"""
	username = models.CharField(max_length=150)
	password = models.CharField(max_length=150)
	nombre = models.CharField(max_length=250, blank=True,null=True)
	perfil = models.IntegerField(blank=True, null=True)

class Proyectos(models.Model):
	"""docstring for Proyectos"""
	nombreProyecto = models.CharField(max_length=250, blank=True, null=True)
	resumen = models.TextField(blank=True, null=True)
	objetivoPrincipal = models.CharField(max_length=250, blank=True, null=True)
	objetivos = models.TextField(blank=True, null=True)
	fechaInicio = models.DateField(auto_now=False, blank=True, null=True)
	fechaFinal = models.DateField(auto_now=False, blank=True, null=True)
	idResponsable = models.IntegerField(blank=True, null=True)

class Proyectos_Usuarios(models.Model):
	"""docstring for Proyectos_Usuarios"""
	idProyecto = models.IntegerField(blank=True, null=True)
	idUsuario = models.IntegerField(blank=True, null=True)
	tiempoAsignado = models.FloatField(blank=True, null=True)

class Actividades(models.Model):
	"""docstring for Actividades"""
	idProyecto = models.IntegerField(blank=True, null=True)
	idActProy = models.CharField(max_length=10, blank=True, null=True)
	idDependencia =  models.IntegerField(blank=True, null=True)
	fechaEntrega = models.DateField(auto_now=False, blank=True, null=True)
	descripcion = models.TextField(blank=True, null=True)
	comentario = models.TextField(blank=True, null=True)
	hrsPlaneadas = models.FloatField(blank=True, null=True)
	idResponsable = models.IntegerField(blank=True, null=True)
	idAutoriza = models.IntegerField(blank=True, null=True)
	idSoporte = models.IntegerField(blank=True, null=True)
	idInformar = models.IntegerField(blank=True, null=True)
	progreso = models.FloatField(blank=True, null=True, default=0)
	tiempoActual = models.FloatField(blank=True, null=True, default=0)

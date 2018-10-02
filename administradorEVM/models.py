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


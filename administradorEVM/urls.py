from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^perfil/$', views.entrar, name='perfil'),
    # url(r'^perfil/', views.perfil, name='perfil'),
]
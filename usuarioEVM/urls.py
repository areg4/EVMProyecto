from django.conf.urls import url

from . import views

urlpatterns = [
    # url(r'^$', views.index, name='index'),
    url(r'^perfilProgramador/(?P<user_id>[0-9]+)/$', views.perfilUsuario, name='perfilProgramador'),
    url(r'^detalleProyecto/$', views.detalleProyecto, name='detalleProyecto'),
    url(r'^updateActividad/$', views.updateActividad, name='updateActividad'),
    url(r'^estimacionProyecto/$', views.estimacionProyecto, name='estimacionProyecto'),
]
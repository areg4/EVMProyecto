from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^perfil/$', views.entrar, name='perfil'),
    url(r'^addProyecto/$', views.addProyecto, name='addProyecto'),
    url(r'^verEquipo/$', views.verEquipo, name='verEquipo'),
    url(r'^verProyectos/', views.verProyectos, name='verProyectos'),
    url(r'^detalleProyecto/', views.detalleProyecto, name='detalleProyecto'), 
    url(r'^verScope/$', views.verScope, name='verScope'),
    url(r'^verStakeholders/$', views.verStakeholders, name='verStakeholders'),
    url(r'^verMatrix/$', views.verMatrix, name='verMatrix'),
    url(r'^verEstimation/$', views.verEstimation, name='verEstimation'),

    url(r'^insertarProyecto/$', views.insertarProyecto, name='insertarProyecto'),
    url(r'^actualizarScope/$', views.actualizarScope, name='actualizarScope'),
    url(r'^addMiembroStake/$', views.addMiembroStake, name='addMiembroStake'),
    url(r'^quitarMiembroStake/$', views.quitarMiembroStake, name='quitarMiembroStake'),
    url(r'^verPerfilMiembro/$', views.verPerfilMiembro, name='verPerfilMiembro'),
    url(r'^actualizarInfoMiembro/$', views.actualizarInfoMiembro, name='actualizarInfoMiembro'),
    url(r'^eliminarMiembro/$', views.eliminarMiembro, name='eliminarMiembro'),
    url(r'^addMiembroEquipo/$', views.addMiembroEquipo, name='addMiembroEquipo'),
    url(r'^altaMiembro/$', views.altaMiembro, name='altaMiembro'),

]
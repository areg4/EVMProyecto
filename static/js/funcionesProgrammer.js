jQuery(document).ready(function($){
	$(document).on("click", ".detalleProyectoProgra",function(){
		idU = $(this).attr('dataU-id');
		idP = $(this).attr('data-id');
		// alert(idU+" "+idP);
		parametros = {
			'idP'	: idP,
			'idU'	: idU,
			'flag'	: 'detallePP'
		}
		$.ajax({
			url: '/usuarioEVM/detalleProyecto/',
			type: 'get',
			data: parametros,
			success: function (data) {
				$("#contPrincipal").html(data);
			}
		});
	});

	$(document).on("click", ".btnEditarActividad",function(){
		id = $(this).attr('data-id');
		$(".camposFijos-"+id).css('display', 'none');
		$(".camposEditables-"+id).removeClass('camposEditables');
		$(".editar-guardar").html('Guardar');
		$(".eliminar-cancelar").html('Cancelar');
	});

	$(document).on("click", ".btnCancelarEditActividad",function(){
		id = $(this).attr('data-id');
		$(".camposFijos-"+id).css('display', '');
		$(".camposEditables-"+id).addClass('camposEditables');
		$(".editar-guardar").html('Editar');
		$(".eliminar-cancelar").html('');
	});

	$(document).on("click", ".btnGuardarEditarActividad",function(){
		idAct = $(this).attr('data-id');
		var formData = new FormData();
		formData.append('idA', idAct);
		formData.append('progresoEdit', $("#progresoEdit"+idAct).val());
		formData.append('tiempoActualEdit', $("#tiempoActualEdit"+idAct).val());
		validacion = 0;
		for(inp of formData.entries()){
			inp[1] = inp[1].trim();
			if (inp[1]=="") {
				validacion = 1;
			}
		}		
		if (validacion == 0) {
			$.ajax({
		    	url: '/usuarioEVM/updateActividad/',
		     	type: 'post',
		      	data: formData,
		      	cache: false,
		      	contentType: false,
		      	processData: false,
		      	success:function(data, textStatus, jqXHR) {
		      		if (jqXHR.status == '204') {
		      			$("#txtModal").html("Error al actualizar la actividad");
		      			$("#modal-login").modal();
		      		}
		      		$('.modal-title').html('Actualizar Actividad');
		      		$("#txtModal").html("Actividad Actualizada");
		      		$("#btnCeMoCo").addClass('moUpdActividad');
		      		$("#modal-login").modal();		      			      	
		      	}
		    });
		}else{
			$('.modal-title').html('Error');
			$("#txtModal").html("Faltan campos por rellenar");
		    $("#modal-login").modal();
		}
	});

	$(document).on("click", ".moUpdActividad",function(){
		$("#btnCeMoCo").removeClass('moUpdActividad');
		flag = $("#pDetalle").attr('data-flag');
		idP = $("#pDetalle").attr('data-id');
		idU = $("#pDetalle").attr('data-u');
		parametros = {
			'idP'	: idP,
			'idU'	: idU,
			'flag'	: flag
		}
		$.ajax({
			url: '/usuarioEVM/detalleProyecto/',
			type: 'get',
	      	data: parametros,
			success:function(data){
				$("#contPrincipal").html(data);
			}
		});
	});
	$(document).on("click", "#pProyectos",function(){
		window.location.reload();
	});
	$(document).on("click", "#pDetalle",function(){
		flag = $(this).attr('data-flag');
		idP = $(this).attr('data-id');
		idU = $(this).attr('data-u');
		parametros = {
			'idP'	: idP,
			'idU'	: idU,
			'flag'	: flag
		}
		$.ajax({
			url: '/usuarioEVM/detalleProyecto/',
			type: 'get',
	      	data: parametros,
			success:function(data){
				$("#contPrincipal").html(data);
			}
		});
	});
	$(document).on("click", "#pEstimation",function(){
		flag = $(this).attr('data-flag');
		idP = $(this).attr('data-id');
		idU = $(this).attr('data-u');
		parametros = {
			'idP'	: idP,
			'idU'	: idU,
			'flag'	: flag
		}
		$.ajax({
			url: '/usuarioEVM/estimacionProyecto/',
			type: 'get',
	      	data: parametros,
			success:function(data){
				$("#contPrincipal").html(data);
			}
		});
	});
});
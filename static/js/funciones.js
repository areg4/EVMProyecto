jQuery(document).ready(function($){
	$("#enviar").click(function(){
		var formData = new FormData($("#form-login")[0]);
		$.ajax({
	      url: 'perfil/',
	      type: 'post',
	      data: formData,
	      cache: false,
	      contentType: false,
	      processData: false,
	      success:function(data, textStatus, jqXHR) {
	      	if (jqXHR.status == '204') {
	      		$("#user").addClass('is-invalid');
	      		$("#password").addClass('is-invalid');
	      		// $("#user").val('');
	      		// $("#password").val('');
	      		$("#modal-login").modal();
	      	}
	        // console.log(response);
	        // if (response == 404) {
	        // 	setTimeout(function(){ alert("Hello") }, 3000);
	        	
	        // }
	        // else{
	        // 	// $("#respuesta").html(response);
	        // 	// location.href = response.myURL;
	        // }
	      }
	    });
	});



	$("#mAdEquipo").click(function(){
		if ($("#mAdProyectos").hasClass('selected')) {
			$("#mAdProyectos").removeClass('selected');
		}
		if (!$(this).hasClass('selected')) {
			$(this).addClass('selected');
		}
		$.ajax({
			url: '/administradorEVM/verEquipo/',
			type:'get',
			data: '',
			success:function(data){
				$("#contPrincipal").html(data);
			}
		});
	});

	$("#mAdProyectos").click(function(){
		if ($("#mAdEquipo").hasClass('selected')) {
			$("#mAdEquipo").removeClass('selected');
		}
		if (!$(this).hasClass('selected')) {
			$(this).addClass('selected');
		}
		idAdmin = $(this).attr('data-id');
		parametros = {
			'idAdmin' : idAdmin
		}
		$.ajax({
			url: '/administradorEVM/verProyectos/',
			type: 'get',
			data: parametros,
			success: function(data){
				$("#contPrincipal").html(data);
			}
		});
	});

	$(document).on("click", ".opcionProy",function(){
		flag = $(this).attr('data-flag');
		idP = $(this).attr('data-id');
		if (flag=='scope') {
			url = '/administradorEVM/verScope/';
			$(".opcionProy").removeClass('optSelected');
			$("#oScope").addClass('optSelected');
		}else if (flag=='stakeholders') {
			url = '/administradorEVM/verStakeholders/';
			$(".opcionProy").removeClass('optSelected');
			$("#oStakeholders").addClass('optSelected');
		}else if (flag=='matrix') {
			url = '/administradorEVM/verMatrix/';
			$(".opcionProy").removeClass('optSelected');
			$("#oMatrix").addClass('optSelected');
		}else if (flag=='estimation') {
			url = '/administradorEVM/verEstimation/';
			$(".opcionProy").removeClass('optSelected');
			$("#oEstimation").addClass('optSelected');
		}
		parametros = {
			'idP'	: idP,
			'flag'	: flag
		}
		$.ajax({
			url: url,
			type: 'get',
	      	data: parametros,
			success:function(data){
				$("#contSeccion").html(data);
			}
		});
	});

	
	$(document).on("click", "#enviarFormAddP",function(){
		var formData = new FormData($("#form-add-proyecto")[0]);
		validacion = 0;
		for(inp of formData.entries()){
			inp[1] = inp[1].trim();
			if (inp[1]=="") {
				validacion = 1;
			}
		}
		// console.log(validacion);
		if (validacion == 0) {
			$.ajax({
		    	url: '/administradorEVM/insertarProyecto/',
		     	type: 'post',
		      	data: formData,
		      	cache: false,
		      	contentType: false,
		      	processData: false,
		      	success:function(data, textStatus, jqXHR) {
		      		if (jqXHR.status == '204') {
		      			$("#txtModal").html("Error al crear el proyecto");
		      			$("#modal-login").modal();
		      		}
		      		$('.modal-title').html('Guardado...');
		      		$("#txtModal").html("Proyecto creado");
		      		$("#btnCeMoCo").addClass('accCeMoCo');
		      		$("#modal-login").modal();
		      		console.log(data);
		      			      	
		      	}
		    });
		}else{
			$('.modal-title').html('Error');
			$("#txtModal").html("Faltan campos por rellenar");
		    $("#modal-login").modal();
		}
	});
	
	$(document).on("click", ".accCeMoCo",function(){
		$("#btnCeMoCo").removeClass('accCeMoCo');
		// addProyecto();
		idAdmin = $("#mAdProyectos").attr('data-id');
		parametros = {
			'idAdmin' : idAdmin
		}
		$.ajax({
			url: '/administradorEVM/verProyectos/',
			type: 'get',
			data: parametros,
			success: function(data){
				$("#contPrincipal").html(data);
			}
		});
	});

	$(document).on("click", "#guardarScope",function(){
		var formData = new FormData($("#form-scope")[0]);
		validacion = 0;
		for(inp of formData.entries()){
			inp[1] = inp[1].trim();
			if (inp[1]=="") {
				validacion = 1;
			}
		}
		formData.append('idP', $("#oScope").attr('data-id'));
		// console.log(validacion);
		if (validacion == 0) {
			$.ajax({
		    	url: '/administradorEVM/actualizarScope/',
		     	type: 'post',
		      	data: formData,
		      	cache: false,
		      	contentType: false,
		      	processData: false,
		      	success:function(data, textStatus, jqXHR) {
		      		if (jqXHR.status == '204') {
		      			$("#txtModal").html("Error al actualizar el scope");
		      			$("#modal-login").modal();
		      		}
		      		$('.modal-title').html('Actualizado');
		      		$("#txtModal").html("Scope actualizado");
		      		$("#btnCeMoCo").addClass('moScopeActu');
		      		$("#modal-login").modal();
		      			      	
		      	}
		    });
		}else{
			$('.modal-title').html('Error');
			$("#txtModal").html("Faltan campos por llenar");
		    $("#modal-login").modal();
		}
	});

	$(document).on("click", ".moScopeActu",function(){
		$("#btnCeMoCo").removeClass('moScopeActu');
		// addProyecto();
		flag = $("#oScope").attr('data-flag');
		idP = $("#oScope").attr('data-id');
		parametros = {
			'idP'	: idP,
			'flag'	: flag
		}
		$.ajax({
			url: '/administradorEVM/verScope/',
			type: 'get',
	      	data: parametros,
			success:function(data){
				$("#contSeccion").html(data);
			}
		});
	});

	// stakeholders
	$(document).on("click", "#addMiembro",function(){
		var formData = new FormData($("#form-stakeholders")[0]);
		validacion = 0;
		for(inp of formData.entries()){
			inp[1] = inp[1].trim();
			if (inp[1]=="") {
				validacion = 1;
			}
		}
		formData.append('idP', $("#oStakeholders").attr('data-id'));
		// console.log(validacion);
		if (validacion == 0) {
			$.ajax({
		    	url: '/administradorEVM/addMiembroStake/',
		     	type: 'post',
		      	data: formData,
		      	cache: false,
		      	contentType: false,
		      	processData: false,
		      	success:function(data, textStatus, jqXHR) {
		      		if (jqXHR.status == '204') {
		      			$("#txtModal").html("Error al agregar miembro");
		      			$("#modal-login").modal();
		      		}
		      		$('.modal-title').html('Agregado');
		      		$("#txtModal").html("Miembro agregado");
		      		$("#btnCeMoCo").addClass('moStakeAdd');
		      		$("#modal-login").modal();
		      			      	
		      	}
		    });
		}else{
			$('.modal-title').html('Error');
			$("#txtModal").html("Faltan campos por llenar");
		    $("#modal-login").modal();
		}
	});

	$(document).on("click", ".moStakeAdd",function(){
		$("#btnCeMoCo").removeClass('moStakeAdd');
		// addProyecto();
		flag = $("#oStakeholders").attr('data-flag');
		idP = $("#oStakeholders").attr('data-id');
		parametros = {
			'idP'	: idP,
			'flag'	: flag
		}
		$.ajax({
			url: '/administradorEVM/verStakeholders/',
			type: 'get',
	      	data: parametros,
			success:function(data){
				$("#contSeccion").html(data);
			}
		});
	});

	$(document).on("click", ".quitarMiembro",function(){
		idP = $(this).attr("data-id-p");
		idU = $(this).attr("data-id-m");

		parametros = {
			'idP'  	: idP,
			'idU'	: idU
		}

		$.ajax({
	    	url: '/administradorEVM/quitarMiembroStake/',
	     	type: 'post',
	      	data: parametros,
	      	success:function(data, textStatus, jqXHR) {
	      		if (jqXHR.status == '204') {
	      			$("#txtModal").html("Error al quitar miembro");
	      			$("#modal-login").modal();
	      		}
	      		$('.modal-title').html('Quitado...');
	      		$("#txtModal").html("Miembro quitado");
	      		$("#btnCeMoCo").addClass('moStakeQuit');
	      		$("#modal-login").modal();
	      			      	
	      	}
	    });
	});

	$(document).on("click", ".moStakeQuit",function(){
		$("#btnCeMoCo").removeClass('moStakeQuit');
		// addProyecto();
		flag = $("#oStakeholders").attr('data-flag');
		idP = $("#oStakeholders").attr('data-id');
		parametros = {
			'idP'	: idP,
			'flag'	: flag
		}
		$.ajax({
			url: '/administradorEVM/verStakeholders/',
			type: 'get',
	      	data: parametros,
			success:function(data){
				$("#contSeccion").html(data);
			}
		});
	});

	$(document).on("click", ".miembroInfo",function(){
		idM = $(this).attr("data-id");
		parametros = {
			'idM' : idM
		}
		$.ajax({
			url: '/administradorEVM/verPerfilMiembro/',
			type: 'get',
	      	data: parametros,
			success:function(data){
				$("#contPrincipal").html(data);
			}
		});
	});

	$(document).on("change", ".inputActMiem",function(){
		$("#actualizarPerfilMiembro").removeAttr('disabled');
	});

	$(document).on("click", "#actualizarPerfilMiembro",function(){
		idM = $(this).attr("data-id");
		var formData = new FormData($("#form-actualizar-perfil-miembro")[0]);
		validacion = 0;
		for(inp of formData.entries()){
			inp[1] = inp[1].trim();
			if (inp[1]=="") {
				validacion = 1;
			}
		}
		formData.append('idM', idM);
		// console.log(validacion);
		if (validacion == 0) {
			$.ajax({
		    	url: '/administradorEVM/actualizarInfoMiembro/',
		     	type: 'post',
		      	data: formData,
		      	cache: false,
		      	contentType: false,
		      	processData: false,
		      	success:function(data, textStatus, jqXHR) {
		      		if (jqXHR.status == '204') {
		      			$("#txtModal").html("Error al actualizar miembro");
		      			$("#modal-login").modal();
		      		}
		      		$('.modal-title').html('Actualizado');
		      		$("#txtModal").html("Miembro actualizado");
		      		$("#btnCeMoCo").addClass('moMiemAct');
		      		$("#modal-login").modal();
		      			      	
		      	}
		    });
		}else{
			$('.modal-title').html('Error');
			$("#txtModal").html("Faltan campos por llenar");
		    $("#modal-login").modal();
		}
	});

	$(document).on("click", ".moMiemAct",function(){
		$("#btnCeMoCo").removeClass('moMiemAct');
		// addProyecto();
		idM = $("#actualizarPerfilMiembro").attr('data-id');
		parametros = {
			'idM'	: idM
		}
		$.ajax({
			url: '/administradorEVM/verPerfilMiembro/',
			type: 'get',
	      	data: parametros,
			success:function(data){
				$("#contPrincipal").html(data);
			}
		});
	});

	$(document).on("click", ".eliminarMiembro",function(){
		idM = $(this).attr('data-id');
		parametros = {
			'idM': idM, 
		}
		$.ajax({
	    	url: '/administradorEVM/eliminarMiembro/',
	     	type: 'post',
	      	data: parametros,
	      	success:function(data, textStatus, jqXHR) {
	      		if (jqXHR.status == '204') {
	      			$("#txtModal").html("Error al eliminar miembro");
	      			$("#modal-login").modal();
	      		}
	      		$('.modal-title').html('Eliminando...');
	      		$("#txtModal").html("Miembro eliminado");
	      		$("#btnCeMoCo").addClass('moMiemElim');
	      		$("#modal-login").modal();
	      			      	
	      	}
	    });
	});

	$(document).on("click", ".moMiemElim",function(){
		$("#btnCeMoCo").removeClass('moMiemElim');
		$.ajax({
			url: '/administradorEVM/verEquipo/',
			type:'get',
			data: '',
			success:function(data){
				$("#contPrincipal").html(data);
			}
		});
	});

	$(document).on("click", "#addMiembroEquipo",function(){
		$.ajax({
			url: '/administradorEVM/addMiembroEquipo/',
			type: 'get',
	      	data: '',
			success:function(data){
				$("#contPrincipal").html(data);
			}
		});
	});

	// altaUsuario
	$(document).on("click", "#altaMiembro",function(){
		var formData = new FormData($("#form-add-perfil-miembro")[0]);
		validacion = 0;
		for(inp of formData.entries()){
			inp[1] = inp[1].trim();
			if (inp[1]=="") {
				validacion = 1;
			}
		}
		// console.log(validacion);
		if (validacion == 0) {
			$.ajax({
		    	url: '/administradorEVM/altaMiembro/',
		     	type: 'post',
		      	data: formData,
		      	cache: false,
		      	contentType: false,
		      	processData: false,
		      	success:function(data, textStatus, jqXHR) {
		      		if (jqXHR.status == '204') {
		      			$("#txtModal").html("Error al dar de alta al miembro");
		      			$("#modal-login").modal();
		      		}
		      		$('.modal-title').html('Alta');
		      		$("#txtModal").html("Miembro agregado");
		      		$("#btnCeMoCo").addClass('moAltMiembro');
		      		$("#modal-login").modal();
		      		console.log(data);
		      			      	
		      	}
		    });
		}else{
			$('.modal-title').html('Error');
			$("#txtModal").html("Faltan campos por rellenar");
		    $("#modal-login").modal();
		}
	});

	$(document).on("click", ".moAltMiembro",function(){
		$("#btnCeMoCo").removeClass('moAltMiembro');
		$.ajax({
			url: '/administradorEVM/verEquipo/',
			type:'get',
			data: '',
			success:function(data){
				$("#contPrincipal").html(data);
			}
		});
	});
});

function addProyecto(){
	$.ajax({
		url: '/administradorEVM/addProyecto/',
		type: 'get',
      	data: '',
		success:function(data){
			$("#contPrincipal").html(data);
		}
	});
}

function detalleProyecto(elemento){
	idProy = elemento.getAttribute('data-id');
	parametros = {
		'idProy'	: idProy,
		'flag'		: 'scope'
	}
	$.ajax({
		url: '/administradorEVM/detalleProyecto/',
		type: 'get',
		data: parametros,
		success: function (data) {
			$("#contPrincipal").html(data);
			$("#oScope").addClass('optSelected');
		}
	});
}
function habilitarBoton(elemento){
	$(elemento).removeAttr('disabled');
}

// document.querySelector(".addProyecto").addEventListener('click', ()=>{
// 	alert("Hello");
// 	$.ajax({
// 		url: '/administradorEVM/addProyecto/',
// 		type: 'get',
//       	data: '',
// 		success:function(data){
// 			console.warn(data)
// 			$("#contPrincipal").html(data);
// 		}
// 	});
// })


// document.addEventListener('click', (e)=>{
// 	console.log(e);
// })
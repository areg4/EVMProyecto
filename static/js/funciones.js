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
});
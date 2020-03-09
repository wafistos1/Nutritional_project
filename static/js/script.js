$newItemForm = $('.rating-rate');
$newItemForm.on('click', function (e) {
	e.preventDefault();
	var rate_val = $(this).attr('data-rate')
	var id = $(this).attr('value')


	$.ajax({
		url: "/rating",
		type: 'POST',

		data: {
			csrfmiddlewaretoken: '{{ csrf_token }}',
			rate: rate_val,
			id: id,

		},
		success: function (data) {
			alert(data['data']);
		},
		error: function (data) {
			console.log("ajax call failed!");
		}
	});
});



$fade = $('.form-group');
$fade.on('click', function (e) {
	e.preventDefault();
	var val = $('#grade option:selected').text()
	$('#row-after').children().remove();
	
	$.ajax({
		url: "/resultat",
		type: 'get',

		data: {
			csrfmiddlewaretoken: '{{ csrf_token }}',
			value: val,

		},
		success: function (data) {
	
			let pk_data = data['data'][0]['id']
		$.each( data['best'], function( i, obj ) {
			
			let name = obj['name']
			let images = obj['images']
			let grade = obj['grade']
			let pk_best = obj['id']
			

			
			$('#row-after').append('\
			<div class="col-md-4">\
			<div class="card mb-2 shadow-sm">\
			  <img class="img-responsive" width="80%" height="225" src="'+ images +'"\
				preserveAspectRatio="xMidYMid slice" focusable="false" role="img" aria-label="Placeholder: Thumbnail">\
			  <div class="card-body">\
				<h5>'+ name +'</h5>\
			  </div>\
			  <div class="col align-items-center" name="Sauvegarder">\
				<div class="d-flex justify-content-between align-items-center">\
				  <div class="col-6 col-md-4">\
					<a href=" aliment/'+ pk_best+'/'+ pk_data + '/"><button type="button"\
						class="btn btn-sm btn-outline-primary">Sauvegarder</button></a>\
				  </div>\
					<div class="col align-self-end">\
					  <img class="img-responsive" width="50%" height="50" src="static/img/nutriscore-' + grade + '.svg"\
						 focusable="false" role="img" >\
					</div>\
				</div>\
			  </div>\
			</div>\
		  </div>');
		
			
		  });

		},
		error: function (data) {
			alert("ajax call failed!");
		}
	});
});


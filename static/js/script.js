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
			alert(data.data);
		},
		error: function (data) {
			console.log("ajax call failed!");
		}
	});
});



		
	



$fade = $('#btn-filter');
$('#btn-filter').on('click', function (e) {
	e.preventDefault();
	var grade = $('#grade').val();
	var categorie = $('#categorie').val();
	var rating = $('#rating').val();
	$('#row-after').children().remove();
	// alert( 'rating: ' + rating + ' grade: ' + grade+ ' categorie: ' + categorie );

	$.ajax({
		url: "/filter",
		type: 'get',

		data: {
			csrfmiddlewaretoken: '{{ csrf_token }}',

			'grade': grade,
			'categorie': categorie,
			'rating': rating,


		},
		success: function (response) {
			var html = '';

			$.each(response['best_product'], function (index, item) {
				html += ' <tr>' + '<td>' + item.id + '</td>' + '<td>' + item.name + '</td>' + '<td>' + item.grade + '</td>' + '</tr>'; 
				
			});

			$('.row-after').children().remove();	  
			  
				// $('.row-after').html(html );
				$(document).ready(function() {
					$('.row-after').DataTable( {
						ajax: html,
						columns: [
							{ data: "name" },
							{ data: "position" },
							{ data: "office" },
							{ data: "extn" },
							{ data: {
								_:    "start_date.display",
								sort: "start_date.timestamp"
							} },
							{ data: "salary" }
						]
					} );
				} );

		},
		error: function (data) {
			alert("ajax call failed!");
		}
	});




});







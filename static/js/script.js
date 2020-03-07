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



$fade = $('.form-control');
$fade.on('click', function (e) {
	e.preventDefault();
	var val = $('#grade option:selected').text()
	$('#row-remove').children().remove();
	
	$.ajax({
		url: "/resultat",
		type: 'get',

		data: {
			csrfmiddlewaretoken: '{{ csrf_token }}',
			value: val,

		},
		success: function (data) {
		alert(data[1]);q

		},
		error: function (data) {
			console.log("ajax call failed!");
		}
	});
});


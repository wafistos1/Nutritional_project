	  $newItemForm = $('.rating-rate');
	  $newItemForm.on('click', function(e) {
		e.preventDefault();
		var  rate_val = $(this).attr('data-rate')
		var  id = $(this).attr('value')
		
		
		$.ajax({
			url: "/rating",
			type: 'POST',
			
			data: {
				csrfmiddlewaretoken: '{{ csrf_token }}',
				rate:rate_val,
				id: id,
				
			},
			success: function(data) {
				alert(data);
			},
			error: function(data) {
				console.log("ajax call failed!");
			}
		  });
	  });



$(document).ready(function () {
	var personsTable = $("#persons_table");
	
	var addPersonToTable = function(person) {
		personsTable.append(
		 '<tr data-personUrl="' + person._links.self.href + '">' +
		 '<td>' +
		 '<span class="innoedit firstName">' + person.firstName + '</span>' +
		 '<input class="inedit firstName"/>' +
		 '</td>' + 
		 '<td>' + 
		 '<span class="innoedit lastName">' + person.lastName + '</span>' +
		 '<input class="inedit lastName"/>' +
		 '</td>' +
		 '<td>' +
		 '<span class="innoedit phone">' + person.phone + '</span>' +
		 '<input class="inedit phone"/>' +
		 '</td>' +
		 '<td>' +
		 '<span class="innoedit room">' + person.room + '</span>' +
		 '<input class="inedit room"/>' +
		 '</td>' +
		 '<td>' +
		 '  <button class="btn btn-sm btn-warning edit innoedit">Edit</button>' +  
		 '  <button class="btn btn-sm btn-danger delete innoedit">Delete</button>' + 
		 '  <button class="btn btn-sm btn-danger update inedit">Update</button>' +  
		 '  <button class="btn btn-sm btn-success cancel inedit">Cancel</button>' + 
		 '</td>' + 
		 '</tr>'
		);
	}
	
	$.ajax({
		type: 'GET',
		url: '/persons',
		success: function(data) {
			$.each(data._embedded.persons, function(i, person) {
				addPersonToTable(person);
			}); 
		},
		error: function() {
			alert("Error loading data!");
		}
	});
	
	personsTable.delegate("button.delete", "click", function() {
		row = $(this).closest("tr");
		$.ajax({
			type: 'DELETE',
			url: $(row).attr('data-courseurl'),
			success: function() {
				row.remove();
			},
			error: function() {
				alert("Can not delete row!");
			}
		});
	});
	
	personsTable.delegate("button.edit", "click", function() {
		row = $(this).closest("tr");
		
		// copy from span to input
		row.find('input.firstName').val( row.find('span.firstName').html() );
		row.find('input.lastName').val( row.find('span.lastName').html() );
		row.find('input.phone').val( row.find('span.phone').html() );
		row.find('input.room').val( row.find('span.room').html() );

		
		row.addClass("inedit");
	});
	
	personsTable.delegate("button.cancel", "click", function() {
		$(this).closest("tr").removeClass('inedit');
	});
	
	personsTable.delegate("button.update", "click", function() {
		row = $(this).closest("tr");
		
		// get input values
		var firstName = row.find('input.firstName').val();
		var lastName= row.find('input.lastName').val();
		var phone= row.find('input.phone').val();
		var room= row.find('input.room').val();
		var personData = {
				firstName: firstName,
                lastName: lastName,
                phone: phone,
                room: room
		};
		
		$.ajax({
			type: 'PUT',
			url: $(row).attr('data-personurl'),
			contentType: "application/json; charset=utf-8",
			dataType: "json",
			data: JSON.stringify(personData),
			success: function() {
				row.find('span.firstName').html(firstName);
				row.find('span.lastName').html(lastName);
				row.find('span.phone').html(phone);
				row.find('span.room').html(room);

			},
			error: function() {
				alert("Can not update!");
			}
			
		});
		
		row.removeClass("inedit");
	});
	
	$("#saveNewPersonBtn").on("click", function() {
		var firstName = $("#formPersonFirstName").val();
		var lastName = $("#formPersonLastName").val();
		var phone = $("#formPersonPhone").val();
		var room = $("#formPersonRoom").val();
		var personData = {
				firstName: firstName,
				lastName: lastName,
				phone: phone,
				room: room
		};
	
		$.ajax({
			type: 'POST',
			url: '/persons',
			contentType: "application/json; charset=utf-8",
			dataType: "json",
			data: JSON.stringify(personData),
			success: function(person) {
				addPersonToTable(person);
			},
			error: function() {
				alert("Can not create new person!");
			}
		});
		$("#newPersonModal").modal('hide');
	});
});
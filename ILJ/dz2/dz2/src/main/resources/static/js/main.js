$(document).ready(function () {
	var coursesTable = $("#courses_table");

	var personsDropdown = function(person) {

	}

	var addCourseToTable = function(course) {
		coursesTable.append(
		 '<tr data-courseUrl="' + course._links.self.href + '">' + 
		 '<td>' +
		 '<span class="innoedit name">' + course.name + '</span>' +
		 '<input class="inedit name"/>' +
		 '</td>' + 
		 '<td>' + 
		 '<span class="innoedit description">' + course.description + '</span>' +
		 '<input class="inedit description"/>' +
		 '</td>' +
		 '<td>' +
		 '<span class="innoedit teacher">' + course._embedded.teacher.firstName + ' ' + course._embedded.teacher.lastName + '</span>' +
		 '<input class="inedit teacher"/>' +
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
		url: '/courses',
		success: function(data) {
			$.each(data._embedded.courses, function(i, course) {
				addCourseToTable(course);
			}); 
		},
		error: function() {
			alert("Error loading data!");
		}
	});
	
	coursesTable.delegate("button.delete", "click", function() {
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
	
	coursesTable.delegate("button.edit", "click", function() {
		row = $(this).closest("tr");

		row.find('input.name').val( row.find('span.name').html() );
		row.find('input.description').val( row.find('span.description').html() );


		row.addClass("inedit");
	});
	
	coursesTable.delegate("button.cancel", "click", function() {
		$(this).closest("tr").removeClass('inedit');
	});
	
	coursesTable.delegate("button.update", "click", function() {
		row = $(this).closest("tr");
		
		// get input values
		var name = row.find('input.name').val();
		var description= row.find('input.description').val();
		var teacher = row.find('input.teacher').val();
		var courseData = {
				name: name,
				description: description,
				teacher: teacher
		};
		
		$.ajax({
			type: 'PUT',
			url: $(row).attr('data-courseurl'),
			contentType: "application/json; charset=utf-8",
			dataType: "json",
			data: JSON.stringify(courseData),
			success: function() {
				row.find('span.name').html(name);
				row.find('span.description').html(description);
				row.find('span.teacher').html(teacher);
			},
			error: function() {
				alert("Can not update!");
			}
			
		});
		
		row.removeClass("inedit");
	});
	
	$("#saveNewCourseBtn").on("click", function() {
		var name = $("#formCourseName").val();
		var description = $("#formCourseDescription").val();
		var teacher = $("#formCourseTeacher").val();
		var courseData = {
				name: name,
				description: description,
				teacher: teacher
		};
	
		$.ajax({
			type: 'POST',
			url: '/courses',
			contentType: "application/json; charset=utf-8",
			dataType: "json",
			data: JSON.stringify(courseData),
			success: function(course) {
				addCourseToTable(course);
			},
			error: function() {
				alert("Can not create new course!");
			}
		});
		$("#newCourseModal").modal('hide');
	});
});
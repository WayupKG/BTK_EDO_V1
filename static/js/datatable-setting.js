$('document').ready(function(){
	$('#myTable').DataTable({
		scrollCollapse: true,
		autoWidth: false,
		responsive: true,
		columnDefs: [{
			targets: "datatable-nosort",
			orderable: false,
		}],
		"pageLength": 25,
		"language": {
			"info": "_START_ - _END_ из _TOTAL_",
			"infoFiltered":   "(Отфильтровано из _MAX_ документов)",
			searchPlaceholder: "поиск",
			paginate: {
				next: '<i class="fa fa-angle-double-right paginate"></i>',
				previous: '<i class="fa fa-angle-double-left paginate"></i>'
			}
		},
		dom: 'Bfrtip',
		buttons: [
			{extend: 'copyHtml5',text: 'Копировать'}, 'excel', {extend: 'print',
																text: 'Печать',
																autoPrint: true,
																exportOptions: {
																	columns: ':visible',
																},
																customize: function (win) {
																				$(win.document.body).find('table').addClass('display').css('color', '#000');
																				$(win.document.body).find('tr:nth-child(odd) td').each(function(index){$(this).css('color', '#000');});
																				$(win.document.body).find('h1').css('text-align','center').css('color', '#000');
																				$(this).css('color', '#000');
																				}
																			}
        ]
	});

	$('#data-table-export').DataTable({
		scrollCollapse: true,
		autoWidth: false,
		responsive: true,
		columnDefs: [{
			targets: "datatable-nosort",
			orderable: false,
		}],
		"lengthMenu": [[10, 25, 50, -1], [10, 25, 50, "All"]],
		"language": {
			"info": "_START_-_END_ of _TOTAL_ entries",
			searchPlaceholder: "Search",
			paginate: {
				next: '<i class="ion-chevron-right"></i>',
				previous: '<i class="ion-chevron-left"></i>'  
			}
		},

	});

	var table = $('.select-row').DataTable();
	$('.select-row tbody').on('click', 'tr', function () {
		if ($(this).hasClass('selected')) {
			$(this).removeClass('selected');
		}
		else {
			table.$('tr.selected').removeClass('selected');
			$(this).addClass('selected');
		}
	});

	var multipletable = $('.multiple-select-row').DataTable();
	$('.multiple-select-row tbody').on('click', 'tr', function () {
		$(this).toggleClass('selected');
	});
	var table = $('.checkbox-datatable').DataTable({
		'scrollCollapse': true,
		'autoWidth': false,
		'responsive': true,
		"lengthMenu": [[10, 25, 50, -1], [10, 25, 50, "All"]],
		"language": {
			"info": "_START_-_END_ of _TOTAL_ entries",
			searchPlaceholder: "Search",
			paginate: {
				next: '<i class="ion-chevron-right"></i>',
				previous: '<i class="ion-chevron-left"></i>'  
			}
		},
		'columnDefs': [{
			'targets': 0,
			'searchable': false,
			'orderable': false,
			'className': 'dt-body-center',
			'render': function (data, type, full, meta){
				return '<div class="dt-checkbox"><input type="checkbox" name="id[]" value="' + $('<div/>').text(data).html() + '"><span class="dt-checkbox-label"></span></div>';
			}
		}],
		'order': [[1, 'asc']]
	});

	$('#example-select-all').on('click', function(){
		var rows = table.rows({ 'search': 'applied' }).nodes();
		$('input[type="checkbox"]', rows).prop('checked', this.checked);
	});

	$('.checkbox-datatable tbody').on('change', 'input[type="checkbox"]', function(){
		if(!this.checked){
			var el = $('#example-select-all').get(0);
			if(el && el.checked && ('indeterminate' in el)){
				el.indeterminate = true;
			}
		}
	});
});
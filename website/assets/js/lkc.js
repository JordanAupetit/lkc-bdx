$(function() { 

	$('.btn-add-hardware').click(function(){

		var hardware = $(".input-add-hardware").val();
		var option = $(".input-add-option").val();
		var kernel_version = $(".input-add-kernel-version").val();
		var kernel_sub = $(".input-add-kernel-sub").val();

		if (hardware == "" || option == "" || kernel_version == "" || kernel_sub == "") {
			alert("One or more inputs are empty.");
			return;
		}

		if (hardware.search(" ") != -1 || option.search(" ") != -1 
			|| kernel_version.search(" ") != -1 || kernel_sub.search(" ") != -1) {
			alert("One or more inputs have a space character.");
			return;
		}

		$.ajax({
		  	type: "POST",
		  	url: "views/add_hardware.php",
		  	data: { hardware: hardware, option: option, kernel_version: kernel_version, kernel_sub: kernel_sub }
		})
		.done(function( msg ) {
			if (msg == 1) {
				alert("A Hardware / option relation already exist with this name.")
			} else {
				alert("Hardware / Options added with success.");
				$(".input-add-hardware").val("");
				$(".input-add-option").val("");
				$(".input-add-kernel-version").val("");
				$(".input-add-kernel-sub").val("");
			}
		});
	});


	$('.btn-search-hardware').click(function(){
		var hardware_search = $(".input-search-hardware").val()

		if (hardware_search == "") {
			alert("Your search input is empty.");
			return;
		}

		if (hardware_search.search(" ") != -1) {
			alert("Your search input have a space character.");
			return;
		}

		$.ajax({
		  	type: "POST",
		  	url: "views/search.php",
		  	data: { search: "hardware", find: hardware_search }
		})
		.done(function( data ) {
			$(".input-search-hardware").val("")

			if (data == 0){
				$(".div-search-hardware").html("No results for this hardware name.")
			} else {
				$(".div-search-hardware").html(data)
				add_event_click("hardware");
			}
		});
	});

	add_event_click = function(type){
		if (type == "hardware") {
			$(".add-hardware-search-input").click(function(){
				val_input = $(this).parent().find("input").val();
				$(".input-add-hardware").val(val_input);
			});
		}
	};
	

	$('.btn-search-options').click(function(){
		var options_search = $(".input-search-options").val()

		if (options_search == "") {
			alert("Your search input is empty.");
			return;
		}

		if (options_search.search(" ") != -1) {
			alert("Your search input have a space character.");
			return;
		}
	});

});
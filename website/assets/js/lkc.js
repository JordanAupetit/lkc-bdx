$(function() { 

	$('.btn-add-hardware').click(function(){

		var hardware       = $(".input-add-hardware").val();
		var option         = $(".input-add-option").val();
		var kernel_version = $(".input-add-kernel-version").val();
		var kernel_sub     = $(".input-add-kernel-sub").val();

		add_relationship("add", hardware, option, kernel_version, kernel_sub);
	});

	add_relationship = function(type, hardware, option, kernel_version, kernel_sub){
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
			if (type == "add") {
				if (msg == 1) {
					alert("A Hardware / option relation already exist with this name.")
				} else {
					alert("Hardware / Options added with success.");
					//alert("Debug ==> " + msg);
					$(".input-add-hardware").val("");
					$(".input-add-option").val("");
					$(".input-add-kernel-version").val("");
					$(".input-add-kernel-sub").val("");
				}
			} else if (type == "update") {
				alert("This relationship has been updated successfully.");
			}
		});
	};


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
			$(".input-search-hardware").val("");

			if (data == 0){
				$(".div-search-hardware").html("No results for this hardware name.");
			} else {
				$(".div-search-hardware").html(data);
				add_event_click("hardware");
			}
		});
	});


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

		$.ajax({
		  	type: "POST",
		  	url: "views/search.php",
		  	data: { search: "options", find: options_search }
		})
		.done(function( data ) {
			$(".input-search-options").val("");

			if (data == 0){
				$(".div-search-options").html("No results for this option name.");
			} else {
				$(".div-search-options").html(data);
				add_event_click("options");
			}
		});
	});

	$('.btn-search-hardware-options').click(function(){
		var hardware_options_search = $(".input-search-hardware-options").val()

		if (hardware_options_search == "") {
			alert("Your search input is empty.");
			return;
		}

		if (hardware_options_search.search(" ") != -1) {
			alert("Your search input have a space character.");
			return;
		}

		$.ajax({
		  	type: "POST",
		  	url: "views/search.php",
		  	data: { search: "hardware_options", find: hardware_options_search }
		})
		.done(function( data ) {
			$(".input-search-hardware-options").val("");

			if (data == 0){
				$(".div-update-hardware-options").html("No results for this name.");
			} else {
				$(".div-update-hardware-options").html(data);
				add_event_click("hardware_options");
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
		else if (type == "options") {
			$(".add-options-search-input").click(function(){
				var name    = $(this).parent().find(".input-opt-name-result").val();
				var version = $(this).parent().find(".input-opt-version-result").val();
				var sub     = $(this).parent().find(".input-opt-sub-result").val();
				$(".input-add-option").val(name);
				$(".input-add-kernel-version").val(version);
				$(".input-add-kernel-sub").val(sub);
			});
		}
		else if (type == "hardware_options") {

			$(".btn-update-relationship").click(function(){
				var hardware       = $(this).parent().find(".input-update-hardware").val();
				var option         = $(this).parent().find(".input-update-option").val();
				var kernel_version = $(this).parent().find(".input-update-version").val();
				var kernel_sub     = $(this).parent().find(".input-update-sub").val();

				add_relationship("update", hardware, option, kernel_version, kernel_sub);
				delete_relationship(false, $(this).parent());
			});

			$(".btn-remove-relationship").click(function(){
				var cancel = confirm("Do you really want delete this relationship?");

				if (cancel) {
					delete_relationship(true, $(this).parent());
				}
			});
		}
	};

	delete_relationship = function(remove_row, parent){
		var hardware_id = parent.find(".input-update-hardware-id").val();
		var option_id   = parent.find(".input-update-option-id").val();

		$.ajax({
		  	type: "POST",
		  	url: "views/delete_relationship.php",
		  	data: { hardware_id: hardware_id, option_id: option_id }
		})
		.done(function( data ) {
			if(remove_row)
				parent.remove();
		});
	};

});
$(function() { 

    $(".alert-div").hide();

    $(".btn-close-alert").click(function(){
        close_alert($(this));
    });

    $(".btn-help").click(function(){
        $("#modalHelp").modal();
    });

    $(".onglet-search-hardware").click(function(){
        $(".div-update-hardware-option").html("");
    });

    $(".onglet-search-tag").click(function(){
        $(".div-update-tag-option").html("");
    });

    $('#modalHelp').on('show.bs.modal', function (e) {
        configuration = true;
    });

    $('#modalHelp').on('hidden.bs.modal', function (e) {
        configuration = false;
    });

    $('.btn-add-option').click(function(){
        var module          = $(".input-add-module-option").val();
        var option          = $(".input-add-option").val();
        var option_view     = $(".input-add-option-view").val();

        add_relationship_option("add_option", module, option, option_view, null);
    });

    $('.btn-add-hardware').click(function(){

        var module                  = $(".input-add-module-hardware").val();
        var hardware                = $(".input-add-hardware").val();
        var hardware_constructor    = $(".input-add-hardware-constructor").val();

        add_relationship_hardware("add_hardware", module, hardware, hardware_constructor, null);
    });

    $('.btn-add-tag').click(function(){

        var tag             = $(".input-add-tag").val();
        var option          = $(".input-add-option").val();
        var option_view     = $(".input-add-option-view").val();

        add_relationship_tag("add_tag", tag, option, option_view, null);
    });

    $('.btn-search').click(function(){
        search_element("");
    });


    $('.btn-search-tag').click(function(){
        search_element("tag");
    });

    $('.btn-search-option').click(function(){
        search_element("option");
    });


    $('.btn-search-hardware-option').click(function(){
        search_element_in_relation("hardware");
    });


    $('.btn-search-tag-option').click(function(){
        search_element_in_relation("tag");
    });

    search_error_input = function(string){
        if (string == "") {
            alert_lkc("danger", "One or more inputs are empty.");
            return false;
        }

        if (string.search(" ") != -1) {
            alert_lkc("danger", "One or more inputs have a space character.");
            return false;
        }
        return true;
    }

    alert_lkc = function(type, message){
        if (type == "success") {
            $(".alert-div").removeClass("alert-danger alert-success");
            $(".alert-div").addClass("alert-success");
        } else if (type == "danger") {
            $(".alert-div").removeClass("alert-danger alert-success");
            $(".alert-div").addClass("alert-danger");
        }

        $(".alert-div > p").html(message);
        $(".alert-div").show();
    }

    close_alert = function(widget){
        widget.parent().hide();
    }

    add_relationship_option = function(type, module_name, option_name, option_view, parent){
        close_alert($(".btn-close-alert"));
        if (!search_error_input(module_name)) return;
        if (!search_error_input(option_name)) return;
        if (!search_error_input(option_view)) return;

        $.ajax({
              type: "POST",
              url: "views/add_element.php",
              data: { type: type, module_name: module_name, option_name: option_name, option_view: option_view}
        })
        .done(function( msg ) {
            if (msg == 1) {
                alert_lkc("danger", "A Module / Option relation already exist.")
            } else {
                alert_lkc("success", "Module / Option added with success.");

                $(".input-add-module-option").val("");
                $(".input-add-option").val("");
                $(".input-add-option-view").val("");
            }
        });
    };

    add_relationship_hardware = function(type, module_name, hardware_model, hardware_constructor, parent){
        close_alert($(".btn-close-alert"));
        if (!search_error_input(module_name)) return;
        if (!search_error_input(hardware_model)) return;
        if (!search_error_input(hardware_constructor)) return;

        $.ajax({
              type: "POST",
              url: "views/add_element.php",
              data: { type: type, module_name: module_name, hardware_model: hardware_model, hardware_constructor: hardware_constructor}
        })
        .done(function( msg ) {
            if (msg == 1) {
                alert_lkc("danger", "A Module / Hardware relation already exist.")
            } else {
                alert_lkc("success", "Module / Hardware added with success.");

                $(".input-add-module-hardware").val("");
                $(".input-add-hardware").val("");
                $(".input-add-hardware-constructor").val("");
            }
        });
    };


    add_relationship_tag = function(type, tag_name, option_name, option_view, parent){
        close_alert($(".btn-close-alert"));
        if (!search_error_input(tag_name)) return;
        if (!search_error_input(option_name)) return;
        if (!search_error_input(option_view)) return;

        $.ajax({
              type: "POST",
              url: "views/add_element.php",
              data: { type: type, tag_name: tag_name, option_name: option_name, option_view: option_view}
        })
        .done(function( msg ) {
            if (msg == 1) {
                alert_lkc("danger", "A Tag / Option relation already exist.")
            } else {
                alert_lkc("success", "Tag / Option added with success.");

                $(".input-add-tag").val("");
                $(".input-add-option").val("");
                $(".input-add-option-view").val("");
            }
        });
    };


    search_element = function(type){
        close_alert($(".btn-close-alert"));

        var element_search;
        var div_search;

        if (type == "") {
            type = $(".select-search").val();
            element_search = $(".input-search").val();
            div_search = $(".div-search");
        } else {
            element_search = $(".input-search-" + type).val();
            div_search = $(".div-search-" + type);
        }

        if (!search_error_input(element_search)) return;

        $.ajax({
              type: "POST",
              url: "views/search.php",
              data: { search: type, find: element_search }
        })
        .done(function( data ) {
            $(".input-search-" + type).val("");

            if (data == 0){
                div_search.html("No results for this " + type + " name.");
            } else {
                div_search.html(data);
                add_event_click(type);
            }
        });
    }

    search_element_in_relation = function(type){
        close_alert($(".btn-close-alert"));

        var element_options_search = $(".input-search-" + type + "-option").val();
        if (!search_error_input(element_options_search)) return;

        $.ajax({
              type: "POST",
              url: "views/search.php",
              data: { search: type + "_option", find: element_options_search }
        })
        .done(function( data ) {
            $(".input-search-" + type + "-option").val("");

            if (data == 0){
                $(".div-update-" + type + "-option").html("No results for this name.");
            } else {
                $(".div-update-" + type + "-option").html(data);
                add_event_click(type + "_option");
            }
        });
    }

    add_event_click = function(type){
        if (type == "hardware") {
            $(".add-hardware-search-input").click(function(){
                var hardware    = $(this).parent().find(".input-search-hardware-result").val();
                var constructor = $(this).parent().find(".input-search-hardware-constructor-result").val();
                $(".input-add-hardware").val(hardware);
                $(".input-add-hardware-constructor").val(constructor);
            });
        }
        if (type == "tag") {
            $(".add-tag-search-input").click(function(){
                val_input = $(this).parent().find("input").val();
                $(".input-add-tag").val(val_input);
            });
        }
        else if (type == "option") {
            $(".add-option-search-input").click(function(){
                var option    = $(this).parent().find(".input-search-option-result").val();
                var view = $(this).parent().find(".input-search-option-view-result").val();
                $(".input-add-option").val(option);
                $(".input-add-option-view").val(view);
            });
        }
        if (type == "module") {
            $(".add-module-search-input").click(function(){
                val_input = $(this).parent().find("input").val();
                $(".input-add-module").val(val_input);
            });
        }
        else if (type == "hardware_option") {

            $(".btn-update-relationship-hardware").click(function(){
                var hardware       = $(this).parent().find(".input-update-hardware").val();
                var hardware_constructor    = $(this).parent().find(".input-update-hardware-constructor").val();
                var module         = $(this).parent().find(".input-update-module").val();

                add_relationship_hardware("add_hardware", module, hardware, hardware_constructor, null);
                delete_relationship(true, $(this).parent(), "hardware");
            });

            $(".btn-update-relationship-option").click(function(){
                var option         = $(this).parent().find(".input-update-option").val();
                var option_view    = $(this).parent().find(".input-update-option-view").val();
                var module         = $(this).parent().find(".input-update-module").val();

                add_relationship_option("add_option", module, option, option_view, null);
                delete_relationship(true, $(this).parent(), "option");
            });

            $(".btn-remove-relationship-hardware").click(function(){
                var cancel = confirm("Do you really want delete this relationship?");
                if (cancel) delete_relationship(true, $(this).parent(), "hardware");
            });

            $(".btn-remove-relationship-option").click(function(){
                var cancel = confirm("Do you really want delete this relationship?");
                if (cancel) delete_relationship(true, $(this).parent(), "option");
            });
        }
        else if (type == "tag_option") {

            $(".btn-update-relationship").click(function(){
                var tag            = $(this).parent().find(".input-update-tag").val();
                var option         = $(this).parent().find(".input-update-option").val();
                var option_view    = $(this).parent().find(".input-update-option-view").val();

                add_relationship_tag("add_tag", tag, option, option_view, null);
                delete_relationship(true, $(this).parent(), "tag");
            });

            $(".btn-remove-relationship").click(function(){
                var cancel = confirm("Do you really want delete this relationship?");

                if (cancel) {
                    delete_relationship(true, $(this).parent(), "tag");
                }
            });
        }
    };

    delete_relationship = function(remove_row, parent, type){
        close_alert($(".btn-close-alert"));

        if (type == "hardware") {
            var module_name   = parent.find(".input-update-module-name").val();
            var hardware_id = parent.find(".input-update-hardware-id").val();
            $.ajax({
                  type: "POST",
                  url: "views/delete_relationship.php",
                  data: { hardware_id: hardware_id, module_name: module_name }
            })
            .done(function( data ) {
                if(remove_row)
                    parent.remove();
            });   
        } else if (type == "option") {
            var module_name   = parent.find(".input-update-module-name").val();
            var option_id = parent.find(".input-update-option-id").val();
            $.ajax({
                  type: "POST",
                  url: "views/delete_relationship.php",
                  data: { option_id: option_id, module_name: module_name }
            })
            .done(function( data ) {
                if(remove_row)
                    parent.remove();
            });   
        } else if (type == "tag") {
            var tag_name = parent.find(".input-update-tag-name").val();
            var option_id = parent.find(".input-update-option-id").val();
            $.ajax({
                  type: "POST",
                  url: "views/delete_relationship.php",
                  data: { tag_name: tag_name, option_id: option_id }
            })
            .done(function( data ) {
                if(remove_row)
                    parent.remove();
            });
        }
        
    };

});
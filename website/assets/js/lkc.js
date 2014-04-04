$(function() { 

    $(".alert-div").hide();

    $(".btn-close-alert").click(function(){
        close_alert($(this));
    });

    $(".btn-help").click(function(){
        $("#modalHelp").modal();
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

//     add_relationship = function(type, element, constructor, option, kernel_version, kernel_sub, parent){
//         close_alert($(".btn-close-alert"));

//         if (element == "" || option == "" || kernel_version == "" || kernel_sub == "") {
//             alert_lkc("danger", "One or more inputs are empty.");
//             return;
//         }

//         if (element.search(" ") != -1 || option.search(" ") != -1 
//             || kernel_version.search(" ") != -1 || kernel_sub.search(" ") != -1) {
//             alert_lkc("danger", "One or more inputs have a space character.");
//             return;
//         }

//         update = false;

//         if (type == "add_hardware")
//             type = "hardware";
//         else if (type == "add_tag")
//             type = "tag";
//         else if (type == "update_hardware") {
//             type = "hardware";
//             update = true;
//         } else if (type == "update_tag") {
//             type = "tag";
//             update = true;
//         }

//         $.ajax({
//               type: "POST",
//               url: "views/add_element.php",
//               data: { type: type, element: element, constructor: constructor, option: option, kernel_version: kernel_version, kernel_sub: kernel_sub }
//         })
//         .done(function( msg ) {
//             if (type == "hardware" && !update) {
//                 if (msg == 1) {
//                     alert_lkc("danger", "A Hardware / option relation already exist with this name.")
//                 } else {
//                     alert_lkc("success", "Hardware / Options added with success.");
//                     $(".input-add-hardware").val("");
//                     $(".input-add-hardware-constructor").val("");
//                     $(".input-add-option").val("");
//                     $(".input-add-kernel-version").val("");
//                     $(".input-add-kernel-sub").val("");
//                 }
//             } else if (type == "tag" && !update) {
//                 if (msg == 1) {
//                     alert_lkc("danger", "A Tag / option relation already exist with this name.")
//                 } else {
//                     alert_lkc("success", "Tag / Options added with success.");
//                     $(".input-add-tag").val("");
//                     $(".input-add-option").val("");
//                     $(".input-add-kernel-version").val("");
//                     $(".input-add-kernel-sub").val("");
//                 }
//             } else if (update) {
//                 alert_lkc("success", "This relationship has been updated successfully.\n\
// You must search again to see this new relationship.");
//                 parent.remove();
//             }
//         });
//     };


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
                //add_event_click(type + "_option");
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

            $(".btn-update-relationship").click(function(){
                var hardware       = $(this).parent().find(".input-update-hardware").val();
                var constructor    = $(this).parent().find(".input-update-hardware-constructor").val();
                var option         = $(this).parent().find(".input-update-option").val();
                var kernel_version = $(this).parent().find(".input-update-version").val();
                var kernel_sub     = $(this).parent().find(".input-update-sub").val();

                add_relationship("update_hardware", hardware, constructor, option, kernel_version, kernel_sub, $(this).parent());
                delete_relationship(false, $(this).parent(), "hardware");
            });

            $(".btn-remove-relationship").click(function(){
                var cancel = confirm("Do you really want delete this relationship?");

                if (cancel) {
                    delete_relationship(true, $(this).parent(), "hardware");
                }
            });
        }
        else if (type == "tag_option") {

            $(".btn-update-relationship").click(function(){
                var tag            = $(this).parent().find(".input-update-tag").val();
                var option         = $(this).parent().find(".input-update-option").val();
                var kernel_version = $(this).parent().find(".input-update-version").val();
                var kernel_sub     = $(this).parent().find(".input-update-sub").val();

                add_relationship("update_tag", tag, "", option, kernel_version, kernel_sub, $(this).parent(), null);
                delete_relationship(false, $(this).parent(), "tag");
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

        var option_id   = parent.find(".input-update-option-id").val();

        if (type == "hardware") {
            var hardware_id = parent.find(".input-update-hardware-id").val();
            $.ajax({
                  type: "POST",
                  url: "views/delete_relationship.php",
                  data: { hardware_id: hardware_id, option_id: option_id }
            })
            .done(function( data ) {
                if(remove_row)
                    parent.remove();
            });   
        } else if (type == "tag") {
            var tag_id = parent.find(".input-update-tag-id").val();
            $.ajax({
                  type: "POST",
                  url: "views/delete_relationship.php",
                  data: { tag_id: tag_id, option_id: option_id }
            })
            .done(function( data ) {
                if(remove_row)
                    parent.remove();
            });
        }
        
    };

});
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

    $('.btn-add-hardware').click(function(){

        var element        = $(".input-add-hardware").val();
        var option         = $(".input-add-option").val();
        var kernel_version = $(".input-add-kernel-version").val();
        var kernel_sub     = $(".input-add-kernel-sub").val();

        add_relationship("add_hardware", element, option, kernel_version, kernel_sub, null);
    });

    $('.btn-add-tag').click(function(){

        var element        = $(".input-add-tag").val();
        var option         = $(".input-add-option").val();
        var kernel_version = $(".input-add-kernel-version").val();
        var kernel_sub     = $(".input-add-kernel-sub").val();

        add_relationship("add_tag", element, option, kernel_version, kernel_sub, null);
    });

    $('.btn-search-hardware').click(function(){
        search_element("hardware");
    });


    $('.btn-search-tag').click(function(){
        search_element("tag");
    });


    $('.btn-search-options').click(function(){
        search_element("options");
    });


    $('.btn-search-hardware-options').click(function(){
        search_element_in_relation("hardware");
    });


    $('.btn-search-tag-options').click(function(){
        search_element_in_relation("tag");
    });

    alert_lkc = function(message){
        $(".alert-div > p").html(message);
        $(".alert-div").show();
    }

    close_alert = function(widget){
        widget.parent().hide();
    }

    add_relationship = function(type, element, option, kernel_version, kernel_sub, parent){
        close_alert($(".btn-close-alert"));

        if (element == "" || option == "" || kernel_version == "" || kernel_sub == "") {
            alert_lkc("One or more inputs are empty.");
            return;
        }

        if (element.search(" ") != -1 || option.search(" ") != -1 
            || kernel_version.search(" ") != -1 || kernel_sub.search(" ") != -1) {
            alert_lkc("One or more inputs have a space character.");
            return;
        }

        update = false;

        if (type == "add_hardware")
            type = "hardware";
        else if (type == "add_tag")
            type = "tag";
        else if (type == "update_hardware") {
            type = "hardware";
            update = true;
        } else if (type == "update_tag") {
            type = "tag";
            update = true;
        }

        $.ajax({
              type: "POST",
              url: "views/add_element.php",
              data: { type: type, element: element, option: option, kernel_version: kernel_version, kernel_sub: kernel_sub }
        })
        .done(function( msg ) {
            if (type == "hardware" && !update) {
                if (msg == 1) {
                    alert_lkc("A Hardware / option relation already exist with this name.")
                } else {
                    alert_lkc("Hardware / Options added with success.");
                    $(".input-add-hardware").val("");
                    $(".input-add-option").val("");
                    $(".input-add-kernel-version").val("");
                    $(".input-add-kernel-sub").val("");
                }
            } else if (type == "tag" && !update) {
                if (msg == 1) {
                    alert_lkc("A Tag / option relation already exist with this name.")
                } else {
                    alert_lkc("Tag / Options added with success.");
                    $(".input-add-tag").val("");
                    $(".input-add-option").val("");
                    $(".input-add-kernel-version").val("");
                    $(".input-add-kernel-sub").val("");
                }
            } else if (update) {
                alert_lkc("This relationship has been updated successfully.\n\
You must search again to see this new relationship.");
                parent.remove();
            }
        });
    };


    search_element = function(type){
        close_alert($(".btn-close-alert"));

        var element_search = $(".input-search-" + type).val()

        if (element_search == "") {
            alert_lkc("Your search input is empty.");
            return;
        }

        if (element_search.search(" ") != -1) {
            alert_lkc("Your search input have a space character.");
            return;
        }

        $.ajax({
              type: "POST",
              url: "views/search.php",
              data: { search: type, find: element_search }
        })
        .done(function( data ) {
            $(".input-search-" + type).val("");

            if (data == 0){
                $(".div-search-" + type).html("No results for this " + type + " name.");
            } else {
                $(".div-search-" + type).html(data);
                add_event_click(type);
            }
        });
    }

    search_element_in_relation = function(type){
        close_alert($(".btn-close-alert"));

        var element_options_search = $(".input-search-" + type + "-options").val()

        if (element_options_search == "") {
            alert_lkc("Your search input is empty.");
            return;
        }

        if (element_options_search.search(" ") != -1) {
            alert_lkc("Your search input have a space character.");
            return;
        }

        $.ajax({
              type: "POST",
              url: "views/search.php",
              data: { search: type + "_option", find: element_options_search }
        })
        .done(function( data ) {
            $(".input-search-" + type + "-options").val("");

            if (data == 0){
                $(".div-update-" + type + "-options").html("No results for this name.");
            } else {
                $(".div-update-" + type + "-options").html(data);
                add_event_click(type + "_option");
            }
        });
    }

    add_event_click = function(type){
        if (type == "hardware") {
            $(".add-hardware-search-input").click(function(){
                val_input = $(this).parent().find("input").val();
                $(".input-add-hardware").val(val_input);
            });
        }
        if (type == "tag") {
            $(".add-tag-search-input").click(function(){
                val_input = $(this).parent().find("input").val();
                $(".input-add-tag").val(val_input);
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
        else if (type == "hardware_option") {

            $(".btn-update-relationship").click(function(){
                var hardware       = $(this).parent().find(".input-update-hardware").val();
                var option         = $(this).parent().find(".input-update-option").val();
                var kernel_version = $(this).parent().find(".input-update-version").val();
                var kernel_sub     = $(this).parent().find(".input-update-sub").val();

                add_relationship("update_hardware", hardware, option, kernel_version, kernel_sub, $(this).parent());
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

                add_relationship("update_tag", tag, option, kernel_version, kernel_sub, $(this).parent(), null);
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
<?php 
    include 'connectBD.php';

    if(isset($_POST["type"])){

        $type = addslashes($_POST["type"]);
        $hardware_id = -1;
        $option_id = -1;
        $module_name = "";
        $tag_name = "";

        if ($type == "add_option") {
            $option_name = addslashes($_POST["option_name"]);
            $option_view = addslashes($_POST["option_view"]);
            $module_name = addslashes($_POST["module_name"]);

            // OPTION
            insert_option($option_name, $option_view, $connexion, $option_id);

            // MODULE
            insert_module($module_name, $connexion);

            // RELATION
            add_relation_module_option($module_name, $option_id, $connexion);
        }


        if ($type == "add_hardware") {
            $hardware_model         = addslashes($_POST["hardware_model"]);
            $hardware_constructor   = addslashes($_POST["hardware_constructor"]);
            $module_name            = addslashes($_POST["module_name"]);

            // HARDWARE
            insert_hardware($hardware_model, $hardware_constructor, $connexion, $hardware_id);

            // MODULE
            insert_module($module_name, $connexion);

            // // RELATION
            add_relation_module_hardware($module_name, $hardware_id, $connexion);
        }

        if ($type == "add_tag") {
            $option_name = addslashes($_POST["option_name"]);
            $option_view = addslashes($_POST["option_view"]);
            $tag_name = addslashes($_POST["tag_name"]);

            // OPTION
            insert_option($option_name, $option_view, $connexion, $option_id);

            // TAG
            insert_tag($tag_name, $connexion);

            // RELATION
            add_relation_tag_option($tag_name, $option_id, $connexion);
        }
    }


    function insert_module($name, $connexion) {
        $req = $connexion->query("SELECT * FROM module_lkc
                                         WHERE name = '".$name."'");
        $reponse = $req->fetch();
        $nb = $req->rowCount();
        $req->closeCursor();

        if ($nb <= 0) {
            $req = $connexion->prepare('INSERT INTO 
                module_lkc(name) 
                VALUES(:name)');
            $req->execute(array(
                'name' => $name
            ));
            $req->closeCursor();
        }
    }

    function insert_option($name, $first_view, $connexion, &$option_id) {
        $req = $connexion->query("SELECT * FROM option_lkc
                                     WHERE name = '".$name."'
                                     AND first_seen = '".$first_view."'");
        $reponse = $req->fetch();
        $nb = $req->rowCount();
        $req->closeCursor();

        if ($nb <= 0) {
            $req = $connexion->prepare('INSERT INTO 
                option_lkc(name, first_seen) 
                VALUES(:name, :first_seen)');
            $req->execute(array(
                'name' => $name,
                'first_seen' => $first_view
            ));
            $req->closeCursor();
            $option_id = $connexion->lastInsertId();
        } else {
            $option_id = $reponse[0];
        }
    }

    function insert_hardware($name, $constructor, $connexion, &$hardware_id) {
        $req = $connexion->query("SELECT * FROM hardware_lkc
                                     WHERE name = '".$name."'
                                     AND constructor = '".$constructor."'");
        $reponse = $req->fetch();
        $nb = $req->rowCount();
        $req->closeCursor();

        if ($nb <= 0) {
            $req = $connexion->prepare('INSERT INTO 
                hardware_lkc(name, constructor) 
                VALUES(:name, :constructor)');
            $req->execute(array(
                'name' => $name,
                'constructor' => $constructor
            ));
            $req->closeCursor();
            $hardware_id = $connexion->lastInsertId();
        } else {
            $hardware_id = $reponse[0];
        }
    }

    function insert_tag($name, $connexion) {
        $req = $connexion->query("SELECT * FROM tag_lkc
                                         WHERE name = '".$name."'");
        $reponse = $req->fetch();
        $nb = $req->rowCount();
        $req->closeCursor();

        if ($nb <= 0) {
            $req = $connexion->prepare('INSERT INTO 
                tag_lkc(name) 
                VALUES(:name)');
            $req->execute(array(
                'name' => $name
            ));
            $req->closeCursor();
        }
    }

    function add_relation_module_option($module_name, $option_id, $connexion) {
        // Check if relation exist
        $req = $connexion->query("SELECT * FROM module_option
                                    WHERE module_name = '".$module_name."' 
                                    AND option_id = '".$option_id."'");
        $reponse = $req->fetch();
        $nb = $req->rowCount();
        $req->closeCursor();

        if ($nb > 0) {
            echo 1;
        } else {
            $req = $connexion->prepare('INSERT INTO 
                module_option(module_name, option_id) 
                VALUES(:module_name, :option_id)');
            $req->execute(array(
                'module_name' => $module_name,
                'option_id' => $option_id
            ));
            $req->closeCursor();

            echo 0;
        }
    }

    function add_relation_module_hardware($module_name, $hardware_id, $connexion) {
        // Check if relation exist
        $req = $connexion->query("SELECT * FROM module_hardware
                                    WHERE module_name = '".$module_name."' 
                                    AND hardware_id = '".$hardware_id."'");
        $reponse = $req->fetch();
        $nb = $req->rowCount();
        $req->closeCursor();

        if ($nb > 0) {
            echo 1;
        } else {
            $req = $connexion->prepare('INSERT INTO 
                module_hardware(module_name, hardware_id) 
                VALUES(:module_name, :hardware_id)');
            $req->execute(array(
                'module_name' => $module_name,
                'hardware_id' => $hardware_id
            ));
            $req->closeCursor();

            echo 0;
        }
    }

    function add_relation_tag_option($tag_name, $option_id, $connexion) {
        // Check if relation exist
        $req = $connexion->query("SELECT * FROM tag_option
                                    WHERE tag_name = '".$tag_name."' 
                                    AND option_id = '".$option_id."'");
        $reponse = $req->fetch();
        $nb = $req->rowCount();
        $req->closeCursor();

        if ($nb > 0) {
            echo 1;
        } else {
            $req = $connexion->prepare('INSERT INTO 
                tag_option(tag_name, option_id) 
                VALUES(:tag_name, :option_id)');
            $req->execute(array(
                'tag_name' => $tag_name,
                'option_id' => $option_id
            ));
            $req->closeCursor();

            echo 0;
        }
    }
?>
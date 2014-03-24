<?php 
    include 'connectBD.php';

    if(isset($_POST["option"])){

        $type = addslashes($_POST["type"]);
        $name_option = addslashes($_POST["option"]);
        $kernel_version = addslashes($_POST["kernel_version"]);
        $kernel_sub = addslashes($_POST["kernel_sub"]);
        $hardware_id = -1;
        $option_id = -1;
        $tag_id = -1;


        if ($type == "hardware") {
            $name_hardware = addslashes($_POST["element"]);

            // HARDWARE
            $req = $connexion->query("SELECT * FROM hardware_lkc
                                         WHERE name = '".$name_hardware."'");
            $reponse = $req->fetch();

            if ($req->rowCount() <= 0) {
                $req = $connexion->prepare('INSERT INTO hardware_lkc(name) VALUES(:name)');
                $req->execute(array('name' => $name_hardware));
                $req->closeCursor();
                $hardware_id = $connexion->lastInsertId();
            } else {
                $hardware_id = $reponse[0];
            }
            $req->closeCursor();

        } else if ($type == "tag") {
            $name_tag = addslashes($_POST["element"]);

            // TAG
            $req = $connexion->query("SELECT * FROM tag_lkc
                                         WHERE name = '".$name_tag."'");
            $reponse = $req->fetch();

            if ($req->rowCount() <= 0) {
                $req = $connexion->prepare('INSERT INTO tag_lkc(name) VALUES(:name)');
                $req->execute(array('name' => $name_tag));
                $req->closeCursor();
                $tag_id = $connexion->lastInsertId();
            } else {
                $tag_id = $reponse[0];
            }
            $req->closeCursor();
        }

        // OPTIONS
        $req = $connexion->query("SELECT * FROM option_lkc
                                     WHERE name = '".$name_option."'
                                     AND kernel_version = '".$kernel_version."'
                                     AND kernel_sub = '".$kernel_sub."'");
        $reponse = $req->fetch();
        $option_exist = $req->rowCount();
        $req->closeCursor();

        if ($option_exist <= 0) {
            $req = $connexion->prepare('INSERT INTO 
                option_lkc(name, kernel_version, kernel_sub) 
                VALUES(:name, :kernel_version, :kernel_sub)');
            $req->execute(array(
                'name' => $name_option,
                'kernel_version' => $kernel_version,
                'kernel_sub' => $kernel_sub
            ));
            $req->closeCursor();
            $option_id = $connexion->lastInsertId();
        } else {
            $option_id = $reponse[0];
        }


        if ($type == "hardware") {

            // Check if relation exist
            $req = $connexion->query("SELECT * FROM hardware_option
                                         WHERE hardware_id = '".$hardware_id."' 
                                        AND option_id = '".$option_id."'");
            $reponse = $req->fetch();
            $relation_exist = $req->rowCount();
            $req->closeCursor();

            // INSERT RELATION
            if ($relation_exist > 0) {
                echo 1;
            } else {
                $req = $connexion->prepare('INSERT INTO 
                    hardware_option(hardware_id, option_id) 
                    VALUES(:hardware_id, :option_id)');
                $req->execute(array(
                    'hardware_id' => $hardware_id,
                    'option_id' => $option_id
                ));
                $req->closeCursor();

                echo 0;
            }

        } else if ($type == "tag") {

            // Check if relation exist
            $req = $connexion->query("SELECT * FROM tag_option
                                         WHERE tag_id = '".$tag_id."' 
                                        AND option_id = '".$option_id."'");
            $reponse = $req->fetch();
            $relation_exist = $req->rowCount();
            $req->closeCursor();

            // INSERT RELATION
            if ($relation_exist > 0) {
                echo 1;
            } else {
                $req = $connexion->prepare('INSERT INTO 
                    tag_option(tag_id, option_id) 
                    VALUES(:tag_id, :option_id)');
                $req->execute(array(
                    'tag_id' => $tag_id,
                    'option_id' => $option_id
                ));
                $req->closeCursor();

                echo 0;
            }
        }
    }
?>
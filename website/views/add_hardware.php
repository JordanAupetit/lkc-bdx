<?php 
	include 'connectBD.php';

	if(isset($_POST["hardware"])){

		$name_hardware = addslashes($_POST["hardware"]);
		$name_option = addslashes($_POST["option"]);
		$kernel_version = addslashes($_POST["kernel_version"]);
		$kernel_sub = addslashes($_POST["kernel_sub"]);
		$hardware_id = -1;
		$option_id = -1;


		// HARDWARE
		$req = $connexion->query("SELECT * FROM hardware_lkc
		 							WHERE name = '".$name_hardware."'");
		$reponse = $req->fetch();
		$hardware_exist = $req->rowCount();
		$req->closeCursor();

		if ($hardware_exist <= 0) {
			$req = $connexion->prepare('INSERT INTO hardware_lkc(name) VALUES(:name)');
			$req->execute(array('name' => $name_hardware));
			$req->closeCursor();
			$hardware_id = $connexion->lastInsertId();
		} else {
			$hardware_id = $reponse[0];
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
	}
?>
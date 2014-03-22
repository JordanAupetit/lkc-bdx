<?php 
	include 'connectBD.php';

	if(isset($_POST["hardware"])){

		$name_hardware = addslashes($_POST["hardware"]);
		$name_option = addslashes($_POST["option"]);

		$req = $connexion->query("SELECT * FROM hardware_lkc
		 							WHERE name = '".$name_hardware."'");
		$reponse = $req->fetch();
		$hardware_exist = count($reponse) - 1;
		$req->closeCursor();

		$req = $connexion->query("SELECT * FROM option_lkc
		 							WHERE name = '".$name_option."'");
		$reponse = $req->fetch();
		$option_exist = count($reponse) - 1;
		$req->closeCursor();

		//echo 1;
		//return;

		if ($hardware_exist <= 0) {
			$req = $connexion->prepare('INSERT INTO hardware_lkc(name) VALUES(:name)');
			$req->execute(array('name' => $name_hardware));
			$req->closeCursor();
		}

		if ($option_exist <= 0) {
			$req = $connexion->prepare('INSERT INTO 
				option_lkc(name, kernel_version, kernel_sub) 
				VALUES(:name, :kernel_version, :kernel_sub)');
			$req->execute(array(
				'name' => $name_option,
				'kernel_version' => '',
				'kernel_sub' => ''
			));
			$req->closeCursor();
		}

		echo 42; // success
	}
?>
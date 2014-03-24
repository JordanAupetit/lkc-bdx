<?php 
	include 'connectBD.php';

	if(isset($_POST["hardware_id"])){

		// DELETE RELATIONSHIP
		$hardware_id = addslashes($_POST["hardware_id"]);
		$option_id = addslashes($_POST["option_id"]);

		$count = $connexion->exec("DELETE FROM hardware_option 
									WHERE hardware_id = '".$hardware_id."' 
									AND option_id = '".$option_id."'");

		echo $count;

		// DELETE HARDWARE
		$req = $connexion->query("SELECT * FROM hardware_option
		 							WHERE hardware_id = '".$hardware_id."'");
		$reponse = $req->fetch();
		$req->closeCursor();

		if ($req->rowCount() <= 0) {
			$connexion->exec("DELETE FROM hardware_lkc
								WHERE id = '".$hardware_id."'");
		}

		// DELETE OPTION
		$req = $connexion->query("SELECT * FROM hardware_option
		 							WHERE option_id = '".$option_id."'");
		$reponse = $req->fetch();
		$req->closeCursor();

		if ($req->rowCount() <= 0) {
			$connexion->exec("DELETE FROM option_lkc
								WHERE id = '".$option_id."'");
		}
	}
?>
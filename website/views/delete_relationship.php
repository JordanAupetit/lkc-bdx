<?php 
	include 'connectBD.php';

	if(isset($_POST["option_id"])){

		// DELETE RELATIONSHIP

		$option_id = addslashes($_POST["option_id"]);

		if (isset($_POST["hardware_id"])) {
			$hardware_id = addslashes($_POST["hardware_id"]);

			$count = $connexion->exec("DELETE FROM hardware_option 
									WHERE hardware_id = '".$hardware_id."' 
									AND option_id = '".$option_id."'");

			echo $count;

			// DELETE HARDWARE
			$req = $connexion->query("SELECT * FROM hardware_option
			 							WHERE hardware_id = '".$hardware_id."'");
			$req->closeCursor();

			if ($req->rowCount() <= 0) {
				$connexion->exec("DELETE FROM hardware_lkc
									WHERE id = '".$hardware_id."'");
			}

		}
		else if (isset($_POST["tag_id"])) {
			$tag_id = addslashes($_POST["tag_id"]);

			$count = $connexion->exec("DELETE FROM tag_option 
									WHERE tag_id = '".$tag_id."' 
									AND option_id = '".$option_id."'");

			echo $count;

			// DELETE TAG
			$req = $connexion->query("SELECT * FROM tag_option
			 							WHERE tag_id = '".$tag_id."'");
			$req->closeCursor();

			if ($req->rowCount() <= 0) {
				$connexion->exec("DELETE FROM tag_lkc
									WHERE id = '".$tag_id."'");
			}
		}
		

		// DELETE OPTION
		$req = $connexion->query("SELECT * FROM hardware_option
		 							WHERE option_id = '".$option_id."'");
		$exist_in_hardware_option = $req->rowCount();
		$req->closeCursor();

		$req = $connexion->query("SELECT * FROM tag_option
		 							WHERE option_id = '".$option_id."'");
		$exist_in_tag_option = $req->rowCount();
		$req->closeCursor();

		if ($exist_in_hardware_option <= 0 && $exist_in_tag_option <= 0) {
			$connexion->exec("DELETE FROM option_lkc
								WHERE id = '".$option_id."'");
		}
	}
?>
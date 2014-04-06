<?php 
	include 'connectBD.php';


	// DELETE RELATIONSHIP

	if (isset($_POST["hardware_id"]) && isset($_POST["module_name"])) {
		$hardware_id = addslashes($_POST["hardware_id"]);
		$module_name = addslashes($_POST["module_name"]);

		$count = $connexion->exec("DELETE FROM module_hardware 
								WHERE hardware_id = '".$hardware_id."' 
								AND module_name = '".$module_name."'");

		delete_hardware($hardware_id, $connexion);
		delete_module($module_name, $connexion);

	}
	else if (isset($_POST["option_id"]) && isset($_POST["module_name"])) {
		$option_id = addslashes($_POST["option_id"]);
		$module_name = addslashes($_POST["module_name"]);

		$count = $connexion->exec("DELETE FROM module_option 
								WHERE option_id = '".$option_id."' 
								AND module_name = '".$module_name."'");

		delete_option($option_id, $connexion);
		delete_module($module_name, $connexion);

	}
	else if (isset($_POST["tag_name"]) && isset($_POST["option_id"])) {
		$tag_name = addslashes($_POST["tag_name"]);
		$option_id = addslashes($_POST["option_id"]);

		$count = $connexion->exec("DELETE FROM tag_option 
								WHERE tag_name = '".$tag_name."' 
								AND option_id = '".$option_id."'");

		delete_tag($tag_name, $connexion);
		delete_option($option_id, $connexion);
	}
	
	function delete_module($module_name, $connexion) {
		$req = $connexion->query("SELECT * FROM module_option
		 							WHERE module_name = '".$module_name."'");
		$nb = 0;
		$nb += $req->rowCount();
		$req->closeCursor();

		$req = $connexion->query("SELECT * FROM module_hardware
		 							WHERE module_name = '".$module_name."'");
		$nb += $req->rowCount();
		$req->closeCursor();

		if ($nb <= 0) {
			$connexion->exec("DELETE FROM module_lkc
								WHERE name = '".$module_name."'");
		}
	}

	function delete_option($option_id, $connexion) {
		$req = $connexion->query("SELECT * FROM module_option
		 							WHERE option_id = '".$option_id."'");
		$nb = 0;
		$nb += $req->rowCount();
		$req->closeCursor();

		$req = $connexion->query("SELECT * FROM tag_option
		 							WHERE option_id = '".$option_id."'");
		$nb += $req->rowCount();
		$req->closeCursor();

		if ($nb <= 0) {
			$connexion->exec("DELETE FROM option_lkc
								WHERE id = '".$option_id."'");
		}
	}

	function delete_hardware($hardware_id, $connexion) {
		$req = $connexion->query("SELECT * FROM module_hardware
		 							WHERE hardware_id = '".$hardware_id."'");
		$req->closeCursor();

		if ($req->rowCount() <= 0) {
			$connexion->exec("DELETE FROM hardware_lkc
								WHERE id = '".$hardware_id."'");
		}
	}

	function delete_tag($tag_name, $connexion) {
		$req = $connexion->query("SELECT * FROM tag_option
		 							WHERE tag_name = '".$tag_name."'");
		$req->closeCursor();

		if ($req->rowCount() <= 0) {
			$connexion->exec("DELETE FROM tag_lkc
								WHERE name = '".$tag_name."'");
		}
	}

?>
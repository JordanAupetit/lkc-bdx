<?php 
	include 'connectBD.php';

	if(isset($_POST["search"])){

		$search = addslashes($_POST["search"]);
		$find = addslashes($_POST["find"]);

		$table = "";

		if ($search = "hardware")
			$table = "hardware_lkc";
		else if ($search = "options")
			$table = "options_lkc";


		$req = $connexion->query("SELECT * FROM ".$table."
		 							WHERE name LIKE '%".$find."%'
		 							ORDER BY name");

		$nb_results = 0;
		while($rep = $req->fetch()){
			echo '<div class="mt10"> <div class="col-sm-8"> <input type="text" class="form-control" value="'.$rep[1].'" placeholder="" disabled> </div>';
            echo '<button class="btn btn-success add-hardware-search-input">Add to input</button> </div>';

			$nb_results = 1;
		}

		if ($nb_results == 0)
			echo 0;

		$req->closeCursor();
	}
?>
<?php 
	include 'connectBD.php';

	if(isset($_POST["search"])){

		$search = addslashes($_POST["search"]);
		$find = addslashes($_POST["find"]);

		$table = "";

		if ($search == "hardware")
			$table = "hardware_lkc";
		else if ($search == "options")
			$table = "option_lkc";
		else if ($search == "hardware_options")
			$table = "hardware_option";

		if ($table == "hardware_lkc" || $table == "option_lkc") {
			$req = $connexion->query("SELECT * FROM ".$table."
		 							WHERE name LIKE '%".$find."%'
		 							ORDER BY name");

			$nb_results = 0;
			while($rep = $req->fetch()){
				
	           	if ($search == "hardware") {
	           		echo '<div class="mt10"> <div class="col-sm-8"> <input type="text" class="form-control" value="'.$rep[1].'" placeholder="" disabled> </div>';
	           		echo '<button class="btn btn-success add-hardware-search-input">Add to input</button> </div>';
	           	} else if ($search == "options") {
	           		echo '<div class="mt10"> <div class="col-sm-3"> <input type="text" class="input-opt-name-result form-control" value="'.$rep[1].'" placeholder="" disabled> </div>';
	           		echo '<div class="col-sm-3"> <input type="text" class="input-opt-version-result form-control" value="'.$rep[2].'" placeholder="" disabled> </div>';
	           		echo '<div class="col-sm-3"> <input type="text" class="input-opt-sub-result form-control" value="'.$rep[3].'" placeholder="" disabled> </div>';
	           		echo '<button class="btn btn-success add-options-search-input">Add to input</button> </div>';
	           	}

				$nb_results = 1;
			}

			if ($nb_results == 0)
				echo 0;

			$req->closeCursor();

		} else if ($table == "hardware_option") {
			$req = $connexion->query("SELECT `option_id`, `hardware_id`, `option_lkc`.`name`, `hardware_lkc`.`name`, 
										       `kernel_version`, `kernel_sub`
										FROM `option_lkc` JOIN `hardware_option` ON (`option_id` = `option_lkc`.`id`)
										     	      JOIN `hardware_lkc` ON (`hardware_id` = `hardware_lkc`.`id`)
										WHERE `hardware_lkc`.`name` LIKE '%".$find."%' OR 
										      `option_lkc`.`name` LIKE '%".$find."%'");


			$nb_results = 0;
			while($rep = $req->fetch()){
				
				echo '	<div class="mt10">
							<input type="text" class="hide input-update-hardware-id" value="'.$rep[1].'"> 
							<input type="text" class="hide input-update-option-id" value="'.$rep[0].'"> 
		                    <div class="col-sm-3"> 
		                        <input type="text" class="input-update-hardware form-control" value="'.$rep[3].'" placeholder=""> 
		                    </div>
		                    <div class="col-sm-3"> 
		                        <input type="text" class="input-update-option form-control" value="'.$rep[2].'" placeholder=""> 
		                    </div>
		                    <div class="col-sm-1"> 
		                        <input type="text" class="input-update-version form-control" value="'.$rep[4].'" placeholder=""> 
		                    </div>
		                    <div class="col-sm-1"> 
		                        <input type="text" class="input-update-sub form-control" value="'.$rep[5].'" placeholder=""> 
		                    </div>
			                <button class="btn btn-success btn-update-relationship">Update</button>
			                <button class="btn btn-danger btn-remove-relationship"><span class="glyphicon glyphicon-remove"></span></button>
			            </div>';

				$nb_results = 1;
			}

			if ($nb_results == 0)
				echo 0;

			$req->closeCursor();
		}
		
	}
?>
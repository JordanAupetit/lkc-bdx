<?php 
	include 'connectBD.php';

	if(isset($_POST["search"])){

		$search = addslashes($_POST["search"]);
		$find = addslashes($_POST["find"]);

		$table = "";

		if ($search == "hardware")
			$table = "hardware_lkc";
		else if ($search == "option")
			$table = "option_lkc";
		else if ($search == "tag")
			$table = "tag_lkc";
		else if ($search == "module")
			$table = "module_lkc";
		else if ($search == "hardware_option")
			$table = "hardware_option";
		else if ($search == "tag_option")
			$table = "tag_option";

		if ($table == "hardware_lkc" || $table == "option_lkc" || $table == "tag_lkc" || $table == "module_lkc") {
			$req = $connexion->query("SELECT * FROM ".$table."
		 							WHERE name LIKE '%".$find."%'
		 							ORDER BY name");

			$nb_results = 0;
			while($rep = $req->fetch()){
				
	           	if ($table == "hardware_lkc") {
	           		echo '<div class="mt10"> <div class="col-sm-5"> <input type="text" class="input-search-hardware-result form-control" value="'.$rep[1].'" disabled> </div>';
	           		echo '<div class="col-sm-5"> <input type="text" class="input-search-hardware-constructor-result form-control" value="'.$rep[2].'" disabled> </div>';
	           		echo '<button class="btn btn-success add-hardware-search-input">Add to input</button> </div>';
	           	} else if ($table == "option_lkc") {
	           		echo '<div class="mt10"> <div class="col-sm-5"> <input type="text" class="input-search-option-result form-control" value="'.$rep[1].'" disabled> </div>';
	           		echo '<div class="col-sm-5"> <input type="text" class="input-search-option-view-result form-control" value="'.$rep[2].'" disabled> </div>';
	           		echo '<button class="btn btn-success add-option-search-input">Add to input</button> </div>';
	           	} else if ($table == "tag_lkc") {
	           		echo '<div class="mt10"> <div class="col-sm-8"> <input type="text" class="form-control" value="'.$rep[1].'" disabled> </div>';
	           		echo '<button class="btn btn-success add-tag-search-input">Add to input</button> </div>';
	           	} else if ($table == "module_lkc") {
	           		echo '<div class="mt10"> <div class="col-sm-8"> <input type="text" class="form-control" value="'.$rep[0].'" disabled> </div>';
	           		echo '<button class="btn btn-success add-module-search-input">Add to input</button> </div>';
	           	}

				$nb_results = 1;
			}

			if ($nb_results == 0)
				echo 0;

			$req->closeCursor();

		}
		 else if ($table == "hardware_option") {

			$req = $connexion->query("SELECT `module_name`, `hardware_id`, `hardware_lkc`.`name`, `hardware_lkc`.`constructor`
										FROM `module_hardware` JOIN `hardware_lkc` ON (`hardware_id` = `hardware_lkc`.`id`)
										WHERE `hardware_lkc`.`name` LIKE '%".$find."%' OR 
										      `module_name` LIKE '%".$find."%'");

			$nb_results = 0;
			while($rep = $req->fetch()){
				
				echo '	<div class="mt10">
							<input type="text" class="hide input-update-hardware-id" value="'.$rep[1].'"> 
							<input type="text" class="hide input-update-module-name" value="'.$rep[0].'"> 
		                    <div class="col-sm-3"> 
		                        <input type="text" class="input-update-module form-control" value="'.$rep[0].'"> 
		                    </div>
		                    <div class="col-sm-3"> 
		                        <input type="text" class="input-update-hardware form-control" value="'.$rep[2].'"> 
		                    </div>
		                    <div class="col-sm-3"> 
		                        <input type="text" class="input-update-hardware-constructor form-control" value="'.$rep[3].'"> 
		                    </div>
			                <button class="btn btn-success btn-update-relationship">Update</button>
			                <button class="btn btn-danger btn-remove-relationship"><span class="glyphicon glyphicon-remove"></span></button>
			            </div>';

				$nb_results++;
			}

			$req->closeCursor();


			$req = $connexion->query("SELECT `module_name`, `option_id`, `option_lkc`.`name`, `option_lkc`.`first_seen`
										FROM `module_option` JOIN `option_lkc` ON (`option_id` = `option_lkc`.`id`)
										WHERE `option_lkc`.`name` LIKE '%".$find."%' OR 
										      `module_name` LIKE '%".$find."%'");

			while($rep = $req->fetch()){
				
				echo '	<div class="mt10">
							<input type="text" class="hide input-update-option-id" value="'.$rep[1].'"> 
							<input type="text" class="hide input-update-module-name" value="'.$rep[0].'"> 
		                    <div class="col-sm-3"> 
		                        <input type="text" class="input-update-module form-control" value="'.$rep[0].'"> 
		                    </div>
		                    <div class="col-sm-3"> 
		                        <input type="text" class="input-update-option form-control" value="'.$rep[2].'"> 
		                    </div>
		                    <div class="col-sm-3"> 
		                        <input type="text" class="input-update-option-view form-control" value="'.$rep[3].'"> 
		                    </div>
			                <button class="btn btn-success btn-update-relationship">Update</button>
			                <button class="btn btn-danger btn-remove-relationship"><span class="glyphicon glyphicon-remove"></span></button>
			            </div>';

				$nb_results++;
			}

			if ($nb_results == 0) echo 0;
			$req->closeCursor();

		} 
		//else if ($table == "tag_option") {

		// 	$req = $connexion->query("SELECT `option_id`, `tag_id`, `option_lkc`.`name`, `tag_lkc`.`name`, 
		// 								       `kernel_version`, `kernel_sub`
		// 								FROM `option_lkc` JOIN `tag_option` ON (`option_id` = `option_lkc`.`id`)
		// 								     	      JOIN `tag_lkc` ON (`tag_id` = `tag_lkc`.`id`)
		// 								WHERE `tag_lkc`.`name` LIKE '%".$find."%' OR 
		// 								      `option_lkc`.`name` LIKE '%".$find."%'");


		// 	$nb_results = 0;
		// 	while($rep = $req->fetch()){
				
		// 		echo '	<div class="mt10">
		// 					<input type="text" class="hide input-update-tag-id" value="'.$rep[1].'"> 
		// 					<input type="text" class="hide input-update-option-id" value="'.$rep[0].'"> 
		//                     <div class="col-sm-3"> 
		//                         <input type="text" class="input-update-tag form-control" value="'.$rep[3].'"> 
		//                     </div>
		//                     <div class="col-sm-3"> 
		//                         <input type="text" class="input-update-option form-control" value="'.$rep[2].'"> 
		//                     </div>
		//                     <div class="col-sm-2"> 
		//                         <input type="text" class="input-update-version form-control" value="'.$rep[4].'"> 
		//                     </div>
		//                     <div class="col-sm-2"> 
		//                         <input type="text" class="input-update-sub form-control" value="'.$rep[5].'"> 
		//                     </div>
		// 	                <button class="btn btn-success btn-update-relationship">Update</button>
		// 	                <button class="btn btn-danger btn-remove-relationship"><span class="glyphicon glyphicon-remove"></span></button>
		// 	            </div>';

		// 		$nb_results = 1;
		// 	}

		// 	if ($nb_results == 0)
		// 		echo 0;

		// 	$req->closeCursor();
		// }
	}
?>
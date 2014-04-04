<?php
	// Reporte toutes les erreurs PHP
    error_reporting(E_ALL);
    ini_set('display_errors', -1);

	/* =====================
	     BD de la Fac Bdx1
	   ===================== */ 

	$sgbd='mysql';
	$host='dbserver';
	$utilisateur='jaupetit'; // Mettez vos identifiants <<<<
	$motDePasse='jaupetit';	 // Mettez vos identifiants <<<<
	$nomBase='jaupetit';	 // Mettez vos identifiants <<<<
	$dns=$sgbd.':host='.$host.';dbname='.$nomBase;

	//Tentative de connexion au serveur
	try
	{
		$connexion=new PDO($dns,$utilisateur,$motDePasse, array(PDO::ATTR_ERRMODE => PDO::ERRMODE_WARNING));
	}
	
	catch(Exception $e)
	{
		die('Erreur :' .$e->getMessage());
	}

?>
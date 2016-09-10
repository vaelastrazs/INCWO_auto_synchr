<?php

	include "main_library.php";
	$logs=null;
	$id_user=null;
	init_logs();

	$id = '3991533';
	$lien="https://www.picata.fr/tarifs/Tarif_ean.csv";
	//$lien="picata_catalog.txt";
	$filename = "picata_catalog.xml";
	
	$to_remove = array('"', '=');
	$to_remplace = array(" ", "?");
	
	$output = file_get_contents($lien);
	$output = iconv('ISO-8859-15', 'UTF-8//TRANSLIT', $output);
	$rows = explode("\n",$output);
	$first_line = array_shift($rows);
	$first_line = substr($first_line,0, strlen ($first_line) - 1); 
	$criterias = explode(";",str_replace($to_remplace,"_",$first_line));
	// $criterias = array("Ean","Reference","Categorie","Constructeur","Libelle","PxHT","StockDispoAchard","EncdeAchard");

	$xml_string = "<?xml version=\"1.0\"?>\n<customer_products>\n";
	foreach($rows as $row) {
		$row = substr($row,0, strlen ($row) - 1);
		$datas = explode(";",$row);
		// prevent malformed product
		if (count($datas) == count($criterias)){
			$xml_string = $xml_string."<customer_product>\n";
			for ($i = 0; $i < (count($datas)); $i++) {
				if ($i == 0)
					$datas[$i] = str_replace($to_remove, "", $datas[$i]);
				$datas[$i] = str_replace("&", "+", $datas[$i]);
				$xml_string = $xml_string."<$criterias[$i]>$datas[$i]</$criterias[$i]>";
			}
			$xml_string = $xml_string."\n</customer_product>\n";
		}
	}
	$xml_string = $xml_string."</customer_products>";
	file_put_contents($filename,$xml_string);

?>
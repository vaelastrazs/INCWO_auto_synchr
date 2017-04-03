<?php
include "main_library.php";

init_logs();
ini_set('max_execution_time', 0);
$catalog_fourniseur = get_csv_catalog();
echo "catalog picata loaded";
$catalog_actual = get_actual_catalog();
echo "catalog incwo loaded";
$cross_check = array_fill(0,$catalog_actual->count()-1,0);

foreach ($catalog_fourniseur->customer_product as $product) {
	$found = false;
	$reference_fourniseur = $product->Référence; //TOIMPROVE Depend du CSV recuperer, a mettre en parametrable
	//echo "Produit-ref-fourn : $reference_fourniseur </br>";
	$i = 0;
	foreach ($catalog_actual->customer_product as $actual_product) {
		
		$reference_incwo = $actual_product->reference;
		//echo "incwo : $reference_incwo </br>";
		if ((int) $reference_fourniseur == (int) $reference_incwo){
			echo "modifiying product id ".$actual_product->id." \n";
			$found = true;
			if ($cross_check[$i]){
				echo "Warning : doublon pour produit ".$actual_product->id." \n";
			}
			$cross_check[$i] = 1;
			update_product($product, $actual_product);
			break;
		}
		$i++;
	}
	if (!$found){
		echo "create new producte for reference $reference_fourniseur \n";
		
		create_new_product($product);
	}
}
for ($i = 0 ; $i < count($cross_check) ; $i ++ ){
	if (!$cross_check[$i]){
		echo "remove unused product ".$catalog_actual->customer_product[$i]->id."\n";
		delete_product($catalog_actual->customer_product[$i]->id);
	}
}


?>
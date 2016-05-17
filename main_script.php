<?php
include "main_library.php";

ini_set('max_execution_time', 0);
$catalog_fourniseur = get_csv_catalog();
$catalog_actual = get_actual_catalog();
$products_fourniseur = $catalog_fourniseur->customer_products;

$products_actual = $catalog_actual->customer_product;


foreach ($catalog_fourniseur->customer_product as $product) {
	$found = false;
	$reference_fourniseur = $product->Référence; //TOIMPROVE Depend du CSV recuperer, a mettre en parametrable
	//echo "Produit-ref-fourn : $reference_fourniseur </br>";
	foreach ($catalog_actual->customer_product as $actual_product) {
		$reference_incwo = $actual_product->reference;
		//echo "incwo : $reference_incwo </br>";
		if ((int) $reference_fourniseur == (int) $reference_incwo){
			echo "modifiying product id ".$actual_product->id." \n";
			$found = true;
			update_product($product, $actual_product);
			break;
		}
	}
	if (!$found){
		echo "create new producte for reference $reference_fourniseur \n";
		
		create_new_product($product);
	}
}
?>
<?php
include "main_library.php";

ini_set('max_execution_time', 0);

init_logs();

$catalog_actual = get_actual_catalog();

foreach ($catalog_actual->customer_product as $actual_product) {
	$id = $actual_product->id;
	delete_product($id);
	echo "Delete;";
}
?>
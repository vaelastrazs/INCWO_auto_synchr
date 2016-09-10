<!DOCTYPE html>
<html>
<body>

<?php
$catalog = simplexml_load_file("picata_catalog.xml");
echo "catalog child : ".$catalog->count()."\n";
foreach ($catalog->customer_product as $product){
	echo "SPAM !!!!";
}

?>

</body>
</html>
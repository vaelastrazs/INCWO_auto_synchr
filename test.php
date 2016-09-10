<?php
include "main_library.php";

init_logs();
$xml_data="<custom_label>
	<business_file_id>".$GLOBALS['id_user']."</business_file_id>
	<label_type>customer_product_brand</label_type>
	<long_label>test</long_label>
	<language>FR</language>
	</custom_label>";
	
	$lien="https://www.incwo.com/custom_labels/create_new/387394?type=customer_product_brand";
	
	$ch = curl_init();
	curl_setopt($ch, CURLOPT_URL, $lien);
	curl_setopt($ch, CURLOPT_HTTPAUTH, CURLAUTH_ANY);
	curl_setopt($ch, CURLOPT_USERPWD, $GLOBALS['logs']);
	curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, 0); 
	curl_setopt($ch, CURLOPT_SSL_VERIFYHOST, 0); 
	curl_setopt($ch, CURLOPT_HTTPHEADER, array("Content-Type: text/xml"));
	curl_setopt($ch, CURLOPT_HEADER, 0);
	curl_setopt($ch, CURLOPT_POST, 1);
	curl_setopt($ch, CURLOPT_POSTFIELDS, $xml_data); 
	curl_setopt($ch, CURLOPT_FOLLOWLOCATION, 0);
	curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);
	//$output = 
	curl_exec($ch);
?>
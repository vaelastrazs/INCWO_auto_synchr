<?php

	include "main_library.php";
	$logs=null;
	$id_user=null;
	init_logs();

	
	$lien="https://www.incwo.com/".$GLOBALS['id_user']."/customer_products.xml";
	$filename = "incwo_catalog.xml";
	
	// create curl resource
	$ch = curl_init();

	// set curlopt
	curl_setopt($ch, CURLOPT_URL, $lien);
	curl_setopt($ch, CURLOPT_HTTPAUTH, CURLAUTH_ANY);
	curl_setopt($ch, CURLOPT_USERPWD, $GLOBALS['logs']);
	curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, 0); 
	curl_setopt($ch, CURLOPT_SSL_VERIFYHOST, 0); 
	curl_setopt($ch, CURLOPT_HEADER, 0);
	curl_setopt($ch, CURLOPT_POST, 0);
	curl_setopt($ch, CURLOPT_FOLLOWLOCATION, 0);
	curl_setopt($ch, CURLOPT_HTTPHEADER, array("Content-Type: text/xml"));

	//return the transfer as a string
	curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);

	// $output contains the output string
	$output = curl_exec($ch);
	
	echo "<pre>$output</pre>";

	
	file_put_contents($filename, $output);
	
	$catalog = simplexml_load_file($filename);
	$current_page = $catalog->pagination[0]->{'current_page'};
	$total_pages = $catalog->pagination[0]->{'total_pages'};
	
	echo "Loading incwo catalog : $current_page / $total_pages \n" ;
	
	$output = str_replace ( "</customer_products>\n" , "" ,$output);
	
	while ((int)$current_page < (int)$total_pages){
		
		$current_page = ((int)$current_page) + 1 ;
		$lien_page = "$lien?page=$current_page";
		echo "Loading incwo catalog : $current_page / $total_pages \n";
		curl_setopt($ch, CURLOPT_URL, "$lien_page");
		$next_page = curl_exec($ch);
		$next_page = format_next_page($next_page);
		$output = $output.$next_page;
		//file_put_contents($filename, $output, FILE_APPEND);
	}
	$output = $output."</customer_products>";
	
	file_put_contents($filename, $output);
	// close curl resource to free up system resources
	curl_close($ch);


?>
<?php
	$logs=null;
	$id_user=null;
	init_logs();
	
	$lien="https://www.incwo.com/custom_labels/list/".$GLOBALS['id_user']."?type=customer_product_brand";
	$filename = "marques.txt";
	file_put_contents($filename, "");
	
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
	$output = curl_exec($ch);
	
	
	if(!$output) { 
		echo "<h1>CURL ERROR: " . curl_error($ch) . "</h1>\n"; 
	}else{
		echo "<pre>" ."test". htmlspecialchars($output) . "</pre>"; 
	} /*
	do {
		// $output contains the output string
		$output = curl_exec($ch);    		
		// look for response
		if(!$output) { 
			echo "ERROR";
			break;
		}

		$categories_list = simplexml_load_string($output);
		foreach ($categories_list->customer_product_category as $category) {
			file_put_contents($filename, "$category->id:$category->name\n", FILE_APPEND);
		}
		
		$total_pages = $categories_list->pagination[0]->{'total_pages'};
		
		$current_page = $categories_list->pagination[0]->{'current_page'};
		echo "Traintement categories...$current_page / $total_pages <br />" ;
		
		$current_page = ((int)$current_page) + 1 ;
		$lien_page = "$lien&page=$current_page";
		curl_setopt($ch, CURLOPT_URL, "$lien_page");
	
	}while ((int)$current_page <= (int)$total_pages)
	
	*/
	curl_close($ch);

?>
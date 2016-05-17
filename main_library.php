<?php
$logs = null;
$id_user = null;

function init_logs(){
	$handler = fopen("logs.txt", "r");
	if ($handler){
		while (($line = fgets($handler)) !== false) {
			$rows = explode("=",$line);
			if ($rows[0] == "user")
				$user = $rows[1];
			else if ($rows[0] == "password")
				$pass = $rows[1];
			else if ($rows[0] == "id_user")
				$GLOBALS['id_user'] = trim($rows[1]);
		}
		if ($user == null OR $pass == null){
			echo "ERROR : No login or password found, script exit";
			exit(22);
		}
		$GLOBALS['logs'] = trim($user).":".trim($pass);
		echo $GLOBALS['id_user'];
	}
}

function format_next_page($next_page){
	$next_page = str_replace ( "<customer_products type=\"array\">\n" , "" ,$next_page);
	$next_page = str_replace ( "</customer_products>\n" , "" ,$next_page);
	return str_replace ( "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n" , "" ,$next_page);
}

function get_actual_catalog()
{
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
	
	$catalog = simplexml_load_file($filename);
	return $catalog;
}


function get_actual_product($id)
{
	$lien="https://www.incwo.com/".$GLOBALS['id_user']."/customer_products/$id.xml";
	

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

	// close curl resource to free up system resources
	curl_close($ch);     
	
	// look for response
	if(!$output) { 
		echo "<h1>CURL ERROR: " . curl_error($ch) . "</h1>\n"; 
	}else{
		echo "<pre>" . htmlspecialchars($output) . "</pre>"; 
	}
}

function get_csv_catalog()
{
	$id = '3991533';
	$lien="https://www.picata.fr/tarifs/Tarif_ean.csv";
	//$lien="picata_catalog.txt";
	$filename = "picata_catalog.xml";
	
	
	$to_remove = array('"', '=');
	$to_remplace = array(" ", "?");

	/*
	$handler = fopen($lien, "r");
	if ($handler) {
		//geting criterias : Need to be at first line of csv.
		$first_line = fgets($handler);
		$first_line = substr($first_line,0, strlen ($first_line) - 2); 
		$criterias = explode(";",$first_line);
		/*
		$catalog = new DomDocument();
		$catalog->loadXML("<customer_products></customer_products>");
		
		while (($line = fgets($handler)) !== false) {
			$line = substr($line,0, strlen ($line) - 1);
			$product = $catalog->createElement("customer_product");
			$datas = explode(";",$line);
			for ($i = 0; $i < (count($datas)); $i++) {
				echo str_replace($to_remove,"_",$datas[$i]).";";
				$criteria = $catalog->createElement("A".str_replace($to_remove,"_",$datas[$i]));
				$value = $catalog->createTextNode($datas[$i]);//mb_convert_encoding($datas[$i], 'utf-8',mb_detect_encoding($datas[$i])));
				//utf8_encode(str_replace(" ","_",$criterias[$i])));
				//$criteria = $catalog->createTextNode(iconv('ISO-8859-15', 'UTF-8//TRANSLIT', html_entity_decode($datas[$i],ENT_COMPAT | ENT_HTML401 , "ISO8859-15")));
				$criteria->appendChild($value);
				$product->appendChild($criteria);
			}
			$catalog->appendChild($product);
echo "</br>";
		}
		fclose($handler);
		*/
	
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
		$xml_string = $xml_string."<customer_product>\n";
		$datas = explode(";",$row);
		for ($i = 0; $i < (count($datas)); $i++) {
			if ($i == 0)
				$datas[$i] = str_replace($to_remove, "", $datas[$i]);
			$datas[$i] = str_replace("&", "+", $datas[$i]);
			$xml_string = $xml_string."<$criterias[$i]>$datas[$i]</$criterias[$i]>";
		}
		$xml_string = $xml_string."\n</customer_product>\n";
	}
	$xml_string = $xml_string."</customer_products>";
	file_put_contents($filename,$xml_string);
	
	return simplexml_load_file($filename);
}

function get_categorie_id($categorie_name){
	$handler = fopen("categories", "r");
	echo $categorie_name;
	if ($handler) {
		while (($line = fgets($handler)) !== false) {
			$array = explode(":",$line);
			if (strcmp(trim(utf8_encode($array[1])),$categorie_name) == 0){
				fclose($handler);
				return $array[0];
			}
		}
		fclose($handler);
	}
	return 0; //Categorie not found
}

function get_brand_id($brand_name){
	
}


function create_new_product($product) {
	$ref = $product->Référence;
	$cost = $product->{"Px HT"};
	$price = $cost*1.2;
	$name = $product->Libellé;
	$total = $product->{"Stock Dispo Achard"}+$product->{"En cde Achard"};
	$categorie_id = get_categorie_id(html_entity_decode($product->Catégorie));
	

	$marque_id = 0; //TODO Marques
	
	
	$xml_data="<customer_product>
    <reference>$ref</reference>
	<is_active>1</is_active>
	<is_from_vendor>0</is_from_vendor>
	<name>$name</name>
	
	<product_category_id>$categorie_id</product_category_id>
	<brand_id>$marque_id</brand_id>
    <is_from_vendor>2</is_from_vendor>
	<activity_classification_choice>commerce</activity_classification_choice>
    <currency_id>58</currency_id>
	<vat_id>607</vat_id>
	<price>$price</price>
    <cost>$cost</cost>
	<total_stock>$total</total_stock>
	</customer_product>";
	

	$lien="https://www.incwo.com/".$GLOBALS['id_user']."/customer_products.xml";
	
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
	
	/*
	if(!$output) { 
		echo "<h1>CURL ERROR: " . curl_error($ch) . "</h1>\n"; 
	}else{
		echo "<pre>" . htmlspecialchars($output) . "</pre>"; 
	} 
	*/
	curl_close($ch);
}


function update_product($product, $actual_product){
	
	$cost = $product->{"Px HT"};
	$price = $cost*1.2;
	$id = $actual_product->id;
	
	$xml_data="
	<customer_product>
	<cost>$cost</cost>
    <price>$price</price>";
	if ($product->product_category_id == 0){
		$categorie_id = get_categorie_id(html_entity_decode($product->Catégorie));
		$xml_data = $xml_data."
		<product_category_id>$categorie_id</product_category_id>";
	}
	$xml_data = $xml_data."
	</customer_product>";
	
	$lien="https://www.incwo.com/".$GLOBALS['id_user']."/customer_products/$id.xml";
	
	$ch = curl_init();
	curl_setopt($ch, CURLOPT_URL, $lien);
	curl_setopt($ch, CURLOPT_HTTPAUTH, CURLAUTH_ANY);
	curl_setopt($ch, CURLOPT_USERPWD, $GLOBALS['logs']);
	curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, 0); 
	curl_setopt($ch, CURLOPT_SSL_VERIFYHOST, 0); 
	curl_setopt($ch, CURLOPT_HTTPHEADER, array("Content-Type: text/xml"));
	curl_setopt($ch, CURLOPT_HEADER, 0);
	curl_setopt($ch, CURLOPT_CUSTOMREQUEST, "PUT");
	curl_setopt($ch, CURLOPT_POSTFIELDS, $xml_data); 
	curl_setopt($ch, CURLOPT_FOLLOWLOCATION, 0);
	curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);


	curl_exec($ch);
	/*$output = curl_exec($ch);

	if(!$output) { 
		echo "<h1>CURL ERROR: " . curl_error($ch) . "</h1>\n"; 
	}else{
		echo "<pre>" . htmlspecialchars($output) . "</pre>"; 
	} 
	*/
	curl_close($ch);
}

function delete_product($id){

	$lien="https://www.incwo.com/".$GLOBALS['id_user']."/customer_products/$id.xml";
	
	$ch = curl_init();
    curl_setopt($ch, CURLOPT_URL,$lien);
	curl_setopt($ch, CURLOPT_HTTPAUTH, CURLAUTH_ANY);
	curl_setopt($ch, CURLOPT_USERPWD, $GLOBALS['logs']);
	curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, 0); 
	curl_setopt($ch, CURLOPT_SSL_VERIFYHOST, 0); 
    curl_setopt($ch, CURLOPT_CUSTOMREQUEST, "DELETE");
	curl_setopt($ch, CURLOPT_RETURNTRANSFER, 0);
	curl_exec($ch);
	curl_close($ch);
}

function format_product($product)
{
	$xml = '<customer_product></customer_product>';
	$incwo_product = new SimpleXMLElement($xml);
	return $incwo_product;
}


function debug_xml($xml){
	 
	print "<pre><textarea style=\"width:200%;height:100%;\">";
	print_r(xml2array_parse($xml));
	print "</textarea></pre>";
}


function xml2array_parse($xml){
     foreach ($xml->children() as $parent => $child){
         $return["$parent"] = xml2array_parse($child)?xml2array_parse($child):"$child";
     }
     return $return; 
}

?>


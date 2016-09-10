from lxml import etree
import subprocess
import re

subprocess.call("php /get_brands.php")
subprocess.call("php /get_categories.php")
subprocess.call("php /get_incwo_catalog.php")
subprocess.call("php /get_picata_catalog.php")
catalog_fourniseur = etree.parse("picata_catalog.xml")
products_fourniseur = catalog_fourniseur.getroot()
print "catalog incwo loaded"
catalog_actual =  etree.parse("incwo_catalog.xml")
products_actual = catalog_actual.getroot()
print "catalog incwo loaded"

with open('incwo_catalog.xml') as f:
    ch = f.read()

regx = re.compile('<customer_product>.*?</customer_product>',re.DOTALL)
te = clock()
for i in xrange(n):
    count = sum(1 for mat in regx.finditer(ch))
cross_check = [False] * count
f.close()
print "catalog incwo has currently ", count," items"


foreach (catalog_fourniseur->customer_product as product) {
	found = false;
	reference_fourniseur = product->Référence; #TOIMPROVE Depend du CSV recuperer, a mettre en parametrable
	i = 0;
	foreach (catalog_actual->customer_product as actual_product) {
		
		reference_incwo = actual_product->reference;
		#echo "incwo : reference_incwo </br>";
		if ((int) reference_fourniseur == (int) reference_incwo){
			#echo "modifiying product id ".actual_product->id." \n";
			found = true;
			if (cross_check[i]){
				echo "Warning : doublon pour produit ".actual_product->id." \n";
			}
			cross_check[i] = 1;
			update_product(product, actual_product);
			break;
		}
		i++;
	}
	if (!found){
		echo "create new producte for reference reference_fourniseur \n";
		
		create_new_product(product);
	}
}
for (i = 0 ; i < count(cross_check) ; i ++ ){
	if (!cross_check[i]){
		echo "remove unused product \n";
		delete_product(catalog_actual->customer_product[i]->id);
	}
}


?>
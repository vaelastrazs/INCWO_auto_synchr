#!/usr/bin/python2.7
# coding: utf-8

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



for product in catalog_actual.xpath("/customer_products/customer_product"):
    found = False
	reference_fourniseur = product->Référence; 		#TOIMPROVE Depend du CSV recuperer, a mettre en parametrable
	prix_fourniseur = product->Px_HT; 				#TOIMPROVE Depend du CSV recuperer, a mettre en parametrable
	marque_fourniseur = product->Constructeur; 		#TOIMPROVE Depend du CSV recuperer, a mettre en parametrable
	categorie_fourniseur = product->Catégorie; 		#TOIMPROVE Depend du CSV recuperer, a mettre en parametrable
	stock_fourniseur = product->Stock_Dispo_Achard; #TOIMPROVE Depend du CSV recuperer, a mettre en parametrable
	cmd_fourniseur = product->En_cde_Achard; 		#TOIMPROVE Depend du CSV recuperer, a mettre en parametrable
	
	i = 0;
	foreach (catalog_actual->customer_product as actual_product):
		
		reference_incwo = actual_product->reference
		#echo "incwo : reference_incwo </br>";
		if (reference_fourniseur == reference_incwo):
			#echo "modifiying product id ".actual_product->id." \n"
			found = True;
			if (cross_check[i]):
				print "Warning : doublon pour produit ".actual_product->id
			cross_check[i] = 1
			update_product(product, actual_product)
			break
		i++
	}
	if (!found){
		print "create new producte for reference reference_fourniseur"
		
		#create_new_product(product)
	}
}
for (i = 0 ; i < count(cross_check) ; i ++ ):
	if (!cross_check[i]):
		print "remove unused product with id : ",catalog_actual->customer_product[i]->id
		#delete_product(catalog_actual->customer_product[i]->id)
	



?>
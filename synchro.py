#!/usr/bin/python2.7
# coding: utf-8

from __future__ import print_function 
from lxml import etree
import subprocess
import re
import myLib



# subprocess.call("/usr/bin/php /var/www/vhosts/synchro.clic-ordi.com/httpdocs/INCWO_auto_synchr/get_brands.php")
# subprocess.call("/usr/bin/php /var/www/vhosts/synchro.clic-ordi.com/httpdocs/INCWO_auto_synchr/get_categories.php")
# subprocess.call("/usr/bin/php /var/www/vhosts/synchro.clic-ordi.com/httpdocs/INCWO_auto_synchr/get_incwo_catalog.php")
# subprocess.call("/usr/bin/php /var/www/vhosts/synchro.clic-ordi.com/httpdocs/INCWO_auto_synchr/get_picata_catalog.php")
catalog_fourniseur = etree.parse("picata_catalog.xml")
products_fourniseur = catalog_fourniseur.getroot()
print("catalog incwo loaded")
catalog_actual =  etree.parse("incwo_catalog.xml")
products_actual = catalog_actual.getroot()
print("catalog incwo loaded")

count = catalog_actual.xpath('count(//customer_product)')
cross_check = [False] * int(count)
print("catalog incwo has currently ", count," items")



for product in catalog_fourniseur.xpath("/customer_products/customer_product"):
    found = False
    reference_fourniseur = ""
    for child in product:
        if child.tag == "Référence":
            reference_fourniseur = child.text	#TOIMPROVE Depend du CSV recuperer, a mettre en parametrable
            print("Référence fournisseur : ", reference_fourniseur)
            break
    i = 0
    for actual_product in catalog_actual.xpath("/customer_products/customer_product") :
        for child in actual_product:
            if child.tag == "reference":
                reference_incwo = child.text	#TOIMPROVE Depend du CSV recuperer, a mettre en parametrable
                print("reference incwo : ", reference_incwo)
                break
        if reference_fourniseur == reference_incwo:
            #echo "modifiying product id ".actual_product->id." \n"
            found = True
            if cross_check[i]:
                print("Warning : doublon pour produit ",actual_product)
            cross_check[i] = 1
            myLib.update_product(product, actual_product)
            break
        i+=1
    if not found:
        print("create new producte for reference reference_fourniseur")
        
        #myLib.create_new_product(product)
    

for i in range(count):
	if not cross_check[i]:
		print("remove unused product: ",catalog_actual.xpath("/customer_products/customer_product")[i])
		#myLib.delete_product(catalog_actual->customer_product[i]->id)

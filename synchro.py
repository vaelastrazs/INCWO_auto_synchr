#!/usr/bin/python2.7
# coding: utf-8

from lxml import etree
import subprocess
import re



# subprocess.call("/usr/bin/php /var/www/vhosts/synchro.clic-ordi.com/httpdocs/INCWO_auto_synchr/get_brands.php")
# subprocess.call("/usr/bin/php /var/www/vhosts/synchro.clic-ordi.com/httpdocs/INCWO_auto_synchr/get_categories.php")
# subprocess.call("/usr/bin/php /var/www/vhosts/synchro.clic-ordi.com/httpdocs/INCWO_auto_synchr/get_incwo_catalog.php")
# subprocess.call("/usr/bin/php /var/www/vhosts/synchro.clic-ordi.com/httpdocs/INCWO_auto_synchr/get_picata_catalog.php")
catalog_fourniseur = etree.parse("picata_catalog.xml")
products_fourniseur = catalog_fourniseur.getroot()
print "catalog incwo loaded"
catalog_actual =  etree.parse("incwo_catalog.xml")
products_actual = catalog_actual.getroot()
print "catalog incwo loaded"

with open('incwo_catalog.xml') as f:
    ch = f.read()

regx = re.compile('<customer_product>.*?</customer_product>',re.DOTALL)
for i in xrange(n):
    count = sum(1 for mat in regx.finditer(ch))
cross_check = [False] * count
f.close()
print "catalog incwo has currently ", count," items"



for product in catalog_fourniseur.xpath("/customer_products/customer_product"):
    found = False
    for child in product:
        print child.tag
        if child.tag == "Référence":
            reference_fourniseur = child.text	#TOIMPROVE Depend du CSV recuperer, a mettre en parametrable
            break
    i = 0
    for actual_product in catalog_actual.xpath("/customer_products/customer_product") :
        for child in product:
            print child.tag
            if child.tag == "reference":
                reference_fourniseur = child.text	#TOIMPROVE Depend du CSV recuperer, a mettre en parametrable
                break
        if reference_fourniseur == reference_incwo:
            #echo "modifiying product id ".actual_product->id." \n"
            found = True
            if cross_check[i]:
                print "Warning : doublon pour produit ".actual_product
            cross_check[i] = 1
            update_product(product, actual_product)
            break
        i+=1
    if not found:
        print "create new producte for reference reference_fourniseur"
        
        #create_new_product(product)
    

for i in range(count):
	if not cross_check[i]:
		print "remove unused product: ",catalog_actual.xpath("/customer_products/customer_product")[i]
		#delete_product(catalog_actual->customer_product[i]->id)

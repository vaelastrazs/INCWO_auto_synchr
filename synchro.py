#!/usr/bin/python2.7
# coding: utf-8

from __future__ import print_function 
from lxml import etree
import time
import re
import myLib

catalog_fourniseur = etree.parse("picata_catalog.xml")
products_fourniseur = catalog_fourniseur.getroot()
# print("catalog picata loaded")
catalog_actual =  etree.parse("incwo_catalog.xml")
products_actual = catalog_actual.getroot()
# print("catalog incwo loaded")

count = catalog_actual.xpath('count(//customer_product)')
cross_check = [False] * int(count)
# print("catalog incwo has currently ", count," items")
threads = []

for product in catalog_fourniseur.findall("./customer_product"):
    found = False
    fournisseur_datas = myLib.get_fournisseur_product_infos(product)
    if not 'reference' in fournisseur_datas:
        # print("produit sans ref, skipping...")
        continue
    # for child in product:
    #     if child.tag == "Référence".decode('utf-8'):
    #         reference_fourniseur = child.text #.decode('iso-8859-15').encode('utf8')	#TOIMPROVE Depend du CSV recuperer, a mettre en parametrable
    #         break
    i = 0
    for actual_product in catalog_actual.findall("./customer_product") :
        if cross_check[i]:
           continue        
        reference_incwo = myLib.get_incwo_ref(actual_product)
        if not reference_incwo:
            print("Ref incwo  not found")
            cross_check[i] = True
            #myLib.delete_product(actual_product)
        elif fournisseur_datas['reference'] == reference_incwo:
            # print("reference incwo found!")
            found = True
            cross_check[i] = True
            incwo_datas = myLib.get_incwo_product_infos(actual_product)
            r = myLib.update_product(fournisseur_datas, incwo_datas)
            if r != None:
                threads.append(r)
            break
        i+=1
    if not found:
        # print("create new producte for reference reference_fourniseur")
        threads.append(myLib.create_product(fournisseur_datas))
    time.sleep(0.01)

for i in range(int(count)):
	if not cross_check[i]:
		print("remove unused product: ",catalog_actual.xpath("/customer_products/customer_product/id")[i])
		myLib.delete_product(catalog_actual.xpath("/customer_products/customer_product")[i])
        
for t in threads:
    t.join()
print("Exiting Main Thread")

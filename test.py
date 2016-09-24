#!/usr/bin/python
# -*- coding: UTF-8 -*-

from __future__ import print_function
from lxml import etree
import subprocess
import re
import myLib

catalog_fourniseur = etree.parse("picata_catalog.xml")
products_fourniseur = catalog_fourniseur.getroot()
print("catalog picata loaded")
catalog_actual =  etree.parse("incwo_catalog.xml")
products_actual = catalog_actual.getroot()
print("catalog incwo loaded")

count = catalog_actual.xpath('count(//customer_product)')
cross_check = [False] * int(count)
print("catalog incwo has currently ", count," items")



for product in catalog_fourniseur.findall("./customer_product"):
    found = False
    fournisseur_datas = myLib.get_fournisseur_product_infos(product)
    if not 'reference' in fournisseur_datas:
        print("produit sans ref, skipping...")
        continue
    # for child in product:
    #     if child.tag == "Référence".decode('utf-8'):
    #         reference_fourniseur = child.text #.decode('iso-8859-15').encode('utf8')	#TOIMPROVE Depend du CSV recuperer, a mettre en parametrable
    #         break
    i = 0
    for actual_product in catalog_actual.findall("./customer_product") :
        
        reference_incwo = myLib.get_incwo_ref(actual_product)
        if not reference_incwo:
            print("produit incwo sans ref, skipping...")
            #myLib.delete_current_product()
        elif fournisseur_datas['reference'] == reference_incwo:
            print("reference incwo found!")
            found = True
            if cross_check[i]:
                print("Warning : doublon pour produit ",actual_product)
            cross_check[i] = True
            incwo_datas = myLib.get_incwo_product_infos(actual_product)
            myLib.update_product(fournisseur_datas, incwo_datas)
            break
        i+=1
    if not found:
        print("create new producte for reference reference_fourniseur")
        myLib.create_product(fournisseur_datas)
        i+=1
    if i == 3:
        break
    
# 	
# xml_data="<customer_product><reference>123456</reference>\
# 		<is_active>1</is_active>\
# 		<is_from_vendor>0</is_from_vendor>\
# 		<name>testItem</name>\
# 		<product_category_id>"+str(myLib.get_incwo_categories_id("Objets Connectés"))+"</product_category_id>\
# 		<brand_id>"+str(myLib.get_incwo_brand_id("Apple"))+"</brand_id>\
# 		<is_from_vendor>2</is_from_vendor>\
# 		<activity_classification_choice>commerce</activity_classification_choice>\
# 		<currency_id>58</currency_id>\
# 		<vat_id>607</vat_id>\
# 		<price>12</price>\
# 		<cost>8</cost>\
# 		<total_stock>1</total_stock>\
# 		</customer_product>"
# lien="https://www.incwo.com/387394/customer_products.xml"
# 
# response = myLib.post_request(lien, xml_data)
# print(response.status_code)
# print(response.text)

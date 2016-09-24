#!/usr/bin/python
# -*- coding: UTF-8 -*-

from lxml import etree
import myLib

catalog_fourniseur = etree.parse("picata_catalog.xml")


catalog_actual = etree.parse("incwo_catalog.xml")
i = 0
for product in catalog_fourniseur.xpath("./customer_product"):
    datas = myLib.get_fournisseur_product_infos(product)
    for actual_product in catalog_actual.findall("./customer_product") :
        
        reference_incwo = myLib.get_incwo_ref(actual_product)
        if not reference_incwo:
            print("produit incwo sans ref, skipping...")
            #myLib.delete_current_product()
        elif datas['reference'] == reference_incwo:
            print("reference incwo found!")
    i += 1
    if i==2:
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

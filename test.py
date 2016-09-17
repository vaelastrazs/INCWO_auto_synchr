#!/usr/bin/python
# -*- coding: UTF-8 -*-

from lxml import etree
import myLib

catalog_actual = etree.parse("picata_catalog.xml")
products_actual = catalog_actual.getroot()
i = 0
for product in catalog_actual.xpath("/customer_products/customer_product"):
    datas = myLib.get_fournisseur_product_infos(product)
    myLib.create_product(datas)
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

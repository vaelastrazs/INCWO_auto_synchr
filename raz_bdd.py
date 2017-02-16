#!/usr/bin/python
# -*- coding: UTF-8 -*-

from __future__ import print_function
from lxml import etree
import subprocess
import re
import myLib
import time

catalog_actual =  etree.parse("incwo_catalog.xml")
products_actual = catalog_actual.getroot()
print("catalog incwo loaded")

count = catalog_actual.xpath('count(//customer_product)')
cross_check = [False] * int(count)
print("catalog incwo has currently ", count," items")

threads = []

for myID in catalog_actual.findall("./customer_product/id") :
    url = "https://www.incwo.com/customer_products/387394/"+myID.text+".xml"
    print("DELETE ", url)
    r = myLib.myRequester("delete",url, None)
    r.start()
    threads.append(r)
    time.sleep(0.01)
    
for t in threads:
    response = t.join()
    print("REPLY : "+response)
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

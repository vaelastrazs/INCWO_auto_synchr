#!/usr/bin/python2.7
# coding: utf-8

from __future__ import print_function 
from lxml import etree
import time
import re
import myLib

catalog_fourniseur = etree.parse("test_picata_catalog.xml")
products_fourniseur = catalog_fourniseur.getroot()
# print("catalog picata loaded")
# print("catalog incwo loaded")

threads = []

for product in catalog_fourniseur.findall("./customer_product"):
    fournisseur_datas = myLib.get_fournisseur_product_infos(product)
    if not 'reference' in fournisseur_datas:
        continue
    threads.append(myLib.create_product(fournisseur_datas))
    time.sleep(0.01)

for t in threads:
    t.join()
print("Exiting Main Thread")

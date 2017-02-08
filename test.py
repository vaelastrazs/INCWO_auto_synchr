#!/usr/bin/python2.7
# coding: utf-8

from __future__ import print_function 
from lxml import etree
from threading import Thread
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
    t = Thread(target=myLib.create_product, args=(fournisseur_datas))
    t.start()
    threads.append(t)
    time.sleep(0.01)

for t in threads:
    try:
        r = t.join()
        print("thread "+t.getName()+" has joined correctly")
    except RuntimeError as e:
        print(e)
        s = "alive" if (t.isAlive()) else "dead"
        print("RuntimeError for thread "+t.getName()+", status : "+s)
        
        
print("Exiting Main Thread")

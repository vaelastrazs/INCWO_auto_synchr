#!/usr/bin/python2.7
# coding: utf-8

from __future__ import print_function 
from lxml import etree
from threading import Thread
import time
import re
import myLib
import log

catalog_fourniseur = etree.parse("test_picata_catalog.xml")
products_fourniseur = catalog_fourniseur.getroot()
log.info("catalog picata loaded")

catalog_actual =  etree.parse("incwo_catalog.xml")
products_actual = catalog_actual.getroot()
log.info("catalog incwo loaded")

count = catalog_actual.xpath('count(//customer_product)')
cross_check = [False] * int(count)

threads = []

for product in catalog_fourniseur.findall("./customer_product"):
    found = False
    fournisseur_datas = myLib.get_fournisseur_product_infos(product)
    if not 'reference' in fournisseur_datas:
        # print("produit sans ref, skipping...")
        continue
    else:
        print("name : {}".format(fournisseur_datas['name']))
        print("ref : {}".format(fournisseur_datas['reference']))
    i = 0
    for actual_product in catalog_actual.findall("./customer_product") :
        if cross_check[i]:
            i+=1
            continue        
        reference_incwo = myLib.get_incwo_ref(actual_product)
        if not reference_incwo:
            log.error("Ref incwo not found") # Demander a Toto si tentative de suppression ou non (gerer si ca veux pas?)
            cross_check[i] = True
            #myLib.delete_product(actual_product)
        elif fournisseur_datas['reference'] == reference_incwo:
            # print("reference incwo found!")
            found = True
            cross_check[i] = True
            incwo_datas = myLib.get_incwo_product_infos(actual_product)
            t = Thread(target=myLib.update_product, args=(fournisseur_datas, incwo_datas,))
            t.start()
            threads.append(t)
            break
        i+=1
    if not found:
        t = Thread(target=myLib.create_product, args=(fournisseur_datas,))
        t.start()
        threads.append(t)
    time.sleep(0.01)
for i in range(int(count)):
	if not cross_check[i]:
		log.warning("unused product with id : "+str(catalog_actual.xpath("/customer_products/customer_product/id")[i].text))
		#myLib.delete_product(catalog_actual.xpath("/customer_products/customer_product")[i])


for t in threads:
    try:
        r = t.join()
        log.debug("thread "+t.getName()+" has joined correctly")
    except RuntimeError as e:
        log.error(e)
        s = "alive" if (t.isAlive()) else "dead"
        log.error("RuntimeError for thread "+t.getName()+", status : "+s)
        
        
log.info("Exiting Test")

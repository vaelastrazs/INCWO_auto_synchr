#!/usr/bin/python2.7
# coding: utf-8

from __future__ import print_function 
from lxml import etree
from threading import Thread
import time
import re
import myLib
import log

PROVIDER_TAG = "PIC"

catalog_fourniseur = etree.parse("picata_catalog.xml")
products_fourniseur = catalog_fourniseur.getroot()
log.info("catalog picata loaded")

catalog_actual =  etree.parse("incwo_catalog.xml")
products_actual = catalog_actual.getroot()
log.info("catalog incwo loaded")

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
    i = 0
    ref_fournisseur = fournisseur_datas['reference']
    for actual_product in catalog_actual.findall("./customer_product") :
        #Case product already checked
        if cross_check[i]:
            i+=1
            continue
        
        #Case inactif product
        if not myLib.is_product_actif(actual_product):
            cross_check[i] = True
            i+=1
            continue

        try:
            reference_incwo = actual_product.find("reference").text
        except AttributeError:
            reference_incwo = None

        if not reference_incwo:
            log.error("Ref incwo not found")
            cross_check[i] = True
            myLib.delete_product(actual_product)
        elif not reference_incwo.startswith(PROVIDER_TAG):
            cross_check[i] = True
            log.info("Product with ref {} not part of picata catalog, skipping.".format(reference_incwo))
        elif ref_fournisseur == reference_incwo:
            #print("reference incwo found!")
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
        product = catalog_actual.xpath("/customer_products/customer_product")[i]
        myLib.delete_product(myLib.get_incwo_product_infos(product))

for t in threads:
    try:
        r = t.join()
        log.debug("thread "+t.getName()+" has joined correctly")
    except RuntimeError as e:
        log.error(e)
        s = "alive" if (t.isAlive()) else "dead"
        log.error("RuntimeError for thread "+t.getName()+", status : "+s)
        
        
log.info("Exiting SynchroScript")

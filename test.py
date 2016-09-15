#!/usr/bin/python
# -*- coding: UTF-8 -*-

from lxml import etree

catalog_actual = etree.parse("picata_catalog.xml")
products_actual = catalog_actual.getroot()
i =0
for product in catalog_actual.xpath("/customer_products/customer_product"):
	print "Ref : ",product.find('Référence'.decode('utf-8')).text, " | cat : ",product.find('Catégorie'.decode('utf-8')).text," | Constructeur : ",product.find('Constructeur'.decode('utf-8')).text," | Prix HT : ",product.find('Px_HT'.decode('utf-8')).text
	i+=1
	if i==100:
		break
#!/usr/bin/python
# -*- coding: UTF-8 -*-

from lxml import etree

catalog_actual = etree.parse("incwo_catalog.xml")
products_actual = catalog_actual.getroot()
for product in catalog_actual.xpath("/customer_products/customer_product"):
	print "Ref : ",product.find('Référence'), " | cat : ",product.find('Catégorie')," | Constructeur : ",product.find('Constructeur')," | Prix HT : ",product.find('Px_HT')
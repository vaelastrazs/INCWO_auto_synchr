#!/usr/bin/python
# -*- coding: UTF-8 -*-

from lxml import etree

catalog_actual = etree.parse("picata_catalog.xml")
products_actual = catalog_actual.getroot()
for product in catalog_actual.xpath("/customer_products/customer_product"):
	print "Ref : ",product.find('Référence'.decode('utf-8')), " | cat : ",product.find('Catégorie'.decode('utf-8'))," | Constructeur : ",product.find('Constructeur'.decode('utf-8'))," | Prix HT : ",product.find('Px_HT'.decode('utf-8'))

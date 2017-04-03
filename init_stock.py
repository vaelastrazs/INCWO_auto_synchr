from __future__ import print_function 
from lxml import etree
import os
import re
import myLib
import log

ENTREPOTS_ID = {
    'stock_dispo' : "297973",
    'stock_cmd' : "297978",
}

# creation du dossier stock
if not os.path.isdir("stock") :
    os.makedirs("stock")

# get sur les categories + creation des dossiers liees
with open('categories.txt', 'r') as fp:
    for line in fp:
        datas = line.split(":")
        dirpath = "stock/"+datas[1]
        if not os.path.isdir(dirpath) :
            os.makedirs(os.path.dirname(dirpath))
    fp.close()

catalog = etree.parse("picata_catalog_init.xml")
for product in catalog.findall("./customer_product") :
    datas = myLib.get_fournisseur_product_infos(product)
    filename = "stock/"+datas["product_category_id"]+"/"+datas["reference"]+".txt"
    with open(filename, 'w') as fp:
        for warehouse_name, warehouse_id in ENTREPOTS_ID.iteritems():
            fp.write(warehouse_id+":"+datas[warehouse_name]+"\n")
        fp.close()
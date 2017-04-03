import myLib
from lxml import etree
import re
import os


ID_USER=387394

with open("Tarif_ean_OK.csv", "r") as f1:
    with open("picata_catalog_init.xml", "w") as f2:
        f2.write("<?xml version=\"1.0\"?>\n<customer_products>\n")
        l =  f1.next()
        tags = l.replace(" ","_").split(";")
        for line in f1:
            f2.write("<customer_product>\n")
            items = line.split(";")
            for i in range(len(tags)):
                if ( re.match("^\".*\"{2}.*\"$", items[i])):
                    items[i] = re.sub("\"{2}","\'",items[i])
                    items[i] = items[i].replace("\"","").replace("\'","\"")
                f2.write("<"+tags[i]+">"+items[i]+"</"+tags[i]+">")
            f2.write("</customer_product>\n")
        f2.write("</customer_products>")
import myLib
from lxml import etree
import re
import os
import io

ID_USER=387394

with open("Tarif_ean_OK.csv", "r") as f1:
    with io.open("picata_catalog_init.xml", "w", encoding="utf8") as f2:
        f2.write(u"<?xml version=\"1.0\"?>\n<customer_products>\n")
        l =  f1.next()
        tags = l.strip().replace(" ","_").split(";")
        for line in f1:
            f2.write(u"<customer_product>\n")
            items = line.strip().split(";")
            for i in range(len(tags)):
                if ( re.match("^\".*\"{2}.*\"$", items[i])):
                    items[i] = re.sub("\"{2}","\'",items[i])
                    items[i] = items[i].replace("\"","").replace("\'","\"")
                string = "<"+tags[i]+">"+items[i]+"</"+tags[i]+">"
                f2.write(string.decode('ISO-8859-15'))
            f2.write(u"\n</customer_product>\n")
        f2.write(u"</customer_products>")
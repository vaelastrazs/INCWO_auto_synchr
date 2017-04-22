import myLib
import log

from lxml import etree
import requests
import re
import os
import io

FILENAME = "picata_catalog.xml"
BLACKLIST_FILENAME = "categories_blacklisted.txt"
url = "https://www.picata.fr/tarifs/Tarif_ean.csv"

PROVIDER_TAG = "PIC"

TAGS = ["barcode","reference","product_category","brand","name","provider_price","stock_dispo","stock_cmd"]

blacklist_items = []
print("--BLACKLIST--")
with open(BLACKLIST_FILENAME, "r") as blacklist_file:
    for blacklist_item in blacklist_file:
        blacklist_items.append(blacklist_item.strip())
        print(blacklist_item)
print("--END_BLKLS--")



r = requests.get(url)
lines = r.content.split("\r\n")
lines.pop(0) # On retire la premier ligne, l'organisation du CSV doit etre parametre via la var TAGS ci dessus
print len(lines)
with io.open(FILENAME, "w", encoding="utf8") as f2:
    f2.write(u"<?xml version=\"1.0\"?>\n<customer_products>\n")
    for line in lines:
        items = line.strip().split(";")
        if(len(TAGS) != len(items)):
            log.warning("CSV line is not correctly formatted :\n{}".format(line))
            continue
        string = ""
        for i in range(len(TAGS)):
            # Premier traitement : Si l'item contient un signe @
            value=items[i].replace('&','&amp;')
            # Deuxieme traitement : Si l'item contient deux signes "" (le premier servant a echapper le deuxieme)
            if ( re.match("^\".*\"{2}.*\"$", value)):
                value = re.sub("\"{2}","\'",value)
                value = value.replace("\"","").replace("\'","\"")
            # Troisieme traitement : On ajoute le tag fournisseur sur la ref
            if (TAGS[i] == "reference"):
                value = PROVIDER_TAG+value
            # Quatrieme traitement : pour l'EAN, on supprime l'encapsulage ="XXXXXXXXXXX"
            if (TAGS[i] == "barcode"):
                if ( re.match("^=\"\d*\"$", value)):
                    value = re.sub("={0,1}\"","",value)
                else:
                    log.warning("product with ref {} don't respect EAN expected format : {}".format(items[1], value))
            # Cinquieme traitement : si la categorie fait partie de celles blackliste
            if (TAGS[i] == "product_category"):
                if value in blacklist_items:
                    log.warning("product with ref {} skipped for being in the blacklist".format(items[1]))
                    continue
                
            string = string+"<"+TAGS[i]+">"+value+"</"+TAGS[i]+">"
        f2.write(u"<customer_product>\n")
        f2.write(string.decode('ISO-8859-15'))
        f2.write(u"\n</customer_product>\n")
    f2.write(u"</customer_products>")
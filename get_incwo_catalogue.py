import myLib
import log

from lxml import etree
import requests
import re
import os
import io

ID_USER=387394
USERNAME="antoningp@clic-ordi.com"                                                                                             
PASSWORD="4nt1c0n32EIO88."

FILENAME = "incwo_catalog.xml"
url = "https://www.incwo.com/"+str(ID_USER)+"/customer_products.xml"
headers = {'content-type': 'application/xml'}


catalog = etree.Element("customer_products",  type="array")
r = requests.get(url, headers=headers, auth=(USERNAME, PASSWORD), verify=False)
current_catalog_page = etree.fromstring(r.content)
total_pages = int(current_catalog_page.find("./pagination/total_pages").text)
current_page = 1
while True:
    print("Loading incwo catalog : {} / {}".format(current_page,total_pages))
    for product in current_catalog_page.findall("./customer_product"):
        catalog.append(product)
    
    if (current_page < total_pages):
        current_page+=1
        next_url = url+"?page="+str(current_page)
        r = requests.get(next_url, headers=headers, auth=(USERNAME, PASSWORD), verify=False)
        current_catalog_page = etree.fromstring(r.content)
    else:
        break

with io.open(FILENAME, "w", encoding="utf8") as f1:
    f1.write(etree.tounicode(catalog, pretty_print=True))

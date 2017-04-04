import myLib
from lxml import etree
import re
import os

ID_USER=387394
filename = "categories.txt"

url="https://www.incwo.com/customer_product_categories/list/387394.xml"
response = myLib.send_request("get", url)
response = re.sub('encoding="UTF-8"', '', response)
xml_categories = etree.fromstring(response)
total_pages = int(xml_categories.find("./pagination/total_pages").text)
current_page = 1
with open('categories.txt', 'w') as fp:
    while True: # Sert de Do ... While pour verifier qu'on traite bien toutes les pages
        print "Processing categories {}/{} ...".format(current_page, total_pages),

        current_page_items_count = int(xml_categories.find("./pagination/current_page_items_count").text)
        processed_items = 0
        for category in xml_categories.findall("./customer_product_category"):
            category_id = category.find("id").text
            category_name = category.find("name").text.encode("utf8")
            # Mise en memoire local des infos sur la categorie
            fp.write(category_id+":"+category_name+"\n")
            # Creation du dossier liee a cette categorie pour la gestion de stock local
            dirpath = "stock/"+category_id
            if not os.path.isdir(dirpath) :
                os.makedirs(dirpath)
            # Compteur pour verifier qu'on a bien recupere toutes les categories
            processed_items = processed_items + 1
            
        if (processed_items == current_page_items_count) :
            print "done"
        else:
            print "error, {} out of {} supposed categories found".format(processed_items, current_page_items_count)
        
        # Condition du Do ... While
        if (current_page < total_pages):
            current_page = current_page+1
            url="https://www.incwo.com/customer_product_categories/list/387394.xml?page={}".format(current_page)
            response = myLib.send_request("get", url)
            response = re.sub('encoding="UTF-8"', '', response)
            xml_categories = etree.fromstring(response)
            
            # Des petites verif de redondances
            if (current_page != int(xml_categories.find("./pagination/current_page").text)):
                print "error in current_page count, expected {}, actual {}".format(current_page,xml_categories.find("./pagination/current_page").text)
            if (total_pages != int(xml_categories.find("./pagination/total_pages").text)):
                print "error in total_page count, expected {}, actual {}".format(total_pages,xml_categories.find("./pagination/total_pages").text)
        else:
            break
    

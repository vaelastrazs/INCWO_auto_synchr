#!/usr/bin/python2.7
# coding: utf-8

from __future__ import print_function
from lxml import etree
import requests

TVA=0.20
marge=0.25
ID_USER=387394
USERNAME="antoningp@clic-ordi.com"                                                                                             
PASSWORD="4nt1c0n32EIO88."

INCWO_PARAMS = ["reference","name","brand_id","product_category_id","price","total_stock","cost"]
# FOURNISSEUR_PARAM = ["Référence","Libellé","Constructeur","Catégorie","Px HT","Stock Dispo Achard","En cde Achard"]
# for i in range(len(FOURNISSEUR_PARAM)):
#     FOURNISSEUR_PARAM[i]= FOURNISSEUR_PARAM[I].decode('utf-8')

PRODUCT_ID=0


def get_incwo_brand_id(brand):
    with open('marques.txt', 'r') as fp:
        for line in fp:
            datas = line.split(":")
            if str(datas[1].strip()) == str(brand):
                print(datas[0])
                return datas[0]
        fp.close()
        print("no brand found")
        return 0
            
def get_incwo_categories_id(category):
    with open('categories.txt', 'r') as fp:
        for line in fp:
            datas = line.split(":")
            if str(datas[1].strip()) == str(category):
                print(datas[0])
                return datas[0]
        fp.close()
        print("no category found")
        return 0

def create_brand(brand):
    #TODO
    return "0"
    
def create_category(category):
    #TODO
    return "0"


# Improuvement : Convert data before instead of doing it here
def get_fournisseur_product_infos(product):
    datas = {}
    for child in product:
        if child.tag == "Référence":
            datas["reference"] = child.text
        if child.tag == "Libellé":
            datas["name"] = child.text
        if child.tag == "Constructeur":
            id_brand = get_incwo_brand_id(child.tag)
            if int(id_brand) == 0:
                id_brand = create_brand(child.tag)
            datas["brand_id"] = id_brand
        if child.tag == "Catégorie":
            id_category = get_incwo_categories_id(child.tag)
            if int(id_category) == 0:
                id_category = create_category(child.tag)
            datas["product_category_id"] = id_category
        if child.tag == "Px_HT":
            cost = float(child.text)
            datas["cost"] = cost
            price = cost*(1.0+TVA)*(1.0*marge)                    
            datas["price"] = price
        if child.tag == "Stock_Dispo_Achard":
            datas["total_stock"] = child.text
        if child.tag == "En_cde_Achard":
            #TODO
            datas["cmd"] = child.text
    return datas

def get_reference(product):
    for child in product:
        if child.tag == "reference":
            return = child.text

def get_incwo_product_infos(product):
    datas = {}
    for child in product:
        if child.tag == "id":
            PRODUCT_ID = child.text
        if child.tag in INCWO_PARAMS:
            datas[child.tag] = child.text
    return datas

# Refactoring needed :
# Mettre les params dans un dico, parcourir les clefs
def prepare_xml(product_infos):
    xml_data="<customer_product><reference>123456</reference>\
            <is_active>1</is_active>\
            <is_from_vendor>0</is_from_vendor>\
            <is_from_vendor>2</is_from_vendor>\
            <activity_classification_choice>commerce</activity_classification_choice>\
            <currency_id>58</currency_id>\
            <vat_id>607</vat_id>"
    for tag, value in product_infos:
        if tag in INCWO_PARAMS:
            xml_data+="<"+tag+">"+value+"</"+tag+">"
    
    xml_data+="</customer_product>"
    return xml_data
    # if name != None:
    #     xml_data+="<name>"+str(name)+"</name>"
    # if brand_id != None:
    #     xml_data += "<brand_id>"+str(brand_id)+"</brand_id>"
    # if product_category_id != None:
    #     xml_data += "<product_category_id>"+str(product_category_id)+"</product_category_id>"
    # if price != None:
    #     xml_data += "<price>"+str(price)+"</price>"
    # if cost != None:
    #     xml_data += "<cost>"+str(product_category_id)+"</cost>"
    # if total_stock != None:
    #     xml_data += "<total_stock>"+str(total_stock)+"</total_stock>"
    

def create_product(product):
    product_infos = get_fournisseur_product_infos(product)
    xml_data = prepare_xml(product_infos)
    url="https://www.incwo.com/"+ID_USER+"/customer_products.xml"
    print("Creating producte :")
    print(send_request("post", url, xml_data))

    

def update_product(fournisseur_product, actual_product):
    fournisseur_product_infos = get_fournisseur_product_infos(fournisseur_product)
    incwo_product_infos = get_incwo_product_infos(actual_product)
    update_infos = {}
    for key in INCWO_PARAMS:
        if fournisseur_product_infos[key] != incwo_product_infos[key]:
            update_infos[key]=fournisseur_product_infos[key]
    if len(update_infos) > 0 :
        print("Update needed for product ",str(PRODUCT_ID))
        xml = prepare_xml(update_infos)
        url = "https://www.incwo.com/"+str(ID_USER)+"/customer_products/"+str(PRODUCT_ID)+".xml";
        print(send_request(put, url, xml))
    else :
        print("Product id ",str(PRODUCT_ID)," up to date")

def send_request(method, url, xml=None):

    headers = {'content-type': 'application/xml'}
    if method == "get":
        return requests.get(url, headers=headers, auth=(USERNAME, PASSWORD), verify=False)
    if method == "post":
        return requests.post(url, data=xml, headers=headers, auth=(USERNAME, PASSWORD), verify=False)
    if method == "put":
        return requests.put(url, data=xml, headers=headers, auth=(USERNAME, PASSWORD), verify=False)
    if method == "delete":
        return requests.delete(url, data=xml, headers=headers, auth=(USERNAME, PASSWORD), verify=False)
    
    # req = urllib2.Request(url, data)
    # req.add_header('User-agent', 'Mozilla/5.0')
    # req.add_header('Content-Type', 'text/xml')    
    # return urllib2.urlopen(req)

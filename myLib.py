#!/usr/bin/python2.7
# coding: utf-8

from __future__ import print_function
from lxml import etree
from threading import Thread, BoundedSemaphore
import time
import sys
import requests

TVA=0.20
marge=0.25
ID_USER=387394
USERNAME="antoningp@clic-ordi.com"                                                                                             
PASSWORD="4nt1c0n32EIO88."

INCWO_PARAMS = ["reference","name","brand_id","product_category_id","price","total_stock","cost"]
STOCK_PARAMS = ["stock_dispo","stock_cmd"]
ENTREPOTS_ID = {
    'stock_dispo' : "297973",
    'stock_cmd' : "297978",
}

# FOURNISSEUR_PARAM = ["Référence","Libellé","Constructeur","Catégorie","Px HT","Stock Dispo Achard","En cde Achard"]
# for i in range(len(FOURNISSEUR_PARAM)):
#     FOURNISSEUR_PARAM[i]= FOURNISSEUR_PARAM[I].decode('utf-8')

PRODUCT_ID=0
INCWO_REF_MASK_LEN = 6

pool_sema = BoundedSemaphore(10)

def get_incwo_brand_id(brand):
    with open('marques.txt', 'r') as fp:
        for line in fp:
            datas = line.split(":")
            if str(datas[1].strip()) == str(brand):
                fp.close()
                return datas[0]
        fp.close()
        return 0
            
def get_incwo_categories_id(category):
    with open('categories.txt', 'r') as fp:
        for line in fp:
            datas = line.split(":")
            if str(datas[1].strip()) == str(category):
                fp.close()
                return datas[0]
        fp.close()
        return 0

def create_brand(brand):
    xml_data =  prepare_xml_brand(brand)
    url="https://www.incwo.com/"+str(ID_USER)+"/custom_labels.xml?type=customer_product_brand"
    print("xml_data : "+xml_data)
    print("url : "+url)
    r = myRequester("post", url, xml_data)
    r.start()
    response = r.join()
    for l in response.splitlines():
        if "<id>" in l:
            id = l[6:-5]
            break
    print("Brand "+brand+" created with id "+id)
    with open('marques.txt', 'a') as fp:
        fp.write(id+":"+brand+"\n")
        fp.close()
    return id
    
# En attente d'un solution INCWO
def create_category(category):
    xml_data =  prepare_xml_category(category)
    url="https://www.incwo.com/customer_product_categories/create/"+str(ID_USER)+".xml"
    print("xml_data : "+xml_data)
    print("url : "+url)
    r = myRequester("post", url, xml_data)
    r.start()
    response = r.join()
    for l in response.splitlines():
        if "<id>" in l:
            id = l[6:-5]
            break
    print("Category "+category+" created with id "+id)
    with open('categories.txt', 'a') as fp:
        fp.write(id+":"+category+"\n")
        fp.close()
    return id
    
# Improuvement : Convert data before instead of doing it here
def get_fournisseur_product_infos(product):
    datas = {}
    for child in product:
        tag = child.tag.encode('utf-8')
        if child.text != None:
            text = child.text.encode('utf-8')
        if tag == "Référence":
            datas["reference"] = text
        if tag == "Libellé":
            datas["name"] = text
        if tag == "Constructeur":
            id_brand = get_incwo_brand_id(text)
            if int(id_brand) == 0:
                id_brand = create_brand(text)
            datas["brand_id"] = str(id_brand)
        if tag == "Catégorie":
            id_category = get_incwo_categories_id(text)
            if int(id_category) == 0:
                id_category = create_category(text)
            datas["product_category_id"] = str(id_category)
        if tag == "Px_HT":
            cost = float(text)
            datas["cost"] = cost
            price = round(cost*(1.0+TVA)*(1.0*marge),2)
            datas["price"] = price
        if tag == "Stock_Dispo_Achard":
            datas["stock_dispo"] = text
        if tag == "En_cde_Achard":
            datas["stock_cmd"] = text
    datas["total_stock"] = float(datas["stock_dispo"]) + float(datas["stock_cmd"])
    return datas

def get_incwo_ref(product):
    for child in product:
        if child.tag.encode('utf-8') == "reference":
            return child.text.encode('utf-8')[INCWO_REF_MASK_LEN:]


def get_incwo_product_infos(product):
    datas = {}
    for child in product:
        tag = child.tag.encode('utf-8')
        if child.text != None:
            text = child.text.encode('utf-8')
        
        if tag == "id":
            PRODUCT_ID = text
            # print("Incwo ID : ", text)
        if tag in INCWO_PARAMS:
            if tag == 'reference':
                text = text[INCWO_REF_MASK_LEN:]
            datas[tag] = text
    return datas

def prepare_xml_product(product_infos):
    xml_data="<customer_product><reference>123456</reference>\
            <is_active>1</is_active>\
            <is_from_vendor>0</is_from_vendor>\
            <is_from_vendor>2</is_from_vendor>\
            <activity_classification_choice>commerce</activity_classification_choice>\
            <currency_id>58</currency_id>\
            <vat_id>607</vat_id>"
    for tag, value in product_infos.iteritems():
        if tag in INCWO_PARAMS:
            xml_data+="<"+tag+">"+str(value)+"</"+tag+">"
    xml_data+="</customer_product>"
    return xml_data

def prepare_xml_stock_movement(warehouse_id, quantity, product_id):
    xml_datas=[]
    for tag, value in stocks.iteritems():
        xml_data+="<stock_movement>\
                    <customer_product_id>"+product_id+"</customer_product_id>\
                    <destination_warehouse_id>"+str(warehouse_id)+"</destination_warehouse_id>\
                    <quantity>"+str(quantity)+"</quantity>\
                    <direction>0</direction>\
                    </stock_movement>"
        xml_datas.append(xml_data)
    return xml_datas

def prepare_xml_brand(brand_name):
    xml_data="<custom_label>\
             <label_type>customer_product_brand</label_type>\
             <long_label>"+brand_name+"</long_label>\
             </custom_label>"
    return xml_data


def prepare_xml_category(category_name):
    xml_data="<customer_product_category><name>"+category_name+"</name></customer_product_category>"
    return xml_data

# Parrallélisation compromise, a voir si refactorisation en thread si besoin
def create_product(product_infos):
    xml_data = prepare_xml_product(product_infos)
    url="https://www.incwo.com/"+str(ID_USER)+"/customer_products.xml"
    # print("sending create (POST request) to ",url," ...")
    r = myRequester("post", url, xml_data)
    r.start()
    response = r.join()
    product_id = 0
    for l in response.splitlines():
        if "<id>" in l:
            product_id = extract_value_from_xml(l)
            break
    if (product_id != 0):
        rs = manage_stock_movement(product_infos, product_id)
    return rs

def manage_stock_movement(product_infos, product_id):
    # creation de la variable stocks pour plus de lisibilité
    stocks = {}
    for tag, value in product_infos.iteritems():
        if tag in STOCK_PARAMS:
            stocks[ENTREPOTS_ID[tag]] = value
    
    # Les stocks sont rangé par catégories pour des question de limite de nbrs de fichier
    filename = "stock/"+product_infos["product_category_id"]+"/"+product_id+".txt"
    rs = []
    #Si le dossier n'existe pas, on le crée
    if not os.path.exists(os.path.dirname(filename)):
        try:
            os.makedirs(os.path.dirname(filename))
        except OSError as exc: # Guard against race condition
            if exc.errno != errno.EEXIST:
                raise
            
    # Si le fichier existe, on lit les valeurs du stock precedent
    if os.path.exists(filename):
        with open(filename, 'r') as fp:
            datas = []
            for line in fp:
                data = line.split(":")
                if (stocks[data[0]] != data[1]):
                    rs.append(update_stock_movement(data[0], stocks[data[0]], product_id))
                    
    # Sinon, crée les movement de stock correspondant
    else:
        for warehouse_id, quantity in stocks.iteritems():
            rs.append(update_stock_movement(warehouse_id, quantity, product_id))
                    
    
    # Dans tout les cas, on (re)ecrit le fichier avec les nouvelles valeurs
    with open(filename, 'w') as fp:
        for warehouse_id, quantity in stocks.iteritems():
            fp.write(warehouse_id+":"+quantity+"\n")
        fp.close()
    
    return rs
        
def update_stock_movement(warehouse_id, quantity, product_id):
    xml_move = prepare_xml_stock_movement(warehouse_id, quantity, product_id)
    url="https://www.incwo.com/"+str(ID_USER)+"/stock_movements.xml"
    r = myRequester("post", url, xml_move)
    r.start
    return r

def delete_product(product):
    print("produit incwo sans ref, skipping...")
    # TODO
    return 0

def compareValues(fournisseur_product_info,incwo_product_info):
    try:
        fournisseur_product_info = float(fournisseur_product_info)
        incwo_product_info = float(incwo_product_info)
    except ValueError:
        fournisseur_product_info = fournisseur_product_info.strip()
        incwo_product_info = incwo_product_info.strip()
    return (fournisseur_product_info != incwo_product_info)
        
        
def update_product(fournisseur_product_infos, incwo_product_infos):
    update_infos = {}
    for key in INCWO_PARAMS:
        if not key in fournisseur_product_infos:
            #print("ERROR, fournisseur info incomplete! Missing ", key)
            raise ValueError("Fournisseur info incomplete!")
        elif not key in incwo_product_infos:
            # print("incwo info incomplete, updating ",key)
            update_infos[key]=fournisseur_product_infos[key]
        elif (compareValues(fournisseur_product_infos[key],incwo_product_infos[key])):
            # print("incwo info outdated, updating ",key)
            # print("Picata ",fournisseur_product_infos[key]," ; incwo_product_infos ", incwo_product_infos[key])
            update_infos[key]=fournisseur_product_infos[key]
    if len(update_infos) > 0 :
        print("Update needed for product ",str(PRODUCT_ID))
        xml = prepare_xml_product(update_infos)
        url = "https://www.incwo.com/"+str(ID_USER)+"/customer_products/"+str(PRODUCT_ID)+".xml";
        print("sending update (PUT request) to ",url," ...")
        r = myRequester('put', url, xml)
        r.start()
        return r
    else :
        # print("Product id ",str(PRODUCT_ID)," up to date")
        return None
    
def extract_value_from_xml(string):
    return etree.fromstring(string).text

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
    
    
class myRequester(Thread):
    
    method = None
    url = None
    xml = None
    
    """ Thread principale pour mettre a jour le catalogue incwo"""

    def __init__(self, method, url, xml):
        Thread.__init__(self)
        self.method = method
        self.url = url
        self.xml = xml
        self._return = None

    def run(self):
        r = None
        headers = {'content-type': 'application/xml'}
        rc = 0
        retry = 0
        while (rc != 200 and rc != 201 and retry < 3):
            pool_sema.acquire()
            retry += 1
            if self.method == "get":
                r = requests.get(self.url, headers=headers, auth=(USERNAME, PASSWORD), verify=False)
            elif self.method == "post":
                r = requests.post(self.url, data=self.xml, headers=headers, auth=(USERNAME, PASSWORD), verify=False)
            elif self.method == "put":
                r = requests.put(self.url, data=self.xml, headers=headers, auth=(USERNAME, PASSWORD), verify=False)
            elif self.method == "delete":
                r = requests.delete(self.url, data=self.xml, headers=headers, auth=(USERNAME, PASSWORD), verify=False)
            if r != None:
                rc = r.status_code
                print(rc)
                if rc != 200 and rc != 201:
                    print("aptempt ",retry)
                    print("Error "+str(rc)+" : "+r.text)
                    time.sleep(1)
            pool_sema.release()
        self._return = r.text


    def join(self, *args, **kwargs):
        super(myRequester, self).join(*args, **kwargs)
        return self._return

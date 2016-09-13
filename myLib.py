#!/usr/bin/python2.7
# coding: utf-8

from lxml import etree
import requests

def get_incwo_brand(id):
    with open('marques.txt', 'r') as fp:
        for line in fp:
            print line
            datas = lines.splite(":")
            if datas[0] == id:
                return datas[1]
            
def get_incwo_categories(id):
    with open('categories.txt', 'r') as fp:
        for line in fp:
            print line
            datas = lines.splite(":")
            if datas[0] == id:
                return datas[1]
            



def update_product(product, actual_product):

    #Useless, for debug purpose    
    for child in product:
        print child.tag
        if child.tag == "Référence":
            reference_fourniseur = child.text	
        if child.tag == "Px_HT":
            prix_fourniseur = child.text
        if child.tag == "Constructeur":
            marque_fourniseur = child.text
        if child.tag == "Catégorie":
            categorie_fourniseur = child.text
        if child.tag == "Stock_Dispo_Achard":
            stock_fourniseur = child.text
        if child.tag == "En_cde_Achard":
            cmd_fourniseur = child.text
            
    for child in actual_product:
        print child.tag
        if child.tag == "id":
            id_incwo = child.text	#TOIMPROVE Depend du CSV recuperer, a mettre en parametrable
        if child.tag == "cost":
            cout_incwo = child.text
        # if child.tag == "Stock_Dispo_Achard":
        #     stock_incwo = child.text
        # if child.tag == "En_cde_Achard":
        #     cmd_incwo = child.text
    marque_incwo = get_incwo_brand(id_incwo)
    categorie_incwo = get_incwo_categories(id_incwo)		

    print "Ref produit : ", reference
    
    print "PICATA :"
    print "prix : ", prix_fourniseur,", marque : ", marque_fourniseur,", categorie :",categorie_fourniseur,\
        ", stock : ",stock_fourniseur,", en commande : ", cmd_fourniseur
    
    print "INCWO :"
    print "cout : ", cout_incwo,", marque : ", marque_incwo,", categorie :",categorie_incwo


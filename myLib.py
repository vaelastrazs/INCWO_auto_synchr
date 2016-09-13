#!/usr/bin/python2.7
# coding: utf-8

from __future__ import print_function
from lxml import etree
import requests

def get_incwo_brand(id):
    with open('marques.txt', 'r') as fp:
        for line in fp:
            datas = line.split(":")
            if datas[0] == id:
                return datas[1]
            
def get_incwo_categories(id):
    with open('categories.txt', 'r') as fp:
        for line in fp:
            datas = line.split(":")
            if datas[0] == id:
                return datas[1]
            



def update_product(product, actual_product):

    #Useless, for debug purpose    
    for child in product:
        print(child.tag)
        if child.tag == "Référence".decode('utf-8')::
            reference_fourniseur = child.text	
        if child.tag == "Px_HT".decode('utf-8')::
            prix_fourniseur = child.text
        if child.tag == "Constructeur".decode('utf-8')::
            marque_fourniseur = child.text
        if child.tag == "Catégorie".decode('utf-8')::
            categorie_fourniseur = child.text
        if child.tag == "Stock_Dispo_Achard".decode('utf-8')::
            stock_fourniseur = child.text
        if child.tag == "En_cde_Achard".decode('utf-8')::
            cmd_fourniseur = child.text
            
    for child in actual_product:
        print(child.tag)
        if child.tag == "id".decode('utf-8')::
            id_incwo = child.text	#TOIMPROVE Depend du CSV recuperer, a mettre en parametrable
        if child.tag == "cost".decode('utf-8')::
            cout_incwo = child.text
        # if child.tag == "Stock_Dispo_Achard":
        #     stock_incwo = child.text
        # if child.tag == "En_cde_Achard":
        #     cmd_incwo = child.text
    marque_incwo = get_incwo_brand(id_incwo)
    categorie_incwo = get_incwo_categories(id_incwo)		

    print("Ref produit : ", reference)
    
    print("PICATA :")
    print("prix : ", prix_fourniseur,", marque : ", marque_fourniseur,", categorie :",categorie_fourniseur,\
        ", stock : ",stock_fourniseur,", en commande : ", cmd_fourniseur)
    
    print("INCWO :")
    print("cout : ", cout_incwo,", marque : ", marque_incwo,", categorie :",categorie_incwo)


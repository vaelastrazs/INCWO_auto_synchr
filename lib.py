#!/usr/bin/python2.7
# coding: utf-8

from lxml import etree
import requests

logs = null;
id_user = null;

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
    reference = product->Référence
    prix_fourniseur = product->Px_HT 				    #TOIMPROVE Depend du CSV recuperer, a mettre en parametrable
    marque_fourniseur = product->Constructeur 		    #TOIMPROVE Depend du CSV recuperer, a mettre en parametrable
    categorie_fourniseur = product->Catégorie 		    #TOIMPROVE Depend du CSV recuperer, a mettre en parametrable
    stock_fourniseur = product->Stock_Dispo_Achard      #TOIMPROVE Depend du CSV recuperer, a mettre en parametrable
    cmd_fourniseur = product->En_cde_Achard             #TOIMPROVE Depend du CSV recuperer, a mettre en parametrable
    
    id_incwo = actual_product->id
    cout_incwo = actual_product->cost			        #TOIMPROVE Depend du CSV recuperer, a mettre en parametrable
    marque_incwo = get_incwo_brand(actual_product->brand_id)
    categorie_incwo =  get_incwo_categories(actual_product->product_category_id)		
    #stock_incwo = actual_product->   #TOIMPROVE Depend du CSV recuperer, a mettre en parametrable
    #cmd_incwo = actual_product->          #TOIMPROVE Depend du CSV recuperer, a mettre en parametrable
    
    print "Ref produit : ", reference
    
    print "PICATA :"
    print "prix : ", prix_fourniseur,", marque : ", marque_fourniseur,", categorie :",categorie_fourniseur,\
        ", stock : ",stock_fourniseur,", en commande : ", cmd_fourniseur
    
    print "INCWO :"
    print "cout : ", cout_incwo,", marque : ", marque_incwo,", categorie :",categorie_incwo


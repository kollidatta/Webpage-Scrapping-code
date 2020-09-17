# -*- coding: utf-8 -*-
"""
Created on Thu Aug 20 23:17:03 2020

"""

from bs4 import BeautifulSoup
import requests
import urllib.request
from scrapy import Selector



def scrapper(page_source):
    sel = Selector(text =page_source)
    
    #html parser
    soup = BeautifulSoup(page_source, "html.parser")
    
    #grab each product
    containers = soup.findAll("div",{"class":"item-container"})
    
    filename = "products.csv"
    file = open(filename,"w")
    headers = "Brand, product_name, shipping_cost, price\n"
    file.write(headers)
    
    for container in containers:
                       
        brand = container.div.div.a.img['title']
       
        title_container = container.findAll("a",{"class":"item-title"})
        product_name = title_container[0].text
        
        shipping_container = container.findAll("li",{"class":"price-ship"})
        shipping = shipping_container[0].text.strip()
        
        price_container = container.findAll("li",{"class":"price-current"})
        price = price_container[0].text.strip()
        price = price[:7]
        
        # print("brand:" +brand)
        # print("product_name:" +product_name)
        # print("shipping cost:" +shipping)
        print("price:", price)
        
        file.write(brand+"," +product_name.replace(",","|")+"," +shipping +","+price+"\n")
   
    # except(ConnectionError, Exception)as e:
    #     print( "Exception is :", e)


#opening the connection and loading the page
try:
        
    url = 'https://www.newegg.ca/p/pl?N=100007708&d=video+cards+for+desktop&page=1'
    response = urllib.request.urlopen(url)
    page = response.read()
    response.close()
    scrapper(page)
except(ConnectionError, Exception)as e:
    print( "Exception is :", e)
  
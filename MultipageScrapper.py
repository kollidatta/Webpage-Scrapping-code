# -*- coding: utf-8 -*-
"""
Created on Thu Sep 17 16:49:28 2020

@author: Sridatta reddy
"""


from bs4 import BeautifulSoup
import requests
import urllib.request
from scrapy import Selector
from time import sleep
from random import randint

filename = "quotes.csv"
file = open(filename,"w+")
headers = "quotes,likes\n"
file.write(headers)

def scrapper(containers):
    for container in containers:
    
        quote = container.div.div.text
        for ch in ['"','“','\n','-','”','―', ',']:
            if ch in quote:
                quote = quote.replace(ch,'')
                
        print(quote)        
        likes = container.find('a',{'class':'smallText'})
        likes = likes.text
        print(likes)
        
        file.write(quote+','+likes+'\n')

for i in range(2,100):
    try:
            
        url = 'https://www.goodreads.com/quotes?page='
        page_no = i
        page_url = url+str(page_no)
        print(page_url)
        response = urllib.request.urlopen(page_url)
        page = response.read()
        response.close()
         
        soup = BeautifulSoup(page, "html.parser")
    
        containers = soup.findAll("div",{"class":"quote"})
        print(len(containers))
        sleep(randint(2,10))
        scrapper(containers)
       
    
    except(ConnectionError, Exception)as e:
        print( "Exception is :", e)


file.close()        
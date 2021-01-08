# -*- coding: utf-8 -*-
"""
Created on Thu Aug 20 22:33:10 2020

@author: prabhakar reddy
"""

from bs4 import BeautifulSoup
import pandas as pd
import pickle
import urllib.request
import re

def get_speech_links():
    ''' scrape content of pages with all presidential transcript links '''
    home_url = 'http://millercenter.org/president/speeches'
    try:
        response = urllib.request.urlopen(home_url)
        page_source = response.read()
        soup = BeautifulSoup(page_source, "html5lib")
        transcript_links = soup.findAll("a", {'class': 'transcript'})
        return transcript_links
    except urllib.request.HTTPError:
        print ('Homepage not available!')
        return None
    
def get_transcript(speech_link):
    ''' scrape title of speech, date of speech and full transcipt contained in the input speech_link URL '''
    speaking = speech_link.split('/')[2]
    new_link = base_url + str(speech_link)
    try:
        response = urllib.request.urlopen(new_link)
        page_source = response.read()
        soup = BeautifulSoup(page_source, "html5lib")
        title = soup.find('title').text
        speech_date = title.split('(', 1)[1].split(')')[0]
        transcript = soup.find('div', {'id': 'transcript'}).text
        transcript = transcript.replace('\n', ' ').replace('\r', '').replace('\t', '')
        return {'speaker': speaking,
                'date': speech_date,
                'title': title,
                'transcript': transcript}
    except urllib.request.HTTPError:
        print ('skipped ' + str(speech_link))
        return None

# iterate through all links and extract content
transcript_links = get_speech_links()
base_url = 'http://millercenter.org/'
transcript_dict = {}
for i, link in enumerate(transcript_links):
    if i % 100 == 0:
        print ('Scraped ' + str(i) + '/' + str(len(transcript_links)) 
               + ' of links...')
    if link.has_attr('href'):
        transcript_data = get_transcript(link['href'])
        if transcript_data is not None:
            key = transcript_data['speaker'] + '|' + transcript_data['date']
            transcript_dict[key] = transcript_data
            
# dump dataframe to pickle object
df = pd.DataFrame.from_dict(transcript_dict, orient='index')
pickle.dump(df, open( "presidential_speeches.pickle", "wb" ))
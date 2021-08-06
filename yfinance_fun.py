from fuzzywuzzy import process
from newsapi import NewsApiClient
import requests
from pprint import pprint

news_api = NewsApiClient(api_key='5e3e6d6c0ebe4d73a178b1d54f299ac0')


def getCompany(text):
    r = requests.get('https://api.iextrading.com/1.0/ref-data/symbols')
    stockList = r.json()
    company_name = process.extractOne(text, stockList)[0]['name'].split(' ')[0]


    top_headlines = news_api.get_top_headlines(q=company_name,
                                               category='business',
                                               language='en')
    if top_headlines['totalResults'] == 0:
        return 'no recent news.'
    else:
        ret = ""
        i = 0
        for article in top_headlines['articles']:
            if i < 5:
                ret += str(article['title']) + ' ' + article['url'] + '\n'
                i += 1
        return ret

print(getCompany('LPSN'))

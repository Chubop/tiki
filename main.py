# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
from newsapi import NewsApiClient


newsapi = NewsApiClient(api_key='5e3e6d6c0ebe4d73a178b1d54f299ac0')

top_headlines = newsapi.get_top_headlines(q="Apple",
                                          category='business',
                                          language='en')

def ticker_to_name(ticker):
    with open('data/lookups/stock_data.txt', 'r') as f:
        # splitting the file by new line and then removing all empty strings
        stock_data = filter(None, f.read().split('\n'))

    for line in stock_data:
        line_segments = line.split('|')
        stock_ticker = line_segments[0]
        stock_name = line_segments[1]
        if stock_ticker == ticker:
            return stock_name


print(ticker_to_name('MSFT'))
print(top_headlines)
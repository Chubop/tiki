from typing import Any, Text, Dict, List
from alpaca_trade_api.rest import REST, TimeFrame
from alpaca_trade_api.stream import Stream
from tabulate import tabulate
import requests
from rasa_sdk import Action, Tracker
from newsapi import NewsApiClient
import datetime
import os
import pandas as pd
from yahoo_earnings_calendar import YahooEarningsCalendar
from rasa_sdk.executor import CollectingDispatcher

#
#
# newsapi = NewsApiClient(api_key='5e3e6d6c0ebe4d73a178b1d54f299ac0')
#
# top_headlines = newsapi.get_top_headlines(q="Apple",
#                                           category='business',
#                                           language='en')
#
# def ticker_to_name(ticker):
#     with open('data/lookups/stock_data.txt', 'r') as f:
#         # splitting the file by new line and then removing all empty strings
#         stock_data = filter(None, f.read().split('\n'))
#
#     for line in stock_data:
#         line_segments = line.split('|')
#         stock_ticker = line_segments[0]
#         stock_name = line_segments[1]
#         if stock_ticker == ticker:
#             return stock_name
#
#
# print(ticker_to_name('MSFT'))
# print(top_headlines)

os.environ["APCA_API_KEY_ID"] = "PKAMMMOBO10KSV" \
                                "X8VN7C"
os.environ["APCA_API_SECRET_KEY"] = "5UQi7mYaLm7NK5hVbVLPzAlEhKDOqqey6JkmZzzI"
os.environ["APCA_API_BASE_URL"] = "https://paper-api.alpaca.markets"

apca = REST()
start = pd.Timestamp('2021-08-03 9:30', tz='America/New_York').isoformat()
end = pd.Timestamp('2021-08-03 16:00', tz='America/New_York').isoformat()
barset_df = apca.get_barset(['LPSN'], 'minute', start=start, end=end).df
print(tabulate(barset_df, headers='keys', tablefmt='psql'))
# print(barset_df._get_value(index='2021-08-02 13:44:00-04:00', col='(\'LPSN\', \'high\')'))
for col in barset_df.columns:
    if col[0] == ['LPSN', 'close'
                          '']:
        print('yippie')
    print(str(col))
from typing import Any, Text, Dict, List
from alpaca_trade_api.rest import REST, TimeFrame
from alpaca_trade_api.stream import Stream
from tabulate import tabulate
import datetime
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

# if it's a weekend, set "start" to Friday.
# TODO: holiday support
weekno = datetime.datetime.today().weekday()

# weekday
start_timestamp = pd.Timestamp.now()

if weekno < 5:
    start_timestamp = start_timestamp.replace(hour=9, minute=30)
elif weekno == 6:
    today = start_timestamp.day
    start_timestamp = start_timestamp.replace(hour=9, minute=30, day=(today - 2))
elif weekno == 5:
    today = start_timestamp.day
    start_timestamp = start_timestamp.replace(hour=9, minute=30, day=(today - 1))

end_timestamp = pd.Timestamp.now()

timezone = 'America/New_York'
freq = 'T'
start = pd.Timestamp(start_timestamp, tz=timezone)
start.round(freq=freq)

start.replace(hour=9, minute=30)
start = start.isoformat()

end = pd.Timestamp(end_timestamp, tz=timezone)
end.round(freq=freq)

end = end.isoformat()

barset_df = apca.get_barset(['LPSN'], 'minute', start=start, end=end).df
barset_df.columns = barset_df.columns.map(lambda t: t[1])
print(tabulate(barset_df, headers='keys', tablefmt='psql'))

# print(barset_df['open']['2021-08-20 15:59:00-04:00'])
val = barset_df.iloc[-1:]['close'][0]
print(val)

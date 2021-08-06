# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List
from alpaca_trade_api.rest import REST, TimeFrame
import requests
from fuzzywuzzy import process
from rasa_sdk import Action, Tracker
from newsapi import NewsApiClient
import datetime
import os
import pandas
from yahoo_earnings_calendar import YahooEarningsCalendar
from rasa_sdk.executor import CollectingDispatcher

# news api init
newsapi = NewsApiClient(api_key='5e3e6d6c0ebe4d73a178b1d54f299ac0')

os.environ["APCA_API_KEY_ID"] = "PKAMMMOBO10KSVX8VN7C"
os.environ["APCA_API_SECRET_KEY"] = "5UQi7mYaLm7NK5hVbVLPzAlEhKDOqqey6JkmZzzI"
os.environ["APCA_API_BASE_URL"] = "https://paper-api.alpaca.markets"

apca = REST()

"""
ticker to name takes a ticker 'AAPL' and returns the market name 'Apple Inc.'
"""


def ticker_to_name(ticker):
    with open(os.path.abspath('../ticki-fixed/data/lookups/stock_data.txt'), 'r') as f:
        stock_data = f.read()
    for line in stock_data:
        line_segments = line.split('|')
        stock_ticker = line_segments[0]
        stock_name = line_segments[1]
        if stock_ticker == ticker:
            return stock_name
    raise IndexError


def convert_date_format(date):
    sections = date.split('-')

    # numerical format of the date as a string.
    year_num = sections[0]
    month_num = sections[1]
    day_num = sections[2]

    month_switcher = {
        "01": "January",
        "02": "February",
        "03": "March",
        "04": "April",
        "05": "May",
        "06": "June",
        "07": "July",
        "08": "August",
        "09": "September",
        "10": "October",
        "11": "November",
        "12": "December"
    }
    day_switcher = {
        '01': '1st',
        '02': '2nd',
        '03': '3rd',
        '04': '4th',
        '05': '5th',
        '06': '6th',
        '07': '7th',
        '08': '8th',
        '09': '9th',
        '10': '10th',
        '11': '11th',
        '12': '12th',
        '13': '13th',
        '14': '14th',
        '15': '15th',
        '16': '16th',
        '17': '17th',
        '18': '18th',
        '19': '19th',
        '20': '20th',
        '21': '21st',
        '22': '22nd',
        '23': '23rd',
        '24': '24th',
        '25': '25th',
        '26': '26th',
        '27': '27th',
        '28': '28th',
        '29': '29th',
        '30': '30th',
        '31': '31st'
    }

    month = month_switcher[month_num]
    day = day_switcher[day_num]

    return month + " " + day + ", " + year_num


class ActionGetPercentChange(Action):
    def name(self) -> Text:
        return "action_get_percent_change"

    async def run(
            self, dispatcher, tracker: Tracker, domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        symbol = tracker.get_slot("symbol")
        time = tracker.get_slot("time")
        # get daily price data for AAPL over the last X trading days.
        # barset = apca.get_barset(symbol, '')

        # dispatcher.utter_message(time)

        return []


class ActionGetStockPrice(Action):

    def name(self) -> Text:
        return "action_get_stock_price"

    async def run(
            self, dispatcher, tracker: Tracker, domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        symbol = tracker.get_slot("symbol")
        URL = 'https://api.polygon.io/v2/aggs/ticker/' + symbol + '/prev?unadjusted=true&apiKey=9WYssjnea_WC1CUJY6rPNFrytFSE129G'
        resp = requests.get(
            url=URL)
        data = resp.json()

        # txt = symbol + " opened today at " + str(data['results'][0]['o'])
        txt = 'currently disabled.'
        dispatcher.utter_message(text=txt)

        return []


class ActionGetStockNews(Action):

    def name(self) -> Text:
        return "action_get_stock_news"

    async def run(
            self, dispatcher, tracker: Tracker, domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        symbol = tracker.get_slot("symbol")
        r = requests.get('https://api.iextrading.com/1.0/ref-data/symbols')
        stock_list = r.json()
        company_name = process.extractOne(symbol, stock_list)[0]['name'].split(' ')[0]

        top_headlines = newsapi.get_top_headlines(q=company_name,
                                                  category='business',
                                                  language='en')
        if top_headlines['totalResults'] == 0:
            dispatcher.utter_message(text='No recent news.')
        else:
            ret = ""
            i = 1
            for article in top_headlines['articles']:
                if i < 6:
                    ret += str(i) + '. ' + article['title'] + ' ' + article['url'] + '\n'
                    i += 1
            dispatcher.utter_message(text=ret)

        return []


class ActionGetStockOpen(Action):

    def name(self) -> Text:
        return "action_get_stock_open"

    async def run(
            self, dispatcher, tracker: Tracker, domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        symbol = tracker.get_slot("symbol")
        URL = 'https://api.polygon.io/v2/aggs/ticker/' + symbol + '/prev?unadjusted=true&apiKey=9WYssjnea_WC1CUJY6rPNFrytFSE129G'
        resp = requests.get(
            url=URL)
        data = resp.json()

        open_value = apca.get_barset(symbol, "minute", limit=10)[symbol][0].o

        txt = symbol + " opened today at " + str(open_value)
        dispatcher.utter_message(text=txt)

        return []


class ActionGetStockClose(Action):

    def name(self) -> Text:
        return "action_get_stock_close"

    async def run(
            self, dispatcher, tracker: Tracker, domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        symbol = tracker.get_slot("symbol")
        URL = 'https://api.polygon.io/v2/aggs/ticker/' + symbol + '/prev?unadjusted=true&apiKey=9WYssjnea_WC1CUJY6rPNFrytFSE129G'
        resp = requests.get(
            url=URL)
        data = resp.json()

        txt = symbol + " closed today at " + str(data['results'][0]['c'])
        dispatcher.utter_message(text=txt)

        return []


class ActionGetStockHigh(Action):

    def name(self) -> Text:
        return "action_get_stock_high"

    async def run(
            self, dispatcher, tracker: Tracker, domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        symbol = tracker.get_slot("symbol")
        URL = 'https://api.polygon.io/v2/aggs/ticker/' + symbol + '/prev?unadjusted=true&apiKey=9WYssjnea_WC1CUJY6rPNFrytFSE129G'
        resp = requests.get(
            url=URL)
        data = resp.json()

        txt = symbol + "'s high today is " + str(data['results'][0]['h'])
        dispatcher.utter_message(text=txt)

        return []


class ActionGetStockLow(Action):

    def name(self) -> Text:
        return "action_get_stock_low"

    async def run(
            self, dispatcher, tracker: Tracker, domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        symbol = tracker.get_slot("symbol")
        URL = 'https://api.polygon.io/v2/aggs/ticker/' + symbol + '/prev?unadjusted=true&apiKey=9WYssjnea_WC1CUJY6rPNFrytFSE129G'
        resp = requests.get(
            url=URL)
        data = resp.json()

        txt = symbol + "'s low today is " + str(data['results'][0]['l'])
        dispatcher.utter_message(text=txt)

        return []


class ActionGetNextEarningsCall(Action):
    def name(self) -> Text:
        return "action_get_next_earnings_call"

    async def run(
            self, dispatcher, tracker: Tracker, domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        symbol = tracker.get_slot("symbol")

        yec = YahooEarningsCalendar()
        time = yec.get_next_earnings_date(symbol)
        date = datetime.datetime.fromtimestamp(
            int(time)
        ).strftime('%m %d,%Y at %H:%M')
        txt = symbol + '\'s next earnings call is on ' + date + '.'
        dispatcher.utter_message(text=txt)

        return []


class ActionGetStockVolume(Action):

    def name(self) -> Text:
        return "action_get_stock_volume"

    async def run(
            self, dispatcher, tracker: Tracker, domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        symbol = tracker.get_slot("symbol")
        URL = 'https://api.polygon.io/v2/aggs/ticker/' + symbol + '/prev?unadjusted=true&apiKey=9WYssjnea_WC1CUJY6rPNFrytFSE129G'
        resp = requests.get(
            url=URL)
        data = resp.json()

        txt = symbol + " has a volume of " + str(data['results'][0]['v'])
        dispatcher.utter_message(text=txt)

        return []


# todo: exchange specific holidays?
class ActionGetNextHoliday(Action):

    def name(self) -> Text:
        return "action_get_next_holiday"

    async def run(
            self, dispatcher, tracker: Tracker, domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        URL = 'https://api.polygon.io/v1/marketstatus/upcoming?&apiKey=9WYssjnea_WC1CUJY6rPNFrytFSE129G'
        resp = requests.get(
            url=URL)
        data = resp.json()

        txt = "The next market holiday is " + data[0]['name'] + ' on ' + convert_date_format(data[0]['date']) + '.'
        dispatcher.utter_message(text=txt)

        return []


class ActionBuyStock(Action):

    def name(self) -> Text:
        return "action_buy_stock"

    async def run(
            self, dispatcher, tracker: Tracker, domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        symbol = tracker.get_slot('symbol')
        number = tracker.get_slot('number')

        first_msg = 'Putting in a BUY order on ticker ' + symbol + ' for ' + str(number) + ' orders...'
        dispatcher.utter_message(text=first_msg)
        apca.submit_order(symbol=symbol, qty=number, side='buy', type='market', time_in_force='day')
        last_msg = 'Success'
        dispatcher.utter_message(last_msg)

        return []


class ActionCheckAccountBalance(Action):

    def name(self) -> Text:
        return "action_check_account_balance"

    async def run(
            self, dispatcher, tracker: Tracker, domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:

        account = apca.get_account()
        if account.trading_blocked:
            dispatcher.utter_message('WARNING: Account is currently restricted from trading.')
        dispatcher.utter_message('${} is available as buying power.'.format(account.buying_power))

        return []


class ActionBuyStockForCash(Action):

    def name(self) -> Text:
        return "action_buy_stock_for_cash"

    async def run(
            self, dispatcher, tracker: Tracker, domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:

        symbol = tracker.get_slot('symbol')
        cash = tracker.get_slot('amount-of-money')

        first_msg = 'Putting in a BUY order on ticker ' + symbol + ' for ' + str(cash) + '...'
        dispatcher.utter_message(text=first_msg)
        apca.get_quotes(symbol, "2021-02-08", limit=1).df
        apca.submit_order(symbol=symbol, qty=number, side='buy', type='market', time_in_force='day')
        last_msg = 'Success'
        dispatcher.utter_message(last_msg)

        return []

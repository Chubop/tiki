"""
populate.py
Populate lookups using live requests. Used to create entity lists and to keep them updated.
"""
import urllib.request

# has a bunch of great stock data that we can split by '|' per line
url = "https://www.nasdaqtrader.com/dynamic/SymDir/nasdaqlisted.txt"


"""
save_to_txt saves the request to "stock_data.txt"
"""


def save_to_txt():
    file = urllib.request.urlopen(url)
    with open('stock_data.txt', 'w') as outfile:
        outfile.write(file.read().decode('utf-8'))


"""
grabs the symbol/ticker of all the current stocks on NASDAQ.
"""


def populate_symbols():
    file = urllib.request.urlopen(url)

    symbols = []
    for line in file:
        decoded_line = line.decode("utf-8")
        split_decoded_line = decoded_line.split('|')

        symbol = split_decoded_line[0]
        if symbol != 'Symbol':
            symbols.append(symbol)

    write_file('symbol', symbols)
    return symbols


"""
write_file writes a text file to the lookups folder using an array object and a given file name
"""


def write_file(file_name, array, entity_name=""):
    # the default entity name inside the file is file_name.
    entity_name = file_name

    with open(file_name + '.yml', 'w') as outfile:
        # TODO: fix the formatting so the first entry has a newline and a dash included as it currently does not.
        # also remove the weird timestamp at the bottom.
        outfile.write("version: \"2.0\"\nnlu:\n  - lookup: " + entity_name + "\n    examples: |" + "\n      - ".join(array))


def ticker_to_name(ticker):
    with open('../data/lookups/stock_data.txt', 'r') as f:
        stock_data = f.read()
    for line in stock_data:
        line_segments = line.split('|')
        stock_ticker = line_segments[0]
        stock_name = line_segments[1]
        if stock_ticker == ticker:
            return stock_name
    raise IndexError


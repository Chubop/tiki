"""
populate.py
Populate lookups using live requests. Used to create entity lists and to keep them updated.
"""
import urllib.request

# has a bunch of great stock data that we can split by '|' per line
url = "https://www.nasdaqtrader.com/dynamic/SymDir/nasdaqlisted.txt"

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


def write_file(file_name, array):
    with open(file_name + '.txt', 'w') as outfile:
        outfile.write("\n      - ".join(array))


populate_symbols()
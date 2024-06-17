import json
from os import X_OK
import time
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib
import urllib.request
import json
import pytz
from datetime import datetime
import os
import shutil

from alpaca.trading.client import TradingClient
from alpaca.trading.requests import MarketOrderRequest, LimitOrderRequest, TakeProfitRequest, StopLossRequest
from alpaca.trading.enums import OrderSide, TimeInForce, OrderClass
import alpaca_trade_api as tradeapi
import requests



API_KEY = 'AKWQSXPBDHSSZBQH60WA' # THIS IS THE REAL
API_SECRET = "zKI0mEDbOilpekjPsZ7rOyjSMcT6HpjcRjD0VJh3" # THIS IS THE REAL
APCA_API_BASE_URL = 'https://paper-api.alpaca.markets/v2'  # Paper trading endpoint # THIS IS THE REAL
#API_KEY = 'PKZDTXRWA06FGKUIBSBC' # THIS IS THE FAKE
#API_SECRET = "jBCGORRU2rHAghgVmcbzDfOYP7m670SClAUGeNsf" # THIS IS THE FAKE
#APCA_API_BASE_URL = 'https://paper-api.alpaca.markets/v2' # THIS IS THE FAKE

def move_files_except(filename):
  if not os.path.exists('old_records'):
      os.makedirs('old_records')
  files = os.listdir('.')
  for file in files:
      if file != filename and os.path.isfile(file):
          shutil.move(file, os.path.join('old_records', file))
#move_files_except('dwight_v1_dev.py')

sequence_file = "sequence_" + str(time.localtime().tm_mon) + "_" + str(time.localtime().tm_mday) + "_" + str(time.localtime().tm_hour) + "_" + str(time.localtime().tm_min) + ".txt"
api_file = "api_" + str(time.localtime().tm_mon) + "_" + str(time.localtime().tm_mday) + "_" + str(time.localtime().tm_hour) + "_" + str(time.localtime().tm_min) + ".txt"


######################################################################################################################################################################################################################################Change back

# API_KEY = 'PK28FQ7082D0XUIBUUUE'
# API_SECRET = "X5N9YiYss1tmbHzgWMx37RbwI3D2rM0mdN3Jvts6"
# APCA_API_BASE_URL = 'https://paper-api.alpaca.markets/v2'  # Paper trading endpoint


trading_client = tradeapi.REST(API_KEY, API_SECRET) # THIS IS THE REAL
#trading_client = TradingClient(API_KEY, API_SECRET, paper=True)  # THIS IS THE FAKE
account = trading_client.get_account()
buying_power = float(account.cash)
amount = buying_power * .1

def append_to_sequence_file(filename, content):
    var = 1
#   try:
#       with open(filename, 'a') as file:
#           file.write(content + '\n')  # Append the content to the file
#           # print("Content appended to", filename)
#   except FileNotFoundError:
#       print("File not found:", filename)
#   except Exception as e:
#       print("An error occurred:", e)


def append_to_api_file(filename, content):
  var = 1
#   try:
#       with open(filename, 'a') as file:  # Open the file in append mode
#           file.write(content + '\n')  # Append the content to the file
#           # print("Content appended to", filename)
#   except FileNotFoundError:
#       print("File not found:", filename)
#   except Exception as e:
#       print("An error occurred:", e)



def send_email(info):
  # Mailgun SMTP server details
  smtp_host = 'smtp.mailgun.org'
#   smtp_port = 587  # Use 587 for TLS

#   # Mailgun SMTP credentials
#   smtp_username = 'postmaster@sandbox9b63cbca518542cc822f975fed41efe9.mailgun.org'
#   smtp_password = 'fab0c99a7e1a42862a23091fd31bd2fa-b02bcf9f-76017ace'

#   # Sender and recipient email addresses
#   sender_email = 'Excited User <mailgun@sandbox9b63cbca518542cc822f975fed41efe9.mailgun.org>'
#   recipient_email = 'josephsteenhuisen@gmail.com'

#   # Email content
#   subject = 'Test Email from Mailgun SMTP'
#   body = info

#   # Create a MIMEText object for the email content
#   message = MIMEMultipart()
#   message['From'] = sender_email
#   message['To'] = recipient_email
#   message['Subject'] = subject
#   message.attach(MIMEText(body, 'plain'))

#   try:
#     # Connect to Mailgun's SMTP server
#     server = smtplib.SMTP(smtp_host, smtp_port)

#     # Start TLS encryption
#     server.starttls()

#     # Login to the SMTP server
#     server.login(smtp_username, smtp_password)

#     # Send the email
#     server.sendmail(sender_email, recipient_email, message.as_string())

#     # Close the connection
#     server.quit()

#     # print("Email sent successfully!")

#   except Exception as e:
#     print("An error occurred:", e)


ra = """{
    "top_gainers": [
        {
            "ticker": "BW",
            "price": "3.11",
            "change_amount": "0.6774",
            "change_percentage": "6823.0769%",
            "volume": "5901853"
        }
    ]
}"""

rb = ra
rc = ra
rd = ra
re = ra


def extract_tickers(json_dump):
  """Extracts tickers from a JSON dump."""
  try:
    data = json.loads(json_dump)
    return {entry['ticker']: entry for entry in data['top_gainers']}
  except json.JSONDecodeError as e:
    print("Error decoding JSON:", e)
    return {}


def filter_common_tickers(old_dump, new_dump):
  """Filters common tickers from two JSON dumps."""
  old_tickers = extract_tickers(old_dump)
  new_tickers = extract_tickers(new_dump)

  common_tickers = {}
  for ticker in old_tickers.keys():
    if ticker in new_tickers:
      common_tickers[ticker] = old_tickers[ticker]

  filtered_data = {"top_gainers": list(common_tickers.values())}
  return json.dumps(filtered_data, indent=4)

count = 0
data_list = [ra, rb, rc, rd, re]


def decide_stocks_tg_at(stocks):
  #for now, we'll just keep the ones from the stock, maybe we'll make sure the stocks are under $15 or something
  return filter_stocks_tg_at(stocks)


def convert_to_target_format(active, gainers, losers):
    def transform_entry(entry):
        return {
            "ticker": entry["symbol"],
            "price": str(entry["price"]),
            "change_amount": str(entry["change"]),
            "change_percentage": f'{entry["changesPercentage"]:.4f}%',
            "volume": "0"  # Assuming volume is not available in the new format
        }

    def top_n_entries(entries, n=20):
        return entries[:n]

    converted_data = {
        "metadata": "Top gainers, losers, and most actively traded US tickers",
        "last_updated": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        "top_gainers": [transform_entry(entry) for entry in top_n_entries(gainers, 20)],
        "top_losers": [transform_entry(entry) for entry in top_n_entries(losers, 20)],
        "most_actively_traded": [transform_entry(entry) for entry in top_n_entries(active, 20)]
    }

    return json.dumps(converted_data, indent=4)

# url = "https://www.alphavantage.co/query?function=TOP_GAINERS_LOSERS&apikey=demo"
url = "https://www.alphavantage.co/query?function=TOP_GAINERS_LOSERS&entitlement=realtime&apikey=J9B7EKCLFJDXFI8F"

def ping_api():
  active = json.loads(urllib.request.urlopen("https://financialmodelingprep.com/api/v3/stock_market/actives?apikey=JsxNLlkcPHhOmQxXh0pus71q4peJnIN0").read())
  gainers = json.loads(urllib.request.urlopen("https://financialmodelingprep.com/api/v3/stock_market/gainers?apikey=JsxNLlkcPHhOmQxXh0pus71q4peJnIN0").read())
  losers = json.loads(urllib.request.urlopen("https://financialmodelingprep.com/api/v3/stock_market/actives?apikey=JsxNLlkcPHhOmQxXh0pus71q4peJnIN0").read())
  #print("\n\n\n\nreturned\n\n" + str(convert_to_target_format(active, gainers, losers)))
  output = json.loads(convert_to_target_format(active, gainers, losers))
  #response = urllib.request.urlopen(url)
  #output = json.loads(response.read())
  append_to_api_file(api_file, "\n\n\n\n\n\n\nApi Ping at " + str(time.localtime().tm_mon) + "_" + str(time.localtime().tm_mday) + "_" + str(time.localtime().tm_hour) + "_" + str(time.localtime().tm_min) + "_" + str(time.localtime().tm_sec) +  "\n" + str(filter_decided_stocks_all(str(output).replace("'", '"'))) + "\nCross Referenced between Top Gainers and Active Trading at " + str(time.localtime().tm_mon) + "_" + str(time.localtime().tm_mday) + "_" + str(time.localtime().tm_hour) + "_" + str(time.localtime().tm_min) + "_" + str(time.localtime().tm_sec) + ":\n\n\n" + filter_decided_stocks_all(str(filter_top_gainers(str(output).replace("'", '"')))))
  return output


def filter_decided_stocks_all(json_data):
    try:
        # Parse JSON data
        data = json.loads(json_data)

        # Combine top gainers, losers, and most actively traded stocks
        all_stocks = data.get("top_gainers", []) + data.get("top_losers", []) + data.get("most_actively_traded", [])

        # Filter out stocks based on criteria
        filtered_stocks = {
            "Top Gainers": [],
            "Top Losers": [],
            "Most Actively Traded": []
        }

        for stock in all_stocks:
            ticker = stock["ticker"]
            price = float(stock["price"])
            amount = float(stock["change_amount"])
            percentage = str(stock["change_percentage"])
            volume = int(stock["volume"])

            if stock in data.get("top_gainers", []):
                filtered_stocks["Top Gainers"].append(f"{ticker}: ${price:.3f} Change Amount: {amount} Change Percentage: {percentage} Volume: {volume}")
            elif stock in data.get("top_losers", []):
                filtered_stocks["Top Losers"].append(f"{ticker}: ${price:.3f} Change Amount: {amount} Change Percentage: {percentage} Volume: {volume}")
            elif stock in data.get("most_actively_traded", []):
                filtered_stocks["Most Actively Traded"].append(f"{ticker}: ${price:.3f} Change Amount: {amount} Change Percentage: {percentage} Volume: {volume}")

        # Construct the final string
        final_string = ""
        for section, stocks in filtered_stocks.items():
            if stocks:
                final_string += f"{section}:\n"
                final_string += '\n'.join(stocks) + "\n\n"

        return final_string

    except json.JSONDecodeError as e:
        print("Invalid JSON data:", e)
        return "None"

def get_current_price(symbol, json_dump):
  # Parse the JSON dump
  data = json.loads(json_dump)

  # Search for the symbol in the "top_gainers" list
  for stock in data["top_gainers"]:
    if stock["ticker"] == symbol:
      return float(stock["price"])  # Convert price to float and return

  # If symbol is not found, return None
  return 0


def get_base_price(api, symbol):
  try:
    # Get the latest quote data for the symbol
    quote = api.get_last_quote(symbol)

    # Extract the price from the quote data
    base_price = float(quote.bidprice) if quote.bidprice else float(
        quote.askprice)

    return base_price
  except Exception as e:
    print(f"Error fetching base price for {symbol}: {e}")
    return 0


def buy_ioc(symbol, quantity, trading_client):
  try:
    market_order = trading_client.submit_order(
        symbol=symbol,
        qty=quantity,
        side='buy',
        time_in_force='day'
    )
    # print(f"Market order for {quantity} shares of {symbol} submitted successfully.")
    return market_order
  except Exception as e:
    print(f"Failed to submit market order. Error: {e}")
    return None

def process_one_shares(shares_dict, decided_stocks, qty="one"):
  # print("Processing shares...")
  for ticker, (share_count, total_investment) in shares_dict.items():
    # place_order = place_bracket_order_2(str(ticker), share_count,decided_stocks)
    # print(place_order)
    print("Ticker = " + str(ticker) + " Share Count = " + str(share_count))
    append_to_sequence_file(sequence_file, "Ticker = " + str(ticker) + " Share Count = " + str(share_count) + "\n")
    place_order = buy_ioc(str(ticker), share_count, trading_client)
    append_to_sequence_file(sequence_file, "Place Order = " + str(place_order))
    break
  return "Shares Processed!"

def process_shares(shares_dict, decided_stocks, qty="one"):
  for ticker, (share_count, total_investment) in shares_dict.items():
    place_order = buy_ioc(str(ticker), share_count, trading_client)
    if place_order is not None and qty == "one":
      break
  return "Shares Processed!"


def filter_stocks(json_data):
  try:
    # Parse JSON data
    data = json.loads(json_data)

    # Filter out stocks based on criteria
    filtered_stocks = []
    for stock in data["top_gainers"]:
        ticker = stock["ticker"]
        price = float(stock["price"])
        change_amount = float(stock["change_amount"])
        change_percentage = float(stock["change_percentage"].strip('%'))

        # Check if the ticker symbol contains ".A" or ".B", "+" and if price is below 30 and change amount is above or equal to 0.50,
        # and change percentage is greater than or equal to 70
        if ".A" not in ticker and ".B" not in ticker and "+" not in ticker and price <= 30 and price >= 2 and change_amount >= 0.50 and change_percentage >= 70:
            filtered_stocks.append(stock)

    # Update the JSON data with filtered stocks
    data["top_gainers"] = filtered_stocks

    return json.dumps(data, indent=4)  # Convert back to JSON format with indentation
  except json.JSONDecodeError as e:
    print("Invalid JSON data:", e)
    return None

def filter_stocks_tg_at(json_data):
  try:
    # Parse JSON data
    data = json.loads(json_data)

    # Filter out stocks based on criteria
    filtered_stocks = []
    for stock in data["top_gainers"]:
        ticker = stock["ticker"]
        price = float(stock["price"])
        change_amount = float(stock["change_amount"])
        change_percentage = float(stock["change_percentage"].strip('%'))

        # Check if the ticker symbol contains ".A" or ".B", "+" and if price is below 30 and change amount is above or equal to 0.50,
        # and change percentage is greater than or equal to 70
        if ".A" not in ticker and ".B" not in ticker and "+" not in ticker and price <= 30 and price >= .5:
            filtered_stocks.append(stock)

    # Update the JSON data with filtered stocks
    data["top_gainers"] = filtered_stocks

    return json.dumps(data, indent=4)  # Convert back to JSON format with indentation
  except json.JSONDecodeError as e:
    print("Invalid JSON data:", e)
    return None


def filter_top_gainers(json_data):
  try:
      data = json.loads(json_data)

      # Get the tickers from most_actively_traded
      most_actively_traded_tickers = {stock['ticker'] for stock in data['most_actively_traded']}
      most_gainer_traded_tickers = {stock['ticker'] for stock in data['top_gainers']}
      # Filter out top_gainers based on if ticker is in most_actively_traded
      filtered_top_gainers = [stock for stock in data['top_gainers'] if stock['ticker'] in most_actively_traded_tickers]
      # Update the JSON data with filtered top_gainers
      data['top_gainers'] = filtered_top_gainers

      return json.dumps(data, indent=4)
  except json.JSONDecodeError as e:
      print("Invalid JSON data:", e)
      return None


def check_top_gainers_exist(json_data):
  try:
      data = json.loads(json_data)
      top_gainers = data.get("top_gainers", [])
      return bool(top_gainers)  # Returns True if top_gainers list is not empty, otherwise False
  except json.JSONDecodeError as e:
      print("Invalid JSON data:", e)
      return None


def get_stock_info(stock_symbol):
    # Load the JSON data
    stock_data = json.loads(urllib.request.urlopen("https://financialmodelingprep.com/api/v3/quote/" + stock_symbol + "?apikey=JsxNLlkcPHhOmQxXh0pus71q4peJnIN0").read())
    # Find the stock information for the given symbol
    for stock in stock_data:
        if stock['symbol'] == stock_symbol:
            price = stock.get('price', 'N/A')
            change_percentage = stock.get('changesPercentage', 'N/A')
            volume = stock.get('volume', 'N/A')
            avg_volume = stock.get('avgVolume', 'N/A')
            volume_ratio = volume / avg_volume if avg_volume != 'N/A' and avg_volume != 0 else 'N/A'
            result = (f"Symbol: {stock_symbol}\n"
                      f"Price: {price}\n"
                      f"Change Percentage: {change_percentage}\n"
                      f"Volume: {volume}\n"
                      f"Average Volume: {avg_volume}\n"
                      f"Volume/Average Volume: {volume_ratio}")
            return result

def filter_decided_stocks(json_data):
  try:
      # Parse JSON data
      data = json.loads(json_data)

      # Extract top gainers
      top_gainers = data.get("top_gainers", [])

      # Create a list of strings containing stock symbols and prices
      stock_info_list = []
      for stock in top_gainers:
          symbol = stock.get("ticker", "")
          price = stock.get("price", "")
          stock_info = get_stock_info(str(symbol))
          if symbol and price:
              stock_info_list.append(stock_info + "\n")

      # Return a string with each stock symbol and price on a new line
      return '\n'.join(stock_info_list)
  except json.JSONDecodeError as e:
      print("Invalid JSON data:", e)
      return "None"

def get_stock_and_price(trading_client):
    time = time.time()###############################################################
    positions = trading_client.list_positions()

     # Loop through each open position
    if (positions):
        for position in positions:
            return position

def run_until_time_and_print_info(hour, minute, x, trading_client, sequence_file):
  current_time = datetime.now(pytz.timezone('America/New_York'))
  while int(current_time.strftime("%I")) < hour or current_time.minute < minute:
    stuff = get_stock_and_price(trading_client)
    if stuff:
        print(str(stuff.symbol) + ": Bought " + str(stuff.qty) + " at " + str(stuff.avg_entry_price) + " and is now at " + str(stuff.market_value) + " and could be sold for a market percent profit of " + str(((stuff.market_value-stuff.avg_entry_price)/stuff.avg_entry_price)*100))
        append_to_sequence_file(sequence_file, str(stuff.symbol) + ": Bought " + str(stuff.qty) + " at " + str(stuff.avg_entry_price) + " and is now at " + str(stuff.market_value) + " and could be sold for a market percent profit of " + str(((stuff.market_value-stuff.avg_entry_price)/stuff.avg_entry_price)*100))
    time.sleep(x)
    current_time = datetime.now(pytz.timezone('America/New_York'))
  print("Ended loop checking information")
  return



original_list = filter_top_gainers(str(ping_api()).replace("'", '"'))
decided_stocks = decide_stocks_tg_at(original_list)



current_time = datetime.now(pytz.timezone('America/New_York'))
hour = int(current_time.strftime("%I"))
minute = int(current_time.minute)
print("\n\nRunning at "+ str(hour) + ":" + str(minute) +"\n\n" + filter_decided_stocks(decided_stocks))

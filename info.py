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
print("Buying Power (10%): ", amount)

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


def compare_top_gainers(old_data, new_data):
  # Convert JSON strings to Python dictionaries
  old_data_dict = json.loads(old_data)
  new_data_dict = json.loads(new_data)

  # Extract lists of top gainers from both dumps
  old_gainers = old_data_dict.get("top_gainers", [])
  new_gainers = new_data_dict.get("top_gainers", [])

  # Compare the lists
  added_gainers = [stock for stock in new_gainers if stock not in old_gainers]
  removed_gainers = [
      stock for stock in old_gainers if stock not in new_gainers
  ]
  unchanged_gainers = [stock for stock in new_gainers if stock in old_gainers]

  return added_gainers, removed_gainers, unchanged_gainers


def clean_stock_data(json_dump_str):
  try:
    data = json.loads(json_dump_str)
    stocks = data.get('top_gainers', [])
    clean_data = []
    for stock in stocks:
      ticker = stock.get('ticker', '')
      price = float(stock.get('price', 0))
      change_amount = float(stock.get('change_amount', 0))
      change_percentage = 0  #float(stock.get('change_percentage', 0))
      volume = int(stock.get('volume', 0))
      clean_data.append(
          f"Ticker: {ticker}, Price: {price}, Change Amount: {change_amount}, Change Percentage: {change_percentage}%, Volume: {volume}"
      )
    return '\n'.join(clean_data)
  except json.JSONDecodeError as e:
    print("Error decoding JSON in 2:", e)
    return "Error decoding JSON in 2"


count = 0
data_list = [ra, rb, rc, rd, re]


def get_next_set():
  global count
  if count >= len(data_list):
    return data_list[-1]
  else:
    count += 1
    return data_list[count - 1]


def wait_until_start(hour, minute):
  current_time = datetime.now(pytz.timezone('America/New_York'))
  while int(
      current_time.strftime("%I")) < hour or current_time.minute < minute:
    time.sleep(1)  # Wait for 1 minute
    current_time = datetime.now(pytz.timezone('America/New_York'))


def do_something_every_2_seconds_until_start(hour, minute):
  current_time = datetime.now(pytz.timezone('America/New_York'))
  while int(
      current_time.strftime("%I")) <= hour and current_time.minute < minute:
    time.sleep(1)
    current_time = datetime.now(pytz.timezone('America/New_York'))


def decide_stocks(stocks):
  #for now, we'll just keep the ones from the stock, maybe we'll make sure the stocks are under $15 or something
  return filter_stocks(stocks)

def decide_stocks_tg_at(stocks):
  #for now, we'll just keep the ones from the stock, maybe we'll make sure the stocks are under $15 or something
  return filter_stocks_tg_at(stocks)

def dict_of_stocks_and_quantity(stocks):
  return stocks


def buy_stocks_sym_quantity(stocks):
  return stocks  #start market orders


def sell_stocks_market_price(stocks):
  return stocks


def check_if_weekday_and_not_holiday_andsotcks_are_active_and_between_right_time(
):
  return False


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




def filter_active_stocks(json_data):
  try:
      # Parse JSON data
      data = json.loads(json_data)

      # Filter out stocks based on criteria
      filtered_stocks = []
      for stock in data["most_actively_traded"]:
          ticker = stock["ticker"]
          price = float(stock["price"])

          # Add stock symbol and price to the filtered list
          filtered_stocks.append(f"{ticker}: ${price:.2f}")

      # Return the list of filtered stocks as a neat string
      return '\n'.join(filtered_stocks)

  except json.JSONDecodeError as e:
      print("Invalid JSON data:", e)
      return None
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


def check_api_for_a_minute(hour, minute, dur):
  #checks api for a minute and uses "filter_stocks" function and returns final list
  # current_time = time.localtime()
  current_time = datetime.now(pytz.timezone('America/New_York'))
  original_list = str(ping_api()).replace(
      "'", '"')  #first api call - implement here
  while int(
      current_time.strftime("%I")) < hour or current_time.minute < minute:
    new_list = str(ping_api()).replace("'", '"')  #update to function here
    original_list = filter_common_tickers(original_list, new_list)
    time.sleep(dur)
    # print("sleeping because " + str(int(current_time.strftime("%I"))) + "<" + str(hour) + " or " + str(current_time.minute) + "<" + str(minute))
    current_time = datetime.now(pytz.timezone('America/New_York'))
  return original_list


def run_for_x_seconds_and_keep_same(x):
  start_time = time.time()  # Get the current time
  original_list = str(ping_api()).replace(
      "'", '"')  #first api call - implement here
  # Run the loop for one minute
  while time.time() - start_time < x:
    new_list = str(ping_api()).replace("'", '"')  #update to function here
    original_list = filter_common_tickers(original_list, new_list)
    # Your code goes here
    time.sleep(1)  # Optional: Sleep for 1 second in each iteration
  return original_list


def calculate_shares_good(json_dump, total_amount):
  # Load JSON data
  data = json.loads(json_dump)

  # Initialize dictionary to store stock symbol, number of shares, and total investment
  shares_dict = {}

  # Calculate total number of stocks
  num_stocks = len(data["top_gainers"])

  # Calculate amount per stock (equal allocation)
  amount_per_stock = total_amount / num_stocks

  # Calculate shares and investment for each stock
  for stock in data["top_gainers"]:
    ticker = stock["ticker"]
    price = float(stock["price"])

    # Calculate the number of shares based on the equal allocation
    share_count = int(amount_per_stock / price)

    # Calculate total investment for this stock
    total_investment = share_count * price

    # Add the ticker, shares, and total investment to the dictionary
    shares_dict[ticker] = (share_count, total_investment)

  return shares_dict


def calculate_shares_good_for_one(json_dump, total_amount):
  # Load JSON data
  data = json.loads(json_dump)

  # Initialize dictionary to store stock symbol, number of shares, and total investment
  shares_dict = {}

  # Calculate total number of stocks
  num_stocks = len(data["top_gainers"])

  # Calculate amount per stock (equal allocation)
  amount_per_stock = total_amount

  # Calculate shares and investment for each stock
  for stock in data["top_gainers"]:
    ticker = stock["ticker"]
    price = float(stock["price"])

    # Calculate the number of shares based on the equal allocation
    share_count = int(amount_per_stock / price)

    # Calculate total investment for this stock
    total_investment = share_count * price

    # Add the ticker, shares, and total investment to the dictionary
    shares_dict[ticker] = (share_count, total_investment)

  return shares_dict


def buy_order(symbol, quantity):
  market_order_data = MarketOrderRequest(symbol=symbol,
                                         qty=quantity,
                                         side=OrderSide.BUY,
                                         time_in_force=TimeInForce.DAY)

  # Market order
  market_order = trading_client.submit_order(order_data=market_order_data)
  return market_order


def place_bracket_order_outdated(symbol, quantity, limit_price, api):
  # Calculate take-profit and stop-loss prices
  take_profit_price = limit_price * 1.01  # 1% higher than the limit price
  stop_loss_price = limit_price * 0.99  # 1% lower than the limit price

  # Place the bracket order
  order = api.submit_order(symbol=symbol,
                           qty=quantity,
                           side='buy',
                           type='limit',
                           time_in_force='gtc',
                           limit_price=limit_price,
                           order_class='bracket',
                           take_profit=dict(limit_price=take_profit_price),
                           stop_loss=dict(stop_price=stop_loss_price))

  return order


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


def place_bracket_order_2(symbol, quantity, decided_stocks):#####################################################
  try:
    limit_price = float(round(get_current_price(symbol, decided_stocks), 2))
    # print("Sym: " + symbol + " Qty: " + str(quantity) + " Limit: " + str(limit_price))
    m_order = MarketOrderRequest(
        symbol=symbol,
        qty=quantity,
        side=OrderSide.BUY,
        time_in_force=TimeInForce.DAY,
        order_class=OrderClass.BRACKET,
        take_profit={'limit_price': round(limit_price * 1.02, 2)},
        stop_loss={
            'stop_price': round(limit_price * 0.98, 2),
            'limit_price': round(limit_price * 0.97, 2)
        })

    order = trading_client.submit_order(order_data=m_order)
    return order
  except Exception as e:
    return 404


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
    return "Would've bought.....Ticker = " + str(ticker) + " Share Count = " + str(share_count)


def process_shares(shares_dict, decided_stocks, qty="one"):
  for ticker, (share_count, total_investment) in shares_dict.items():
    place_order = buy_ioc(str(ticker), share_count, trading_client)
    if place_order is not None and qty == "one":
      break
  return "Shares Processed!"


def get_accepted_orders(api):
  try:
    # Fetch all orders
    orders = api.list_orders()

    # Filter accepted orders
    accepted_orders = [order for order in orders if order.status == 'accepted']

    return accepted_orders
  except Exception as e:
    print("Error fetching accepted orders:", e)
    return None


def summarize_accepted_orders(accepted_orders):
  stock_summary = {}
  if (accepted_orders):

    for order in accepted_orders:
      symbol = order.symbol
      qty = int(order.qty)
      if symbol in stock_summary:
        stock_summary[symbol] += qty
      else:
        stock_summary[symbol] = qty

    summary_string = "Stock Orders Placed:\n"
    # Reverse the order of stocks being added
    for symbol, qty in reversed(stock_summary.items()):
      summary_string += f"{symbol}: {qty} shares\n"

    return summary_string


def cancel_all_positions(trading_client):
  # Retrieve all open positions
  positions = trading_client.list_positions()

  # Cancel each open position
  for position in positions:
    # print(position)
    symbol = position.symbol
    try:
      trading_client.close_position(symbol)
      # print(f"Position for {symbol} has been closed.")
    except Exception as e:
      print(f"Failed to close position for {symbol}. Error: {e}")


def close_positions_with_limit_order(trading_client):
  # Retrieve all open positions
  positions = trading_client.list_positions()

  # Loop through each open position
  if (positions):
    for position in positions:
      symbol = position.symbol
      quantity = position.qty
      current_price = str(position.current_price)

      # Get the price the stock was bought for
      bought_price = float(position.avg_entry_price)
      # print(bought_price + " bought price")
      # Calculate the limit price 2% above the bought price
      limit_price = round(bought_price * 1.02, 2)

      # Place a limit order 2% above the bought price
      try:
        market_order = trading_client.submit_order(
            symbol=symbol,
            qty=quantity,
            side='sell',  # or OrderSide.SELL for sell orders
            type= 'limit',
            time_in_force='day',  # or any other TimeInForce option
            limit_price=limit_price
            )

        # Submit market order
        #market_order = trading_client.submit_order(order_data=market_order_data)

        # print(market_order)
        print(
            f"Limit order placed for {symbol} at {limit_price} and current price is {current_price}."
        )
        append_to_sequence_file(sequence_file, f"Limit order placed for {symbol} at {limit_price} and current price is {current_price}." + "\n")
      except Exception as e:
        print(f"Failed to place limit order for {symbol}. Error: {e}")


def get_bought_price(trading_client, symbol):
  market_price = trading_client.get_last_trade(symbol).price
  return market_price


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


def run_for_x_seconds_and_match_tg_and_at(hour, minute, second, x):
  original_list = str(ping_api()).replace("'", '"')  #first api call - implement here
  # Run the loop for one minute
  current_time = datetime.now(pytz.timezone('America/New_York'))
  while int(current_time.strftime("%I")) < hour or current_time.minute < minute or (current_time.minute <= minute and current_time.second < second):
    new_list = str(ping_api()).replace("'", '"')  #update to function here
    original_list = filter_top_gainers(new_list)
    # Your code goes here
    time.sleep(x)  # Optional: Sleep for 1 second in each iteration
    current_time = datetime.now(pytz.timezone('America/New_York'))
  return original_list



def check_top_gainers_exist(json_data):
  try:
      data = json.loads(json_data)
      top_gainers = data.get("top_gainers", [])
      return bool(top_gainers)  # Returns True if top_gainers list is not empty, otherwise False
  except json.JSONDecodeError as e:
      print("Invalid JSON data:", e)
      return None


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
          if symbol and price:
              stock_info_list.append(f"{symbol}: ${price}")

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

def wait_until_start(hour, minute, second):
  current_time = datetime.now(pytz.timezone('America/New_York'))
  while int(current_time.strftime("%I")) < hour or current_time.minute < minute or (current_time.minute <= minute and current_time.second < second):
    time.sleep(1)  # Wait for 1 second
    current_time = datetime.now(pytz.timezone('America/New_York'))

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



current_time = datetime.now(pytz.timezone('America/New_York'))
# int(current_time.strftime("%I")) >= hour AND current_time.minute >= minute

hour = 9
minute = 30

print("Waiting until " + str(hour) + ":" + str(minute))


wait_until_start(hour, minute, 0)
original_list = filter_top_gainers(str(ping_api()).replace("'", '"'))
decided_stocks = decide_stocks_tg_at(original_list)
if check_top_gainers_exist(decided_stocks):
  print("\n\n\n################################################################\nTop Gainers Exist from Cross Reference")
else:
  print("\n\n\n################################################################\nTop Gainers do not exist from Cross Reference")
  decided_stocks = decide_stocks(run_for_x_seconds_and_keep_same(5))
order = process_one_shares(calculate_shares_good_for_one(decided_stocks, amount), decided_stocks)
print("Running at "+ str(datetime.now(pytz.timezone('America/New_York'))) +"\n" + order + "\n" + filter_decided_stocks(decided_stocks))




wait_until_start(hour, minute, 30)
original_list = filter_top_gainers(str(ping_api()).replace("'", '"'))
decided_stocks = decide_stocks_tg_at(original_list)
if check_top_gainers_exist(decided_stocks):
  print("\n\n\n################################################################\nTop Gainers Exist from Cross Reference")
else:
  print("\n\n\n################################################################\nTop Gainers do not exist from Cross Reference")
  decided_stocks = decide_stocks(run_for_x_seconds_and_keep_same(5))
order = process_one_shares(calculate_shares_good_for_one(decided_stocks, amount), decided_stocks)
print("Running at "+ str(datetime.now(pytz.timezone('America/New_York'))) +"\n" + order + "\n" + filter_decided_stocks(decided_stocks))




wait_until_start(hour, minute + 1, 0)
original_list = filter_top_gainers(str(ping_api()).replace("'", '"'))
decided_stocks = decide_stocks_tg_at(original_list)
if check_top_gainers_exist(decided_stocks):
  print("\n\n\n################################################################\nTop Gainers Exist from Cross Reference")
else:
  print("\n\n\n################################################################\nTop Gainers do not exist from Cross Reference")
  decided_stocks = decide_stocks(run_for_x_seconds_and_keep_same(5))
order = process_one_shares(calculate_shares_good_for_one(decided_stocks, amount), decided_stocks)
print("Running at "+ str(datetime.now(pytz.timezone('America/New_York'))) +"\n" + order + "\n" + filter_decided_stocks(decided_stocks))



wait_until_start(hour, minute + 1, 30)
original_list = filter_top_gainers(str(ping_api()).replace("'", '"'))
decided_stocks = decide_stocks_tg_at(original_list)
if check_top_gainers_exist(decided_stocks):
  print("\n\n\n################################################################\nTop Gainers Exist from Cross Reference")
else:
  print("\n\n\n################################################################\nTop Gainers do not exist from Cross Reference")
  decided_stocks = decide_stocks(run_for_x_seconds_and_keep_same(5))
order = process_one_shares(calculate_shares_good_for_one(decided_stocks, amount), decided_stocks)
print("Running at "+ str(datetime.now(pytz.timezone('America/New_York'))) +"\n" + order + "\n" + filter_decided_stocks(decided_stocks))



wait_until_start(hour, minute + 2, 0)
original_list = filter_top_gainers(str(ping_api()).replace("'", '"'))
decided_stocks = decide_stocks_tg_at(original_list)
if check_top_gainers_exist(decided_stocks):
  print("\n\n\n################################################################\nTop Gainers Exist from Cross Reference")
else:
  print("\n\n\n################################################################\nTop Gainers do not exist from Cross Reference")
  decided_stocks = decide_stocks(run_for_x_seconds_and_keep_same(5))
order = process_one_shares(calculate_shares_good_for_one(decided_stocks, amount), decided_stocks)
print("Running at "+ str(datetime.now(pytz.timezone('America/New_York'))) +"\n" + order + "\n" + filter_decided_stocks(decided_stocks))




wait_until_start(hour, minute + 2, 30)
original_list = filter_top_gainers(str(ping_api()).replace("'", '"'))
decided_stocks = decide_stocks_tg_at(original_list)
if check_top_gainers_exist(decided_stocks):
  print("\n\n\n################################################################\nTop Gainers Exist from Cross Reference")
else:
  print("\n\n\n################################################################\nTop Gainers do not exist from Cross Reference")
  decided_stocks = decide_stocks(run_for_x_seconds_and_keep_same(5))
order = process_one_shares(calculate_shares_good_for_one(decided_stocks, amount), decided_stocks)
print("Running at "+ str(datetime.now(pytz.timezone('America/New_York'))) +"\n" + order + "\n" + filter_decided_stocks(decided_stocks))




wait_until_start(hour, minute + 3, 0)
original_list = filter_top_gainers(str(ping_api()).replace("'", '"'))
decided_stocks = decide_stocks_tg_at(original_list)
if check_top_gainers_exist(decided_stocks):
  print("\n\n\n################################################################\nTop Gainers Exist from Cross Reference")
else:
  print("\n\n\n################################################################\nTop Gainers do not exist from Cross Reference")
  decided_stocks = decide_stocks(run_for_x_seconds_and_keep_same(5))
order = process_one_shares(calculate_shares_good_for_one(decided_stocks, amount), decided_stocks)
print("Running at "+ str(datetime.now(pytz.timezone('America/New_York'))) +"\n" + order + "\n" + filter_decided_stocks(decided_stocks))



wait_until_start(hour, minute + 3, 30)
original_list = filter_top_gainers(str(ping_api()).replace("'", '"'))
decided_stocks = decide_stocks_tg_at(original_list)
if check_top_gainers_exist(decided_stocks):
  print("\n\n\n################################################################\nTop Gainers Exist from Cross Reference")
else:
  print("\n\n\n################################################################\nTop Gainers do not exist from Cross Reference")
  decided_stocks = decide_stocks(run_for_x_seconds_and_keep_same(5))
order = process_one_shares(calculate_shares_good_for_one(decided_stocks, amount), decided_stocks)
print("Running at "+ str(datetime.now(pytz.timezone('America/New_York'))) +"\n" + order + "\n" + filter_decided_stocks(decided_stocks))



wait_until_start(hour, minute + 4, 0)
original_list = filter_top_gainers(str(ping_api()).replace("'", '"'))
decided_stocks = decide_stocks_tg_at(original_list)
if check_top_gainers_exist(decided_stocks):
  print("\n\n\n################################################################\nTop Gainers Exist from Cross Reference")
else:
  print("\n\n\n################################################################\nTop Gainers do not exist from Cross Reference")
  decided_stocks = decide_stocks(run_for_x_seconds_and_keep_same(5))
order = process_one_shares(calculate_shares_good_for_one(decided_stocks, amount), decided_stocks)
print("Running at "+ str(datetime.now(pytz.timezone('America/New_York'))) +"\n" + order + "\n" + filter_decided_stocks(decided_stocks))





wait_until_start(hour, minute + 4, 30)
original_list = filter_top_gainers(str(ping_api()).replace("'", '"'))
decided_stocks = decide_stocks_tg_at(original_list)
if check_top_gainers_exist(decided_stocks):
  print("\n\n\n################################################################\nTop Gainers Exist from Cross Reference")
else:
  print("\n\n\n################################################################\nTop Gainers do not exist from Cross Reference")
  decided_stocks = decide_stocks(run_for_x_seconds_and_keep_same(5))
order = process_one_shares(calculate_shares_good_for_one(decided_stocks, amount), decided_stocks)
print("Running at "+ str(datetime.now(pytz.timezone('America/New_York'))) +"\n" + order + "\n" + filter_decided_stocks(decided_stocks))





wait_until_start(hour, minute + 5, 0)
original_list = filter_top_gainers(str(ping_api()).replace("'", '"'))
decided_stocks = decide_stocks_tg_at(original_list)
if check_top_gainers_exist(decided_stocks):
  print("\n\n\n################################################################\nTop Gainers Exist from Cross Reference")
else:
  print("\n\n\n################################################################\nTop Gainers do not exist from Cross Reference")
  decided_stocks = decide_stocks(run_for_x_seconds_and_keep_same(5))
order = process_one_shares(calculate_shares_good_for_one(decided_stocks, amount), decided_stocks)
print("Running at "+ str(datetime.now(pytz.timezone('America/New_York'))) +"\n" + order + "\n" + filter_decided_stocks(decided_stocks))


print("\n\n############################################\nFinished\n###############################################\n\n")

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




with open('api_key.txt', 'r') as file:
    api_key = file.read().strip()




######################################################################################################################################################################################################################################Change back
API_KEY = api_key
API_SECRET = "zKI0mEDbOilpekjPsZ7rOyjSMcT6HpjcRjD0VJh3"
#API_KEY = 'PKOHFJJ9MRD1MEV1GETG'
#API_SECRET = "aYHkc8x4p0BxMdWJd6hsxmAm0eGi6pgIHCiuvTB3"
#APCA_API_BASE_URL = 'https://api.alpaca.markets'
APCA_API_BASE_URL = 'https://paper-api.alpaca.markets/v2'  # Paper trading endpoint
def move_files_except(filename):
  if not os.path.exists('old_records'):
      os.makedirs('old_records')
  files = os.listdir('.')
  for file in files:
      if file != filename and os.path.isfile(file):
          shutil.move(file, os.path.join('old_records', file))
#move_files_except('dwight_v1_dev.py')
sequence_file = "sequence_terminate_" + str(time.localtime().tm_mon) + "_" + str(time.localtime().tm_mday) + "_" + str(time.localtime().tm_hour) + "_" + str(time.localtime().tm_min) + ".txt"
api_file = "api_terminate_" + str(time.localtime().tm_mon) + "_" + str(time.localtime().tm_mday) + "_" + str(time.localtime().tm_hour) + "_" + str(time.localtime().tm_min) + ".txt"
trading_client = tradeapi.REST(API_KEY, API_SECRET)
def append_to_sequence_file(filename, content):
  print('not applicable')
  # try:
  #     with open(filename, 'a') as file:
  #         file.write(content + '\n')  # Append the content to the file
  #         # print("Content appended to", filename)
  # except FileNotFoundError:
  #     print("File not found:", filename)
  # except Exception as e:
  #     print("An error occurred:", e)


def append_to_api_file(filename, content):
  print('not applicable')
  # try:
  #     with open(filename, 'a') as file:  # Open the file in append mode
  #         file.write(content + '\n')  # Append the content to the file
  #         # print("Content appended to", filename)
  # except FileNotFoundError:
  #     print("File not found:", filename)
  # except Exception as e:
  #     print("An error occurred:", e)


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
######################################################################################################################################################################################################################################Change back


open_positions = trading_client.list_positions()
append_to_sequence_file(sequence_file, "Open Positions before closing:\n" + str(open_positions) + "\n")
print("Open Positions before closing:\n" + str(open_positions) + "\n")
print("Closing all positions")
##########################################################cancel_all_positions(trading_client)
time.sleep(3)
open_positions = trading_client.list_positions()
append_to_sequence_file(sequence_file, "Open Positions after closing:\n" + str(open_positions) + "\n")
print("Closing Machine")
print()
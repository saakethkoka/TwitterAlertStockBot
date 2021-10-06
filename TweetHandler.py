import json
import order_manager
import time
from twilio_config import send_message
from params import *


def send_order(ticker, amount):
    try:
        order_id = order_manager.send_limit_buy_order(ticker, amount)
    except:
        return
    time.sleep(1)
    for i in range(0, 4):
        if order_manager.order_is_filled(order_id):
            break
        order_manager.cancel_order(order_id)
        order_id = order_manager.send_limit_buy_order(ticker, amount)
        time.sleep(.1)
    order_manager.cancel_order(order_id)
    try:
        num_shares = order_manager.get_num_shares(order_id)
        try:
            order_manager.set_oco_sell_order(ticker, num_shares, stop_loss_percent, limit_up_percent)
        except:
            send_message(ticker + ": Failed to set OCO sell order")
    except:
        return


def handleTweet(raw_data):
    json_data = json.loads(raw_data)

    try:
        if json_data["user"]["id"] != "373620043":
            return
    except:
        return



    tickers = json_data["entities"]["symbols"]
    ticker_list = []
    for item in tickers:
        ticker_list.append(item['text'].upper())
    with open('mention_list.txt', 'r') as f:
        mention_list = f.readlines()
        for i in range(0, len(mention_list)):
            mention_list[i] = mention_list[i].strip()

    for ticker in ticker_list:
        if not ticker in mention_list:
            send_message("New ticker tweeted, attempting to bid... " + ticker)
            send_order(ticker, amount_per_trade) # Amount of $ to trade
            mention_list.append(ticker)
            with open('mention_list.txt', 'w') as f:
                for item in mention_list:
                    f.writelines(item + '\n')

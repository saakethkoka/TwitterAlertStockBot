import order_manager
import time
from twilio_config import send_message
from params import *
from logging_config import logger


def send_order(ticker, amount):
    try:
        order_id = order_manager.send_limit_buy_order(ticker, amount)
    except Exception as e:
        logger.error(e)
        return
    time.sleep(1)
    for i in range(0, 4):
        if order_manager.order_is_filled(order_id):
            logger.info("Order filled: " + ticker + " " + str(order_id))
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
            logger.error("Could not set OCO sell order")
            send_message(ticker + ": Failed to set OCO sell order")
    except:
        logger.error("Could not fill order")
        return


def handleTweet(raw_data):
    json_data = json.loads(raw_data)
    try:
        logger.info("Tweet: " + json_data['text'])
    except:
        return

    try:
        if json_data["user"]["id"] != user_id_number:
            return
    except:
        return



    tickers = json_data["entities"]["symbols"]
    ticker_list = []
    for item in tickers:
        ticker_list.append(item['text'].upper())
    with open('src/mention_list.txt', 'r') as f:
        mention_list = f.readlines()
        for i in range(0, len(mention_list)):
            mention_list[i] = mention_list[i].strip()




    for ticker in ticker_list:
        if not ticker in mention_list:
            fundamental_data = order_manager.c.search_instruments(ticker, projection=order_manager.c.Instrument.Projection.FUNDAMENTAL).json()
            if fundamental_data[ticker]["fundamental"]["marketCap"] > market_cap_threshold:
                logger.info("Market cap of " + ticker + " is greater than " + str(market_cap_threshold))
                return
            send_message("New ticker tweeted, attempting to bid... " + ticker)
            send_order(ticker, amount_per_trade) # Amount of $ to trade
            mention_list.append(ticker)
            with open('src/mention_list.txt', 'w') as f:
                for item in mention_list:
                    f.writelines(item + '\n')
        else:
            logger.info("Already mentioned: " + ticker)
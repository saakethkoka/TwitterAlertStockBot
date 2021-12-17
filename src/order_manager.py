import TDA_config
from tda.orders.equities import equity_buy_limit
from tda.orders.common import Duration, Session
from tda.utils import Utils
from tda import auth

# Authenticating
try:
    c = auth.client_from_token_file(TDA_config.token_path, TDA_config.api_key)
except FileNotFoundError:
    from selenium import webdriver
    with webdriver.Chrome(executable_path='/chromedriver') as driver:
        c = auth.client_from_login_flow(
            driver, TDA_config.api_key, TDA_config.redirect_uri, TDA_config.token_path)

# Sends a buy order to the TDA API for a number of shares which does not exceed the max_amount of $
def send_limit_buy_order(ticker, max_amount):
    price = c.get_quote(ticker).json()[ticker]["askPrice"]
    # Calcualting how many shares
    num_shares = (int)(max_amount/price)
    # If price exceeds max amount willing to trade, then order is skipped
    if num_shares == 0:
        raise Exception('Share price greater than max_amount')
    # Sending order
    builder = equity_buy_limit(ticker, num_shares, price)
    builder.set_duration(Duration.GOOD_TILL_CANCEL)
    builder.set_session(Session.SEAMLESS)
    response = c.place_order(TDA_config.client_id, builder.build())
    return Utils(c, TDA_config.client_id).extract_order_id(response)

# Sets a trailing stop order for a given ticker
def set_trailing_stop(ticker, num_shares, percent_change):
    order = {
        "complexOrderStrategyType": "NONE",
        "orderType": "TRAILING_STOP",
        "session": "NORMAL",
        "stopPriceLinkBasis": "BID",
        "stopPriceLinkType": "PERCENT",
        "stopPriceOffset": percent_change,
        "duration": "GOOD_TILL_CANCEL",
        "orderStrategyType": "SINGLE",
        "orderLegCollection": [
            {
                "instruction": "SELL",
                "quantity": num_shares,
                "instrument": {
                    "symbol": ticker,
                    "assetType": "EQUITY"
                }
            }
        ]
    }
    response = c.place_order(TDA_config.client_id, order)
    return Utils(c, TDA_config.client_id).extract_order_id(response)

# Sets a trailing stop and a limit order for a given ticker
def set_oco_sell_order(ticker, num_shares, percent_loss, percent_gain):
    curr_price = c.get_quote(ticker).json()[ticker]["bidPrice"]
    target_price = (1 + percent_gain/100) * curr_price
    target_price = round(target_price, 2)
    order = {
        "orderStrategyType": "OCO",
        "childOrderStrategies": [
            {
                "orderType": "LIMIT",
                "session": "NORMAL",
                "price": target_price,
                "duration": "GOOD_TILL_CANCEL",
                "orderStrategyType": "SINGLE",
                "orderLegCollection": [
                    {
                        "instruction": "SELL",
                        "quantity": num_shares,
                        "instrument": {
                            "symbol": ticker,
                            "assetType": "EQUITY"
                        }
                    }
                ]
            },
            {
                "complexOrderStrategyType": "NONE",
                "orderType": "TRAILING_STOP",
                "session": "NORMAL",
                "stopPriceLinkBasis": "BID",
                "stopPriceLinkType": "PERCENT",
                "stopPriceOffset": percent_loss,
                "duration": "GOOD_TILL_CANCEL",
                "orderStrategyType": "SINGLE",
                "orderLegCollection": [
                    {
                        "instruction": "SELL",
                        "quantity": num_shares,
                        "instrument": {
                            "symbol": ticker,
                            "assetType": "EQUITY"
                        }
                    }
                ]
            }
        ]
    }
    response = c.place_order(TDA_config.client_id, order)
    return Utils(c, TDA_config.client_id).extract_order_id(response)

def cancel_order(order_id):
    c.cancel_order(order_id, TDA_config.client_id)

def get_num_shares(order_id):
    return c.get_order(order_id, TDA_config.client_id).json()["filledQuantity"]

def order_is_filled(order_id):
    return c.get_order(order_id, TDA_config.client_id).json()["status"] == "FILLED"
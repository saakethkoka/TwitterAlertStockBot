# TwitterAlertStockBot
This bot will execute buy orders on a stock when it gets newly mentioned by a specific 
Twitter account. 

The bot takes a list of params which can be modified in the params.py file:

1. user_to_track: The Twitter account to track.
2. market_cap_threshold: The minimum market cap of the stock to execute a buy order.
3. amount_to_trade: The amount of the stock to trade.
4. stop_loss_percentage: The percentage of the current price to set the stop loss. (Where to cut losses)
5. limit_up_percentage: The percentage of the current price to set the limit sell order. (Where to take profits)


## Requirements

1. TD Ameritrade account: https://www.tdameritrade.com ($500 minimum funding)
2. TD Ameritrade developer account: https://developer.tdameritrade.com/ (Free with TD Ameritrade account)
Make sure you create an app with permissions to execute trades.
3. Twitter developer account: https://developer.twitter.com/en (Free)
4. Twilio account: https://www.twilio.com/ (Free trial account is sufficient)

## Installation

1. Clone the repository:
```
git clone https://github.com/saakethkoka/TwitterAlertStockBot.git
```
2. Install the requirements:
```
pip install -r requirements.txt
```

## Configuration

1. Create a TDA_config.py file in /src with the following contents:
```python
token_path = 'src/token.json'
api_key = '<your_api_key>'
redirect_uri = 'http://localhost/'
client_id = '<your_client_id>'
```
2. Create a twilio_config.py file in /src with the following contents:
```python
from twilio.rest import Client

account_sid = '<your_account_sid>' # Modify this
auth_token = '<your_auth_token>' # Modify this
client = Client(account_sid, auth_token)

def send_message(message_text):
    message = client.messages.create(
        body= message_text,
        from_='<from number supplied from twilio>', # Modify this
        to='<your phone number>' # Modify this
    )
    print(message.sid)
```

3. Create a twitter_config.py file in /src with the following contents:
```python
import tweepy

consumer_key = '<your_consumer_key>' # Modify this
consumer_secret = '<your_consumer_secret>' # Modify this
access_token = '<your_access_token>' # Modify this
access_token_secret = '<your_access_token_secret>' # Modify this

auth = tweepy.OAuthHandler(consumer_key=consumer_key, consumer_secret=consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth, wait_on_rate_limit_notify=True)
```

4. Download a chromedriver that works for your browser. You can check your
browser's version by going to chrome://version in chrome.
https://sites.google.com/chromium.org/driver/
Place the chromedriver executable in /src.

# Running

```
python src/TweetListener.py
```

The first time you run the bot, you will need to authorize the bot to access your
tdameritrade account. The bot will open up a browser and ask you to authorize by
logging into the account and verifiying with your phone.

Once this is done, the bot will store the credentials in a file called
token.json in /src. TD Amertirade says these credentials will be valid for only 90
days but I have had no issue using them for longer than that. If you have a problem 
with the credentials, you can refresh them by deleting the token.json file and re-running
the bot which will restart the authorization process.

In order to have the proper functionality, you should run the stock_mentions_tracker
script in parallel with the bot:
```
python src/stock_mentions_tracker.py
```

In order to run these bots in detached mode and
not have to worry about terminating them when closing the shell, you
can use nohup:
```
nohup python src/TweetListener.py &
nohup python src/stock_mentions_tracker.py &
```
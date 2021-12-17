from twitter_cred import *
import json

# Which Twitter user to track
user_to_track = "elonmusk"
# Dont change this line if you don't intend to modify functionality
user_id_number = api.get_user(user_to_track).id

# Maximum Market Cap stock to buy (Millions)
market_cap_threshold = 1000

# $ amount towards each trade
amount_per_trade = 300

# % loss to sell at
stop_loss_percent = 3

# % gain to sell at
limit_up_percent = 7
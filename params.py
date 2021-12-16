from twitter_cred import *
import json
# Which Twitter user to track
user_to_track = "SaakethKoka"
user_id_number = api.get_user(user_to_track).id

# $ amount towards each trade
amount_per_trade = 2

# % loss to sell at
stop_loss_percent = 3

# % gain to sell at
limit_up_percent = 3
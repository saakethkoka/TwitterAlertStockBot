from twitter_cred import *
import json
import time


def run_track_mentions():
    while(True):
        i = 0
        with open('mention_list.txt', 'r') as f:
            mention_list = f.readlines()
            for i in range(0, len(mention_list)):
                mention_list[i] = mention_list[i].strip()
        print(mention_list)
    
    
        for status in tweepy.Cursor(api.user_timeline, screen_name='MrZackMorris', tweet_mode="extended").items():
            print(status.created_at, status.entities["symbols"], i)
            for ticker in status.entities["symbols"]:
                ticker = ticker["text"].upper()
                if not ticker in mention_list:
                    mention_list.append(ticker)
                    print(mention_list)
            time.sleep(.1)
            i += 1
    
    
        with open('mention_list.txt', 'w') as f:
            for item in mention_list:
                f.writelines(item + '\n')
        
        time.sleep(1800)

run_track_mentions()
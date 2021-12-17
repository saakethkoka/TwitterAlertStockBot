from twitter_cred import *
import time
from params import *
import logging


def run_track_mentions(screen_name):
    maxTweetsParsed = 0
    while(True):
        i = 0
        with open('src/mention_list.txt', 'r') as f:
            mention_list = f.readlines()
            for i in range(0, len(mention_list)):
                mention_list[i] = mention_list[i].strip()
    
        for status in tweepy.Cursor(api.user_timeline, screen_name=screen_name, tweet_mode="extended").items():
            if status.full_text[0] == 'R' and status.full_text[1] == 'T':
                continue
            for ticker in status.entities["symbols"]:
                ticker = ticker["text"].upper()
                if not ticker in mention_list:
                    mention_list.append(ticker)
            time.sleep(.1)
            i += 1

        with open('src/mention_list.txt', 'w') as f:
            for item in mention_list:
                f.writelines(item + '\n')

        if i > maxTweetsParsed:
            maxTweetsParsed = i
            logging.info("Max Tweets Parsed by Stock Mentions Tracker:", maxTweetsParsed)
        time.sleep(1800)

run_track_mentions(user_to_track)
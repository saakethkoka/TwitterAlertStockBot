from twitter_cred import *
import json
import time


def run_track_mentions():
    maxTweetsParsed = 0
    while(True):
        i = 0
        with open('mention_list.txt', 'r') as f:
            mention_list = f.readlines()
            for i in range(0, len(mention_list)):
                mention_list[i] = mention_list[i].strip()
    
        for status in tweepy.Cursor(api.user_timeline, screen_name='MrZackMorris', tweet_mode="extended").items():
            if status.full_text[0] == 'R' and status.full_text[1] == 'T':
                continue
            for ticker in status.entities["symbols"]:
                ticker = ticker["text"].upper()
                if not ticker in mention_list:
                    mention_list.append(ticker)
            time.sleep(.1)
            i += 1
    

        with open('mention_list.txt', 'w') as f:
            for item in mention_list:
                f.writelines(item + '\n')

        if i > maxTweetsParsed:
            maxTweetsParsed = i
            print("Max Tweets Parsed by Stock Mentions Tracker:", maxTweetsParsed)
        time.sleep(1800)

run_track_mentions()
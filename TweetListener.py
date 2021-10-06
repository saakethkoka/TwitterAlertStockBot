from TweetHandler import handleTweet
from twitter_cred import *
from twilio_config import send_message


class MaxListener(tweepy.StreamListener):

    def on_data(self, raw_data):
        self.process_data(raw_data)
        return True

    def process_data(self, raw_data):
        print(raw_data)
        handleTweet(raw_data)

    def on_error(self, status_code):
        if status_code == 420:
            send_message("Twitter Listener lost connection, Killing Script")
            return False

class MaxStream():

    def __init__(self, auth, listener):
        self.stream = tweepy.Stream(auth=auth, listener=listener)

    def start(self):
        self.stream.filter(follow=['373620043'])

if __name__ == '__main__':

    listener = MaxListener()

    print(api.get_user('MrZackMorris'))

    stream = MaxStream(auth, listener)
    stream.start()



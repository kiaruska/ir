#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import gzip
import codecs
import re
import os
import time
import sys

class TweetParser(object):

    def __init__(self, filename):
       self.filename = filename
       #name, ext = os.path.splitext(self.filename)
       self.list_filename = self.filename + ".list"
       self.text_filename = self.filename + ".text"
       self.tweet_set = set()

    def extract_tweets(self, jason_user):
        user = jason_user['user']
        tweets = []
        for tweet in jason_user['tweets']:
            tweet_time_str = "%a %b %d %H:%M:%S +0000 %Y"
            tweet_time = time.strptime(tweet['created_at'], tweet_time_str)
            epoch = int(time.mktime(tweet_time))
            tweets.append( (tweet['id_str'], epoch, tweet['text']) )
        return user, tweets

    def correct_text(self, text):
        """Cleans the text"""
        text = " ".join(text.splitlines()) # split text
        text = text.strip() # remove trailing spaces
        text = re.sub("http\:\S*", " ", text) # remove http://X
        text = re.sub("#", ' ', text) # remove hashes
	text = re.sub("@\w*", ' ', text) #remove usernames
        text = re.sub("\s+", ' ', text) # remove multiple whitespaces
        return text

    def parse(self):
        """Since the data is so big we have to do this on the fly"""
        if self.filename[-3:] == ".gz":
            self.data = gzip.open(self.filename)
        else:
            self.data = open(self.filename)
        self.t_list = codecs.open(self.list_filename, 'w')
        self.t_file = codecs.open(self.text_filename, 'w', 'utf-8')
        # the real parsing
        self.parse_data()

        self.data.close()
        self.t_list.close()
        self.t_file.close()

    def parse_data(self):
        # data → the tweets
        # t_list → the tweet list
        # t_file → the tweet text
        for tweets_to_write in self.data:
            user, tweets = self.extract_tweets(json.loads(tweets_to_write))
            print(user) # just to have a feeling of advancing
            # first the tweet list
            self.t_list.write(str(user))
            self.t_list.write(" ")
            tweet_numbers = map(lambda x: x[0], tweets)
            s = " ".join(map(str, tweet_numbers))
            self.t_list.write(s)
            self.t_list.write("\n")
            # then the tweet text
            for number, created_at, text in tweets:
                if number not in self.tweet_set:
                    self.tweet_set.add(number)
                    self.t_file.write(u"{0} {1} {2}\n".format( \
                            number, created_at, self.correct_text(text)))


if __name__ == '__main__':
    filename = sys.argv[1]
    parser = TweetParser(filename)
    parser.parse()


#!/usr/bin/env python2.6
# -*- coding: utf-8 -*-

import json
import gzip
import codecs
import sys
from collections import defaultdict

#import lzma

class TweetParser(object):
	
	def __init__(self, filename):
		self.filename = filename
		self.hashtags = dict(defaultdict(list))

	def extract_hashtags(self, juser):				# juser is a json object containing the tweets of the user
		user = juser['user']
		for tweet in juser['tweets']:				# get the tweets objects
			tweetID = tweet['id_str']
			for hashes in tweet['entities']['hashtags']:	# get the hashtag objects
				#h = hashes['text']			# get the hashtag text (the hashtag)
				h = hashes['text'].lower()
				
				if h not in self.hashtags:
					diz = defaultdict(list)
					diz[user].append(tweetID)
					self.hashtags[h] = diz	
				else:
					if self.hashtags[h][user]:
						 self.hashtags[h][user].append(tweetID)
	def parse(self):
		if self.filename[-3:] == ".xz":
			self.data = lzma.LZMAFile(self.filename)
		else:	self.data = open(self.filename)
			
		self.output = codecs.open(self.filename + '.hashtags.user2', 'w', 'utf-8' )
		self.parse_data()
		self.data.close()
		self.output.close()

	def parse_data(self):
		counter = 0
		
		print( "Extracting hashtags from tweets..." )
		for tweets_to_write in self.data:
			self.extract_hashtags(json.loads(tweets_to_write))
			counter += 1
			if counter % 2000 == 0:
				print( "Read {0} lines. Dictionary size is {1}.".format( counter, len(self.hashtags) ) )
		
		print( "Done.\nNow sorting them and saving..." )
		sortedHashtags = sorted( self.hashtags.keys() ) #, key=str.lower )
		for h in sortedHashtags:
			diz = self.hashtags[h]
			sortedUsers = sorted( diz.keys() ) #, key=str.lower ) #ordinare numeri????
			tweets = ''
			for u in sortedUsers:
				tweets += " #" + str(u)
				if self.hashtags[h][u]:
					for ids in self.hashtags[h][u]:
						tweets += ' ' + str(ids)
				
			self.output.write( u"{0}{1}\n".format( h,tweets ) )
		print( "Done." )


if __name__ == '__main__':
    filename = sys.argv[1]
    parser = TweetParser(filename)
    parser.parse()


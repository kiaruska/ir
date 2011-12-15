#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

import json
import gzip
import bz2
import codecs
import re
import os
import time
import sys
import locale


class TweetParser(object):
	def __init__(self, filename):
		self.filename = filename
		self.hashtags = dict()

	def extract_hashtags(self, juser):				# juser is a json object containing the tweets of the user
		user = juser['user']
		for tweet in jason_user['tweets']:			# get the tweets objects
			tweetID = tweet['id_str']
			for hashes in tweet['entities']['hashtags']:	# get the hashtag objects
				h = hashes['text']			# get the hashtag text (the hashtag)
				#h = unicode.lower( hashes['text'] )
				
				if h not in self.hashtags:
					self.hashtags[h] = set()
				
				self.hashtags[h].add(tweetID)
	
	def parse(self):
		if self.filename[-3:] == ".gz":
			self.data = gzip.open(self.filename)
		elif self.filename[-4:] == ".bz2":
			self.data = bz2.BZ2File(self.filename)
		else:	self.data = open(self.filename)
			
		self.output = codecs.open(self.filename + '.hashtags', 'w', 'utf-8' )
		self.parse_data()
		self.data.close()
		self.output.close()

	def parse_data(self):
		counter = 0
		
		print( "Extracting hashtags from tweets..." )
		for tweets_to_write in self.data:
			self.extract_hashtags(json.loads(tweets_to_write))
			counter += 1
			if counter % 1000 == 0:
				print( "Dictionary size is {0}.".format( len(self.hashtags) ) )
		
		print( "Done.\nNow sorting them and saving..." )
		sortedHashtags = sorted( self.hashtags.keys(), key=unicode.lower )
		for h in sortedHashtags:
			tweets = ''
			for ids in self.hashtags[h]:
				tweets += ' ' + str( ids )
			
			self.output.write(u"{0}{1}\n".format( h, tweets ) )
		print( "Done." )


if __name__ == '__main__':
    filename = sys.argv[1]
    parser = TweetParser(filename)
    parser.parse()


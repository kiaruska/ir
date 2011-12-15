#!/usr/bin/env python2.6
# -*- coding: utf-8 -*-

""" 
usage: 		./graph.py twitter-graph-file.graph
output: 	the graph file with the following format:

follower1 	#politicians followed		politician1 politician2 ...
follower2 	#politicians followed		politician2 politician3 ...
follower3 	#politicians followed		politician5 ...

The first lines contains the followers with less politicians.
"""

import sys
import gzip

class Graph ( object ):
	'''map for the associations follower -> [politicians]'''
	users = dict()
	'''politicians parsed'''
	politicians = set()
	'''to keep the followers in some order'''
	sortedUsers = []

	def invert ( self, fileName ):
		'''if file is compressed use gzip.open..'''
		if fileName[-3:] == '.gz':
			input = gzip.open( fileName )
		else:	input = open( fileName )
		
		'''this creates an entry in the dictionary for every follower'''
		for politician in input:
			politician = politician.rstrip()
			self.politicians.add( politician )
			'''add the politician to the followers'''
			for follower in input:
				if follower == '\n':
					break
				follower = follower.rstrip()
				if follower not in self.users:
					self.users[follower] = []
				self.users[follower].append( politician )		
		
		'''also keep the users in ascending order of policians followed'''
		self.sortedUsers = sorted( self.users.keys(), key=lambda f: len(self.users[f]) )
	
	def save ( self, fileName ):
		output = open( fileName, 'w' )
		for follower in self.sortedUsers:
			# also print the length of the politicians list
			output.write( follower + ' ' + str(len(self.users[follower])) + ' ' + ' '.join( self.users[follower] ) + '\n' )
			#output.write( follower + ' ' + ' '.join( self.users[follower] ) + '\n' )
		output.close()

	def statistics ( self ):
		currentLen = len( self.politicians )
		stats = dict()
		print( 'Some statistics:' )
		
		'''collect informations on the lengths'''
		for f in self.sortedUsers:
			index = len( self.users[f] )
			stats[index] = stats.setdefault( index, 0 ) + 1
		
		for i in stats.keys():
			print( '  Users that follow {0} politician{1}: {2}.'.format( i, '' if i == 1 else 's', stats[i] ) )
			
		print( '  Total users: {0} (+ {1} politicians).'.format( len( self.sortedUsers ), len( self.politicians ) ) )
		
		
		'''Test if a politician follows some other politician'''
		intersection = self.politicians & set( self.users.keys() )
		if len( intersection ) > 0:
			print( '\nSome politician is also a follower:' )
			for p in intersection:
				print( '  Politician {0} follows: {1}.'.format( p, ' '.join( self.users[p] ) ) )

		'''check total unique users with: cat Tweet.graph.file | sort | uniq | wc -l'''
			
		
if __name__ == '__main__':
	assert( len(sys.argv) == 2 )
	graph = Graph()
	print( 'Inverting the graph file...' )
	graph.invert( sys.argv[1] )
	print( 'Inverted.\nSaving in {0}.sorted'.format( sys.argv[1] ) )
	graph.save( sys.argv[1] + '.sorted' )
	print( 'Saved.\n' )
	graph.statistics()


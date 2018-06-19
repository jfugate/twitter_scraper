#!/usr/bin/python
import csv

def csvfile_initialize(output_file):
	with open(output_file, 'wb') as csvout:
		writer = csv.DictWriter(csvout, fieldnames = ["username", "follower_count", "follower_name", "following_count", "following_name", "tweet_history"])
		writer.writeheader()

def export_following(data, user, counter, output_file):
	'''
	data = list of usernames that given user follows
	user = user we are making query agains
	counter = total number of users being followed by user in question
	output_file = path to our output
	'''
	with open(output_file, 'ab') as csvout:
		writer = csv.DictWriter(csvout, fieldnames = ["username", "follower_count", "follower_name", "following_count", "following_name", "tweet_history"])
		for name in data:
            writer.writerows('username': user, 'following_count': counter,'following_name': name)
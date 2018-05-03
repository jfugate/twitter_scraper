#!/usr/bin/python
import tweepy
from pprint import pprint
import argparse, os


'''
This block sets up our authentication. The keys/secrets should NOT be stored in plain text in this script.
Will be setting up environment variables to prevent this later.
'''
def set_creds():
	consumer_key = os.getenv('consumer_key')
	consumer_secret = os.getenv('consumer_secret')
	auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
	key = os.getenv('key')
	secret = os.getenv('secret')
	auth.set_access_token(key, secret)
	api = tweepy.API(auth)
	return api

'''
user = api.get_user('someTwitterUsername')
the above is an example of getting the user profile object from Twitter
can use the vars(user)['user_profile_propert'] method or user.user_profile_property with pprint
to obtain the data
'''


#Function to dump the profile data
def profile_dump(username, outputPath):
	set_creds()
	profile_obj = api.get_user(username)

#Function to dump all historic tweets
def tweet_dump(username, outputPath):
	set_creds()

#Function to dump all followers of the given user
def follower_list(username, outputPath):
	set_creds()

#Function to show who all the given user follows
def follwing_list(username, outputPath):
	set_creds()
	result_list = api.friends_ids(username)
	final_list = []
	for i in result_list:
		user = api.get_user(i)
		final_list.append(user.screen_name)
	#Need code for writing to CSV file or other output method here

#parse the command line arguments
def parse_arguments():
	parser = argparse.ArgumentParser()
	parser.add_argument("-u", "--user", help="The @username or user_id number of the Twitter user", action="store", dest="user_id")
	parser.add_argument("-o", "--output-path", help="Path to store data that is gathered.", action="store", dest="output_path")
	parser.add_argument("-p", "--profile_dump", help="Dump relevant data from user's public Twitter profile.", action="store_true", default=False, dest="prof_dump")
	parser.add_argument("-t", "--tweet-history", help="Dump all of user's publicly available Tweets.", action="store_true", default=False, dest="tweet_history")
	parser.add_argument("-f", "--follower-list", help="Dump the usernames of all the given user's followers.", action="store_true", default=False, dest="followers")
	parser.add_argument("-F", "--following", help="Dump all usernamse that the given user is following.", action="store_true", default=False, dest="following")

	results = parser.parse_args()
	#Make sure a username and output path are provided:
	if results.user_id == "" or results.output_path == "":
		print("Username/Output Path not provided, please provide a user/output_path.")
		parser.print_help()
	else:
		if results.prof_dump:
			profile_dump(results.user_id, results.output_path)
		elif results.tweet_history:
			tweet_dump(results.user_id, results.output_path)
		elif results.followers:
			follower_list(results.user_id, results.output_path)
		elif results.following:
			follwing_list(results.user_id, results.output_path)


parse_arguments()
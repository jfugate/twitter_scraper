#!/usr/bin/python
import tweepy
from pprint import pprint
import argparse, os, time, json, csv
import exporter

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
can use the vars(user)['user_profile_propert'] method to obtain the data
'''


#Function to dump the profile data
def profile_dump(username, outputPath):
	api = set_creds()
	profile_obj = api.get_user(username)
	exporter.export_profile(profile_obj, outputPath)

#Function to dump all historic tweets
'''
useful formats for tweet_dump from manual testing
tweets = api.user_timeline('username')
vars(tweets[0])['_json']['text'].encode("utf-8")
'#AlwaysPunchNazis'
vars(tweets[0])['_json']['created_at'].encode("utf-8")
'Thu May 03 19:04:48 +0000 2018'

'''
def tweet_dump(username, output_path):
	api = set_creds()

#Function to dump all followers of the given user
def follower_list(username, output_path):
	api = set_creds()
	result_list = []
	counter = 0
	print('Patience Comrade, this may take a long time.....')
	for i in api.followers_ids(username):
		result_list.append(api.get_user(i).screen_name)
		counter += 1
		print("Number of users that follow " + username + " found so far: " + str(counter))
		time.sleep(5)
	#print(result_list)
	exporter.export_follower(result_list, username, counter, output_path)

#Function to show who all the given user follows
def following_list(username, output_path):
	api = set_creds()
	result_list = []
	counter = 0
	print('Patience Comrade, this may take a long time.....')
	for i in api.friends_ids(username):
		result_list.append(api.get_user(i).screen_name)
		counter += 1
		print("Number of users " + username + " follows found so far: " + str(counter))
		time.sleep(5)
	exporter.export_following(result_list, username, counter, output_path)

def tweet_dump(screen_name, output_path):
	api = set_creds()

	#initialize a list to hold all the tweepy Tweets
	alltweets = []	
	
	#make initial request for most recent tweets (200 is the maximum allowed count)
	new_tweets = api.user_timeline(screen_name = screen_name,count=200)
	
	#save most recent tweets
	alltweets.extend(new_tweets)
	
	#save the id of the oldest tweet less one
	oldest = alltweets[-1].id - 1
	
	#keep grabbing tweets until there are no tweets left to grab
	while len(new_tweets) > 0:
		print "getting tweets before %s" % (oldest)
		
		#all subsiquent requests use the max_id param to prevent duplicates
		new_tweets = api.user_timeline(screen_name = screen_name,count=200,max_id=oldest)
		
		#save most recent tweets
		alltweets.extend(new_tweets)
		
		#update the id of the oldest tweet less one
		oldest = alltweets[-1].id - 1
		
		print "...%s tweets downloaded so far" % (len(alltweets))
	
	#transform the tweepy tweets into a 2D array that will populate the csv	
	outtweets = [[tweet.id_str, tweet.created_at, tweet.text.encode("utf-8")] for tweet in alltweets]
	with open('%s_tweets.csv' % screen_name, 'wb') as f:
		writer = csv.writer(f)
		writer.writerow(["id","created_at","text"])
		writer.writerows(outtweets)
	pass

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
			following_list(results.user_id, results.output_path)


parse_arguments()
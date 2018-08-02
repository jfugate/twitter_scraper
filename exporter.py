#!/usr/bin/python


'''def export_profile(user, outPath):
	try:
	    with open(outPath, 'a') as profileOut:
		    table = {'description': user.description, 'Followers': user.followers_count, 'location': user.location,
			    	 'name': user.name, 'profile_image': user.profile_image_url, 'profile_banner_image': user.profile_banner_url,
			 	     'verified': user.verified, 'time_zone': user.time_zone, 'account_created': user.created_at}
		    profileOut.write('description: {description:s}; Follower Count: {Followers:d}; location: {location:s}; name: {name:s}; Avatar Link: {profile_image:s}; '
		    'Banner Link: {profile_banner_image:s}; Is account verified: {verified:b}, time zone: {time_zone:s} \n'.format(**table))
	except AttributeError as err:
		err = str(err)
		att = err.split(' ')[-1]
		print "This profile is missing the following setting: " + att'''

def export_profile(user, outPath):
	att_list = [ 'description', 'followers_count', 'location', 'name', 'profile_image_url', 'profile_banner_url', 'verified', 'time_zone', 'created_at' ]
	keys = []
	table = {}
	for att in att_list:
		if hasattr(user, att):
			 keys.append(att)
		else:
			pass
	for i in keys:
		new_val = getattr(user, i)
		table[i] = new_val
	with open(outPath, 'a') as profileOut:
		for key, value in table.items():
			profileOut.write(str(key) + ' => ' + str(value) + '\n')

def export_follower(result_list, username, counter, outPath):
	with open(outPath, 'a') as follower_out:
		follower_out.write('Number of users total followed by ' + username + ' is ' + str(counter) + ' this is a list of those users:\n')
		follower_out.write(','.join(result_list))

def export_following(result_list, username, counter, outPath):
	with open(outPath, 'a') as following_out:
		following_out.write('Number of users total following ' + username + ' is ' + str(counter) + ' this is a list of those users:\n')
		following_out.write(','.join(result_list))

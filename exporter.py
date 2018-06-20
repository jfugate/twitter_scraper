#!/usr/bin/python

def export_profile(user, outPath):
	with open(outPath, 'a') as profileOut:
		table = {'description': user.description, 'Followers': user.followers_count, 'location': user.location,
				 'name': user.name, 'profile_image': user.profile_image_url, 'profile_banner_image': user.profile_banner_url,
			 	 'verified': user.verified, 'time_zone': user.time_zone, 'account_created': user.created_at}
		profileOut.write('description: {description:s}; Follower Count: {Followers:d}; location: {location:s}; name: {name:s}; Avatar Link: {profile_image:s}; '
		'Banner Link: {profile_banner_image:s}; Is account verified: {verified:b}, time zone: {time_zone:s} \n'.format(**table))


def export_follower(result_list, username, counter, outPath):
	with open(outPath, 'a') as follower_out:
		follower_out.write('Number of users total followed by ' + username + ' is ' + str(counter) + ' this is a list of those users:\n')
		follower_out.write(','.join(result_list))
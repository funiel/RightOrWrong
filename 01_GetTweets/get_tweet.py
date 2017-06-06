import tweepy
from tweepy import OAuthHandler
import json
import re
import argparse
import csv

parser = argparse.ArgumentParser()
parser.add_argument("user", help="Twitter account to use", type=str)
args = parser.parse_args()


consumer_key = 'YOUR CONSUMER KEY'
consumer_secret = 'YOUR SECRET KEY'
access_key = 'YOUR ACCESS KEY'
access_secret = 'YOUR ACCESS SECRET'

def get_all_tweets(screen_name):
	#Twitter only allows access to a users most recent 3240 tweets with this method

	#authorize twitter, initialize tweepy
	auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_key, access_secret)
	api = tweepy.API(auth)

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
		print ("getting tweets before %s" % (oldest))

		#all subsiquent requests use the max_id param to prevent duplicates
		new_tweets = api.user_timeline(screen_name = screen_name,count=200,max_id=oldest)

		#save most recent tweets
		alltweets.extend(new_tweets)

		#update the id of the oldest tweet less one
		oldest = alltweets[-1].id - 1

		print ("...%s tweets downloaded so far" % (len(alltweets)))
	outtweets = []
	for tweet in alltweets:
		outtweet = re.sub(r"http\S+", "", tweet._json['text'])
		outtweets.append((outtweet))


	with open('%s_tweets.txt' % screen_name, 'w') as f:
		f.write("\n".join(outtweets))
		f.close()

	# with open('%s_tweets.csv' % screen_name, 'w') as f:
	# 	spamwriter = csv.writer(f)
	# 	spamwriter.writerow("\n".join(outtweets).encode("utf-8"))
	# pass


if __name__ == '__main__':
	#pass in the username of the account you want to download
	get_all_tweets(args.user)

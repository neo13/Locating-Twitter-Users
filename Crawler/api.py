#
#
# first draft of tweeter data minner
#
#
import twitter
import json

class API(object):
	"""This class is used to authenticate the tokens that provided for it and handle the tweeter APIs"""
	class __api__(object):
		def __init__(self, api):
			super(API.__api__, self).__init__()
			self.api = api

		def get_profile(self, user_id):	
			try:		
				return self.api.users.lookup(user_id=user_id, include_entities=False)[0]
			except twitter.TwitterHTTPError:
				return []

		def get_followees(self, user_id, cursor=-1):
			try:
				return self.api.friends.ids(user_id=user_id, cursor=cursor, count=5000)
			except twitter.TwitterHTTPError:
				return []

		def get_followers(self, user_id, cursor=-1):
			try:
				return self.api.followers.ids(user_id=user_id, cursor=cursor, count=5000)
			except twitter.TwitterHTTPError:
				return []

		def get_timeline(self, user_id, cursor=-1):
			if cursor == -1:
				try:
					return self.api.statuses.user_timeline(user_id=user_id, count=200, trim_user=True, exclude_replies=False, include_rts=True)
				except twitter.TwitterHTTPError:
					return []
			else:
				try:
					return self.api.statuses.user_timeline(user_id=user_id, since_id=cursor, count=200, trim_user=True, exclude_replies=False, include_rts=True)
				except twitter.TwitterHTTPError:
					return []

		def get_favourites(self, user_id):
			try:
				return self.api.favorites.list(user_id=user_id, count=200)
			except twitter.TwitterHTTPError:
				return []

		def get_retweeters(self, tweet_id, cursor=-1):
			if cursor == -1:
				try:
					return self.api.statuses.retweeters.ids(_id=tweet_id)
				except twitter.TwitterHTTPError:
					return []
			else:
				try:
					return self.api.statuses.retweeters.ids(_id=tweet_id, cursor=cursor)
				except twitter.TwitterHTTPError:
					return []

	def __init__(self, file):
		super(API, self).__init__()
		stream = open(file, "r+")
		raw = stream.read()
		tokens = json.loads(raw)
		self.apis = []
		self.authenticate(tokens['APPS'])

	def __iter__(self):
		return iter(self.apis)

	def authenticate(self, tokens):
		#This function gets a token array and return [] a array of tweeter api.
		for token in tokens:
			auth = twitter.oauth.OAuth(token['tokens']['access_token'], token['tokens']['access_secret'], token['tokens']['consumer_key'], token['tokens']['consumer_secret'])
			api = twitter.Twitter(auth=auth)
			self.apis.append(self.__api__(api))

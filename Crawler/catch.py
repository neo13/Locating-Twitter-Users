class Catch(object):
	"""This class will handle data base connection and queries"""
	redis_socket = "/tmp/redis.sock"
	db = "mining"

	def __init__(self):
		super(Catch, self).__init__()
		self.user = Redis(unix_socket_path=self.redis_socket, db=0),
		self.tweet = Redis(unix_socket_path=self.redis_socket, db=1)

	def catch_user(self, users):
		for user in users:
			if not self.catch['user'].exists(str(user)) and not self.catch['user'].exists(str(user)+'-unvisited'):
				self.catch['user'].set(str(user)+'-unvisited', user.cursor.join("|") )

	def catch_tweet(self, tweets):
		for tweet in tweets:
			if not self.catch['tweet'].exists(str(tweet)) and not self.catch['tweet'].exists(str(tweet)+'-unvisited'):
				self.catch['tweet'].set(str(tweet)+'-unvisited', tweets.cursor.join("|") )

	def create_user_pool(self, n):
		res = []
		unvisited_users = self.user.keys("*-unvisited")
		for key in unvisited_users[0:n]:
			new_key = key.split('-')[0]
			res.append(new_key)
			self.user.rename(key, new_key)
		return res

	def create_tweet_pool(self, n):
		res = []
		unvisited_tweets = self.tweet.keys("*-unvisited")
		return [ Tweet.objects(tweet_id=key.split('-')[0]) for key in unvisited_tweets[0:n] ]

	def _uncatch_user(self, users):
		for user in users:
			if self.catch['user'].exists(str(user)+'-unvisited'):
				self.catch['user'].rename(str(user)+'-unvisited', str(user))

	def _uncatch_tweet(self, tweets):
		for tweet in tweets:
			if self.catch['tweet'].exists(str(tweet)+'-unvisited'):
				self.catch['tweet'].rename(str(tweet)+'-unvisited', str(tweet))
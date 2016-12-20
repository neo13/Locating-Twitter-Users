import time
import api, file

class tweeter_crawler(object):
	token_file = "tokens.json"
	tweeter_limit = 15
	restiriction_time_window = 15 * 60

	def __init__(self):
		super(tweeter_crawler, self).__init__()
		self.api_handle = API.API(self.token_file)
		self.apps_count = len(self.api_handle.apis)

	def tik(self):
		if 'timestamp1' in dir(self):
			self.timestamp2 = time.time()
		else:
			self.timestamp1 = time.time()

	def next_user(self):
		try:
			self.user_pointer += 1
			return self.user_pool[self.user_pointer]
		except AttributeError:
			#we should decide which users whould be the next users to crawl
			#we will meet n * m user in each loop that n is the number of apps and m is the thereshold of each loop
			self.user_pool = self.data_handle.create_user_pool(self.apps_count * self.tweeter_limit)
			self.user_pointer = 0
			return self.user_pool[0]

	def next_tweet(self):
		try:
			self.tweet_pointer += 1
			return self.tweet_pool[self.tweet_pointer][0]
		except AttributeError:
			#we should decide which users whould be the next users to crawl
			#we will meet n * m user in each loop that n is the number of apps and m is the thereshold of each loop
			self.tweet_pool = self.data_handle.create_tweet_pool(self.apps_count * self.tweeter_limit)
			self.tweet_pointer = 0
			return self.tweet_pool[0][0]

	def calculate_wait_time(self):
		return self.restiriction_time_window - int(self.timestamp2 - self.timestamp1);

	def clear(self):
		del self.timestamp1, self.timestamp2, self.user_pool, self.user_pointer, self.tweet_pool, self.tweet_pointer
		self.data_handle.flush_user(self.user_pool)
		self.data_handle.flush_tweet(self.tweet_pool)

	def loop(self):
		while True:
			#we have to consider the time window of tweeter which is 15 min
			self.tik()
			for api in self.api_handle:
				#for each api we have a restiricted number of request for each element so
				for i in range(self.tweeter_limit):
					#in each loop we have a set of queries
					try:
						user_id = self.next_user()
						print "User has been fetched"
						#we should take a user_info and save it as a user profile
						user = self.data_handle.user(api.get_profile(user_id))
						print "User Profile has been created"
						#we should take user_timeline contents and save it as contents
						#we have a 180 per user restriction for timeline so 180/15=12 time a loop which gets at most 2400 tweet for each user
						for j in range(12):
							try:
								response = api.get_timeline(user_id=user.user_id, cursor=user.tweet_cursor)
 								if(not response):
									print "Noting More..."
									break
								self.data_handle.tweets(user=user, tweets_array=response)					
							except AttributeError:
								response = api.get_timeline(user_id=user.user_id)
								print "we got Tweet."
								if(not response):
									print "Noting More..."
									break
								self.data_handle.tweets(user=user, tweets_array=response)
													
						#we should take user_flowers and save them as followers and also put them in queue
						try:
							if user.followers_cursor:
								print 'get some followers'
								self.data_handle.add_followers(user=user, followers=api.get_followers(user_id=user.user_id, cursor=user.followers_cursor))
						except AttributeError:
							print 'get some followers'
							self.data_handle.add_followers(user=user, followers=api.get_followers(user_id=user.user_id))
						#we should take user_friends and save them as followees and also put them in queue
						try:
							if user.followees_cursor:
								print 'who followed this guy?!!!'
								self.data_handle.add_followees(user=user, followees=api.get_followees(user_id=user.user_id, cursor=user.followees_cursor))
						except AttributeError:
							print 'who followed this guy?!!!'
							self.data_handle.add_followees(user=user, followees=api.get_followees(user_id=user.user_id))
						#we should take user_favoriets and save them as favoriets
						if not user.favourites:
							print "this parts my favourite"
							self.data_handle.add_favourites(user=user, favourites=api.get_favourites(user_id=user.user_id))
					except:
						pass

			for api in self.api_handle:
				#for each api we have a restiricted number of request for each element so
				for i in range(self.tweeter_limit):
					#in each loop we have a set of queries
					try:
						tweet = self.next_tweet()
						try:
							self.data_handle.add_retweeters(tweet=tweet, retweeters=api.get_retweeters(tweet_id=tweet.tweet_id, cursor=tweet.retweeters_cursor))
						except AttributeError:
							self.data_handle.add_retweeters(tweet=tweet, retweeters=api.get_retweeters(tweet_id=tweet.tweet_id))
					except:
						pass
			
			self.tik()
			time.sleep(self.calculate_wait_time())
			self.clear()

tc = tweeter_crawler()
tc.loop()

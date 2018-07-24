from threading import Thread
from TwitterAPI import TwitterAPI
from datetime import datetime, timedelta
from dateutil import parser

# how many tweets to review for deletion
NUM_TWEETS = 200

api = TwitterAPI(
    'consumer_key',
    'consumer_secret',
    'access_token_key',
    'access_token_secret'
)

# how many days before deletion
cutoff_date = datetime.utcnow() - timedelta(days=7)


class DeleteTweet(Thread):

    def __init__(self, tweet_id):
        Thread.__init__(self)
        self.tweet_id = tweet_id

    def run(self):
        r = api.request('statuses/destroy/:%d' % self.tweet_id)
        print('OK' if r.status_code == 200 else 'PROBLEM: %d' % self.tweet_id)


try:
    r = api.request(
        'statuses/user_timeline', {'count': NUM_TWEETS})
    for item in r:
        created_at = parser.parse(item['created_at']).replace(tzinfo=None)
        if created_at < cutoff_date:
            print("Deleting {}: [{}]".format(
                item['id'], created_at))
            DeleteTweet(item['id']).start()
        else:
            print("Too recent {}: [{}]".format(
                item['id'], created_at))

except Exception as e:
    print('Stopping: %s' % str(e))

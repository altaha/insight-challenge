import json

class TweetSanitizer(object):
    def __init__(self):
        self.tweets_with_unicode = 0

    def sanitize_tweet(self, json_tweet):
        return self._load_json_tweet(json_tweet)

    def num_tweets_with_unicode(self):
        return self.tweets_with_unicode

    def _load_json_tweet(self, json_tweet):
        tweet = json.loads(json_tweet)
        text = tweet['text']
        created_at = tweet['created_at']
        return Tweet(text, created_at)

class Tweet(object):
    def __init__(self, text, created_at):
        self.text = text
        self.created_at = created_at

    def __str__(self):
        return '{text} (timestamp: {created_at})'.format(
            text=self.text,
            created_at=self.created_at,
        )

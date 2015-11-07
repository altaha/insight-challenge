import json


class TweetSanitizer(object):
    def __init__(self):
        self.tweets_with_unicode = 0
        self.escaping_map = [
            ('\/', '/',),
            ('\\\\', '\\',),
            ("\\'", "'",),
            ('\\"', '"',),
            ('\\n', ' ',),
            ('\\t', ' ',),
        ]

    def sanitize_tweet(self, json_tweet):
        (text, created_at,) = self._load_json_tweet(json_tweet)
        text = self._drop_unicode(text)
        text = self._unescape(text)
        return Tweet(text, created_at)

    def num_tweets_with_unicode(self):
        return self.tweets_with_unicode

    def _load_json_tweet(self, json_tweet):
        tweet = json.loads(json_tweet)
        (text, created_at,) = ('', '',)
        if 'text' in tweet:
            text = tweet['text']
        if 'created_at' in tweet:
            created_at = tweet['created_at']
        return (text, created_at,)

    def _drop_unicode(self, input_string):
        string = ''.join([c for c in input_string if ord(c) < 128])
        if len(string) < len(input_string):
            self.tweets_with_unicode += 1
        return string

    def _unescape(self, string):
        for tup in self.escaping_map:
            string = string.replace(tup[0], tup[1])
        # Remove excess whitespace leading, trailing, and in between
        string = " ".join(string.split())
        return string


class Tweet(object):
    def __init__(self, text, created_at):
        self.text = text
        self.created_at = created_at

    def __str__(self):
        return '{text} (timestamp: {created_at})'.format(
            text=self.text,
            created_at=self.created_at,
        )

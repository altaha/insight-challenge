from collections import deque, Counter
from datetime import datetime
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
        if created_at:
            self.date_time = datetime.strptime(
                created_at,
                '%a %b %d %H:%M:%S +0000 %Y',
            )

    def __str__(self):
        return '{text} (timestamp: {created_at})'.format(
            text=self.text,
            created_at=self.created_at,
        )

    def is_valid(self):
        return self.created_at != ''

    def get_edges(self):
        words = self.text.split()
        hashtags = set([word.lower() for word in words if word[0] == '#'])
        edges = []
        while len(hashtags) > 0:
            hash1 = hashtags.pop()
            edges += [Edge(hash1, hash2) for hash2 in hashtags]
        return edges


class Edge(object):
    def __init__(self, hashtag1, hashtag2):
        if hashtag1 < hashtag2:
            self.hashtag1 = hashtag1
            self.hashtag2 = hashtag2
        else:
            self.hashtag1 = hashtag2
            self.hashtag2 = hashtag1

    def __str__(self):
        return '{}-{}'.format(self.hashtag1, self.hashtag2)

    def get_hashtags(self):
        return (self.hashtag1, self.hashtag2,)


class TweetGraphDegree(object):
    def __init__(self):
        self.tweets = deque()
        self.edge_counter = Counter()
        self.node_counter = Counter()
        self.nodes_total = 0
        self.window_size = 60

    def average_degree(self):
        if len(self.node_counter) == 0:
            return 0
        return float(self.nodes_total) / len(self.node_counter)

    def total(self):
        return self.nodes_total

    def num_nodes(self):
        return len(self.node_counter)

    def add_tweet(self, tweet):
        if not tweet.is_valid():
            return

        edges = tweet.get_edges()
        for edge in edges:
            edge_name = str(edge)
            if self.edge_counter[edge_name] == 0:
                self.nodes_total += 2
            self.edge_counter[edge_name] += 1

            hashtags = edge.get_hashtags()
            for hashtag in hashtags:
                self.node_counter[hashtag] += 1

        self.tweets.appendleft(tweet)

        # Determine old tweets to be removed
        while self._is_tweet_out_of_window(tweet, self.tweets[-1]):
            self._remove_last_tweet()

    def _remove_last_tweet(self):
        removed_tweet = self.tweets.pop()
        edges = removed_tweet.get_edges()
        for edge in edges:
            edge_name = str(edge)
            self.edge_counter[edge_name] -= 1
            if self.edge_counter[edge_name] == 0:
                self.nodes_total -= 2
                del self.edge_counter[edge_name]

            hashtags = edge.get_hashtags()
            for hashtag in hashtags:
                self.node_counter[hashtag] -= 1
                if self.node_counter[hashtag] == 0:
                    del self.node_counter[hashtag]

    def _is_tweet_out_of_window(self, lead_tweet, test_tweet):
        time_delta = lead_tweet.date_time - test_tweet.date_time
        if time_delta.total_seconds() > self.window_size:
            return True
        return False


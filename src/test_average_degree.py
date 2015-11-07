import unittest

from tweeter import Tweet, TweetSanitizer


tweets_series = [
    {
        'text': 'Spark Summit East this week! #Spark #Apache',
         'created_at': 'Thu Oct 29 17:51:01 +0000 2015'
    },
    {
        'text': 'Just saw a great post on Insight Data Engineering #Apache #Hadoop #Storm',
         'created_at': 'Thu Oct 29 17:51:30 +0000 2015'
    },
    {
        'text': 'Doing great work #Apache',
         'created_at': 'Thu Oct 29 17:51:55 +0000 2015'
    },
    {
        'text': 'Excellent post on #Flink and #Spark',
         'created_at': 'Thu Oct 29 17:52:02 +0000 2015'
    },
]


class TestGraphDegree(unittest.TestCase):
    def setUp(self):
        self.sanitizer = TweetSanitizer()

    def test_degree_with_only_one_edge(self):
        tweets = [Tweet(t['text'], t['created_at']) for t in tweets_series[0:1]]
        expected_degree = ''
        self.assertEqual(expected_degree, 1)

    def test_degree_with_two_tweets(self):
        tweets = [Tweet(t['text'], t['created_at']) for t in tweets_series[0:2]]
        expected_degree = ''
        self.assertEqual(expected_degree, 9.0/4.0)

    def test_tweet_with_no_edges(self):
        tweets = [Tweet(t['text'], t['created_at']) for t in tweets_series[0:3]]
        expected_degree = ''
        self.assertEqual(expected_degree, 9.0/4.0)

    def test_tweets_in_60s_window(self):
        tweets = [Tweet(t['text'], t['created_at']) for t in tweets_series[1:4]]
        expected_degree = ''
        self.assertEqual(expected_degree, 8.0/5.0)

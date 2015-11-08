import unittest

from tweeter import Tweet, TweetGraphDegree


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
    def get_graph_from_tweets(self, tweets):
        graph = TweetGraphDegree()
        for tweet in tweets:
            graph.add_tweet(tweet)
        return graph

    def test_degree_with_only_one_edge(self):
        tweets = [Tweet(t['text'], t['created_at']) for t in tweets_series[0:1]]
        graph = self.get_graph_from_tweets(tweets)
        average_degree = graph.average_degree()
        self.assertEqual(average_degree, 1.0/1.0)

    def test_degree_with_two_tweets(self):
        tweets = [Tweet(t['text'], t['created_at']) for t in tweets_series[0:2]]
        graph = self.get_graph_from_tweets(tweets)
        average_degree = graph.average_degree()
        self.assertEqual(average_degree, 8.0/4.0)

    def test_tweet_with_no_edges(self):
        tweets = [Tweet(t['text'], t['created_at']) for t in tweets_series[0:3]]
        graph = self.get_graph_from_tweets(tweets)
        average_degree = graph.average_degree()
        self.assertEqual(average_degree, 8.0/4.0)

    def test_tweets_in_60s_window(self):
        tweets = [Tweet(t['text'], t['created_at']) for t in tweets_series[0:4]]
        graph = self.get_graph_from_tweets(tweets)
        average_degree = graph.average_degree()
        self.assertEqual(average_degree, 10.0/5.0)

import unittest

from tweeter import Tweet, TweetGraphDegree


tweets_series = [
    {
        'text': 'Spark Summit East this week! #Spark #Apache',
         'created_at': 'Thu Oct 29 17:51:01 +0000 2015',
    },
    {
        'text': 'Just saw a great post on Insight Data Engineering #Apache #Hadoop #Storm',
         'created_at': 'Thu Oct 29 17:51:30 +0000 2015',
    },
    {
        'text': 'Doing great work #Apache',
         'created_at': 'Thu Oct 29 17:51:55 +0000 2015',
    },
    {
        'text': 'Excellent post on #Flink and #Spark',
         'created_at': 'Thu Oct 29 17:51:57 +0000 2015',
    },
    {
        'text': 'New and improved #HBase connector for #Spark',
        'created_at': 'Thu Oct 29 17:51:59 +0000 2015',
    },
    {
        'text': 'New 2.7.1 version update for #Hadoop #Apache',
        'created_at': 'Thu Oct 29 17:52:05 +0000 2015',
    },
]


class TestGraphDegree(unittest.TestCase):
    def get_graph_from_tweets(self, tweets):
        '''Creates a degree graph from provided list of tweets'''
        graph = TweetGraphDegree()
        for tweet in tweets:
            graph.add_tweet(tweet)
        return graph

    def assert_graph_degree(self, graph, expected_nodes_total, expected_num_nodes):
        '''Asserts graph calculates its degree with the expected values'''
        expected_degree = expected_nodes_total / expected_num_nodes
        self.assertEqual(graph.total(), expected_nodes_total)
        self.assertEqual(graph.num_nodes(), expected_num_nodes)
        self.assertEqual(graph.average_degree(), expected_degree)

    def test_degree_with_only_one_edge(self):
        tweets = [Tweet(t['text'], t['created_at']) for t in tweets_series[0:1]]
        graph = self.get_graph_from_tweets(tweets)
        self.assert_graph_degree(graph, 2.0, 2.0)

    def test_degree_with_two_tweets(self):
        tweets = [Tweet(t['text'], t['created_at']) for t in tweets_series[0:2]]
        graph = self.get_graph_from_tweets(tweets)
        self.assert_graph_degree(graph, 8.0, 4.0)

    def test_tweet_with_no_edges(self):
        tweets = [Tweet(t['text'], t['created_at']) for t in tweets_series[0:3]]
        graph = self.get_graph_from_tweets(tweets)
        self.assert_graph_degree(graph, 8.0, 4.0)

    def test_two_more_tweets(self):
        tweets = [Tweet(t['text'], t['created_at']) for t in tweets_series[0:5]]
        graph = self.get_graph_from_tweets(tweets)
        self.assert_graph_degree(graph, 12.0, 6.0)

    def test_tweets_in_60_window(self):
        tweets = [Tweet(t['text'], t['created_at']) for t in tweets_series[0:6]]
        graph = self.get_graph_from_tweets(tweets)
        self.assert_graph_degree(graph, 10.0, 6.0)

    def test_remove_multiple_tweets_from_window(self):
        tweets = [Tweet(t['text'], t['created_at']) for t in tweets_series[0:5]]
        tweets += [Tweet('New version #Hadoop #Apache', 'Thu Oct 29 17:52:57 +0000 2015')]
        graph = self.get_graph_from_tweets(tweets)
        self.assert_graph_degree(graph, 6.0, 5.0)

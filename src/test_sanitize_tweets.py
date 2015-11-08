import json
import unittest

from tweeter import Tweet, TweetSanitizer


json_tweet = (
    '{"created_at":"Thu Oct 29 17:51:01 +0000 2015", "id":659789759787589632,'
    '"id_str":"659789759787589632", "text":"Spark Summit East this week! #Spark #Apache"}'
)

unicode_json = (
    '{'
    '"created_at": "Thu Oct 29 18:10:49 +0000 2015",'
    '"text": "Im at Terminal de Integra\u00e7\u00e3o do Varadouro in Jo\u00e3o Pessoa"'
    '}'
)

escaped_tweet = {
    "created_at": "Thu Oct 30 18:10:49 +0000 2015",
    "text": ", PB https:\/\/t.co\/HOl34REL1a"
}

all_escaped_tweet = {
    "created_at": "Fri Oct 30 18:10:49 +0000 2015",
    "text": "  \/Hello \\\\ \\\' \\\" n\\no   di\\tce "
}


class TestTweetSanitizer(unittest.TestCase):
    def setUp(self):
        self.sanitizer = TweetSanitizer()

    def test_load_json(self):
        """Loads basic JSON tweet that doesnt require sanitization"""
        expected_output = 'Spark Summit East this week! #Spark #Apache (timestamp: Thu Oct 29 17:51:01 +0000 2015)'
        sanitized_output = str(self.sanitizer.sanitize_tweet(json_tweet))
        self.assertEqual(expected_output, sanitized_output)

    def test_remove_unicode(self):
        tweet = unicode_json
        expected_output = "Im at Terminal de Integrao do Varadouro in Joo Pessoa (timestamp: Thu Oct 29 18:10:49 +0000 2015)"
        sanitized_output = str(self.sanitizer.sanitize_tweet(tweet))
        self.assertEqual(expected_output, sanitized_output)

        sanitized_output = self.sanitizer.sanitize_tweet(tweet)
        num_unicode = self.sanitizer.num_tweets_with_unicode()
        self.assertEqual(num_unicode, 2)

    def test_unescape_text(self):
        tweet = json.dumps(escaped_tweet)
        expected_output = ', PB https://t.co/HOl34REL1a (timestamp: Thu Oct 30 18:10:49 +0000 2015)'
        sanitized_output = str(self.sanitizer.sanitize_tweet(tweet))
        self.assertEqual(expected_output, sanitized_output)

        sanitized_output = self.sanitizer.sanitize_tweet(tweet)
        num_unicode = self.sanitizer.num_tweets_with_unicode()
        self.assertEqual(num_unicode, 0)

    def test_all_escape_charecters(self):
        tweet = json.dumps(all_escaped_tweet)
        expected_output = '/Hello \ \' " n o di ce (timestamp: Fri Oct 30 18:10:49 +0000 2015)'
        sanitized_output = str(self.sanitizer.sanitize_tweet(tweet))
        self.assertEqual(expected_output, sanitized_output)


class TestTweet(unittest.TestCase):
    def test_name(self):
        tweet = Tweet('Hello', '123')
        expected = 'Hello (timestamp: 123)'
        self.assertEqual(expected, str(tweet))

    def test_one_edge(self):
        tweet = Tweet('Hello #Abra #Kadabra', '123')
        expected_edges = ['#abra-#kadabra']
        edges = tweet.get_edges()
        self.assertEqual(len(expected_edges), len(edges))
        self.assertEqual(expected_edges[0], str(edges[0]))

    def test_many_edges(self):
        tweet = Tweet('Hello #One #two #THREE', '123')
        expected_edges = ['#one-#two', '#one-#three', '#three-#two']
        edges = tweet.get_edges()
        self.assertEqual(len(expected_edges), len(edges))
        for edge in edges:
            self.assertIn(str(edge), expected_edges)

    def test_edges_for_duplicate_hashtags(self):
        tweet = Tweet('Hello #A #a', '123')
        expected_edges = []
        self.assertEqual(expected_edges, tweet.get_edges())

    def test_edges_for_no_hashtags(self):
        tweet = Tweet('Hello No hash', '123')
        expected_edges = []
        self.assertEqual(expected_edges, tweet.get_edges())

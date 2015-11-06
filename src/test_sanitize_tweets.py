import unittest

from sanitize_tweets import TweetSanitizer

test_json = (
    '{"created_at":"Thu Oct 29 17:51:01 +0000 2015", "id":659789759787589632,'
    '"id_str":"659789759787589632", "text":"Spark Summit East this week! #Spark #Apache"}'
)

test_unicode = (
    '{"created_at":"Thu Oct 29 18:10:49 +0000 2015", "text":"Im at Terminal de Integra\u00e7\u00e3o do Varadouro in Jo\u00e3o Pessoa"}'
)

test_escaped = (
    '{"created_at":"Thu Oct 29 18:10:49 +0000 2015", "text":", PB https:\/\/t.co\/HOl34REL1a"}'
)

all_escape_chars = (
    '{"  \/Hello \\ \' \" n\no   di\tce "}'
)

class TestSanitizer(unittest.TestCase):
    def setUp(self):
        self.sanitizer = TweetSanitizer()

    def test_load_json(self):
        """Loads basic JSON tweet that doesnt require sanitization"""
        expected_output = 'Spark Summit East this week! #Spark #Apache (timestamp: Thu Oct 29 17:51:01 +0000 2015)'
        sanitized_output = self.sanitizer.sanitize_tweet(test_unicode)
        self.assertEqual(expected_output, sanitized_output)

    def test_remove_unicode(self):
        expected_output = 'Im at Terminal de Integrao do Varadouro in Joo Pessoa (timestamp: Thu Oct 29 18:10:49 +0000 2015)'
        sanitized_output = self.sanitizer.sanitize_tweet(test_unicode)
        self.assertEqual(expected_output, sanitized_output)

        sanitized_output = self.sanitizer.sanitize_tweet(test_unicode)
        num_unicode = self.sanitizer.num_with_unicode()
        self.assertEqual(num_unicode, 2)

    def test_unescape_text(self):
        expected_output = ', PB https://t.co/HOl34REL1a (timestamp: Thu Oct 29 18:10:49 +0000 2015)'
        sanitized_output = self.sanitizer.sanitize_tweet(test_escaped)
        self.assertEqual(expected_output, sanitized_output)

    def test_all_escape_charecters(self):
        expected_output = '/Hellow \ \' " n o di ce (timestamp: Wed Oct 29 18:10:49 +0000 2015)'
        sanitized_output = self.sanitizer.sanitize_tweet(all_escape_chars)
        self.assertEqual(expected_output, sanitized_output)
        pass

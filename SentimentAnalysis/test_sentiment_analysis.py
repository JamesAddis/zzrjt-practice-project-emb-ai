
from sentiment_analysis import sentiment_analyzer
import unittest

class TestSentimentAnalyser(unittest.TestCase):
    def test_sentiment_analyzer(self):
        self.assertEqual(sentiment_analyzer("I love working with python")["label"],"SENT_POSITIVE")
        self.assertEqual(sentiment_analyzer("I hate working with python")["label"],"SENT_NEGATIVE")
        self.assertEqual(sentiment_analyzer("I am neutral on python")["label"],"SENT_NEUTRAL")

unittest.main()
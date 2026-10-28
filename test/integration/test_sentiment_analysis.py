
from SentimentAnalysis.sentiment_analysis import sentiment_analyzer
import unittest

class TestIntegrationSentimentAnalyser(unittest.TestCase):
    def test_sentiment_analyzer_negative(self):
        actual_result=sentiment_analyzer("I hate working with python")
        self.assertEqual(actual_result["label"],"SENT_NEGATIVE")
        self.assertEqualLess(actual_result["score"], 0)
        self.assertGreater(actual_result["score"], -1)

    def test_sentiment_analyzer_positive(self):
        actual_result=sentiment_analyzer("I love working with python")
        self.assertEqual(actual_result["label"],"SENT_POSITIVE")
        self.assertEqualLess(actual_result["score"], 1)
        self.assertGreater(actual_result["score"], 0)

    def test_sentiment_analyzer_neutral(self):
        actual_result=sentiment_analyzer("I am neutral with python")
        self.assertEqual(actual_result["label"],"SENT_NEUTRAL")
        self.assertEqualLess(actual_result["score"], -0.5)
        self.assertGreater(actual_result["score"], 0.5)

    def test_sentiment_analyzer_invalid(self):
        actual_result=sentiment_analyzer("412q2a zxzasdf ashrn[\ne  eqwe asfhgtetsodgno")
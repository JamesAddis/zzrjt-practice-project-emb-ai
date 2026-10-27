import unittest
import re
import requests

import config

TEXT_MISSING="Text is required"
TEXT_EMPTY="Text is required, cannot be an empty string"
TEXT_DIGIT="Text cannot be only digit/numerical value"
AI_ISSUE="Invalid input ! Try again"
REGEX_RESULT_PATT=r"^The given text has been identified as (POSTIVE_RESULT|NEGATIVE_RESULT|NEUTRAL_RESULT) with a score of (\-?(?:\d+|\d+\.\d+)$"
TIMEOUT_DEFAULT=120
class TestE2EWebForm(unittest.TestCase):
    driver = None

    def tearDown(self):
        if self.driver != None:
            self.driver.close()

    def _input_submit_method(self, drv, text_input):
        query_params={"textToAnalyze":text_input}
        return requests.post(
            config.E2E_API_SERVER,
            query_params=query_params,
            timeout=config.SERVER_TIMEOUT)
    
    def _input_valid_submit_method(self, text_input, expected_label, expected_score_min, expected_score_max):

        response_result = self._input_submit_method(self, text_input)
        self.assertEqual(response.status_code,200,"Should respond with success")
        
        self.assertRegex(REGEX_RESULT_PATT,response.text)
        regex_results=re.search(REGEX_RESULT_PATT, response.text).groups()
        
        actual_label = regex_results[0]
        actual_score = regex_results[1]
        
        self.assertEqual(actual_label,expected_label, f"Result should be {expected_label}")
        self.assertTrue(score.isdigit(), "score should be a digit")
        self.assertGreater(actual_score, expected_score_min)
        self.assertLessEqual(actual_score, expected_score_max)
        
    def _input_invalid_submit_method(self, text_input, expected_code, expected_error):
        response_result = self._input_submit_method(text_input)
        self.assertEqual(response.status_code,expected_code, f"Should respond with error code: {expected_code}")
        json_result = json.loads(response_result.text)
        self.assertEqual(isinstance(json_result, dict), "Should be a json response")
        self.assertEqual(json_result["message"],expected_error, "Wrong messsage result")

    def test_input_valid_positive_result(self):
        ''' Test form handles positive sentiment
        '''
        self._input_valid_submit_method("I love working with python", "POSTIVE_RESULT", 0, 1)
        self._input_valid_submit_method("Integration testing is a lovely concept", "POSTIVE_RESULT", 0, 1)

    def test_input_valid_neutral_result(self):
        ''' Test form handles neutral sentiment
        '''
        self._input_valid_submit_method("Working with python is fine", "NEUTRAL_RESULT",-0.5, 0.5)
        self._input_valid_submit_method("Integration testing is required", "NEUTRAL_RESULT",-0.5, 0.5)

    def test_input_valid_negative_result(self):
        ''' Test form handles negative sentiment
        '''
        self._input_valid_submit_method("I HATE working with python", "NEGATIVE_RESULT",-0.5, 0.5)
        self._input_valid_submit_method("Integration testing is a waste of time!", "NEUTRAL_RESULT",-0.5, 0.5)

    def test_input_empty_error_message(self):
        ''' Test form handles empty string validation
        '''
        _input_invalid_submit_method("       ", TEXT_EMPTY)
        _input_invalid_submit_method("\t\t", TEXT_EMPTY)

    def test_input_digit_error_message(self):
        ''' Test form handles empty string validation
        '''
        self._input_invalid_submit_method("20", TEXT_DIGIT)
        self._input_invalid_submit_method("4.1", TEXT_DIGIT)
        self._input_invalid_submit_method("0", TEXT_DIGIT)
        self._input_invalid_submit_method("-2", TEXT_DIGIT)

    def test_input_invalid_error_message(self):
        ''' Test form handles empty string validation
        '''
        self._input_invalid_submit_method("dasdsae323123 e213wdsadadwa", AI_ISSUE)
        self._input_invalid_submit_method("ga4ewqkghdcmfgshrtr5  awaszgsrfhswtrgng", AI_ISSUE)
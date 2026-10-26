import unittest
import re
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

import config

TEXT_EMPTY="Text is required, cannot be an empty string"
TEXT_DIGIT="Text cannot be only digit/numerical value"
AI_ISSUE="Invalid input ! Try again"
REGEX_RESULT_PATT=r"^The given text has been identified as (POSTIVE_RESULT|NEGATIVE_RESULT|NEUTRAL_RESULT) with a score of (\-?(?:\d+|\d+\.\d+)$"


class TestE2EWebForm(unittest.TestCase):
    def setUp():
        self.driver = webdriver.Remote(command_executor=config.E2E_SELENIUM_SERVER, options=config.selenium_options)
    def tearDown(self):
        if self.driver != None:
            self.driver.close()

    def _input_submit_method(self, text_input):
        # setup
        drv = self.driver
        drv.get(config.E2E_WEB_SERVER)
        result = drv.find_element(By.CSS_SELECTOR, "#sentiment_result")
        box = drv.find_element(By.NAME, "textToAnalyze")
        btn = drv.find_element(By.TAG_NAME, "button")

        # pre checks
        pre_test_result = result.get_attribute('innerText')
        self.assertEqual(pre_test_result.strip(), "","A Result is already set on startup")

        # enter text and trigger submit
        actions = ActionChains(drv)
        actions.move_to_element(box)
        actions.click(on_element:box)
        actions.send_keys(text_input)
        actions.send_keys(Keys.RETURN)
        actions.move_to_element(btn)
        actions.click(on_element:btn)
        actions.move_to_element(result)

        # get result from html element
        text_result=result.get_attribute('innerText')
        return text_result
    
    def _input_valid_submit_method(self, text_input, expected_label, expected_score_min, expected_score_max):

        text_result = self._input_submit_method(text_input)
        
        self.assertRegex(REGEX_RESULT_PATT,text_result, f"Result does match expected format: {response.text}")
        regex_results=re.search(REGEX_RESULT_PATT, response.text).groups()
        
        actual_label = regex_results[0]
        actual_score = regex_results[1]
        
        self.assertEqual(actual_label,expected_label, f"Result should be {expected_label}")
        self.assertTrue(score.isdigit(), "score should be a digit")
        self.assertGreater(actual_score, expected_score_min)
        self.assertLessEqual(actual_score, expected_score_max)
        result_classes = self.driver.find_element(By.CSS_SELECTOR, "#sentiment_result").getAttribute("class").split(" ")
        self.assertFalse(Arrays.asList(result_classes).contains("text-danger"), "Should not have red text class")

    def _input_invalid_submit_method(self, driver, text_input, expected_error):
        text_result = self._input_submit_method(text_input)
        self.assertEqual(text_result.strip(), expected_error, "Wrong messsage result")
        result_classes = self.driver.find_element(By.CSS_SELECTOR, "#sentiment_result").getAttribute("class").split(" ")
        self.assertTrue(Arrays.asList(result_classes).contains("text-danger"), "Should have red text class")

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
        self._input_invalid_submit_method("       ", TEXT_EMPTY)
        self._input_invalid_submit_method(s"\t\t", TEXT_EMPTY)

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
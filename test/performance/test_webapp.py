

import csv
import os
import time

from locust import run_single_user, task
from locust_plugins.users.playwright import PageWithRetry, PlaywrightUser, PlaywrightScriptUser, pw, event

csvfile = open(config.PERFORMANCE_TEST_DATA)
iter = csv.reader(csvfile)

class TestWebApplication(PlaywrightUser):
    host = config.PERFORMANCE_TEST_WEBSITE_URL

    multiplier = config.PERFORMANCE_TEST_WEBSITE_INSTANCES  # run ten concurrent playwright sessions/browsers for each Locust user. This helps improve load generation efficiency.

    @task
    @pw
    async def successfulPrompting(self, page: PageWithRetry):
        try:
            try:
                sentiment_prompt,expected_result = next(iter)
            except StopIteration:
                csvfile.seek(0, 0)
                sentiment_prompt,expected_result = next(iter)
                
            async with event(self, "Load up Index Page"):  # log this as an event
                await page.goto(config.PERFORMANCE_TEST_SITE_PATH)

            async with event(self, "Submit Sentiment"):
                async with page.expect_navigation(wait_until="domcontentloaded"):
                    text_input = await page.locator("input[name=textToAnalyze]")
                    submit_button = await page.locator("button")
                    sentiment_result = page.locator("#sentiment_result")
                    await text_input.hover()
                    await text_input.click()
                    await text_input.clear()
                    await text_input.fill(sentiment_prompt)
                    await submit_button.hover()
                    await submit_button.click()
            async with event(self, "Submitted Sentiment"):
                await expect(sentiment_result).to_contain_text(REGEX_RESULT_PATT, timeout=config.PAGE_SUBMIT_TIMEOUT)
                await expect(sentiment_result).to_contain_text(expected_result)
                await expect(sentiment_result).not_to_contain_class("text-danger", timeout=config.PAGE_SUBMIT_TIMEOUT)
        except:
            pass

    @task
    @pw
    async def submitNumber(self, page: PageWithRetry):
        try:
            async with event(self, "Load up Index Page"):  # log this as an event
                await page.goto("/")

            async with event(self, "Submit Sentiment"):
                async with page.expect_navigation(wait_until="domcontentloaded"):
                    text_input = await page.locator("input[name=textToAnalyze]")
                    submit_button = await page.locator("button")
                    sentiment_result = page.locator("#sentiment_result")
                    await text_input.hover()
                    await text_input.click()
                    await text_input.clear()
                    await text_input.fill(os.urandom())
                    await submit_button.hover()
                    await submit_button.click()
            async with event(self, "Submitted Digit"):
                await expect(sentiment_result).to_contain_text(TEXT_DIGIT, timeout=config.PAGE_SUBMIT_TIMEOUT)
                await expect(sentiment_result).to_contain_class("text-danger", timeout=config.PAGE_SUBMIT_TIMEOUT)
        except:
            pass
    @task
    @pw
    async def submitWhitespaceText(self, page: PageWithRetry):
        try:
            async with event(self, "Load up Index Page"):  # log this as an event
                await page.goto("/")

            async with event(self, "Submit Whitespace text"):
                async with page.expect_navigation(wait_until="domcontentloaded"):
                    text_input = await page.locator("input[name=textToAnalyze]")
                    submit_button = await page.locator("button")
                    sentiment_result = page.locator("#sentiment_result")
                    await text_input.hover()
                    await text_input.click()
                    await text_input.clear()
                    await text_input.fill("/t/t\n    \t\t")
                    await submit_button.hover()
                    await submit_button.click()
            async with event(self, "Submitted Missing Text"):
                await expect(sentiment_result).to_contain_text(TEXT_EMPTY, timeout=config.PAGE_SUBMIT_TIMEOUT)
                await expect(sentiment_result).to_contain_class("text-danger", timeout=config.PAGE_SUBMIT_TIMEOUT)
        except:
            pass
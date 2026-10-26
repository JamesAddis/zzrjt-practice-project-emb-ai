PERFORMANCE_TEST_SERVER="localhost:5000"
REGEX_RESULT_PATT=r"^The given text has been identified as (POSTIVE_RESULT|NEGATIVE_RESULT|NEUTRAL_RESULT) with a score of (\-?(?:\d+|\d+\.\d+)$"

import csv
import os
from locust_plugins.users.playwright import PageWithRetry, PlaywrightUser, PlaywrightScriptUser, pw, event

csvfile = open(config.PERFORMANCE_TEST_DATA)
iter = csv.reader(csvfile)

class TestWebSiteNoJs(PlaywrightUser):
    host = config.PERFORMANCE_TEST_WEBSITE_URL

    @task
    @pw
    async def WebsiteNoJsUser(self, page: PageWithRetry):
        self.browser.new_context(java_script_enabled=False)
        try:
            try:
                sentiment_prompt,expected_result = next(iter)
            except StopIteration:
                csvfile.seek(0, 0)
                sentiment_prompt,expected_result = next(iter)

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
                    await text_input.fill(sentiment_prompt)
                    await submit_button.hover()
                    await submit_button.click()
            async with event(self, "Submitted Sentiment via POST"):
                async with page.expect_navigation(wait_until="domcontentloaded"):
                sentiment_result = page.locator("#sentiment_result")
                await expect(sentiment_result).to_contain_text(REGEX_RESULT_PATT)
                await expect(sentiment_result).to_contain_text(expected_result)
                await expect(sentiment_result).not_to_contain_class("text-danger")
    except:
        pass
    
    @task
    @pw
    async def submitWhitespaceText(self, page: PageWithRetry):
        self.browser.new_context(java_script_enabled=False)
        try:
            async with event(self, "Load up Index Page"):  # log this as an event
                await page.goto("/")
            async with event(self, "Submit empty string via POST"):
                text_input = await page.locator("input[name=textToAnalyze]")
                submit_button = await page.locator("button")
                await text_input.hover()
                await text_input.click()
                await text_input.clear()
                await text_input.fill("\t\n\n\t\n   \t\t")
                await submit_button.hover()
                await submit_button.click()
            async with event(self, "Submitted empty string via POST"):
                async with page.expect_navigation(wait_until="domcontentloaded"):
                    sentiment_result = page.locator("#sentiment_result")
                    await expect(sentiment_result).to_contain_text(TEXT_EMPTY)
                    await expect(sentiment_result).to_contain_class("text-danger")
    except:
        pass
    
    @task
    @pw
    async def submitNumber(self, page: PageWithRetry):
        self.browser.new_context(java_script_enabled=False)
        try:
            async with event(self, "Load up Index Page"):  # log this as an event
                await page.goto("/")
            async with event(self, "Submit Invalid number via POST"):
                text_input = await page.locator("input[name=textToAnalyze]")
                submit_button = await page.locator("button")
                await text_input.hover()
                await text_input.click()
                await text_input.clear()
                await text_input.fill(os.urandom())
                await submit_button.hover()
                await submit_button.click()
            async with event(self, "Submitted Invalid number via POST"):
                async with page.expect_navigation(wait_until="domcontentloaded"):
                    sentiment_result = page.locator("#sentiment_result")
                    await expect(sentiment_result).to_contain_text(TEST_DIGIT)
                    await expect(sentiment_result).to_contain_class("text-danger")
    except:
        pass
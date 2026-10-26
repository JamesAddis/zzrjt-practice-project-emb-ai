import csv
import os

csvfile = open(config.PERFORMANCE_TEST_DATA)
iter = csv.reader(csvfile)

class TestApi(HttpUser):
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
        except:
            pass

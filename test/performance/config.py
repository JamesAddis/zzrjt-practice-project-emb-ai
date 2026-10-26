PERFORMANCE_TEST_SITE="localhost:5000"
PERFORMANCE_TEST_API="localhost:5000"
PERFORMANCE_TEST_SITE_PATH="/"
PERFORMANCE_TEST_API_PATH="/api/sentiment_"
PERFORMANCE_TEST_DATA=os.path.join(os.path.dirname(__file__), "testdata_from_csv.csv")
REGEX_RESULT_PATT=r"^The given text has been identified as (POSTIVE_RESULT|NEGATIVE_RESULT|NEUTRAL_RESULT) with a score of (\-?(?:\d+|\d+\.\d+)$"